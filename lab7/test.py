import unittest
import sys
import os
from io import StringIO
from contextlib import redirect_stdout

# Add the current directory to the path so we can import main
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from main import (
    connect_to_database,
    execute_query,
    display_menu,
    display_single_queries,
    display_inner_join_queries,
    display_group_by_queries,
    display_all_queries
)
from queries import (
    SINGLE_QUERIES,
    INNER_JOIN_QUERIES,
    GROUP_BY_QUERIES,
    ALL_QUERIES
)

class TestDatabaseConnection(unittest.TestCase):
    
    def test_connect_to_database_success(self):
        """Test successful database connection"""
        result = connect_to_database()
        
        self.assertIsNotNone(result)
        self.assertTrue(result.is_connected())
        
        # Clean up
        if result:
            result.close()
    
    def test_connect_to_database_connection_properties(self):
        """Test that connection has expected properties"""
        connection = connect_to_database()
        
        if connection:
            self.assertTrue(connection.is_connected())
            # Test that we can create a cursor
            cursor = connection.cursor()
            self.assertIsNotNone(cursor)
            cursor.close()
            connection.close()
        else:
            self.skipTest("Database connection failed - skipping test")

class TestQueryExecution(unittest.TestCase):
    
    def setUp(self):
        """Set up test fixtures"""
        self.connection = connect_to_database()
        if not self.connection:
            self.skipTest("Database connection failed - skipping query tests")
    
    def tearDown(self):
        """Clean up test fixtures"""
        if self.connection and self.connection.is_connected():
            self.connection.close()
    
    def test_execute_query_success(self):
        """Test successful query execution with real data"""
        query = "SELECT customer_id, password FROM customers LIMIT 5"
        query_name = "Test Query"
        
        # Capture and suppress output
        output = StringIO()
        with redirect_stdout(output):
            try:
                execute_query(self.connection, query, query_name)
                self.assertTrue(True)  # If we get here, the function executed successfully
            except Exception as e:
                self.fail(f"execute_query raised an exception: {e}")
    
    def test_execute_query_no_results(self):
        """Test query execution with no results"""
        query = "SELECT customer_id, password FROM customers WHERE customer_id = -1"
        query_name = "Empty Query"
        
        output = StringIO()
        with redirect_stdout(output):
            try:
                execute_query(self.connection, query, query_name)
                self.assertTrue(True)
            except Exception as e:
                self.fail(f"execute_query raised an exception: {e}")
    
    def test_execute_query_database_error(self):
        """Test query execution with database error"""
        query = "SELECT * FROM nonexistent_table"
        query_name = "Error Query"
        
        output = StringIO()
        with redirect_stdout(output):
            try:
                execute_query(self.connection, query, query_name)
                self.assertTrue(True)
            except Exception as e:
                self.fail(f"execute_query should handle exceptions gracefully: {e}")
    
    def test_all_single_queries(self):
        """Test all single queries execute without errors"""
        for query_name, query in SINGLE_QUERIES.items():
            with self.subTest(query_name=query_name):
                output = StringIO()
                with redirect_stdout(output):
                    try:
                        execute_query(self.connection, query, query_name)
                        self.assertTrue(True)
                    except Exception as e:
                        self.fail(f"Query '{query_name}' failed: {e}")
    
    def test_all_inner_join_queries(self):
        """Test all inner join queries execute without errors"""
        for query_name, query in INNER_JOIN_QUERIES.items():
            with self.subTest(query_name=query_name):
                output = StringIO()
                with redirect_stdout(output):
                    try:
                        execute_query(self.connection, query, query_name)
                        self.assertTrue(True)
                    except Exception as e:
                        self.fail(f"Query '{query_name}' failed: {e}")
    
    def test_all_group_by_queries(self):
        """Test all group by queries execute without errors"""
        for query_name, query in GROUP_BY_QUERIES.items():
            with self.subTest(query_name=query_name):
                output = StringIO()
                with redirect_stdout(output):
                    try:
                        execute_query(self.connection, query, query_name)
                        self.assertTrue(True)
                    except Exception as e:
                        self.fail(f"Query '{query_name}' failed: {e}")

