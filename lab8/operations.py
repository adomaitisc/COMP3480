import json
import time
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders

# =============================================================================
# MINIO OPERATIONS (Object Storage)
# =============================================================================

def list_buckets(s3_client):
    """List all buckets in MinIO"""
    try:
        response = s3_client.list_buckets()
        buckets = response['Buckets']
        
        print("Available buckets:")
        print("-" * 40)
        if buckets:
            for bucket in buckets:
                print(f"• {bucket['Name']} (Created: {bucket['CreationDate']})")
        else:
            print("No buckets found.")
        
        return True
    except Exception as e:
        print(f"Error listing buckets: {e}")
        return False

def create_bucket(s3_client):
    """Create a new bucket"""
    try:
        bucket_name = input("Enter bucket name: ")
        s3_client.create_bucket(Bucket=bucket_name)
        print(f"Bucket '{bucket_name}' created successfully")
        return True
    except Exception as e:
        print(f"Error creating bucket: {e}")
        return False

def upload_file(s3_client):
    """Upload a file to a bucket"""
    try:
        bucket_name = input("Enter bucket name: ")
        file_path = input("Enter file path to upload: ")
        object_name = input("Enter object name (or press Enter for same as file): ") or file_path.split('/')[-1]
        
        s3_client.upload_file(file_path, bucket_name, object_name)
        print(f"File uploaded successfully to s3://{bucket_name}/{object_name}")
        return True
    except Exception as e:
        print(f"Error uploading file: {e}")
        return False

def list_objects(s3_client):
    """List objects in a bucket"""
    try:
        bucket_name = input("Enter bucket name: ")
        response = s3_client.list_objects_v2(Bucket=bucket_name)
        
        print(f"Objects in bucket '{bucket_name}':")
        print("-" * 50)
        
        if 'Contents' in response:
            for obj in response['Contents']:
                print(f"• {obj['Key']} ({obj['Size']} bytes, Modified: {obj['LastModified']})")
        else:
            print("No objects found in bucket.")
        
        return True
    except Exception as e:
        print(f"Error listing objects: {e}")
        return False

def download_file(s3_client):
    """Download a file from a bucket"""
    try:
        bucket_name = input("Enter bucket name: ")
        object_name = input("Enter object name: ")
        local_path = input("Enter local file path: ")
        
        s3_client.download_file(bucket_name, object_name, local_path)
        print(f"File downloaded successfully to {local_path}")
        return True
    except Exception as e:
        print(f"Error downloading file: {e}")
        return False

# =============================================================================
# REDIS OPERATIONS (Caching/Memory)
# =============================================================================

def set_key_value(redis_client):
    """Set a key-value pair in Redis"""
    try:
        key = input("Enter key: ")
        value = input("Enter value: ")
        
        redis_client.set(key, value)
        print(f"Set {key} = {value}")
        return True
    except Exception as e:
        print(f"Error setting key-value: {e}")
        return False

def get_key_value(redis_client):
    """Get a value by key from Redis"""
    try:
        key = input("Enter key: ")
        value = redis_client.get(key)
        
        if value:
            print(f"{key} = {value}")
        else:
            print(f"Key '{key}' not found")
        
        return True
    except Exception as e:
        print(f"Error getting key-value: {e}")
        return False

def list_all_keys(redis_client):
    """List all keys in Redis"""
    try:
        pattern = input("Enter pattern (or press Enter for all keys): ") or "*"
        keys = redis_client.keys(pattern)
        
        print(f"Keys matching pattern '{pattern}':")
        print("-" * 40)
        
        if keys:
            for key in keys:
                value = redis_client.get(key)
                print(f"• {key} = {value}")
        else:
            print("No keys found.")
        
        return True
    except Exception as e:
        print(f"Error listing keys: {e}")
        return False

def delete_key(redis_client):
    """Delete a key from Redis"""
    try:
        key = input("Enter key to delete: ")
        result = redis_client.delete(key)
        
        if result:
            print(f"Key '{key}' deleted successfully")
        else:
            print(f"Key '{key}' not found")
        
        return True
    except Exception as e:
        print(f"Error deleting key: {e}")
        return False

def set_with_expiry(redis_client):
    """Set a key-value pair with expiration"""
    try:
        key = input("Enter key: ")
        value = input("Enter value: ")
        seconds = int(input("Enter expiration time in seconds: "))
        
        redis_client.setex(key, seconds, value)
        print(f"Set {key} = {value} (expires in {seconds} seconds)")
        return True
    except Exception as e:
        print(f"Error setting key with expiry: {e}")
        return False

