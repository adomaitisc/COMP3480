# Lab 7: Containerized MySQL with Python Driver

The goal of this lab is to use the containerized MySQL database from the last lab and connect to it using a custom Python driver with an interactive query interface.

## Project Overview

This lab implements a complete MySQL database application with:

- **Containerized MySQL Database**: Using Docker Compose
- **Python Query Interface**: Interactive menu-driven application
- **Comprehensive Test Suite**: Unit tests for all functionality
- **13 Pre-built Queries**: Organized by type (Single, Inner Join, Group-By)

## Project Structure

```
lab7/
├── main.py              # Main application with interactive menu
├── queries.py           # All SQL queries organized by type
├── test.py              # Comprehensive unit test suite
├── requirements.txt     # Python dependencies
└── README.md            # This file
```

## Prerequisites

- Docker and Docker Compose installed
- Python 3.7+ with pip
- No conflicting MySQL instance running on port 3306
- [Lab 6 Instructions on Deploying the MySQL instance](../lab6/README.md)

## Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Run the Tests

```bash
python test.py
```

### 3. Run the Python Driver

```bash
python main.py
```

## Interactive Menu System

The application provides a hierarchical menu:

1. **Single Queries** (3 queries)
2. **Inner Join Queries** (5 queries)
3. **Group-By Queries** (5 queries)
4. **All Queries** (13 total queries)

## Queries

The queries are organized in the `queries.py` file, it is organized by type of query:

- Single Queries
- Inner Join Queries
- Group-By Queries

You can read more about the queries in the [Lab 5 README.md file.](../lab5/README.md)
