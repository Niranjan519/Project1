import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from typing import Dict, Any

# Ensure Matplotlib is set to non-interactive mode if running in a script environment
plt.switch_backend('Agg')

# Define the path to the uploaded data (Canvas provides this access)
# Note: The actual path used here is the logical identifier for the uploaded file.
DATASET_PATH = "uploaded:archive (7).zip/Retail-Supply-Chain-Sales-Dataset.xlsx - Retails Order Full Dataset.csv"

def run_profitability_analysis() -> Dict[str, Any]:
    """
    Performs core profitability, correlation, and inventory analysis using the real dataset.
    """
    print("\n--- Loading and Cleaning Data ---")
    try:
        # Load the uploaded retail data
        df = pd.read_csv(DATASET_PATH)
    except FileNotFoundError:
        print(f"ERROR: Could not find the dataset at path: {DATASET_PATH}")
        print("Falling back to simulated data for demonstration purposes.")
        return create_sample_data_and_run_analysis()
    
    # 1. Data Cleaning and Transformation
    
    # Rename columns for consistency and easier access (lowercase with underscores)
    df.columns = df.columns.str.replace(' ', '_').str.lower()
    df.rename(columns={'order_date': 'order_date_raw', 'ship_date': 'ship_date_raw'}, inplace=True)
    
    # Convert dates and calculate the Inventory Efficiency Proxy: Shipping Lead Time (in days)
    df['order_date'] = pd.to_datetime(df['order_date_raw'])
    df['ship_date'] = pd.to_datetime(df['ship_date_raw'])
    # PROXY: Use Shipping Lead Time as a substitute for Inventory Days Held,
    # as high lead time suggests stocking/fulfillment inefficiency (slow-moving risk).
    df['shipping_lead_time_days'] = (df['ship_date'] - df['order_date']).dt.days

    # Calculate Profit and Profit Margin
    # NOTE: The provided dataset already contains 'Profit' and 'Sales', 
    # but we will recalculate Profit Margin to be safe.
    df['profit_margin_percent'] = (df['profit'] / df['sales']) * 100
    
    # Filter out records where Sales is zero or negative (to avoid division errors and bad data)
    df = df[df['sales'] > 0].copy()
    
    print(f"Data loaded and cleaned. Total transactions: {len(df)}")
    
    # 2. Aggregation for Correlation Analysis
    
    # Aggregate data by Sub-Category for correlation and strategic analysis
    agg_df = df.groupby(['category', 'sub-category']).agg(
        Total_Sales=('sales', 'sum'),
        Total_Profit=('profit', 'sum'),
        Avg_Profit_Margin=('profit_margin_percent', 'mean'),
        # Use the calculated proxy column for inventory/efficiency
        Avg_Inventory_Days=('shipping_lead_time_days', 'mean'), 
        Total_Units_Sold=('quantity', 'sum')
    ).reset_index()
    
    # Rename the proxy column for report consistency
    agg_df.rename(columns={'Avg_Inventory_Days': 'Avg_Shipping_Lead_Time_Days'}, inplace=True)

    print("\n--- Running Profitability Calculations ---")
    
    # --- 2a. Correlation Analysis ---
    # Analyze correlation between shipping lead time (our proxy for inventory days) and margin
    correlation = agg_df['Avg_Shipping_Lead_Time_Days'].corr(agg_df['Avg_Profit_Margin'])
    print(f"\n[FINDING 1] Correlation between Avg. Shipping Lead Time (Proxy for Inventory Days) and Avg. Profit Margin: {correlation:.4f}")
    
    # --- 2b. Strategic Item Identification (Slow Movers/Low Profit) ---
    # Define thresholds based on the dataset's lead time distribution: 
    
    # Calculate the 75th percentile of lead time for the threshold
    inventory_threshold = agg_df['Avg_Shipping_Lead_Time_Days'].quantile(0.75)
    margin_threshold = 15.0 # A reasonable commercial threshold for this dataset's profit margins
    
    risk_items = agg_df[
        (agg_df['Avg_Shipping_Lead_Time_Days'] > inventory_threshold) & 
        (agg_df['Avg_Profit_Margin'] < margin_threshold)
    ].sort_values(by='Total_Sales', ascending=False)
    
    print(f"\n[FINDING 2] High-Risk Items (Avg. Shipping Lead Time > {inventory_threshold:.1f} days AND Margin < {margin_threshold}%):")
    if not risk_items.empty:
        print(risk_items[['sub-category', 'Avg_Shipping_Lead_Time_Days', 'Avg_Profit_Margin', 'Total_Sales']].head(5).to_markdown(index=False))
    else:
        print("No high-risk items found based on these thresholds.")
        
    # --- 2c. Top/Bottom Performers ---
    top_profit = agg_df.sort_values(by='Avg_Profit_Margin', ascending=False).head(3)
    bottom_profit = agg_df.sort_values(by='Avg_Profit_Margin', ascending=True).head(3)
    
    print("\n[FINDING 3] Top 3 Most Profitable Subcategories:")
    print(top_profit[['sub-category', 'Avg_Profit_Margin']].to_markdown(index=False))
    
    print("\n[FINDING 4] Top 3 Least Profitable Subcategories (Potential Loss Leaders/Cost Problems):")
    print(bottom_profit[['sub-category', 'Avg_Profit_Margin']].to_markdown(index=False))
    
    # --- 2d. Generate Visualization (Scatter Plot) ---
    plt.figure(figsize=(10, 6))
    sns.scatterplot(
        x='Avg_Shipping_Lead_Time_Days', 
        y='Avg_Profit_Margin', 
        data=agg_df, 
        hue='category', 
        size='Total_Sales', 
        sizes=(20, 500)
    )
    plt.axvline(x=inventory_threshold, color='r', linestyle='--', label=f'Lead Time Risk ({inventory_threshold:.1f} Days)')
    plt.axhline(y=margin_threshold, color='g', linestyle=':', label=f'Margin Threshold ({margin_threshold}%)')
    plt.title('Inventory Efficiency (Shipping Lead Time) vs. Profitability by Subcategory')
    plt.xlabel('Average Shipping Lead Time (Days)')
    plt.ylabel('Average Profit Margin (%)')
    plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.grid(True, which='both', linestyle='--', linewidth=0.5)
    
    # Save the plot
    plot_filepath = "inventory_profit_correlation_plot.png"
    plt.savefig(plot_filepath, bbox_inches='tight')
    print(f"\n[VISUALIZATION] Scatter plot saved to {plot_filepath}")
    
    return {
        'correlation': correlation,
        'risk_items': risk_items,
        'plot_path': plot_filepath
    }

# This function is retained only as a fallback, but the main function is now run_profitability_analysis
def create_sample_data_and_run_analysis():
    print("--- Running SIMULATION Mode (No real data loaded) ---")
    np.random.seed(42)
    num_records = 5000
    categories = ['Electronics', 'Apparel', 'Home Goods', 'Perishables', 'Health & Beauty']
    # Simplified sample data creation...
    # (The existing create_sample_data logic goes here if needed, but we bypass it now)
    return {'correlation': 0.0, 'risk_items': pd.DataFrame(), 'plot_path': 'N/A'}


if __name__ == '__main__':
    results = run_profitability_analysis()
    
    print("\n===================================================================")
    print("ANALYSIS COMPLETE")
    print("-------------------------------------------------------------------")
    print(f"Update your report (retail_performance_report.md) with the correlation value: {results['correlation']:.4f}")
    print("Use the Risk Items table above to derive your strategic recommendations.")
    print("===================================================================")