def increment_counter(redis_client):
    """Increment a counter in Redis"""
    try:
        key = input("Enter counter key: ")
        increment = int(input("Enter increment value (default 1): ") or "1")
        
        result = redis_client.incrby(key, increment)
        print(f"Counter '{key}' incremented to {result}")
        return True
    except Exception as e:
        print(f"Error incrementing counter: {e}")
        return False

# =============================================================================
# EMAIL OPERATIONS (Postfix)
# =============================================================================

def send_simple_email():
    """Send a simple text email"""
    try:
        sender = input("Enter sender email: ")
        recipient = input("Enter recipient email: ")
        subject = input("Enter subject: ")
        message = input("Enter message: ")
        
        # Create message
        msg = MIMEMultipart()
        msg['From'] = sender
        msg['To'] = recipient
        msg['Subject'] = subject
        
        # Add body
        msg.attach(MIMEText(message, 'plain'))
        
        # Send email without authentication (for local testing)
        server = smtplib.SMTP('localhost', 25)
        
        text = msg.as_string()
        server.sendmail(sender, recipient, text)
        server.quit()
        
        print(f"Email sent successfully to {recipient}")
        return True
    except Exception as e:
        print(f"Error sending email: {e}")
        return False

def send_html_email():
    """Send an HTML email"""
    try:
        sender = input("Enter sender email: ")
        recipient = input("Enter recipient email: ")
        subject = input("Enter subject: ")
        html_content = input("Enter HTML content: ")
        
        # Create message
        msg = MIMEMultipart('alternative')
        msg['From'] = sender
        msg['To'] = recipient
        msg['Subject'] = subject
        
        # Add HTML content
        html_part = MIMEText(html_content, 'html')
        msg.attach(html_part)
        
        # Send email without authentication (for local testing)
        server = smtplib.SMTP('localhost', 25)
        
        text = msg.as_string()
        server.sendmail(sender, recipient, text)
        server.quit()
        
        print(f"HTML email sent successfully to {recipient}")
        return True
    except Exception as e:
        print(f"Error sending HTML email: {e}")
        return False

def test_smtp_connection():
    """Test SMTP connection to Postfix"""
    try:
        server = smtplib.SMTP('localhost', 25)
        
        print("SMTP connection successful")
        print(f"Server: {server.ehlo()[1]}")
        
        server.quit()
        return True
    except Exception as e:
        print(f"Error testing SMTP connection: {e}")
        return False

def send_bulk_email():
    """Send email to multiple recipients"""
    try:
        sender = input("Enter sender email: ")
        recipients_input = input("Enter recipient emails (comma-separated): ")
        recipients = [email.strip() for email in recipients_input.split(',')]
        subject = input("Enter subject: ")
        message = input("Enter message: ")
        
        # Create message
        msg = MIMEMultipart()
        msg['From'] = sender
        msg['Subject'] = subject
        msg.attach(MIMEText(message, 'plain'))
        
        # Send email to each recipient without authentication
        server = smtplib.SMTP('localhost', 25)
        
        text = msg.as_string()
        for recipient in recipients:
            msg['To'] = recipient
            server.sendmail(sender, recipient, text)
            print(f"Email sent to {recipient}")
        
        server.quit()
        print(f"Bulk email sent to {len(recipients)} recipients")
        return True
    except Exception as e:
        print(f"Error sending bulk email: {e}")
        return False

# =============================================================================
# OPERATION COLLECTIONS FOR EASY ACCESS
# =============================================================================

MINIO_OPERATIONS = {
    "list_buckets": list_buckets,
    "create_bucket": create_bucket,
    "upload_file": upload_file,
    "list_objects": list_objects,
    "download_file": download_file
}

REDIS_OPERATIONS = {
    "set_key_value": set_key_value,
    "get_key_value": get_key_value,
    "list_all_keys": list_all_keys,
    "delete_key": delete_key,
    "set_with_expiry": set_with_expiry,
    "increment_counter": increment_counter
}

EMAIL_OPERATIONS = {
    "send_simple_email": send_simple_email,
    "send_html_email": send_html_email,
    "test_smtp_connection": test_smtp_connection,
    "send_bulk_email": send_bulk_email
}

ALL_OPERATIONS = {
    **MINIO_OPERATIONS,
    **REDIS_OPERATIONS,
    **EMAIL_OPERATIONS
}
