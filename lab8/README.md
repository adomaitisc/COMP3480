# Lab 8: Containerized Services with Python Driver

This lab demonstrates the use of multiple containerized services (MinIO, Redis, and Postfix) with a Python driver for interaction and management.

## Services Overview

### 1. MinIO (Object Storage)

- **Purpose**: S3-compatible object storage
- **Ports**: 9000 (API), 9001 (Web Console)
- **Credentials**: minioadmin / minioadmin
- **Web Console**: http://localhost:9001

### 2. Redis (Caching/Memory)

- **Purpose**: In-memory data structure store
- **Port**: 6379
- **Password**: redispassword
- **Features**: Key-value storage, caching, session management

### 3. Postfix (Email Server)

- **Purpose**: SMTP email server
- **Ports**: 25 (SMTP), 587 (SMTP Submission)
- **Credentials**: admin / password
- **Domain**: example.com

## Setup Instructions

### 1. Start the Services

```bash
docker-compose up -d
```

### 2. Install Python Dependencies

```bash
pip install -r requirements.txt
```

### 3. Run the Python Driver

```bash
python main.py
```

## Python Driver Features

The Python driver provides an interactive menu system to interact with all three services:

### MinIO Operations

- List buckets
- Create new buckets
- Upload files
- List objects in buckets
- Download files

### Redis Operations

- Set key-value pairs
- Get values by key
- List all keys
- Delete keys
- Set keys with expiration
- Increment counters

### Email Operations

- Send simple text emails
- Send HTML emails
- Test SMTP connection
- Send bulk emails

## Usage Examples

### MinIO Example

1. Start the driver: `python main.py`
2. Select "1" for MinIO Operations
3. Choose "2" to create a bucket
4. Enter bucket name: `my-bucket`
5. Choose "3" to upload a file
6. Enter bucket: `my-bucket`, file path, and object name

### Redis Example

1. Select "2" for Redis Operations
2. Choose "1" to set a key-value
3. Enter key: `user:123`, value: `John Doe`
4. Choose "2" to get the value
5. Enter key: `user:123`

### Email Example

1. Select "3" for Email Operations
2. Choose "1" to send a simple email
3. Enter sender, recipient, subject, and message
4. Email will be sent via Postfix

### Common Commands

```bash
# View all containers
docker-compose ps

# View logs
docker-compose logs

# Stop all services
docker-compose down

# Stop and remove volumes
docker-compose down -v

# Restart specific service
docker-compose restart redis
```

## File Structure

```
lab8/
├── docker-compose.yml    # Service definitions
├── main.py              # Python driver
├── operations.py        # Service operations
├── requirements.txt     # Python dependencies
└── README.md           # This file
```

## Notes

- All services use persistent volumes for data storage
- Services are configured with health checks
- The Python driver provides a user-friendly interface for all operations
- All services are accessible from localhost on their respective ports

## Postfix Email Server Addendum

### **Important Note About Email Testing**

The Postfix email server has limitations. Here's what you need to know:

#### **What Works:**

- SMTP server accepts connections on port 25
- Email messages are processed by Postfix
- Python driver can connect and send emails
- All email operations (simple, HTML, bulk) function correctly

#### **What Doesn't Work:**

- Emails to external domains (like gmail.com, wit.edu) will be rejected
- No actual email delivery to real recipients
- No SMTP authentication (uses port 25 without auth)

#### **Why This Happens:**

- Postfix is configured as a local mail server without external relay
- No MX records exist for test domains (example.com)
- No authentication is configured for security reasons

#### **For Real Email Testing:**

To send actual emails, you would need to:

1. Configure Postfix to relay through a real SMTP service (Gmail, SendGrid, etc.)
2. Set up proper authentication credentials
3. Use port 587 with STARTTLS and authentication
