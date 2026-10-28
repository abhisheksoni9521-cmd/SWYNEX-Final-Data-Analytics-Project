
from pathlib import Path
import pandas as pd

BASE_DIR = Path(__file__).resolve().parent
RAW_FILE = BASE_DIR / "data" / "raw" / "Sample - Superstore.csv.csv"

PROCESSED_DIR = BASE_DIR / "data" / "processed"
REPORT_DIR = BASE_DIR / "reports"

PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
REPORT_DIR.mkdir(parents=True, exist_ok=True)

# Load original data
df = pd.read_csv(RAW_FILE, encoding="latin1")

original_rows = len(df)
original_columns = len(df.columns)
missing_before = int(df.isna().sum().sum())
duplicates_before = int(df.duplicated().sum())

# 1. Remove exact duplicate rows, if any
df = df.drop_duplicates().copy()

# 2. Clean extra spaces in text columns
text_columns = df.select_dtypes(include=["object", "str"]).columns

for col in text_columns:
    df[col] = df[col].str.strip()

# 3. Convert date columns to proper datetime format
for col in ["Order Date", "Ship Date"]:
    df[col] = pd.to_datetime(
        df[col],
        format="mixed",
        errors="coerce"
    )

# 4. Convert Postal Code to text
# It is an identifier, not a quantity
df["Postal Code"] = df["Postal Code"].astype("string")

# 5. Validate important numeric columns
for col in ["Sales", "Quantity", "Discount", "Profit"]:
    df[col] = pd.to_numeric(df[col], errors="coerce")

# 6. Check invalid dates and numeric values
invalid_order_dates = int(df["Order Date"].isna().sum())
invalid_ship_dates = int(df["Ship Date"].isna().sum())
invalid_sales = int((df["Sales"] < 0).sum())
invalid_quantity = int((df["Quantity"] <= 0).sum())
invalid_discount = int(
    ((df["Discount"] < 0) | (df["Discount"] > 1)).sum()
)

# Check shipping date before order date
invalid_date_order = int(
    (df["Ship Date"] < df["Order Date"]).sum()
)

# 7. Save cleaned dataset
output_file = PROCESSED_DIR / "superstore_cleaned.csv"
df.to_csv(output_file, index=False, date_format="%Y-%m-%d")

# 8. Create cleaning report
report_file = REPORT_DIR / "cleaning_summary.txt"

with open(report_file, "w", encoding="utf-8") as f:
    f.write("SWYNEX TASK 1 - DATA CLEANING SUMMARY\n")
    f.write("=" * 42 + "\n\n")
    f.write(f"Original rows: {original_rows}\n")
    f.write(f"Original columns: {original_columns}\n")
    f.write(f"Missing values before cleaning: {missing_before}\n")
    f.write(f"Exact duplicate rows found: {duplicates_before}\n")
    f.write(f"Rows after duplicate removal: {len(df)}\n\n")
    f.write("VALIDATION RESULTS\n")
    f.write("-" * 25 + "\n")
    f.write(f"Invalid order dates: {invalid_order_dates}\n")
    f.write(f"Invalid ship dates: {invalid_ship_dates}\n")
    f.write(f"Negative sales values: {invalid_sales}\n")
    f.write(f"Non-positive quantities: {invalid_quantity}\n")
    f.write(f"Discounts outside 0-1: {invalid_discount}\n")
    f.write(f"Ship date before order date: {invalid_date_order}\n\n")
    f.write(f"Missing values after cleaning: {int(df.isna().sum().sum())}\n")
    f.write(f"Final rows: {len(df)}\n")
    f.write(f"Final columns: {len(df.columns)}\n")

print("DATA CLEANING COMPLETED")
print("-" * 40)
print(f"Original shape: ({original_rows}, {original_columns})")
print(f"Final shape: {df.shape}")
print(f"Missing values before: {missing_before}")
print(f"Duplicate rows found: {duplicates_before}")
print(f"Missing values after: {int(df.isna().sum().sum())}")
print(f"Invalid order dates: {invalid_order_dates}")
print(f"Invalid ship dates: {invalid_ship_dates}")
print(f"Invalid sales values: {invalid_sales}")
print(f"Invalid quantities: {invalid_quantity}")
print(f"Invalid discounts: {invalid_discount}")
print(f"Ship date before order date: {invalid_date_order}")
print(f"\nCleaned CSV saved to: {output_file}")
print(f"Cleaning report saved to: {report_file}")
