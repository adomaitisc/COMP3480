import redis
import boto3
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from operations import (
    MINIO_OPERATIONS,
    REDIS_OPERATIONS,
    EMAIL_OPERATIONS,
    ALL_OPERATIONS
)

def connect_to_redis():
    """Connect to Redis server"""
    try:
        r = redis.Redis(
            host='localhost',
            port=6379,
            password='redispassword',
            decode_responses=True
        )
        # Test connection
        r.ping()
        print("Connected to Redis successfully")
        return r
    except Exception as e:
        print(f"Error connecting to Redis: {e}")
        return None

def connect_to_minio():
    """Connect to MinIO server"""
    try:
        s3_client = boto3.client(
            's3',
            endpoint_url='http://localhost:9000',
            aws_access_key_id='minioadmin',
            aws_secret_access_key='minioadmin',
            region_name='us-east-1'
        )
        # Test connection by listing buckets
        s3_client.list_buckets()
        print("Connected to MinIO successfully")
        return s3_client
    except Exception as e:
        print(f"Error connecting to MinIO: {e}")
        return None

def connect_to_postfix():
    """Test Postfix connection"""
    try:
        # Test SMTP connection without authentication
        server = smtplib.SMTP('localhost', 25)
        server.quit()
        print("Connected to Postfix successfully")
        return True
    except Exception as e:
        print(f"Postfix connection issue: {e}")
        print("   (Email operations may still work)")
        return True  # Return True to allow testing email operations

def execute_minio_operation(s3_client, operation_name, operation_func):
    """Execute a MinIO operation"""
    try:
        print(f"\nExecuting: {operation_name}")
        print("=" * 80)
        result = operation_func(s3_client)
        if result:
            print("Operation completed successfully")
        else:
            print("Operation failed")
    except Exception as e:
        print(f"Error executing operation: {e}")

def execute_redis_operation(redis_client, operation_name, operation_func):
    """Execute a Redis operation"""
    try:
        print(f"\nExecuting: {operation_name}")
        print("=" * 80)
        result = operation_func(redis_client)
        if result:
            print("Operation completed successfully")
        else:
            print("Operation failed")
    except Exception as e:
        print(f"Error executing operation: {e}")

def execute_email_operation(operation_name, operation_func):
    """Execute an email operation"""
    try:
        print(f"\nExecuting: {operation_name}")
        print("=" * 80)
        result = operation_func()
        if result:
            print("Operation completed successfully")
        else:
            print("Operation failed")
    except Exception as e:
        print(f"Error executing operation: {e}")

def display_menu():
    print("\n" + "=" * 60)
    print("Lab 8: Containerized Services with Python Driver")
    print("=" * 60)
    
    print("\nAvailable Service Categories:")
    print("1. MinIO Operations (Object Storage)")
    print("2. Redis Operations (Caching/Memory)")
    print("3. Email Operations (Postfix)")
    print("4. All Operations")
    print("0. Exit")
    
    return input("\nSelect a category (0-4): ")

def display_minio_operations():
    print("\n" + "-" * 40)
    print("MINIO OPERATIONS")
    print("-" * 40)
    
    operations = list(MINIO_OPERATIONS.items())
    for i, (key, _) in enumerate(operations, 1):
        name = key.replace('_', ' ').title()
        print(f"{i}. {name}")
    
    print("0. Back to main menu")
    return input(f"\nSelect an operation (0-{len(operations)}): ")

def display_redis_operations():
    print("\n" + "-" * 40)
    print("REDIS OPERATIONS")
    print("-" * 40)
    
    operations = list(REDIS_OPERATIONS.items())
    for i, (key, _) in enumerate(operations, 1):
        name = key.replace('_', ' ').title()
        print(f"{i}. {name}")
    
    print("0. Back to main menu")
    return input(f"\nSelect an operation (0-{len(operations)}): ")

def display_email_operations():
    print("\n" + "-" * 40)
    print("EMAIL OPERATIONS")
    print("-" * 40)
    
    operations = list(EMAIL_OPERATIONS.items())
    for i, (key, _) in enumerate(operations, 1):
        name = key.replace('_', ' ').title()
        print(f"{i}. {name}")
    
    print("0. Back to main menu")
    return input(f"\nSelect an operation (0-{len(operations)}): ")

