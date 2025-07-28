# Lab 7: Containerized MySQL with Python Driver

The goal of this lab is to use the containerized MySQL database from the last lab and connect to it using a custom Python driver.

## Important

If there is an instance of MySQL running on your machine, you need to stop it before running the Docker Compose command otherwise you might be accessing the wrong database. Or you could change the port mappings in the Docker Compose file.

## Starting the container

Please, refer to the Lab 6 README.md file for instructions on how to start the container.

## Accessing the database with the Python Driver

The Python driver is a loop that will run until the connection is closed, it has the queries implemented in the lab 5 assignment.

```sh
python3 main.py
```

## Built in Queries and Functions

Please, refer to the Lab 5 README.md file for detailed intstructions and information on each query.
