CREATE TABLE orders (
    order_id SERIAL PRIMARY KEY,
    customer_id VARCHAR(50) NOT NULL,
    status VARCHAR(20) DEFAULT 'pending',
    total_amount NUMERIC(10,2),
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE order_items (
    id SERIAL PRIMARY KEY,
    order_id INT REFERENCES orders(order_id),
    product_id VARCHAR(50) NOT NULL,
    product_name VARCHAR(200),
    quantity INT NOT NULL,
    unit_price NUMERIC(10,2)
);

CREATE TABLE inventory (
    product_id VARCHAR(50) PRIMARY KEY,
    product_name VARCHAR(200),
    quantity_available INT NOT NULL DEFAULT 0,
    warehouse_location VARCHAR(100),
    last_updated TIMESTAMP DEFAULT NOW()
);

CREATE TABLE billing (
    invoice_id SERIAL PRIMARY KEY,
    order_id INT REFERENCES orders(order_id),
    amount NUMERIC(10,2),
    payment_status VARCHAR(20) DEFAULT 'unpaid',
    invoice_date TIMESTAMP DEFAULT NOW()
);
