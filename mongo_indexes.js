// ==========================================
// RETAILSYNC - MONGODB INDEXES
// Run: mongosh < mongo_indexes.js
// ==========================================

use retailsync_analytics

print("Creating indexes on product_catalog...");
db.product_catalog.createIndex({ "product_id": 1 }, { unique: true });
db.product_catalog.createIndex({ "category": 1 });
db.product_catalog.createIndex({ "reviews.comment": "text" });

print("Creating indexes on customer_activity...");
db.customer_activity.createIndex({ "customer_id": 1 });

print("✅ All indexes created successfully!");
print("\nVerifying...");
print("product_catalog indexes:");
printjson(db.product_catalog.getIndexes());
print("customer_activity indexes:");
printjson(db.customer_activity.getIndexes());