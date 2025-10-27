# Project1
Analysis Project
Retail Business Performance & Profitability Analysis

🎯 Project Overview

This project provides a comprehensive, data-driven analysis of retail operations with the primary goal of improving profitability and inventory efficiency. By analyzing historical sales, profit, and fulfillment metrics, we identified high-risk product categories that are consuming resources (via long lead times) while delivering low profit margins.

The key output is a strategic framework and BI dashboard design focused on monitoring the trade-off between inventory speed and financial return.

🔑 Key Problem Solved

Traditional reporting often focuses on top-line sales, masking underlying operational inefficiencies. This analysis directly addresses the issue of profit erosion caused by:

Poor Fulfillment: Excessively long Shipping Lead Times (used as a proxy for slow inventory movement/high carrying costs).

Unprofitable Products: Sub-categories that generate sales but contribute minimal or negative profit margins.

By combining these two dimensions, the project pinpoints the specific areas requiring immediate inventory rationalization and supply chain optimization.

🛠️ Tools and Technologies

Tool

Purpose

Key Functionality

SQL (T-SQL/PostgreSQL Syntax)

Data Cleansing & Aggregation

Calculated core metrics (profit_margin_percent, avg_shipping_lead_time_days) aggregated by category and region.

Python (Pandas)

Statistical Analysis & Modeling

Calculated the correlation between lead time and margin, and applied a risk model to identify the Danger Quadrant of products.

Tableau / Power BI

Visualization & Reporting

Designed an interactive dashboard centered on the Scatter Plot visualization for real-time risk assessment.

Markdown

Documentation

Used to generate this report and the formal project report.

🚀 Analysis Methodology

The project followed a four-phase methodology:

1. Data Preparation (SQL)

Loaded raw transactional data, including Order Date, Ship Date, Sales, and Profit.

Cleaned and standardized financial data, removing records that could skew profitability metrics (e.g., records with zero sales or missing dates).

2. Metric Creation (SQL)

Two critical metrics were calculated and aggregated:

Profit Margin %: SUM(Profit) / SUM(Sales) * 100

Avg. Shipping Lead Time (Days): AVG(Ship Date - Order Date)

3. Risk Identification (Python)

Correlation: Verified a negative correlation between lead time and profit margin, confirming the hypothesis that slower fulfillment correlates with lower returns.

Thresholds: Established dynamic risk thresholds:

High Lead Time: Above the 75th percentile for all sub-categories.

Low Margin: Below a 15.0% profitability benchmark.

Danger Quadrant: Sub-categories satisfying both High Lead Time and Low Margin criteria were flagged for managerial action.

4. Dashboard Implementation (BI Mockup)

Created a visual layout focused on the Scatter Plot (Lead Time vs. Margin) to make risk immediately apparent.

Included supporting visualizations like Profit Margin % by Top Sub-Category (Bar Chart) and High-Risk Detail Tables.

📝 Strategic Insights Delivered

The analysis provides actionable insights categorized by risk profile:

Risk Quadrant

Characteristics

Recommended Action

High Risk (Danger Quadrant)

High Lead Time, Low Margin

Rationalization & Clearance. Immediately reduce stock and review whether the product line should be continued.

Fulfillment Focus

High Lead Time, High Margin

Logistics Optimization. The product is profitable, but the process is inefficient. Focus resources on reducing lead time (e.g., better forecasting, faster shipping).

Pricing Focus

Low Lead Time, Low Margin

Pricing Review. The product moves quickly but doesn't contribute enough profit. Test small price increases or bundle with high-margin items.

🔗 Repository Structure

Retail-Performance-Report.md: The formal two-page technical report.

tableau_dashboard_mockup.html: The visual representation of the key BI deliverable.

README.md: This summary document.

data/: Contains the source CSV files used for analysis.

⏭️ Next Steps

The next stage of the project involves deploying the live tableau dashboard to production and integrating it with daily data feeds to enable continuous performance monitoring by category managers.
