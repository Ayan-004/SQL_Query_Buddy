from sqlalchemy import create_engine, text

DB_URL = 'sqlite:///retail.db'
engine = create_engine(DB_URL)

#---Schema Definition---
create_customers_table = """
CREATE TABLE customers (
 customer_id INTEGER PRIMARY KEY,
 name TEXT NOT NULL,
 email TEXT UNIQUE,
 region TEXT,
 signup_date DATE
);
"""

create_products_table = """
CREATE TABLE products (
 product_id INTEGER PRIMARY KEY,
 name TEXT NOT NULL,
 category TEXT,
 price DECIMAL(10,2)
);
"""

create_orders_table = """
CREATE TABLE orders (
 order_id INTEGER PRIMARY KEY,
 customer_id INTEGER,
 order_date DATE,
 total_amount DECIMAL(10,2),
 FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
);
"""

create_order_items_table = """
CREATE TABLE order_items (
 item_id INTEGER PRIMARY KEY,
 order_id INTEGER,
 product_id INTEGER,
 quantity INTEGER,
 subtotal DECIMAL(10,2),
 FOREIGN KEY (order_id) REFERENCES orders(order_id),
 FOREIGN KEY (product_id) REFERENCES products(product_id)
);
"""

#---Sample Data Insertion---
insert_customers = """
INSERT INTO customers (customer_id, name, email, region, signup_date) VALUES
(1, 'Alice Chen', 'alice.chen@example.com', 'California', '2023-02-01'),
(2, 'John Patel', 'john.patel@example.com', 'New York', '2023-05-15'),
(3, 'Maria Lopez', 'maria.lopez@example.com', 'Texas', '2022-11-30'),
(4, 'David Johnson', 'david.johnson@example.com', 'Florida', '2023-07-22'),
(5, 'Sofia Khan', 'sofia.khan@example.com', 'Illinois', '2023-04-10');
(6, 'Michael Brown', 'michael.brown@example.com', 'Washington', '2023-01-15'),
(7, 'Emily Davis', 'emily.davis@example.com', 'California', '2022-12-05'),
(8, 'Daniel Wilson', 'daniel.wilson@example.com', 'New York', '2023-08-01'),
(9, 'Sarah Miller', 'sarah.miller@example.com', 'Texas', '2023-03-20'),
(10, 'Kevin Lee', 'kevin.lee@example.com', 'Arizona', '2023-06-11'),
(11, 'Laura Hall', 'laura.hall@example.com', 'Illinois', '2022-10-10'),
(12, 'Robert King', 'robert.king@example.com', 'Florida', '2023-09-18'),
(13, 'Jessica Wright', 'jessica.wright@example.com', 'Washington', '2023-02-25'),
(14, 'Tom Clark', 'tom.clark@example.com', 'California', '2023-11-05'),
(15, 'Olivia Allen', 'olivia.allen@example.com', 'New York', '2022-09-30');
"""

insert_products = """
INSERT INTO products (product_id, name, category, price) VALUES
(1, 'Laptop Pro 15', 'Electronics', 1200.00),
(2, 'Wireless Mouse', 'Accessories', 40.00),
(3, 'Standing Desk', 'Furniture', 300.00),
(4, 'Noise Cancelling Headphones', 'Electronics', 150.00),
(5, 'Office Chair Deluxe', 'Furniture', 180.00);
(6, 'USB-C Hub', 'Accessories', 60.00),
(7, 'Ergonomic Keyboard', 'Accessories', 130.00),
(8, '4K Monitor 27"', 'Electronics', 350.00),
(9, 'Accounting Software License', 'Software', 250.00),
(10, 'Executive Leather Chair', 'Furniture', 450.00),
(11, 'Bluetooth Speaker', 'Electronics', 80.00),
(12, 'Webcam HD Pro', 'Accessories', 90.00),
(13, 'Laptop Stand', 'Accessories', 45.00),
(14, 'Project Management Tool (1yr)', 'Software', 400.00),
(15, 'Smartwatch', 'Electronics', 220.00);
"""

inser_orders = """
INSERT INTO orders (order_id, customer_id, order_date, total_amount) VALUES
(101, 1, '2024-01-12', 1240.00),
(102, 2, '2024-03-05', 340.00),
(103, 3, '2024-02-20', 1600.00),
(104, 1, '2024-04-02', 330.00),
(105, 4, '2024-05-15', 480.00),
(106, 5, '2024-06-10', 180.00);
(107, 6, '2024-01-20', 440.00),
(108, 7, '2024-02-10', 130.00),
(109, 8, '2024-02-15', 250.00),
(110, 1, '2024-03-01', 45.00),
(111, 10, '2024-03-12', 450.00),
(112, 11, '2024-04-05', 80.00),
(113, 15, '2024-04-10', 170.00),
(114, 2, '2024-05-01', 400.00),
(115, 9, '2024-05-08', 300.00),
(116, 4, '2024-05-20', 90.00),
(117, 7, '2024-06-01', 350.00),
(118, 12, '2024-06-05', 45.00),
(119, 1, '2023-12-15', 220.00),
(120, 3, '2024-01-18', 130.00),
(121, 5, '2024-03-22', 60.00);
"""

insert_order_items = """
INSERT INTO order_items (item_id, order_id, product_id, quantity, subtotal) VALUES
(1, 101, 1, 1, 1200.00),
(2, 101, 2, 1, 40.00),
(3, 102, 2, 2, 80.00),
(4, 102, 4, 1, 150.00),
(5, 103, 3, 5, 1500.00),
(6, 103, 2, 2, 80.00),
(7, 104, 5, 1, 180.00),
(8, 104, 2, 3, 120.00),
(9, 105, 4, 3, 450.00),
(10, 106, 5, 1, 180.00);
(11, 107, 8, 1, 350.00),
(12, 107, 12, 1, 90.00),
(13, 108, 7, 1, 130.00),
(14, 109, 9, 1, 250.00),
(15, 110, 13, 1, 45.00),
(16, 111, 10, 1, 450.00),
(17, 112, 11, 1, 80.00),
(18, 113, 12, 1, 90.00),
(19, 113, 6, 1, 60.00),
(20, 114, 14, 1, 400.00),
(21, 115, 3, 1, 300.00),
(22, 116, 12, 1, 90.00),
(23, 117, 8, 1, 350.00),
(24, 118, 13, 1, 45.00),
(25, 119, 15, 1, 220.00),
(26, 120, 7, 1, 130.00),
(27, 121, 6, 1, 60.00),
(28, 107, 2, 1, 40.00),
(29, 115, 5, 2, 360.00),
(30, 119, 2, 2, 80.00);
"""

#List of all statements to execute
sql_statements = [
    create_customers_table,
    create_products_table,
    create_orders_table,
    create_order_items_table,
    insert_customers,
    insert_products,
    inser_orders,
    insert_order_items
]

def setup_database():
    try:
        with engine.connect() as conn:
            print("Connection established")
            for stmt in sql_statements:
                conn.execute(text(stmt))
            conn.commit()
        print("Database 'retail.db' created and populated successfully.")
    except Exception as e:
        print(f"An error occurred: {e}")
        
if __name__ == "__main__":
    setup_database()