class TestMenuFunctions(unittest.TestCase):
    
    def test_display_menu(self):
        """Test main menu display"""
        # We'll test that the function doesn't crash and returns a string
        # Note: This test will pause for input, so we'll just verify the function exists
        self.assertTrue(callable(display_menu))
    
    def test_display_single_queries(self):
        """Test single queries menu"""
        self.assertTrue(callable(display_single_queries))
        self.assertEqual(len(SINGLE_QUERIES), 3)  # Should have 3 single queries
    
    def test_display_inner_join_queries(self):
        """Test inner join queries menu"""
        self.assertTrue(callable(display_inner_join_queries))
        self.assertEqual(len(INNER_JOIN_QUERIES), 5)  # Should have 5 inner join queries
    
    def test_display_group_by_queries(self):
        """Test group by queries menu"""
        self.assertTrue(callable(display_group_by_queries))
        self.assertEqual(len(GROUP_BY_QUERIES), 5)  # Should have 5 group by queries
    
    def test_display_all_queries(self):
        """Test all queries menu"""
        self.assertTrue(callable(display_all_queries))
        self.assertEqual(len(ALL_QUERIES), 13)  # Should have 13 total queries

class TestQueryCollections(unittest.TestCase):
    
    def test_single_queries_structure(self):
        """Test that single queries have expected structure"""
        for query_name, query in SINGLE_QUERIES.items():
            self.assertIsInstance(query_name, str)
            self.assertIsInstance(query, str)
            self.assertIn("SELECT", query.upper())
            self.assertIn("FROM", query.upper())
    
    def test_inner_join_queries_structure(self):
        """Test that inner join queries have expected structure"""
        for query_name, query in INNER_JOIN_QUERIES.items():
            self.assertIsInstance(query_name, str)
            self.assertIsInstance(query, str)
            self.assertIn("SELECT", query.upper())
            self.assertIn("INNER JOIN", query.upper())
    
    def test_group_by_queries_structure(self):
        """Test that group by queries have expected structure"""
        for query_name, query in GROUP_BY_QUERIES.items():
            self.assertIsInstance(query_name, str)
            self.assertIsInstance(query, str)
            self.assertIn("SELECT", query.upper())
            self.assertIn("GROUP BY", query.upper())
    
    def test_all_queries_consistency(self):
        """Test that all queries collection is consistent"""
        expected_total = len(SINGLE_QUERIES) + len(INNER_JOIN_QUERIES) + len(GROUP_BY_QUERIES)
        self.assertEqual(len(ALL_QUERIES), expected_total)
        
        # Check that all individual queries are included in ALL_QUERIES
        for query_name in SINGLE_QUERIES:
            self.assertIn(query_name, ALL_QUERIES)
        for query_name in INNER_JOIN_QUERIES:
            self.assertIn(query_name, ALL_QUERIES)
        for query_name in GROUP_BY_QUERIES:
            self.assertIn(query_name, ALL_QUERIES)

class TestQueryContent(unittest.TestCase):
    
    def test_authenticate_customer_query(self):
        """Test authenticate customer query structure"""
        query = SINGLE_QUERIES["authenticate_customer"]
        self.assertIn("customers", query.lower())
        self.assertIn("email_address", query.lower())
        self.assertIn("customer_id", query.lower())
        self.assertIn("password", query.lower())
    
    def test_products_with_categories_query(self):
        """Test products with categories query structure"""
        query = INNER_JOIN_QUERIES["products_with_categories_and_price"]
        self.assertIn("products", query.lower())
        self.assertIn("categories", query.lower())
        self.assertIn("inner join", query.lower())
        self.assertIn("final_price", query.lower())
    
    def test_customers_per_state_query(self):
        """Test customers per state query structure"""
        query = GROUP_BY_QUERIES["customers_per_state"]
        self.assertIn("addresses", query.lower())
        self.assertIn("state", query.lower())
        self.assertIn("group by", query.lower())
        self.assertIn("count", query.lower())

if __name__ == '__main__':
    # Run tests using unittest.main() which is the modern approach
    unittest.main(verbosity=2) 