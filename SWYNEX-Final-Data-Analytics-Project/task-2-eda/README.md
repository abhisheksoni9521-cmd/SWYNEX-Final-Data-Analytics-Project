# SWYNEX Exploratory Data Analysis

A beginner-friendly Python project for exploring the cleaned Sample Superstore dataset. It creates summary tables, charts, a plain-language insight report, and a review file for unusual rows.

## Project files

- `data/superstore_cleaned.csv` — cleaned input dataset
- `analyze.py` — analysis script
- `charts/` — six charts included with this project; running the script also saves fresh PNG charts
- `reports/insights.txt` — data-backed findings
- `reports/` — descriptive statistics, category/region/product/customer summaries, and rows for review

## CMD mein run karne ke steps (Hinglish)

1. Windows Start menu se **Command Prompt (CMD)** kholiye.
2. Project folder mein jaane ke liye `cd /d "PROJECT_FOLDER_PATH"` likhiye. `PROJECT_FOLDER_PATH` ko apne folder ke actual address se replace karein.
3. Zaroori Python libraries install karne ke liye chalaiye:

   ```bat
   py -m pip install -r requirements.txt
   ```

4. Analysis chalane ke liye likhiye:

   ```bat
   py analyze.py
   ```

Agar `py` command nahi chale, Python 3 install karke installation ke waqt **Add Python to PATH** select karein. Uske baad `py` ki jagah `python` command use kar sakte hain.

Script `data\superstore_cleaned.csv` file padhegi aur naye charts `charts\` mein aur report/summaries `reports\` mein save karegi. Har run par results refresh ho jaate hain.

## Main questions explored

- How do monthly sales move over time?
- Which categories, sub-categories, regions, customers, and products contribute the most sales or profit?
- How do discounts relate to profit?
- Which rows deserve a closer look because of losses, very high discounts, unusual sales values, or ship dates before order dates?

An anomaly flag is a prompt for investigation, not proof that a record is wrong.
