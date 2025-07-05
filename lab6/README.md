# Lab 6: Containerized MySQL

The goal of this lab is to containerize the last lab's [Lab 5](../lab5) MySQL database. We will use Docker Compose to create a containerized MySQL database, allowing us to pass custom settings and environment variables to the container, as well as a dedicated volume to persist the database data.

## Important

If there is an instance of MySQL running on your machine, you need to stop it before running the Docker Compose command otherwise you might be accessing the wrong database. Or you could change the port mappings in the Docker Compose file.

## Starting the container

Simple up command, the flag `-d` means "detached" mode, meaning the container will run in the background and we won't have to keep the terminal open.

```sh
docker compose up -d
```

## Stopping the container

Stopping the container does not mean the data is gone, we have a special volume attribute at the Docker Compose file for data persistence.

```sh
docker compose down
```

## Importing the database
The `-h` flag allow us to set a host, which could even be remote. The `-P` specifies the port and the `-p` means you want to use password.
```sh
# First, we check if the database is accessible
mysql -h 127.0.0.1 -P 3306 -u root -p
# If it prompts for a password, and the one in the Docker Compose file is correct, we can proceed to import the database
mysql -h 127.0.0.1 -P 3306 -u root -p < createguitar.sql
```

## Accessing the database

```sh
mysql -h 127.0.0.1 -P 3306 -u root -p
```

## Accessing the database via IDE (DBeaver or TablePlus)

1. Open TablePlus and create a new MySQL connection
2. Set up the following connection settings:
   - Host: `localhost` or `127.0.0.1`
   - User: `root`
   - Password: `WaterLab@6`
   - Database: `my_guitar_shop`
   - Port: `3306`
   - SSL mode: `Disabled`

## Recalling a few queries

```sql
-- 1. Authenticate a customer by email
SELECT customer_id, password
FROM customers
WHERE email_address = 'erinv@gmail.com';

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

-- 3. Products grouped by category
SELECT c.category_name,
       COUNT(*) AS product_count
FROM products AS p
INNER JOIN categories as c
ON p.category_id = c.category_id
GROUP BY c.category_name;
```
