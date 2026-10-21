import pandas as pd
from pathlib import Path

# Find the project folder
PROJECT_FOLDER = Path(__file__).resolve().parent
DATA_FOLDER = PROJECT_FOLDER / "data"

# EXTRACT: Read the original sales data
input_file = DATA_FOLDER / "sales.csv"

df = pd.read_csv(input_file)

print("Original Sales Data:")
print(df)

# TRANSFORM: Remove exact duplicate rows
df = df.drop_duplicates()

# Remove rows containing missing values
df = df.dropna()

# Calculate revenue for each product sale
df["revenue"] = df["quantity"] * df["price"]

# LOAD: Save the processed data
output_file = DATA_FOLDER / "cleaned_sales.csv"

df.to_csv(output_file, index=False)

print("\nETL Pipeline Completed Successfully!")
print("Processed rows:", len(df))
print("Output file:", output_file)

print("\nCleaned Sales Data:")
print(df)
