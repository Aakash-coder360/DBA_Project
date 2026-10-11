-- 1. Orders Table (Transactional Core)
CREATE TABLE orders (
    order_id SERIAL PRIMARY KEY,
    customer_id VARCHAR(50) NOT NULL,
    status VARCHAR(20) DEFAULT 'pending',
    total_amount NUMERIC(10,2) NOT NULL,
    created_at TIMESTAMP DEFAULT NOW()
);

-- 2. Order Items Table (Links Orders to Products)
CREATE TABLE order_items (
    id SERIAL PRIMARY KEY,
    order_id INT REFERENCES orders(order_id) ON DELETE CASCADE,
    product_id VARCHAR(50) NOT NULL,
    quantity INT NOT NULL CHECK (quantity > 0),
    unit_price NUMERIC(10,2) NOT NULL
);

-- 3. Inventory Table (Stock Management)
CREATE TABLE inventory (
    product_id VARCHAR(50) PRIMARY KEY,
    product_name VARCHAR(200) NOT NULL,
    quantity_available INT NOT NULL DEFAULT 0,
    warehouse_location VARCHAR(100),
    last_updated TIMESTAMP DEFAULT NOW()
);

-- 4. Billing Table (Financial Records)
CREATE TABLE billing (
    invoice_id SERIAL PRIMARY KEY,
    order_id INT REFERENCES orders(order_id) ON DELETE CASCADE,
    amount NUMERIC(10,2) NOT NULL,
    payment_status VARCHAR(20) DEFAULT 'unpaid',
    invoice_date TIMESTAMP DEFAULT NOW()
);


-- Insert 50 Inventory Products
INSERT INTO inventory (product_id, product_name, quantity_available, warehouse_location)
SELECT 
    'prod_' || i,
    'Product Name ' || i,
    (random() * 100)::int,
    'WH-' || (ARRAY['Hyderabad', 'Bengaluru', 'Mumbai', 'Delhi'])[floor(random() * 4 + 1)]
FROM generate_series(1000, 1050) AS i;

-- Insert 5,000 Orders
INSERT INTO orders (customer_id, status, total_amount, created_at)
SELECT 
    'cust_' || (random() * 1000)::int,
    (ARRAY['pending', 'shipped', 'delivered', 'cancelled'])[floor(random() * 4 + 1)],
    (random() * 5000 + 100)::numeric(10,2),
    NOW() - (random() * 30 || ' days')::interval
FROM generate_series(1, 5000);

-- Insert Order Items (3 items per order)
INSERT INTO order_items (order_id, product_id, quantity, unit_price)
SELECT 
    o.order_id,
    'prod_' || (random() * 50 + 1000)::int,
    (random() * 5 + 1)::int,
    (random() * 500 + 50)::numeric(10,2)
FROM orders o, generate_series(1, 3);

-- Insert Billing Records (1 per order)
INSERT INTO billing (order_id, amount, payment_status)
SELECT 
    order_id,
    total_amount,
    (ARRAY['paid', 'unpaid', 'refunded'])[floor(random() * 3 + 1)]
FROM orders;


-- Index on Orders (For fast date range and customer lookups)
CREATE INDEX idx_orders_created_at ON orders(created_at);
CREATE INDEX idx_orders_customer_id ON orders(customer_id);
CREATE INDEX idx_orders_status ON orders(status);

-- Index on Order Items (For fast joins)
CREATE INDEX idx_order_items_order_id ON order_items(order_id);
CREATE INDEX idx_order_items_product_id ON order_items(product_id);

-- Index on Billing (For fast financial reporting)
CREATE INDEX idx_billing_order_id ON billing(order_id);
CREATE INDEX idx_billing_status ON billing(payment_status);


-- View 1: Daily Sales (For the "Visual Graphs" tab)
CREATE OR REPLACE VIEW vw_daily_sales AS
SELECT 
    DATE(created_at) AS order_date,
    COUNT(order_id) AS total_orders,
    SUM(total_amount) AS daily_revenue,
    ROUND(AVG(total_amount), 2) AS avg_order_value
FROM orders
WHERE status != 'cancelled'
GROUP BY DATE(created_at)
ORDER BY order_date DESC;

-- View 2: Low Stock Alerts (For the "Inventory" tab)
CREATE OR REPLACE VIEW vw_low_stock AS
SELECT 
    product_id, 
    product_name, 
    quantity_available, 
    warehouse_location,
    CASE 
        WHEN quantity_available < 10 THEN 'CRITICAL'
        WHEN quantity_available < 30 THEN 'LOW'
        ELSE 'OK'
    END AS stock_status
FROM inventory
WHERE quantity_available < 50
ORDER BY quantity_available ASC;

-- View 3: Top Selling Products (For Analytics)
CREATE OR REPLACE VIEW vw_top_products AS
SELECT 
    oi.product_id,
    i.product_name,
    SUM(oi.quantity) AS total_sold,
    SUM(oi.quantity * oi.unit_price) AS total_revenue
FROM order_items oi
JOIN inventory i ON oi.product_id = i.product_id
GROUP BY oi.product_id, i.product_name
ORDER BY total_sold DESC;


-- 1. Test the Daily Sales View
EXPLAIN ANALYZE 
SELECT * FROM vw_daily_sales LIMIT 10;

-- 2. Test a "Slow" query BEFORE index logic (Sequential Scan)
EXPLAIN ANALYZE 
SELECT * FROM orders WHERE customer_id = 'cust_500';

-- 3. Test the same query using the Index (Index Scan)
EXPLAIN ANALYZE 
SELECT * FROM orders WHERE customer_id = 'cust_500' AND status = 'shipped';

-- 4. Test a complex join (Dashboard Query)
EXPLAIN ANALYZE
SELECT 
    o.order_id, 
    o.customer_id, 
    o.total_amount,
    i.product_name,
    b.payment_status
FROM orders o
JOIN order_items oi ON o.order_id = oi.order_id
JOIN inventory i ON oi.product_id = i.product_id
LEFT JOIN billing b ON o.order_id = b.order_id
WHERE o.created_at > NOW() - INTERVAL '7 days'
LIMIT 100;


SELECT 'Orders' AS table_name, COUNT(*) FROM orders
UNION ALL
SELECT 'Order Items', COUNT(*) FROM order_items
UNION ALL
SELECT 'Inventory', COUNT(*) FROM inventory
UNION ALL
SELECT 'Billing', COUNT(*) FROM billing;

-- Check Daily Sales View
SELECT * FROM vw_daily_sales LIMIT 5;

-- Check Low Stock View
SELECT * FROM vw_low_stock LIMIT 5;