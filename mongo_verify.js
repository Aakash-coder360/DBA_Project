// ==========================================
// RETAILSYNC - VERIFY EVERYTHING
// Run: mongosh < mongo_verify.js
// ==========================================

use retailsync_analytics

print("\n=== DOCUMENT COUNTS ===");
print("product_catalog: " + db.product_catalog.countDocuments());
print("customer_activity: " + db.customer_activity.countDocuments());

print("\n=== INDEXES ===");
print("product_catalog:");
printjson(db.product_catalog.getIndexes());
print("customer_activity:");
printjson(db.customer_activity.getIndexes());

print("\n=== AVG RATINGS ===");
printjson(db.product_catalog.aggregate([
  { $unwind: "$reviews" },
  { $group: { _id: "$name", avg_rating: { $avg: "$reviews.rating" } } }
]).toArray());

print("\n=== ABANDONMENT RATE ===");
printjson(db.customer_activity.aggregate([
  { $group: {
      _id: null,
      total: { $sum: 1 },
      abandoned: { $sum: { $cond: ["$cart_abandoned", 1, 0] } }
  }}
]).toArray());