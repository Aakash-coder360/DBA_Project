// =========================================================
// RetailSync — MongoDB Setup Script
// =========================================================
// Run this in mongosh to set up the database structure.
// No sample data is inserted — collections start empty and
// fill up only through the dashboard / API.
//
// Usage:
//   mongosh < mongo_setup.js
// or paste these commands one by one into mongosh
// =========================================================

// 1. Select / create the database
use retailsync;

// 2. Create empty collections
db.createCollection("products");
db.createCollection("customer_activity");

// 3. Create indexes for fast lookups
db.products.createIndex({ category: 1 });
db.customer_activity.createIndex({ customer_id: 1 });
db.customer_activity.createIndex({ product_id: 1 });

// 4. Verify
print("Collections created:");
print(db.getCollectionNames());

print("products count:", db.products.countDocuments());
print("customer_activity count:", db.customer_activity.countDocuments());
