import mysql.connector

class MySQLWriter:
    def __init__(self, host, user, password, database):
        # Establish the database connection
        self.conn = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=database
        )
        self.cursor = self.conn.cursor()

    def read_existing_followings(self):
        """Read existing followings from MySQL table."""
        return self._read_existing_data('followings')

    def read_existing_blockings(self):
        """Read existing blockings from MySQL table."""
        return self._read_existing_data('blocking')

    def read_existing_mutings(self):
        """Read existing mutings from MySQL table."""
        return self._read_existing_data('muting')

    def _read_existing_data(self, table):
        """Generic method to read existing data from a given table."""
        existing_data = {}
        try:
            # Use the correct column names from your table
            self.cursor.execute(f"SELECT address, fetched_addresses FROM {table}")
            for (address, fetched_addresses) in self.cursor:
                fetched_set = set(fetched_addresses.split(',')) if fetched_addresses else set()
                existing_data[address] = fetched_set
        except mysql.connector.Error as err:
            print(f"Error: {err}")
        return existing_data

    def write_data(self, table, data):
        """
        Writes the given data to the specified MySQL table.
        `data` should be a list of lists where each inner list represents a row.
        Example: data = [['address1', 'new_following1'], ['address2', 'new_following2']]
        """
        try:
            for row in data:
                address = row[0]  # Assuming your column is named `user_address`
                new_address = row[1]
                self.cursor.execute(f"""
                    INSERT INTO {table} (address, fetched_addresses) 
                    VALUES (%s, %s)
                    ON DUPLICATE KEY UPDATE fetched_addresses = CONCAT(fetched_addresses, ',', %s)
                """, (address, new_address, new_address))

            # Commit the transaction
            self.conn.commit()
            print(f"Data written to {table} table successfully.")
        
        except mysql.connector.Error as err:
            print(f"Error: {err}")

    def close_connection(self):
        """Close the database connection."""
        self.cursor.close()
        self.conn.close()
