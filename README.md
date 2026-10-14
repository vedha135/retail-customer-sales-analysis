# Retail Customer & Sales Analysis :

**A Data Analytics Project using Python, SQL, and Power BI**

## 1. Project Overview :

Retail businesses generate large amounts of transactional data every day. Analyzing this data helps businesses understand revenue performance, customer purchasing patterns, product demand, and market performance.

This project focuses on analyzing retail customer and sales data to organize raw transactional information into useful summaries and interactive visualizations.

The project combines Python-based data processing, SQL-based data querying, and Power BI dashboard visualization in a single analytics workflow.

## 2. Project Objectives :

The main objectives of this project are:

- Analyze overall retail sales performance.
- Calculate key performance indicators (KPIs).
- Understand monthly revenue trends.
- Identify top-performing products and customers.
- Compare sales performance across countries.
- Analyze customer segments and repeat-customer activity.
- Present business metrics through a Power BI dashboard.
- Organize the project files for reproducibility and portfolio presentation.

## 3. Tools and Technologies

| Tool | Purpose |
|---|---|
| Python | Data processing and analysis |
| Pandas | Data manipulation and summary generation |
| NumPy | Numerical operations where required |
| Oracle SQL | Querying and analyzing structured data |
| Power BI | Interactive dashboard and visualization |
| CSV | Storing processed datasets and summaries |
| GitHub | Project versioning and portfolio presentation |

## 4. Project Workflow

The project follows this general workflow:

1. **Data preparation:** Work with the retail sales dataset and prepare the data for analysis.
2. **Data processing:** Use Python to process the data and generate analytical summary files.
3. **Sales analysis:** Prepare summaries for KPIs, monthly sales, products, countries, customers, and segments.
4. **SQL analysis:** Write SQL queries to investigate sales performance and answer business questions.
5. **Visualization:** Present sales metrics and trends in Power BI.
6. **Documentation:** Maintain the code, datasets, query files, dashboard screenshot, and project explanation in GitHub.

## 5. Key Business Questions

This project explores questions such as:

- What is the overall revenue generated?
- How many units were sold?
- How many orders and customers are represented in the analysis?
- What is the average order value?
- How does revenue change over time?
- Which countries contribute the most revenue?
- Which products generate the highest revenue?
- Which customers contribute the most revenue?
- How is revenue distributed across customer segments?
- How many repeat customers are identified by the analysis?

## 6. Python Data Analysis

Python is used to process the retail dataset and produce summary files for further analysis.

The repository includes summary datasets covering:

- Key performance indicators
- Monthly sales
- Country-wise sales
- Product sales
- Customer summaries
- Customer segment summaries
- Top customers
- Top products

These outputs can be used for reporting, SQL analysis, and dashboard development.

## 7. Power BI Dashboard

The Power BI dashboard, titled **Retail Customer & Sales Analysis**, combines high-level sales metrics with detailed visualizations.

### Key Performance Indicators

- Total Revenue
- Total Quantity
- Total Orders
- Total Customers
- Average Order Value
- Repeat Customers

### Dashboard Visualizations

- Monthly Revenue Trend
- Top 10 Countries by Revenue
- Revenue by Customer Segment
- Top 10 Products by Revenue
- Top 10 Customers by Revenue
- Revenue by Country Map

### Dashboard Filters

The dashboard includes filters for date, country, stock code, and product description, allowing users to explore different portions of the data.

### Dashboard Preview

![Retail Customer and Sales Analysis Dashboard](power%20bi%20retail%20sales%20screenshot_.png)

## 8. SQL Analysis

SQL is used to formulate business questions and analyze structured sales data.

The repository contains a SQL query script and an expected-output reference document.

The planned SQL analysis covers sales metrics, product performance, customer performance, and sales trends, subject to the queries included in the script.

**Validation status:** The expected-output document is a reference. Actual query results must be verified by executing the queries in Oracle SQL*Plus. Screenshots of verified results will be added after execution.

### SQL Files

- `retail_sales_analysis1` — SQL query script
- `SQL_Queries_and_Expected_Outputs1.pdf` — Expected-output reference

## 9. Repository Structure

```text
retail-customer-sales-analysis/
│
├── README.md
├── analysis.py
│
├── country_sales.csv
├── customer_summary.csv
├── kpi_summary.csv
├── monthly_sales.csv
├── product_sales.csv
├── segment_summary.csv
├── top_customers.csv
├── top_products.csv
│
├── power bi retail sales screenshot_.png
├── retail_sales_analysis1
└── SQL_Queries_and_Expected_Outputs1.pdf
```

## 10. How to Run the Python Analysis

### Prerequisites

- Python installed on your computer
- Required Python packages
- The input dataset expected by the script

### Steps

1. Clone or download this repository.
2. Open the project folder in Visual Studio Code or another Python editor.
3. Install the dependencies required by `analysis.py`.
4. Make sure the input dataset is available at the path expected by the script.
5. Run the Python script.
6. Review the generated CSV summaries.

Example command:

```bash
python analysis.py
```

Install only the dependencies imported by the actual script. The input file path and required packages should be checked before running the code on another computer.

## 11. SQL Execution Plan

The SQL workflow is:

1. Import the existing `cleaned_sales.csv` dataset into Oracle SQL*Plus using an appropriate import method.
2. Confirm the table structure and column names.
3. Execute the SQL queries against the imported table.
4. Compare actual results with the expected-output reference.
5. Capture screenshots of the verified query outputs.
6. Save the final SQL script and add the screenshots to GitHub.

## 12. Key Deliverables

- Python analysis script
- Generated CSV summary files
- Power BI dashboard screenshot
- SQL query script
- Expected-output reference PDF
- Project documentation in README format

## 13. Limitations and Validation

- SQL outputs must be verified in Oracle SQL*Plus before being presented as actual results.
- Results depend on the source dataset, data preparation, and metric definitions.
- Dashboard metrics should be interpreted according to the calculations and filters configured in Power BI.
- Reproducibility depends on having the required source data and Python dependencies.

## 14. Future Improvements

- Complete Oracle SQL*Plus execution and document verified outputs.
- Add screenshots of actual SQL query results.
- Document the data-cleaning rules and KPI formulas.
- Add further business recommendations based on validated findings.
- Include the original Power BI `.pbix` file through a suitable file-hosting method if its size exceeds GitHub's browser upload limit.

## 15. Conclusion

This project demonstrates a retail sales analytics workflow that brings together Python data processing, SQL querying, and Power BI visualization.

By organizing transaction-level data into sales, product, customer, and country summaries, the project provides a foundation for exploring business performance and communicating findings through an analytics portfolio.

## Author

**Vedhasree**

Aspiring Data Analyst | Python | SQL | Power BI

GitHub: [vedha135](https://github.com/vedha135)
