import os
import platform
import csv

def clear_screen():
    """Clear the console based on the operating system."""
    if platform.system() == "Windows":
        os.system('cls')  # Clears the console for Windows
    else:
        os.system('clear')  # Clears the console for Unix/Linux/MacOS

def import_data(db, csv_path, table, columns):
    with open(csv_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            data_tuple = tuple(row[col] if col in row else None for col in columns)
            placeholders = ', '.join(['?'] * len(columns))
            # Use INSERT OR IGNORE to avoid inserting duplicate rows
            sql = f'INSERT OR IGNORE INTO {table} ({", ".join(columns)}) VALUES ({placeholders});'
            db.execute_query(sql, data_tuple)
