<<<<<<< HEAD
# Lab 5: MySQL Locally

In this lab, we'll install MySQL locally and execute a series of queries agaisnt the provided `my_guitar_shop` database.

## MySQL Installation (MacOS)
```sh
brew install mysql

brew services start mysql
```

## Accessing database from `.sql` file
```sh
# creating the database
mysql -u root < createguitar.sql

# accessing the database
mysql -u root -p my_guitar_shop
```

## Single Queries (3)
```sql
-- 1. Authenticate a customer by email
SELECT customer_id, password
FROM customers
WHERE email_address = 'erinv@gmail.com';

-- 2. List all administrators with contact details
SELECT admin_id, email_address, first_name, last_name
FROM administrators;

-- 3. Show all product categories
SELECT category_id, category_name
FROM categories;
```

## Inner Join Queries (5)
```sql
-- 1. Products with category names and calculated final price
SELECT c.category_name,
       p.product_code,
       p.product_name,
       (p.list_price - p.list_price * p.discount_percent / 100) AS final_price
FROM products AS p
INNER JOIN categories AS c
ON p.category_id = c.category_id;

-- 2. Customers with their shipping address details
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

-- 3. Orders with customer name and ship address
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

-- 4. Order items with product name and order date
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

-- 5. Order items grouped by product category (join only)
SELECT oi.item_id,
       p.product_name,
       c.category_name
FROM order_items AS oi
INNER JOIN products AS p
ON oi.product_id = p.product_id
INNER JOIN categories AS c
ON p.category_id = c.category_id;
```

## Group-By Queries (5)
```sql
-- 1. Count number of customers per state
SELECT a.state,
       COUNT(*) AS num_customers
FROM addresses AS a
GROUP BY a.state

-- 2. Total quantity sold per product
SELECT p.product_name,
       SUM(oi.quantity) AS total_sold
FROM order_items as oi
ON p.product_id = oi.product_id
GROUP BY p.product_name;

-- 3. Products grouped by category
SELECT c.category_name,
       COUNT(*) AS product_count
FROM products AS p
INNER JOIN categories as c
ON p.category_id = c.category_id
GROUP BY c.category_name;

-- 4. Maximum order value (ship + tax) pre customer
SELECT o.customer_id,
       MAX(o.ship_amount + o.tax_amount) AS max_order_value
FROM orders AS o
GROUP BY o.customer_id;

-- 5. Number of orders and total revenue per month
SELECT DATE_FORMAT(order_date, '%Y-%m') AS order_month,
       COUNT(*) AS order_count,
       SUM(ship_amount + tax_amount) AS revenue
FROM orders
GROUP BY order_month;
```
=======
## Queries

Products:

```sql
-- Select all products along with their Categories (category_id -> category.category_id -> category.category_name)
-- Ordered alphabetically, based on Product name
mysql> SELECT categories.category_name,
       product_code, product_name, description, list_price, discount_percent,
       (list_price - list_price * discount_percent / 100) as final_price
       FROM products INNER JOIN categories
         ON products.category_id = categories.category_id
       ORDER BY product_name ASC; 

-- Same query, filtering by price range
-- Unfortunately, we can't use the final_price in the WHERE clause, so we must calculate again.
mysql> SELECT categories.category_name,
       product_code, product_name, description, list_price, discount_percent,
       (list_price - list_price * discount_percent / 100) as final_price
       FROM products INNER JOIN categories
         ON products.category_id = categories.category_id
       WHERE (list_price - list_price * discount_percent / 100) BETWEEN 49.99 AND 149.99
       ORDER BY product_name ASC;


>>>>>>> 7d83fe4 (lab5)
