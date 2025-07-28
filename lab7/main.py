import mysql.connector
from mysql.connector import Error
from queries import (
    SINGLE_QUERIES, 
    INNER_JOIN_QUERIES, 
    GROUP_BY_QUERIES, 
    ALL_QUERIES
)

def connect_to_database():
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='root',
            password='WaterLab@6',
            database='my_guitar_shop'
        )
        if connection.is_connected():
            return connection
    except Error as e:
        print(f"Error connecting to MySQL: {e}")
        return None

def execute_query(connection, query, query_name):
    try:
        cursor = connection.cursor()
        cursor.execute(query)
        results = cursor.fetchall()
        
        # Get column names
        columns = [desc[0] for desc in cursor.description]
        
        print(f"\nResults for: {query_name}")
        print("=" * 80)
        
        if results:
            # Calculate column widths based on content
            col_widths = []
            for i, col in enumerate(columns):
                # Start with column name width
                max_width = len(str(col))
                # Check all values in this column
                for row in results:
                    val_width = len(str(row[i])) if row[i] is not None else 4
                    max_width = max(max_width, val_width)
                # Add some padding and cap at reasonable width
                col_widths.append(min(max_width + 2, 30))
            
            # Print column headers
            header_parts = []
            for i, col in enumerate(columns):
                header_parts.append(f"{col:<{col_widths[i]}}")
            header = " | ".join(header_parts)
            print(header)
            print("-" * len(header))
            
            # Print data rows
            for row in results:
                row_parts = []
                for i, val in enumerate(row):
                    # Handle None values
                    display_val = str(val) if val is not None else "NULL"
                    # Truncate if too long
                    if len(display_val) > col_widths[i] - 2:
                        display_val = display_val[:col_widths[i] - 5] + "..."
                    row_parts.append(f"{display_val:<{col_widths[i]}}")
                formatted_row = " | ".join(row_parts)
                print(formatted_row)
            
            print(f"\nTotal rows returned: {len(results)}")
        else:
            print("No results found.")
            
        cursor.close()
        
    except Error as e:
        print(f"Error executing query: {e}")

def display_menu():
    print("\n" + "=" * 60)
    print("Lab 7: Containerized MySQL with Python Driver")
    print("=" * 60)
    
    print("\nAvailable Query Categories:")
    print("1. Single Queries")
    print("2. Inner Join Queries") 
    print("3. Group-By Queries")
    print("4. All Queries")
    print("0. Exit")
    
    return input("\nSelect a category (0-4): ")

def display_single_queries():
    print("\n" + "-" * 40)
    print("SINGLE QUERIES")
    print("-" * 40)
    
    queries = list(SINGLE_QUERIES.items())
    for i, (key, query) in enumerate(queries, 1):
        # Extract a readable name from the key
        name = key.replace('_', ' ').title()
        print(f"{i}. {name}")
    
    print("0. Back to main menu")
    return input("\nSelect a query (0-3): ")

def display_inner_join_queries():
    print("\n" + "-" * 40)
    print("INNER JOIN QUERIES")
    print("-" * 40)
    
    queries = list(INNER_JOIN_QUERIES.items())
    for i, (key, query) in enumerate(queries, 1):
        # Extract a readable name from the key
        name = key.replace('_', ' ').title()
        print(f"{i}. {name}")
    
    print("0. Back to main menu")
    return input("\nSelect a query (0-5): ")

def display_group_by_queries():
    print("\n" + "-" * 40)
    print("GROUP-BY QUERIES")
    print("-" * 40)
    
    queries = list(GROUP_BY_QUERIES.items())
    for i, (key, query) in enumerate(queries, 1):
        # Extract a readable name from the key
        name = key.replace('_', ' ').title()
        print(f"{i}. {name}")
    
    print("0. Back to main menu")
    return input("\nSelect a query (0-5): ")

def display_all_queries():
    print("\n" + "-" * 40)
    print("ALL QUERIES")
    print("-" * 40)
    
    queries = list(ALL_QUERIES.items())
    for i, (key, query) in enumerate(queries, 1):
        # Extract a readable name from the key
        name = key.replace('_', ' ').title()
        print(f"{i}. {name}")
    
    print("0. Back to main menu")
    return input(f"\nSelect a query (0-{len(queries)}): ")

def main():
    connection = connect_to_database()
    if not connection:
        print("Failed to connect to database. Please ensure MySQL is running and the database exists.")
        return
    
    try:
        while True:
            choice = display_menu()
            
            if choice == '0':
                print("\nGoodbye!")
                break
            elif choice == '1':
                sub_choice = display_single_queries()
                if sub_choice == '0':
                    continue
                try:
                    query_index = int(sub_choice) - 1
                    if 0 <= query_index < len(SINGLE_QUERIES):
                        query_name, query = list(SINGLE_QUERIES.items())[query_index]
                        execute_query(connection, query, query_name.replace('_', ' ').title())
                    else:
                        print("Invalid selection. Please try again.")
                except ValueError:
                    print("Please enter a valid number.")
                    
            elif choice == '2':
                sub_choice = display_inner_join_queries()
                if sub_choice == '0':
                    continue
                try:
                    query_index = int(sub_choice) - 1
                    if 0 <= query_index < len(INNER_JOIN_QUERIES):
                        query_name, query = list(INNER_JOIN_QUERIES.items())[query_index]
                        execute_query(connection, query, query_name.replace('_', ' ').title())
                    else:
                        print("Invalid selection. Please try again.")
                except ValueError:
                    print("Please enter a valid number.")
                    
            elif choice == '3':
                sub_choice = display_group_by_queries()
                if sub_choice == '0':
                    continue
                try:
                    query_index = int(sub_choice) - 1
                    if 0 <= query_index < len(GROUP_BY_QUERIES):
                        query_name, query = list(GROUP_BY_QUERIES.items())[query_index]
                        execute_query(connection, query, query_name.replace('_', ' ').title())
                    else:
                        print("Invalid selection. Please try again.")
                except ValueError:
                    print("Please enter a valid number.")
                    
            elif choice == '4':
                sub_choice = display_all_queries()
                if sub_choice == '0':
                    continue
                try:
                    query_index = int(sub_choice) - 1
                    if 0 <= query_index < len(ALL_QUERIES):
                        query_name, query = list(ALL_QUERIES.items())[query_index]
                        execute_query(connection, query, query_name.replace('_', ' ').title())
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
        if connection and connection.is_connected():
            connection.close()

if __name__ == "__main__":
    main()


