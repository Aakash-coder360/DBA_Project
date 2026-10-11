// ==========================================
// RETAILSYNC - MONGODB SEED DATA
// Run: mongosh < mongo_seed.js
// ==========================================

use retailsync_analytics

// Drop existing collections (clean start)
db.product_catalog.drop();
db.customer_activity.drop();

print("Inserting product_catalog...");
db.product_catalog.insertMany([
  {
    "product_id": "prod_1042",
    "name": "Wireless Noise-Canceling Headphones",
    "category": "Electronics",
    "brand": "SonicPro",
    "price": 799.00,
    "specs": { "battery_life": "30 hours", "bluetooth": "5.2", "weight": "250g" },
    "reviews": [
      { "user": "Alice", "rating": 5, "comment": "Amazing sound quality!", "date": "2026-09-15" },
      { "user": "Bob", "rating": 4, "comment": "Good but expensive.", "date": "2026-09-20" },
      { "user": "Charlie", "rating": 5, "comment": "Best purchase this year.", "date": "2026-10-01" }
    ]
  },
  {
    "product_id": "prod_1090",
    "name": "4K Ultra HD Smart TV",
    "category": "Electronics",
    "brand": "VisionMax",
    "price": 2701.00,
    "specs": { "screen_size": "55 inches", "resolution": "3840x2160", "smart_os": "Android TV" },
    "reviews": [
      { "user": "David", "rating": 3, "comment": "Screen is great, smart features are slow.", "date": "2026-08-10" },
      { "user": "Eve", "rating": 4, "comment": "Good value for money.", "date": "2026-09-05" }
    ]
  },
  {
    "product_id": "prod_2001",
    "name": "Smart Fitness Watch",
    "category": "Wearables",
    "brand": "FitTrack",
    "price": 199.00,
    "specs": { "battery_life": "7 days", "water_resistance": "50m", "heart_rate": true },
    "reviews": [
      { "user": "Frank", "rating": 4, "comment": "Tracks my steps accurately.", "date": "2026-09-28" }
    ]
  }
]);

print("Inserting customer_activity...");
db.customer_activity.insertMany([
  {
    "customer_id": "cust_118",
    "session_id": "sess_abc123",
    "browsing_history": [
      { "category": "Electronics", "product_id": "prod_1042", "time_spent_seconds": 120 },
      { "category": "Electronics", "product_id": "prod_1090", "time_spent_seconds": 300 }
    ],
    "cart_abandoned": false,
    "last_login": new Date("2026-10-11T10:00:00Z")
  },
  {
    "customer_id": "cust_204",
    "session_id": "sess_def456",
    "browsing_history": [
      { "category": "Wearables", "product_id": "prod_2001", "time_spent_seconds": 45 },
      { "category": "Electronics", "product_id": "prod_1042", "time_spent_seconds": 600 }
    ],
    "cart_abandoned": true,
    "last_login": new Date("2026-10-10T18:30:00Z")
  },
  {
    "customer_id": "cust_305",
    "session_id": "sess_ghi789",
    "browsing_history": [
      { "category": "Electronics", "product_id": "prod_1090", "time_spent_seconds": 200 }
    ],
    "cart_abandoned": false,
    "last_login": new Date("2026-10-11T14:15:00Z")
  }
]);

print("✅ Seed data inserted!");
print("Product Catalog:", db.product_catalog.countDocuments());
print("Customer Activity:", db.customer_activity.countDocuments());