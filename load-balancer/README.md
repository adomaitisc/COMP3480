# Load Balancer with Nginx

The goal of this activity is to create a load balancer using Nginx and 2 FastAPI applications. The FastAPI applications are very simple, and serve just enough content to validate that the load balancer is working.

## Important Notes

- The Nginx service will proxy the requests to the FastAPI applications.
- The configuration file is in the `nginx.conf` file, and it will be mounted to the Nginx container as a volume.
- You must build the application images before running the Docker Compose command.

## Starting the containers

```sh
docker compose up -d
```

## Stopping the containers

```sh
docker compose down
```
