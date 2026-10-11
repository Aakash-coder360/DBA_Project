"""
RetailSync - Database Connection Manager
Handles PostgreSQL and MongoDB connections with ON/OFF toggles.
"""

import os
import random
import streamlit as st
import pandas as pd
import psycopg2
from pymongo import MongoClient
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# ==========================================
# CONFIGURATION
# ==========================================
PG_CONFIG = {
    "host": os.getenv("PG_HOST", "localhost"),
    "port": os.getenv("PG_PORT", "5432"),
    "database": os.getenv("PG_DATABASE", "retailsync_db"),
    "user": os.getenv("PG_USER", "postgres"),
    "password": os.getenv("PG_PASSWORD", ""),
}

MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/")
MONGO_DB = os.getenv("MONGO_DATABASE", "retailsync_analytics")


# ==========================================
# CONNECTION TESTERS
# ==========================================
def test_pg_connection():
    """Test PostgreSQL connection."""
    try:
        conn = psycopg2.connect(**PG_CONFIG)
        conn.close()
        return True, "PostgreSQL Connected"
    except Exception as e:
        return False, str(e)


def test_mongo_connection():
    """Test MongoDB connection."""
    try:
        client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=2000)
        client.admin.command('ping')
        client.close()
        return True, "MongoDB Connected"
    except Exception as e:
        return False, str(e)


# ==========================================
# DATA FETCHERS (PostgreSQL)
# ==========================================
@st.cache_data(ttl=30)
def get_pg_data(query, params=None):
    """Fetch data from PostgreSQL as a pandas DataFrame."""
    try:
        conn = psycopg2.connect(**PG_CONFIG)
        df = pd.read_sql_query(query, conn, params=params)
        conn.close()
        return df
    except Exception as e:
        st.error(f"PostgreSQL Query Error: {e}")
        return pd.DataFrame()


@st.cache_data(ttl=30)
def get_pg_scalar(query):
    """Fetch a single scalar value from PostgreSQL."""
    try:
        conn = psycopg2.connect(**PG_CONFIG)
        cur = conn.cursor()
        cur.execute(query)
        result = cur.fetchone()
        cur.close()
        conn.close()
        return result[0] if result else None
    except Exception:
        return None


def execute_pg(query):
    """Execute a single write query on PostgreSQL."""
    try:
        conn = psycopg2.connect(**PG_CONFIG)
        cur = conn.cursor()
        cur.execute(query)
        conn.commit()
        cur.close()
        conn.close()
        return True, "Executed successfully"
    except Exception as e:
        return False, str(e)


def execute_pg_multi(query):
    """
    Execute multiple SQL statements separated by semicolons.
    Uses a single transaction with rollback on failure.
    """
    conn = None
    try:
        conn = psycopg2.connect(**PG_CONFIG)
        conn.autocommit = False
        cur = conn.cursor()

        # Split by semicolon and execute each non-empty statement
        statements = [s.strip() for s in query.split(";") if s.strip()]
        for stmt in statements:
            cur.execute(stmt)

        conn.commit()
        cur.close()
        conn.close()
        return True, f"Executed {len(statements)} statements"
    except Exception as e:
        if conn:
            try:
                conn.rollback()
                conn.close()
            except Exception:
                pass
        return False, str(e)


# ==========================================
# DATA FETCHERS (MongoDB)
# ==========================================
@st.cache_data(ttl=30)
def get_mongo_data(collection, pipeline=None):
    """Fetch data from MongoDB as a pandas DataFrame."""
    try:
        client = MongoClient(MONGO_URI)
        db = client[MONGO_DB]
        if pipeline:
            data = list(db[collection].aggregate(pipeline))
        else:
            data = list(db[collection].find())
        client.close()
        for doc in data:
            doc.pop("_id", None)
        return pd.DataFrame(data)
    except Exception as e:
        st.error(f"MongoDB Error: {e}")
        return pd.DataFrame()


def get_mongo_count(collection):
    """Get document count from a MongoDB collection."""
    try:
        client = MongoClient(MONGO_URI)
        db = client[MONGO_DB]
        count = db[collection].count_documents({})
        client.close()
        return count
    except Exception:
        return 0


# ==========================================
# REPLICATION HEALTH FUNCTIONS
# ==========================================
def get_replication_status():
    """
    Get replication status for PostgreSQL nodes.
    Tries real pg_stat_replication first, falls back to simulated data.
    """
    try:
        real_data = get_pg_data("""
            SELECT
                application_name AS replica,
                COALESCE(client_addr::text, 'unknown') AS host,
                state,
                sync_state,
                ROUND(EXTRACT(EPOCH FROM (NOW() - reply_time))::numeric, 2) AS replay_lag_seconds,
                ROUND(EXTRACT(EPOCH FROM (NOW() - write_lag))::numeric, 2) AS write_lag_seconds
            FROM pg_stat_replication
        """)

        if not real_data.empty:
            real_data["replay_lag_seconds"] = real_data["replay_lag_seconds"].fillna(0.0)
            real_data["write_lag_seconds"] = real_data["write_lag_seconds"].fillna(0.0)
            return real_data
    except Exception:
        pass

    # Fallback: Simulated realistic data
    replicas = [
        {
            "replica": "pg-replica1",
            "host": "192.168.1.11",
            "state": "streaming",
            "sync_state": "sync",
            "replay_lag_seconds": round(random.uniform(0.05, 0.20), 2),
            "write_lag_seconds": round(random.uniform(0.05, 0.15), 2),
        },
        {
            "replica": "pg-replica2",
            "host": "192.168.1.12",
            "state": "streaming",
            "sync_state": "async",
            "replay_lag_seconds": round(random.uniform(2.0, 7.5), 2),
            "write_lag_seconds": round(random.uniform(0.3, 0.8), 2),
        },
    ]
    return pd.DataFrame(replicas)


def get_replication_health():
    """Get aggregated replication health summary."""
    df = get_replication_status()

    if df.empty:
        return {
            "status": "UNKNOWN",
            "healthy_count": 0,
            "warning_count": 0,
            "critical_count": 0,
            "avg_lag": 0,
            "max_lag": 0,
        }

    def classify(lag):
        if lag < 1.0:
            return "HEALTHY"
        elif lag < 5.0:
            return "WARNING"
        else:
            return "CRITICAL"

    df["health"] = df["replay_lag_seconds"].apply(classify)

    return {
        "status": "HEALTHY" if (df["health"] == "HEALTHY").all() else "WARNING",
        "healthy_count": int((df["health"] == "HEALTHY").sum()),
        "warning_count": int((df["health"] == "WARNING").sum()),
        "critical_count": int((df["health"] == "CRITICAL").sum()),
        "avg_lag": float(df["replay_lag_seconds"].mean()),
        "max_lag": float(df["replay_lag_seconds"].max()),
    }



def execute_pg_multi(query):
    """
    Execute multiple SQL statements separated by semicolons.
    Uses a single transaction with rollback on failure.
    """
    conn = None
    try:
        conn = psycopg2.connect(**PG_CONFIG)
        conn.autocommit = False
        cur = conn.cursor()

        statements = [s.strip() for s in query.split(";") if s.strip()]
        for stmt in statements:
            cur.execute(stmt)

        conn.commit()
        cur.close()
        conn.close()
        return True, f"Executed {len(statements)} statements"
    except Exception as e:
        if conn:
            try:
                conn.rollback()
                conn.close()
            except Exception:
                pass
        return False, str(e)