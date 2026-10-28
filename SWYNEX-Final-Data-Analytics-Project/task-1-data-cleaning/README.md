
# SWYNEX Task 1: Data Cleaning & Preparation

## Project Overview
This project focuses on inspecting, cleaning, and validating a
Sample Superstore sales dataset using Python and Pandas.

## Tools Used
- Python
- Pandas
- CSV
- Git and GitHub

## Dataset Details
- Original records: 9,994
- Columns: 21
- Dataset type: Sales and order transactions

## Data Cleaning Steps
1. Inspected dataset dimensions and column names.
2. Checked missing values and exact duplicate rows.
3. Removed extra spaces from text columns.
4. Converted Order Date and Ship Date into datetime format.
5. Converted Postal Code into a text identifier.
6. Validated numeric fields including Sales, Quantity,
   Discount, and Profit.
7. Checked date consistency between order and ship dates.
8. Exported the cleaned dataset to CSV.
9. Generated an initial inspection report and a cleaning summary.

## Results
- Final records: 9,994
- Final columns: 21
- Missing values after cleaning: 0
- Exact duplicate rows initially found: 0
- Invalid order dates: 0
- Invalid ship dates: 0
- Discounts outside the 0–1 range: 0
- Ship dates before order dates: 0

## Project Structure
```text
SWYNEX-Data-Cleaning-Preparation/
├── data/
│   ├── raw/
│   └── processed/
│       └── superstore_cleaned.csv
├── reports/
│   ├── initial_inspection.txt
│   └── cleaning_summary.txt
├── data_cleaning.py
└── README.md
```

## How to Run
Install the required library:

```bash
python -m pip install pandas
```

Run the script from the project root:

```bash
python data_cleaning.py
```

## Conclusion
The dataset was inspected and validated using Python and Pandas.
The cleaned dataset and reports were saved for further analysis.

Note: The dataset is used for educational purposes.
