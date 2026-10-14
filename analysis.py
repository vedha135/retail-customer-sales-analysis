from pathlib import Path
import pandas as pd
import numpy as np

# ============================================================
# 1. FIND DATASET
# ============================================================

project_root = Path.cwd()

files = list(project_root.rglob("Online Retail.xlsx"))

if not files:
    print("ERROR: Online Retail.xlsx not found")
    raise SystemExit

file_path = files[0]

print("File found:", file_path)


# ============================================================
# 2. LOAD DATASET
# ============================================================

df = pd.read_excel(file_path)

print("\nDATASET LOADED SUCCESSFULLY")
print("-" * 60)
print("Rows:", df.shape[0])
print("Columns:", df.shape[1])
print("\nColumns:")
print(df.columns.tolist())


# ============================================================
# 3. BASIC DATA PREPARATION
# ============================================================

# Clean column names
df.columns = df.columns.str.strip()

# Convert data types
df["InvoiceDate"] = pd.to_datetime(df["InvoiceDate"], errors="coerce")
df["Quantity"] = pd.to_numeric(df["Quantity"], errors="coerce")
df["UnitPrice"] = pd.to_numeric(df["UnitPrice"], errors="coerce")

# Remove rows without essential transaction information
df = df.dropna(
    subset=["InvoiceNo", "StockCode", "InvoiceDate", "Quantity", "UnitPrice"]
)

# Clean text columns
df["Description"] = df["Description"].astype(str).str.strip()
df["Country"] = df["Country"].astype(str).str.strip()

# Customer ID as string
df["CustomerID"] = df["CustomerID"].astype("string").str.strip()


# ============================================================
# 4. HANDLE CANCELLATIONS
# ============================================================

# In this dataset, invoices beginning with C represent cancellations
df["IsCancellation"] = df["InvoiceNo"].astype(str).str.startswith("C")

print("\nCANCELLATIONS")
print("-" * 60)
print("Cancelled transactions:", df["IsCancellation"].sum())


# ============================================================
# 5. CREATE VALID SALES DATA
# ============================================================

sales = df[
    (df["IsCancellation"] == False)
    & (df["Quantity"] > 0)
    & (df["UnitPrice"] > 0)
].copy()

# Revenue
sales["Revenue"] = sales["Quantity"] * sales["UnitPrice"]

print("\nVALID SALES DATA")
print("-" * 60)
print("Rows after cleaning:", len(sales))
print("Total Revenue:", round(sales["Revenue"].sum(), 2))
print("Total Quantity:", sales["Quantity"].sum())
print("Unique Invoices:", sales["InvoiceNo"].nunique())
print("Unique Customers:", sales["CustomerID"].nunique())


# ============================================================
# 6. MONTHLY SALES ANALYSIS
# ============================================================

sales["YearMonth"] = sales["InvoiceDate"].dt.to_period("M").astype(str)

monthly_sales = (
    sales.groupby("YearMonth")
    .agg(
        Revenue=("Revenue", "sum"),
        Quantity=("Quantity", "sum"),
        Orders=("InvoiceNo", "nunique"),
        Customers=("CustomerID", "nunique")
    )
    .reset_index()
)

monthly_sales["Average_Order_Value"] = (
    monthly_sales["Revenue"] / monthly_sales["Orders"]
).round(2)

monthly_sales["Revenue"] = monthly_sales["Revenue"].round(2)

monthly_sales = monthly_sales.sort_values("YearMonth")


# ============================================================
# 7. COUNTRY PERFORMANCE
# ============================================================

country_sales = (
    sales.groupby("Country")
    .agg(
        Revenue=("Revenue", "sum"),
        Quantity=("Quantity", "sum"),
        Orders=("InvoiceNo", "nunique"),
        Customers=("CustomerID", "nunique")
    )
    .reset_index()
)

country_sales["Average_Order_Value"] = (
    country_sales["Revenue"] / country_sales["Orders"]
).round(2)

country_sales["Revenue"] = country_sales["Revenue"].round(2)

country_sales = country_sales.sort_values(
    "Revenue", ascending=False
)


# ============================================================
# 8. PRODUCT PERFORMANCE
# ============================================================

product_sales = (
    sales.groupby(["StockCode", "Description"])
    .agg(
        Revenue=("Revenue", "sum"),
        Quantity=("Quantity", "sum"),
        Orders=("InvoiceNo", "nunique"),
        Customers=("CustomerID", "nunique")
    )
    .reset_index()
)

product_sales["Average_Order_Value"] = (
    product_sales["Revenue"] / product_sales["Orders"]
).round(2)

product_sales["Revenue"] = product_sales["Revenue"].round(2)

product_sales = product_sales.sort_values(
    "Revenue", ascending=False
)


# ============================================================
# 9. CUSTOMER ANALYSIS
# ============================================================

customer_sales = sales.dropna(subset=["CustomerID"]).copy()

customer_summary = (
    customer_sales.groupby("CustomerID")
    .agg(
        Revenue=("Revenue", "sum"),
        Quantity=("Quantity", "sum"),
        Orders=("InvoiceNo", "nunique"),
        Products=("StockCode", "nunique"),
        Last_Purchase=("InvoiceDate", "max"),
        First_Purchase=("InvoiceDate", "min")
    )
    .reset_index()
)

customer_summary["Average_Order_Value"] = (
    customer_summary["Revenue"] / customer_summary["Orders"]
).round(2)

customer_summary["Customer_Lifetime_Days"] = (
    customer_summary["Last_Purchase"]
    - customer_summary["First_Purchase"]
).dt.days

customer_summary["Repeat_Customer"] = np.where(
    customer_summary["Orders"] > 1,
    "Yes",
    "No"
)

customer_summary["Revenue"] = customer_summary["Revenue"].round(2)


