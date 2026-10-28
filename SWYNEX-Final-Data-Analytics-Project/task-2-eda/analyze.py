"""Beginner-friendly exploratory data analysis for the Sample Superstore dataset."""
from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parent
DATA_FILE = ROOT / "data" / "superstore_cleaned.csv"
CHARTS = ROOT / "charts"
REPORTS = ROOT / "reports"
REQUIRED = ["Order Date", "Ship Date", "Customer Name", "Region", "Category",
            "Sub-Category", "Product Name", "Sales", "Quantity", "Discount", "Profit"]


def money(value):
    return f"${value:,.2f}"


def main():
    CHARTS.mkdir(exist_ok=True)
    REPORTS.mkdir(exist_ok=True)
    df = pd.read_csv(DATA_FILE)
    missing = [col for col in REQUIRED if col not in df.columns]
    if missing:
        raise ValueError(f"Required columns are missing: {missing}")

    df["Order Date"] = pd.to_datetime(df["Order Date"], errors="coerce")
    df["Ship Date"] = pd.to_datetime(df["Ship Date"], errors="coerce")
    for col in ["Sales", "Profit", "Quantity", "Discount"]:
        df[col] = pd.to_numeric(df[col], errors="coerce")
    invalid_dates = int(df[["Order Date", "Ship Date"]].isna().any(axis=1).sum())
    numeric_missing = int(df[["Sales", "Profit", "Quantity", "Discount"]].isna().any(axis=1).sum())
    clean = df.dropna(subset=["Order Date", "Ship Date", "Sales", "Profit", "Quantity", "Discount"]).copy()
    clean["Month"] = clean["Order Date"].dt.to_period("M").dt.to_timestamp()

    # Compact summary tables are useful for checking and reusing the results.
    clean[["Sales", "Profit", "Quantity", "Discount"]].describe().T.to_csv(REPORTS / "descriptive_statistics.csv")
    monthly = clean.groupby("Month", as_index=False).agg(Sales=("Sales", "sum"), Profit=("Profit", "sum"))
    monthly.to_csv(REPORTS / "monthly_sales_profit.csv", index=False)
    category = clean.groupby("Category", as_index=False).agg(Sales=("Sales", "sum"), Profit=("Profit", "sum"), Rows=("Sales", "size"))
    category.to_csv(REPORTS / "category_summary.csv", index=False)
    subcategory = clean.groupby("Sub-Category", as_index=False).agg(Sales=("Sales", "sum"), Profit=("Profit", "sum"), Rows=("Sales", "size"))
    subcategory.sort_values("Profit").to_csv(REPORTS / "subcategory_summary.csv", index=False)
    region = clean.groupby("Region", as_index=False).agg(Sales=("Sales", "sum"), Profit=("Profit", "sum"), Rows=("Sales", "size"))
    region.to_csv(REPORTS / "region_summary.csv", index=False)
    customers = clean.groupby("Customer Name", as_index=False).agg(Sales=("Sales", "sum"), Profit=("Profit", "sum"), Orders=("Order ID", "nunique"))
    customers.nlargest(10, "Sales").to_csv(REPORTS / "top_customers.csv", index=False)
    products = clean.groupby("Product Name", as_index=False).agg(Sales=("Sales", "sum"), Profit=("Profit", "sum"), Units=("Quantity", "sum"))
    products.nlargest(10, "Sales").to_csv(REPORTS / "top_products.csv", index=False)
    discount = clean.groupby("Discount", as_index=False).agg(Sales=("Sales", "sum"), Profit=("Profit", "sum"), Rows=("Sales", "size"))
    discount.to_csv(REPORTS / "discount_summary.csv", index=False)

    # Charts
    plt.style.use("seaborn-v0_8-whitegrid")
    fig, ax = plt.subplots(figsize=(11, 5))
    ax.plot(monthly["Month"], monthly["Sales"], marker="o", linewidth=1.8, color="#2563eb")
    ax.set(title="Monthly Sales Trend", xlabel="Order month", ylabel="Sales ($)")
    fig.tight_layout(); fig.savefig(CHARTS / "monthly_sales_trend.png", dpi=160); plt.close(fig)

    fig, ax = plt.subplots(figsize=(8, 5))
    cats = category.sort_values("Sales")
    ax.barh(cats["Category"], cats["Sales"], color="#0f766e", label="Sales")
    ax.set(title="Sales by Category", xlabel="Sales ($)")
    fig.tight_layout(); fig.savefig(CHARTS / "sales_by_category.png", dpi=160); plt.close(fig)

    fig, ax = plt.subplots(figsize=(8, 5))
    regs = region.sort_values("Profit")
    ax.barh(regs["Region"], regs["Profit"], color="#7c3aed")
    ax.set(title="Profit by Region", xlabel="Profit ($)")
    fig.tight_layout(); fig.savefig(CHARTS / "profit_by_region.png", dpi=160); plt.close(fig)

    fig, ax = plt.subplots(figsize=(9, 7))
    subs = subcategory.sort_values("Profit")
    ax.barh(subs["Sub-Category"], subs["Profit"], color=["#dc2626" if x < 0 else "#16a34a" for x in subs["Profit"]])
    ax.axvline(0, color="black", linewidth=.8)
    ax.set(title="Profit by Sub-Category", xlabel="Profit ($)")
    fig.tight_layout(); fig.savefig(CHARTS / "profit_by_subcategory.png", dpi=160); plt.close(fig)

    fig, ax = plt.subplots(figsize=(8, 5))
    ax.scatter(clean["Discount"], clean["Profit"], alpha=.3, s=18, color="#ea580c")
    ax.axhline(0, color="black", linewidth=.8)
    ax.set(title="Discount and Profit per Order Line", xlabel="Discount rate", ylabel="Profit ($)")
    fig.tight_layout(); fig.savefig(CHARTS / "discount_vs_profit.png", dpi=160); plt.close(fig)

    fig, ax = plt.subplots(figsize=(8, 5))
    prod = products.nlargest(10, "Sales").sort_values("Sales")
    ax.barh(prod["Product Name"], prod["Sales"], color="#0891b2")
    ax.set(title="10 Products with Highest Sales", xlabel="Sales ($)")
    fig.tight_layout(); fig.savefig(CHARTS / "top_products_sales.png", dpi=160); plt.close(fig)

    # Flag rows for review; these are investigation cues, not proof of data errors.
    q1, q3 = clean["Sales"].quantile([.25, .75]); iqr = q3 - q1
    sales_outlier = (clean["Sales"] < q1 - 1.5 * iqr) | (clean["Sales"] > q3 + 1.5 * iqr)
    late_ship = clean["Ship Date"] < clean["Order Date"]
    anomaly = clean.loc[(clean["Profit"] < 0) | (clean["Discount"] >= .5) | sales_outlier | late_ship].copy()
    anomaly.to_csv(REPORTS / "rows_for_review.csv", index=False)

    total_sales, total_profit = clean["Sales"].sum(), clean["Profit"].sum()
    loss_count = int((clean["Profit"] < 0).sum())
    cat_sales = category.loc[category["Sales"].idxmax()]
    cat_profit = category.loc[category["Profit"].idxmax()]
    best_region = region.loc[region["Profit"].idxmax()]
    worst_region = region.loc[region["Profit"].idxmin()]
    worst_sub = subcategory.loc[subcategory["Profit"].idxmin()]
    best_sub = subcategory.loc[subcategory["Profit"].idxmax()]
    high_discount = clean.loc[clean["Discount"] >= .5]
    high_disc_profit = high_discount["Profit"].sum()
    year = clean.groupby(clean["Order Date"].dt.year)["Sales"].sum()
    year_growth = (year.iloc[-1] / year.iloc[-2] - 1) * 100 if len(year) > 1 else float("nan")
    top_customer = customers.nlargest(1, "Sales").iloc[0]
    insights = [
        f"1. Dataset scope: {len(clean):,} usable order lines from {clean['Order Date'].min():%Y-%m-%d} to {clean['Order Date'].max():%Y-%m-%d}. Total sales are {money(total_sales)} and total profit is {money(total_profit)}.",
        f"2. {cat_sales['Category']} has the highest category sales ({money(cat_sales['Sales'])}); {cat_profit['Category']} also has the highest category profit ({money(cat_profit['Profit'])}).",
        f"3. {best_region['Region']} is the most profitable region ({money(best_region['Profit'])}); {worst_region['Region']} is the least profitable ({money(worst_region['Profit'])}).",
        f"4. {worst_sub['Sub-Category']} has the largest sub-category loss ({money(worst_sub['Profit'])}), while {best_sub['Sub-Category']} has the highest profit ({money(best_sub['Profit'])}).",
        f"5. {loss_count:,} order lines ({loss_count / len(clean):.1%}) have negative profit. Review the rows in reports/rows_for_review.csv to see which product, discount, and region combinations are involved.",
        f"6. Order lines discounted by 50% or more total {len(high_discount):,}; together they have {money(high_disc_profit)} profit. Check reports/discount_summary.csv and charts/discount_vs_profit.png for the pattern.",
        f"7. Sales in {int(year.index[-1])} were {year_growth:.1f}% higher than in {int(year.index[-2])}; see the monthly chart for seasonality and month-to-month variation.",
        f"8. {top_customer['Customer Name']} is the top customer by sales ({money(top_customer['Sales'])}); top-customer results are in reports/top_customers.csv.",
        f"Data checks: {invalid_dates} rows had invalid/missing dates; {numeric_missing} rows had missing/non-numeric measures; {int(late_ship.sum())} rows have Ship Date before Order Date. High-value sales flags use the 1.5×IQR rule and should be reviewed, not automatically treated as errors."
    ]
    (REPORTS / "insights.txt").write_text("EXPLORATORY DATA ANALYSIS — SAMPLE SUPERSTORE\n\n" + "\n\n".join(insights) + "\n", encoding="utf-8")
    print(f"Done: analyzed {len(clean):,} rows; charts and reports saved in {ROOT}.")

if __name__ == "__main__":
    main()
