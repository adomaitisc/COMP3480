# Lab 5: MySQL Queries Implementation
# All queries from the README organized by type

# =============================================================================
# SINGLE QUERIES (3)
# =============================================================================

# 1. Authenticate a customer by email
AUTHENTICATE_CUSTOMER = """
SELECT customer_id, password
FROM customers
WHERE email_address = 'erinv@gmail.com';
"""

# 2. List all administrators with contact details
LIST_ADMINISTRATORS = """
SELECT admin_id, email_address, first_name, last_name
FROM administrators;
"""

# 3. Show all product categories
SHOW_CATEGORIES = """
SELECT category_id, category_name
FROM categories;
"""

# =============================================================================
# INNER JOIN QUERIES (5)
# =============================================================================

# 1. Products with category names and calculated final price
PRODUCTS_WITH_CATEGORIES_AND_PRICE = """
SELECT c.category_name,
       p.product_code,
       p.product_name,
       (p.list_price - p.list_price * p.discount_percent / 100) AS final_price
FROM products AS p
INNER JOIN categories AS c
ON p.category_id = c.category_id;
"""

# 2. Customers with their shipping address details
CUSTOMERS_WITH_SHIPPING_ADDRESS = """
SELECT c.customer_id,
       c.first_name,
       c.last_name,
       a.line1,
       a.city,
       a.state,
       a.zip_code
FROM customers AS c
INNER JOIN addresses AS a
ON c.shipping_address_id = a.address_id;
"""

# 3. Orders with customer name and ship address
ORDERS_WITH_CUSTOMER_AND_ADDRESS = """
SELECT o.order_id,
       c.first_name,
       c.last_name,
       a.line1 AS ship_address,
       o.ship_date
FROM orders AS o
INNER JOIN customers AS c
ON o.customer_id = c.customer_id
INNER JOIN addresses AS a
ON o.ship_address_id = a.address_id;
"""

# 4. Order items with product name and order date
ORDER_ITEMS_WITH_PRODUCT_AND_DATE = """
SELECT oi.order_id,
       o.order_date,
       p.product_name,
       oi.quantity,
       oi.item_price
FROM order_items AS oi
INNER JOIN orders AS o
ON oi.order_id = o.order_id
INNER JOIN products AS p
ON oi.product_id = p.product_id;
"""

# 5. Order items grouped by product category (join only)
ORDER_ITEMS_BY_CATEGORY = """
SELECT oi.item_id,
       p.product_name,
       c.category_name
FROM order_items AS oi
INNER JOIN products AS p
ON oi.product_id = p.product_id
INNER JOIN categories AS c
ON p.category_id = c.category_id;
"""

# =============================================================================
# GROUP-BY QUERIES (5)
# =============================================================================

# 1. Count number of customers per state
CUSTOMERS_PER_STATE = """
SELECT a.state,
       COUNT(*) AS num_customers
FROM addresses AS a
GROUP BY a.state;
"""

# 2. Total quantity sold per product
TOTAL_QUANTITY_PER_PRODUCT = """
SELECT p.product_name,
       SUM(oi.quantity) AS total_sold
FROM order_items AS oi
INNER JOIN products AS p
ON p.product_id = oi.product_id
GROUP BY p.product_name;
"""

# 3. Products grouped by category
PRODUCTS_BY_CATEGORY = """
SELECT c.category_name,
       COUNT(*) AS product_count
FROM products AS p
INNER JOIN categories AS c
ON p.category_id = c.category_id
GROUP BY c.category_name;
"""

# 4. Maximum order value (ship + tax) per customer
MAX_ORDER_VALUE_PER_CUSTOMER = """
SELECT o.customer_id,
       MAX(o.ship_amount + o.tax_amount) AS max_order_value
FROM orders AS o
GROUP BY o.customer_id;
"""

# 5. Number of orders and total revenue per month
ORDERS_AND_REVENUE_PER_MONTH = """
SELECT DATE_FORMAT(order_date, '%Y-%m') AS order_month,
       COUNT(*) AS order_count,
       SUM(ship_amount + tax_amount) AS revenue
FROM orders
GROUP BY order_month;
"""

# =============================================================================
# QUERY COLLECTIONS FOR EASY ACCESS
# =============================================================================

SINGLE_QUERIES = {
    "authenticate_customer": AUTHENTICATE_CUSTOMER,
    "list_administrators": LIST_ADMINISTRATORS,
    "show_categories": SHOW_CATEGORIES
}

INNER_JOIN_QUERIES = {
    "products_with_categories_and_price": PRODUCTS_WITH_CATEGORIES_AND_PRICE,
    "customers_with_shipping_address": CUSTOMERS_WITH_SHIPPING_ADDRESS,
    "orders_with_customer_and_address": ORDERS_WITH_CUSTOMER_AND_ADDRESS,
    "order_items_with_product_and_date": ORDER_ITEMS_WITH_PRODUCT_AND_DATE,
    "order_items_by_category": ORDER_ITEMS_BY_CATEGORY
}

GROUP_BY_QUERIES = {
    "customers_per_state": CUSTOMERS_PER_STATE,
    "total_quantity_per_product": TOTAL_QUANTITY_PER_PRODUCT,
    "products_by_category": PRODUCTS_BY_CATEGORY,
    "max_order_value_per_customer": MAX_ORDER_VALUE_PER_CUSTOMER,
    "orders_and_revenue_per_month": ORDERS_AND_REVENUE_PER_MONTH
}

ALL_QUERIES = {
    **SINGLE_QUERIES,
    **INNER_JOIN_QUERIES,
    **GROUP_BY_QUERIES
}