# ============================================================
# 10. RFM CUSTOMER SEGMENTATION
# ============================================================

analysis_date = sales["InvoiceDate"].max() + pd.Timedelta(days=1)

rfm = (
    customer_sales.groupby("CustomerID")
    .agg(
        Recency=("InvoiceDate", lambda x: (analysis_date - x.max()).days),
        Frequency=("InvoiceNo", "nunique"),
        Monetary=("Revenue", "sum")
    )
    .reset_index()
)

rfm["Monetary"] = rfm["Monetary"].round(2)


# RFM scores
rfm["R_Score"] = pd.qcut(
    rfm["Recency"].rank(method="first"),
    5,
    labels=[5, 4, 3, 2, 1]
).astype(int)

rfm["F_Score"] = pd.qcut(
    rfm["Frequency"].rank(method="first"),
    5,
    labels=[1, 2, 3, 4, 5]
).astype(int)

rfm["M_Score"] = pd.qcut(
    rfm["Monetary"].rank(method="first"),
    5,
    labels=[1, 2, 3, 4, 5]
).astype(int)

rfm["RFM_Score"] = (
    rfm["R_Score"].astype(str)
    + rfm["F_Score"].astype(str)
    + rfm["M_Score"].astype(str)
)


# Customer segments
def assign_segment(row):

    if row["R_Score"] >= 4 and row["F_Score"] >= 4 and row["M_Score"] >= 4:
        return "Champions"

    elif row["R_Score"] >= 4 and row["F_Score"] >= 3:
        return "Loyal Customers"

    elif row["R_Score"] >= 4 and row["M_Score"] >= 4:
        return "Potential Loyalists"

    elif row["R_Score"] <= 2 and row["F_Score"] >= 4:
        return "At Risk"

    elif row["R_Score"] <= 2 and row["M_Score"] >= 4:
        return "High Value At Risk"

    elif row["R_Score"] <= 2:
        return "Lost Customers"

    else:
        return "Regular Customers"


rfm["Segment"] = rfm.apply(assign_segment, axis=1)


# ============================================================
# 11. RFM SEGMENT SUMMARY
# ============================================================

segment_summary = (
    rfm.groupby("Segment")
    .agg(
        Customers=("CustomerID", "count"),
        Revenue=("Monetary", "sum"),
        Average_Recency=("Recency", "mean"),
        Average_Frequency=("Frequency", "mean")
    )
    .reset_index()
)

segment_summary["Revenue"] = segment_summary["Revenue"].round(2)
segment_summary["Average_Recency"] = segment_summary["Average_Recency"].round(2)
segment_summary["Average_Frequency"] = segment_summary["Average_Frequency"].round(2)

segment_summary = segment_summary.sort_values(
    "Revenue",
    ascending=False
)


# ============================================================
# 12. KPI SUMMARY
# ============================================================

kpi_summary = pd.DataFrame({
    "Metric": [
        "Total Revenue",
        "Total Quantity",
        "Total Orders",
        "Total Customers",
        "Average Order Value",
        "Repeat Customers",
        "Repeat Customer Rate"
    ],
    "Value": [
        round(sales["Revenue"].sum(), 2),
        int(sales["Quantity"].sum()),
        int(sales["InvoiceNo"].nunique()),
        int(customer_sales["CustomerID"].nunique()),
        round(
            sales["Revenue"].sum() /
            sales["InvoiceNo"].nunique(),
            2
        ),
        int(
            (customer_summary["Orders"] > 1).sum()
        ),
        round(
            (customer_summary["Orders"] > 1).mean() * 100,
            2
        )
    ]
})


# ============================================================
# 13. TOP CUSTOMERS
# ============================================================

top_customers = (
    customer_summary
    .sort_values("Revenue", ascending=False)
    .head(20)
)


# ============================================================
# 14. TOP PRODUCTS
# ============================================================

top_products = (
    product_sales
    .head(20)
)


# ============================================================
# 15. SAVE OUTPUT FILES
# ============================================================

output_dir = project_root / "Data" / "Notebooks" / "Outputs"
output_dir.mkdir(parents=True, exist_ok=True)

sales.to_csv(
    output_dir / "cleaned_sales.csv",
    index=False
)

monthly_sales.to_csv(
    output_dir / "monthly_sales.csv",
    index=False
)

country_sales.to_csv(
    output_dir / "country_sales.csv",
    index=False
)

product_sales.to_csv(
    output_dir / "product_sales.csv",
    index=False
)

customer_summary.to_csv(
    output_dir / "customer_summary.csv",
    index=False
)

rfm.to_csv(
    output_dir / "rfm_customer_segments.csv",
    index=False
)

segment_summary.to_csv(
    output_dir / "segment_summary.csv",
    index=False
)

kpi_summary.to_csv(
    output_dir / "kpi_summary.csv",
    index=False
)

top_customers.to_csv(
    output_dir / "top_customers.csv",
    index=False
)

top_products.to_csv(
    output_dir / "top_products.csv",
    index=False
)


# ============================================================
# 16. DISPLAY KEY RESULTS
# ============================================================

print("\n" + "=" * 60)
print("RETAIL CUSTOMER & SALES ANALYSIS COMPLETED")
print("=" * 60)

print("\nKEY KPIs")
print("-" * 60)
print(kpi_summary)

print("\nTOP 10 COUNTRIES")
print("-" * 60)
print(country_sales.head(10))

print("\nTOP 10 PRODUCTS")
print("-" * 60)
print(product_sales.head(10))

print("\nCUSTOMER SEGMENTS")
print("-" * 60)
print(segment_summary)

print("\nOUTPUT FILES SAVED TO:")
print(output_dir)

print("\nANALYSIS COMPLETED SUCCESSFULLY!")