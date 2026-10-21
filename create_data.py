import csv
import os

data_folder = "data"
os.makedirs(data_folder, exist_ok=True)

file_path = os.path.join(data_folder, "sales.csv")

sales_data = [
    ["order_id", "product", "category", "quantity", "price"],
    [101, "Laptop", "Electronics", 2, 50000],
    [102, "Mouse", "Accessories", 3, 500],
    [103, "Keyboard", "Accessories", 1, 1500],
    [104, "Monitor", "Electronics", 2, 10000],
    [105, "Mouse", "Accessories", 1, 500],
    [106, "Headphones", "Accessories", 2, 2000],
    [107, "Laptop", "Electronics", 1, 50000],
    [108, "Monitor", "Electronics", 1, 10000],
]

with open(file_path, "w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)
    writer.writerows(sales_data)

print("Sales data created successfully!")
print("File location:", os.path.abspath(file_path))
