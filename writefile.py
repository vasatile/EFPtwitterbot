import os
import psycopg2
from urllib.parse import urlparse

class PostgresWriter:
    def __init__(self):
        # Get the DATABASE_URL from environment variables
        db_url = os.getenv('DATABASE_URL')
        
        if not db_url:
            print("DATABASE_URL environment variable is not set.")
            return
        
        # Parse the DATABASE_URL
        url = urlparse(db_url)
        
        # Extract the database connection info
        host = url.hostname
        user = url.username
        password = url.password
        database = url.path[1:]  # Remove the leading '/' from the path
        port = url.port

        # Establish the database connection
        try:
            self.conn = psycopg2.connect(
                host=host,
                user=user,
                password=password,
                dbname=database,
                port=port
            )
            self.cursor = self.conn.cursor()
            print("Connected to PostgreSQL database successfully.")
            print(f"Connected to database: {self.conn.get_dsn_parameters()['dbname']}")
        except psycopg2.Error as err:
            print(f"Connection error: {err}")

    def read_existing_followings(self):
        """Read existing followings from PostgreSQL table."""
        return self._read_existing_data('followings')

    def read_existing_blockings(self):
        """Read existing blockings from PostgreSQL table."""
        return self._read_existing_data('blocking')

    def read_existing_mutings(self):
        """Read existing mutings from PostgreSQL table."""
        return self._read_existing_data('muting')

    def _read_existing_data(self, table):
        """Generic method to read existing data from a given table."""
        existing_data = {}
        if not self.table_exists(table):
            print(f"Table {table} does not exist.")
            return existing_data
        
        try:
            # Use double quotes for case-sensitive table names
            self.cursor.execute(f'SELECT address, fetched_addresses FROM "{table}"')
            rows = self.cursor.fetchall()
            for address, fetched_addresses in rows:
                fetched_set = set(fetched_addresses.split(',')) if fetched_addresses else set()
                existing_data[address] = fetched_set
        except psycopg2.Error as err:
            print(f"Error reading from {table}: {err}")
            self.conn.rollback()  # Rollback on error
        return existing_data

    def table_exists(self, table):
        """Check if a table exists in the database."""
        self.cursor.execute("""
            SELECT EXISTS (
                SELECT 1 
                FROM information_schema.tables 
                WHERE table_name = %s
            )
        """, (table,))
        return self.cursor.fetchone()[0]

    def write_data(self, table, data):
        """
        Writes the given data to the specified PostgreSQL table.
        data should be a list of lists where each inner list represents a row.
        Example: data = [['address1', 'new_following1'], ['address2', 'new_following2']]
        """
        try:
            for row in data:
                address = row[0]  # Assuming your column is named address
                new_address = row[1]
                self.cursor.execute(f"""
                    INSERT INTO "{table}" (address, fetched_addresses) 
                    VALUES (%s, %s)
                    ON CONFLICT (address) DO UPDATE 
                    SET fetched_addresses = CONCAT(EXCLUDED.fetched_addresses, ',', %s)
                """, (address, new_address, new_address))

            # Commit the transaction
            self.conn.commit()
            print(f"Data written to {table} table successfully.")
        
        except psycopg2.Error as err:
            print(f"Error writing to {table}: {err}")
            self.conn.rollback()  # Rollback the transaction on error

    def close_connection(self):
        """Close the database connection."""
        self.cursor.close()
        self.conn.close()
        print("Database connection closed.")