def display_all_operations():
    print("\n" + "-" * 40)
    print("ALL OPERATIONS")
    print("-" * 40)
    
    operations = list(ALL_OPERATIONS.items())
    for i, (key, _) in enumerate(operations, 1):
        name = key.replace('_', ' ').title()
        print(f"{i}. {name}")
    
    print("0. Back to main menu")
    return input(f"\nSelect an operation (0-{len(operations)}): ")

def main():
    print("Connecting to services...")
    
    # Connect to all services
    redis_client = connect_to_redis()
    minio_client = connect_to_minio()
    postfix_connected = connect_to_postfix()
    
    if not redis_client and not minio_client and not postfix_connected:
        print("Failed to connect to any services. Please ensure all containers are running.")
        return
    
    try:
        while True:
            choice = display_menu()
            
            if choice == '0':
                print("\nGoodbye!")
                break
            elif choice == '1':
                if not minio_client:
                    print("MinIO is not available. Please ensure the container is running.")
                    continue
                    
                sub_choice = display_minio_operations()
                if sub_choice == '0':
                    continue
                try:
                    op_index = int(sub_choice) - 1
                    if 0 <= op_index < len(MINIO_OPERATIONS):
                        op_name, op_func = list(MINIO_OPERATIONS.items())[op_index]
                        execute_minio_operation(minio_client, op_name, op_func)
                    else:
                        print("Invalid selection. Please try again.")
                except ValueError:
                    print("Please enter a valid number.")
                    
            elif choice == '2':
                if not redis_client:
                    print("Redis is not available. Please ensure the container is running.")
                    continue
                    
                sub_choice = display_redis_operations()
                if sub_choice == '0':
                    continue
                try:
                    op_index = int(sub_choice) - 1
                    if 0 <= op_index < len(REDIS_OPERATIONS):
                        op_name, op_func = list(REDIS_OPERATIONS.items())[op_index]
                        execute_redis_operation(redis_client, op_name, op_func)
                    else:
                        print("Invalid selection. Please try again.")
                except ValueError:
                    print("Please enter a valid number.")
                    
            elif choice == '3':
                if not postfix_connected:
                    print("Postfix is not available. Please ensure the container is running.")
                    continue
                    
                sub_choice = display_email_operations()
                if sub_choice == '0':
                    continue
                try:
                    op_index = int(sub_choice) - 1
                    if 0 <= op_index < len(EMAIL_OPERATIONS):
                        op_name, op_func = list(EMAIL_OPERATIONS.items())[op_index]
                        execute_email_operation(op_name, op_func)
                    else:
                        print("Invalid selection. Please try again.")
                except ValueError:
                    print("Please enter a valid number.")
                    
            elif choice == '4':
                sub_choice = display_all_operations()
                if sub_choice == '0':
                    continue
                try:
                    op_index = int(sub_choice) - 1
                    if 0 <= op_index < len(ALL_OPERATIONS):
                        op_name, op_func = list(ALL_OPERATIONS.items())[op_index]
                        
                        # Determine which service this operation belongs to
                        if op_name in MINIO_OPERATIONS:
                            if minio_client:
                                execute_minio_operation(minio_client, op_name, op_func)
                            else:
                                print("MinIO is not available for this operation.")
                        elif op_name in REDIS_OPERATIONS:
                            if redis_client:
                                execute_redis_operation(redis_client, op_name, op_func)
                            else:
                                print("Redis is not available for this operation.")
                        elif op_name in EMAIL_OPERATIONS:
                            if postfix_connected:
                                execute_email_operation(op_name, op_func)
                            else:
                                print("Postfix is not available for this operation.")
                    else:
                        print("Invalid selection. Please try again.")
                except ValueError:
                    print("Please enter a valid number.")
            else:
                print("Invalid selection. Please try again.")
            
            input("\nPress Enter to continue...")
            
    except KeyboardInterrupt:
        print("\n\nGoodbye!")
    finally:
        if redis_client:
            redis_client.close()

if __name__ == "__main__":
    main()
