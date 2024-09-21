import csv

class CSVWriter:
    def __init__(self, filename):
        self.filename = filename
        
        
    def read_existing_data(self):
        """
        Reads the existing data from the CSV file and returns it as a dictionary.
        The key is the unique address and the value is a set of fetched addresses.
        """
        existing_data = {}
        try:
            with open(self.filename, mode='r', encoding='utf-8', newline='') as file:
                reader = csv.reader(file)
                for row in reader:
                    if row:  # Ensure the row is not empty
                        key = row[0]
                        values = set(row[1:])  # Use a set for easy comparison
                        existing_data[key] = values
        except FileNotFoundError:
            print("CSV file not found. Starting with an empty dataset.")
        return existing_data


    def write_data(self, data):
        """
        Writes the entire dataset to the CSV file.
        Each entry in data should be a list where the first element is the key (address)
        and the rest are the values (fetched addresses).
        """
        try:
            with open(self.filename, mode='w', encoding='utf-8', newline='') as file:  # 'w' mode for writing
                writer = csv.writer(file)
                writer.writerows(data)  # Write all rows at once
            print(f"Data written to {self.filename} successfully.")
        except Exception as e:
            print(f"An error occurred while writing to {self.filename}: {e}")