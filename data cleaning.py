import pandas as pd

# Load the dataset
file_path =  "Nassau Candy Distributor (1).csv"  # change to your file name if needed
df = pd.read_csv(file_path)

# Display basic info
print("Initial Data Info:")
print(df.info())
print(df.head())


# 🔹 1. Validate cost and sales values
# Remove negative or unrealistic values
df = df[df['Cost'] >= 0]
df = df[df['Sales'] > 0]

# 🔹 2. Remove zero-sales or invalid profit records
# If Profit column exists
if 'Profit' in df.columns:
    df = df[df['Profit'].notnull()]
    df = df[df['Profit'] != 0]

# 🔹 3. Handle missing unit values
# Fill missing 'Units' with median (better than mean for business data)
if 'Units' in df.columns:
    df['Units'] = df['Units'].fillna(df['Units'].median())

# Alternatively, you can drop missing rows:
# df = df.dropna(subset=['Units'])

# 🔹 4. Standardize product and division labels
if 'Product' in df.columns:
    df['Product'] = df['Product'].str.strip().str.lower().str.title()

if 'Division' in df.columns:
    df['Division'] = df['Division'].str.strip().str.lower().str.title()

# 🔹 Remove duplicate rows
df = df.drop_duplicates()

# 🔹 Optional: Reset index after cleaning
df = df.reset_index(drop=True)

# Final cleaned data info
print("\nCleaned Data Info:")
print(df.info())
print(df.head())

# Save cleaned data
df.to_csv("1.A.cleaned_data.csv", index=False)

print("\nData cleaning completed and saved as 'cleaned_data.csv'")

# 🔹 5. Profitability Metrics Calculation

required_cols = ['Sales', 'Cost', 'Units']
for col in required_cols:
    if col not in df.columns:
        print(f" Column '{col}' not found. Please check your dataset.")
        exit()

# 🔸 Profit per Unit
df['Profit_per_Unit'] = (df['Sales'] - df['Cost']) / df['Units']

# 🔸 Gross Margin (%)
df['Gross_Margin_%'] = ((df['Sales'] - df['Cost']) / df['Sales']) * 100

# 🔸 Total Profit Contribution
df['Total_Profit'] = (df['Sales'] - df['Cost'])
if 'Product' in df.columns:
    product_summary = df.groupby('Product').agg({
        'Sales': 'sum',
        'Cost': 'sum',
        'Units': 'sum',
        'Total_Profit': 'sum'
    }).reset_index()
    product_summary['Profit_per_Unit'] = product_summary['Total_Profit'] / product_summary['Units']
    product_summary['Gross_Margin_%'] = (product_summary['Total_Profit'] / product_summary['Sales']) * 100
    print("\n📊 Product-wise Profitability Summary:")
    print(product_summary.head())
    product_summary.to_csv("product_profit_summary.csv", index=False)
df.to_csv("2.A.final_profit_data.csv", index=False)
print("\n Profitability metrics calculated and saved!")

# 4. PRODUCT LEVEL PROFITABILITY ANALYSIS
product_analysis = df.groupby('Product Name').agg({
    'Sales': 'sum',
    'Cost': 'sum',
    'Units': 'sum',
    'Total_Profit': 'sum'
}).reset_index()

# Gross Margin %
product_analysis['Gross_Margin_%'] = (product_analysis['Total_Profit'] /product_analysis['Sales']) * 100

# Profit Per Unit
product_analysis['Profit_per_Unit'] = (product_analysis['Total_Profit'] /product_analysis['Units'])

# Save master product analysis
product_analysis.to_csv("3.A.product_level_profitability_analysis.csv",index=False)


#  RANK PRODUCTS BY GROSS PROFIT
rank_gross_profit = product_analysis.sort_values(by='Total_Profit', ascending=False)
print("\n🏆 Top Products By Gross Profit")
print(rank_gross_profit[['Product Name', 'Total_Profit']].head(10))
rank_gross_profit.to_csv("3.B.rank_products_by_gross_profit.csv",index=False)

#  RANK PRODUCTS BY GROSS MARGIN
rank_gross_margin = product_analysis.sort_values(by='Gross_Margin_%',ascending=False)
print("\n🏆 Top Products By Gross Margin")
print(rank_gross_margin[['Product Name', 'Gross_Margin_%']].head(10))
rank_gross_margin.to_csv("3.C.rank_products_by_gross_margin.csv",index=False)

#  THRESHOLDS
profit_threshold = product_analysis['Total_Profit'].median()
margin_threshold = product_analysis['Gross_Margin_%'].median()
sales_threshold = product_analysis['Sales'].median()

# HIGH-PROFIT / HIGH-MARGIN PRODUCTS
high_profit_high_margin = product_analysis[(product_analysis['Total_Profit'] >= profit_threshold) &
    (product_analysis['Gross_Margin_%'] >= margin_threshold)]

print("\n✅ High-Profit / High-Margin Products")
print(high_profit_high_margin[
        ['Product Name',
         'Total_Profit',
         'Gross_Margin_%']])
high_profit_high_margin.to_csv("3.D.high_profit_high_margin_products.csv",index=False)

# HIGH-SALES / LOW-MARGIN PRODUCTS
high_sales_low_margin = product_analysis[(product_analysis['Sales'] >= sales_threshold) &
    (product_analysis['Gross_Margin_%'] < margin_threshold)]
print("\n High-Sales / Low-Margin Products")
print(high_sales_low_margin[
        ['Product Name',
         'Sales',
         'Gross_Margin_%']])
high_sales_low_margin.to_csv("3.E.high_sales_low_margin_products.csv",index=False)

# LOW-SALES / LOW-PROFIT PRODUCTS
low_sales_low_profit = product_analysis[(product_analysis['Sales'] < sales_threshold) &
    (product_analysis['Total_Profit'] < profit_threshold)]
print("\n Low-Sales / Low-Profit Products")
print(low_sales_low_profit[
        ['Product Name',
         'Sales',
         'Total_Profit']])
low_sales_low_profit.to_csv("3.F.low_sales_low_profit_products.csv",index=False)
print("\nFiles Generated:")
print("1. cleaned_data.csv")
print("2. final_profit_data.csv")
print("3. product_level_profitability_analysis.csv")
print("4. rank_products_by_gross_profit.csv")
print("5. rank_products_by_gross_margin.csv")
print("6. high_profit_high_margin_products.csv")
print("7. high_sales_low_margin_products.csv")
print("8. low_sales_low_profit_products.csv")

# 4. DIVISION-LEVEL PERFORMANCE ANALYSIS
division_analysis = df.groupby('Division').agg({
    'Sales': 'sum',
    'Cost': 'sum',
    'Total_Profit': 'sum',
    'Units': 'sum'}).reset_index()
# Average Margin by Division
division_analysis['Average_Margin_%'] = (
    division_analysis['Total_Profit'] /
    division_analysis['Sales']) * 100
# Profit per Unit
division_analysis['Profit_per_Unit'] = (
    division_analysis['Total_Profit'] /
    division_analysis['Units'])
print("\nDivision Summary")
print(division_analysis)
division_analysis.to_csv("4.A.division_performance_analysis.csv",index=False)

# AVERAGE MARGIN BY DIVISION
avg_margin_division = division_analysis[['Division', 'Average_Margin_%']].sort_values(by='Average_Margin_%',ascending=False)
print("\nAverage Margin By Division")
print(avg_margin_division)
avg_margin_division.to_csv("4.B.average_margin_by_division.csv",index=False)

# REVENUE VS PROFIT IMBALANCE
division_analysis['Profit_to_Revenue_%'] = (
    division_analysis['Total_Profit'] /
    division_analysis['Sales']) * 100
revenue_profit_imbalance = division_analysis[
    ['Division',
     'Sales',
     'Total_Profit',
     'Profit_to_Revenue_%']].sort_values(by='Sales',ascending=False)
print("\nRevenue vs Profit Comparison")
print(revenue_profit_imbalance)
revenue_profit_imbalance.to_csv("4.C.revenue_vs_profit_imbalance.csv",index=False)

# STRONG FINANCIAL EFFICIENCY DIVISIONS
margin_threshold = division_analysis['Average_Margin_%'].median()
strong_financial_efficiency = division_analysis[division_analysis['Average_Margin_%']>= margin_threshold]
print("\nStrong Financial Efficiency Divisions")
print(strong_financial_efficiency[
        ['Division',
         'Sales',
         'Total_Profit',
         'Average_Margin_%']])
strong_financial_efficiency.to_csv("4.D.strong_financial_efficiency_divisions.csv",index=False)


# STRUCTURAL MARGIN ISSUE DIVISIONS
structural_margin_issues = division_analysis[division_analysis['Average_Margin_%']< margin_threshold]
print("\nStructural Margin Issue Divisions")
print(structural_margin_issues[
        ['Division',
         'Sales',
         'Total_Profit',
         'Average_Margin_%']])
structural_margin_issues.to_csv("4.E.structural_margin_issue_divisions.csv",index=False)

# DIVISION PERFORMANCE RANKING
division_ranking = division_analysis.sort_values(by='Total_Profit',ascending=False)
division_ranking.to_csv("division_profit_ranking.csv",index=False)
print("\nTop Divisions By Profit")
print(division_ranking[
        ['Division',
         'Total_Profit']])

print("\nGenerated Files:")
print("1. division_performance_analysis.csv")
print("2. average_margin_by_division.csv")
print("3. revenue_vs_profit_imbalance.csv")
print("4. strong_financial_efficiency_divisions.csv")
print("5. structural_margin_issue_divisions.csv")
print("6. division_profit_ranking.csv")

# 5 PROFIT CONCENTRATION (PARETO) ANALYSIS
# Sort products by Profit (Descending)
pareto_profit = product_analysis.sort_values(by='Total_Profit',ascending=False).reset_index(drop=True)
# Cumulative Profit %
pareto_profit['Cumulative_Profit'] = (pareto_profit['Total_Profit'].cumsum())
total_profit = pareto_profit['Total_Profit'].sum()
pareto_profit['Cumulative_Profit_%'] = (pareto_profit['Cumulative_Profit'] /total_profit) * 100
# Products contributing to 80% Profit
profit_80_products = pareto_profit[pareto_profit['Cumulative_Profit_%'] <= 80]
num_products_profit_80 = len(profit_80_products)
total_products = len(product_analysis)
profit_80_percentage = (num_products_profit_80 /total_products) * 100

print(f"{profit_80_percentage:.2f}% of products "f"generate 80% of total profit.")
# Save
profit_80_products.to_csv("5.A.products_contributing_80_percent_profit.csv",index=False)

#  80% REVENUE CONTRIBUTION ANALYSIS
pareto_revenue = product_analysis.sort_values(by='Sales',ascending=False).reset_index(drop=True)
pareto_revenue['Cumulative_Sales'] = (pareto_revenue['Sales'].cumsum())
total_sales = pareto_revenue['Sales'].sum()
pareto_revenue['Cumulative_Sales_%'] = (pareto_revenue['Cumulative_Sales'] /total_sales) * 100
revenue_80_products = pareto_revenue[pareto_revenue['Cumulative_Sales_%'] <= 80]
num_products_revenue_80 = len(revenue_80_products)
revenue_80_percentage = (num_products_revenue_80 /total_products) * 100

print(f"{revenue_80_percentage:.2f}% of products "f"generate 80% of total revenue.")
revenue_80_products.to_csv("5.B.products_contributing_80_percent_revenue.csv",index=False)

# OVER-DEPENDENCY RISK ANALYSIS
top10_profit = pareto_profit.head(10)
top10_profit_share = (top10_profit['Total_Profit'].sum() /total_profit) * 100
print(f"Top 10 products contribute "f"{top10_profit_share:.2f}% of total profit.")
if top10_profit_share > 50:
    risk_level = "HIGH"
elif top10_profit_share > 30:
    risk_level = "MEDIUM"
else:
    risk_level = "LOW"
print(f"Risk Level: {risk_level}")
risk_summary = pd.DataFrame({
    'Metric': [
        'Total Products',
        'Products for 80% Profit',
        'Products for 80% Revenue',
        'Top 10 Profit Share (%)',
        'Risk Level'],
    'Value': [
        total_products,
        num_products_profit_80,
        num_products_revenue_80,
        round(top10_profit_share, 2),
        risk_level]})

risk_summary.to_csv("5.C.pareto_risk_analysis.csv",index=False)
pareto_profit.to_csv("5.D.pareto_profit_analysis.csv",index=False)
pareto_revenue.to_csv("5.E.pareto_revenue_analysis.csv",index=False)
print("\n Pareto Analysis Completed")
print("\nGenerated Files:")
print("1. pareto_profit_analysis.csv")
print("2. pareto_revenue_analysis.csv")
print("3. products_contributing_80_percent_profit.csv")
print("4. products_contributing_80_percent_revenue.csv")
print("5. pareto_risk_analysis.csv")

# 6. COST STRUCTURE DIAGNOSTICS
# Product-level cost analysis
cost_analysis = df.groupby('Product Name').agg({
    'Sales': 'sum',
    'Cost': 'sum',
    'Total_Profit': 'sum',
    'Units': 'sum'}).reset_index()
cost_analysis['Cost_to_Sales_%'] = (cost_analysis['Cost'] /cost_analysis['Sales']) * 100
cost_analysis['Gross_Margin_%'] = (cost_analysis['Total_Profit'] /cost_analysis['Sales']) * 100
cost_analysis.to_csv("6.A.cost_structure_analysis.csv",index=False)

#  COST VS SALES ANALYSIS
cost_vs_sales = cost_analysis[
    ['Product Name',
     'Sales',
     'Cost',
     'Cost_to_Sales_%']]
cost_vs_sales.to_csv(
    "cost_vs_sales_analysis.csv",
    index=False)
print("\nCost vs Sales Analysis Generated")

# COST-HEAVY / MARGIN-POOR PRODUCTS
cost_threshold = cost_analysis['Cost_to_Sales_%'].median()
margin_threshold = cost_analysis['Gross_Margin_%'].median()
cost_heavy_margin_poor = cost_analysis[(cost_analysis['Cost_to_Sales_%'] >= cost_threshold) &(cost_analysis['Gross_Margin_%'] < margin_threshold)]
print("\nCost-Heavy / Margin-Poor Products")
print(cost_heavy_margin_poor[
        ['Product Name',
         'Sales',
         'Cost',
         'Gross_Margin_%']])
cost_heavy_margin_poor.to_csv("6.B.cost_heavy_margin_poor_products.csv",index=False)

# PRICING INEFFICIENCIES
pricing_inefficiencies = cost_analysis[cost_analysis['Gross_Margin_%'] < 10]
print("\nPricing Inefficiencies")
print(pricing_inefficiencies[
        ['Product Name',
         'Sales',
         'Cost',
         'Gross_Margin_%']])
pricing_inefficiencies.to_csv("6.C.pricing_inefficiencies.csv",index=False)

# PRODUCTS NEEDING REPRICING
repricing_products = cost_analysis[cost_analysis['Gross_Margin_%'] < 15]
repricing_products.to_csv("6.D.products_needing_repricing.csv",index=False)

# PRODUCTS NEEDING COST RENEGOTIATION
cost_renegotiation = cost_analysis[cost_analysis['Cost_to_Sales_%'] > 85]
cost_renegotiation.to_csv("6.E.products_needing_cost_renegotiation.csv",index=False)

# 28. PRODUCTS FOR DISCONTINUATION REVIEW
discontinuation_review = cost_analysis[(cost_analysis['Total_Profit'] <= 0)]
discontinuation_review.to_csv("6.F.products_for_discontinuation_review.csv",index=False)

flagged_summary = pd.DataFrame({
    'Category': [
        'Cost Heavy Margin Poor',
        'Pricing Inefficiencies',
        'Need Repricing',
        'Need Cost Renegotiation',
        'Discontinuation Review'],
    'Product Count': [
        len(cost_heavy_margin_poor),
        len(pricing_inefficiencies),
        len(repricing_products),
        len(cost_renegotiation),
        len(discontinuation_review)]})
flagged_summary.to_csv("6.G.cost_structure_flagged_summary.csv",index=False)
print("\nCost Structure Diagnostics Completed")
print("\nGenerated Files:")
print("1. cost_structure_analysis.csv")
print("2. cost_vs_sales_analysis.csv")
print("3. cost_heavy_margin_poor_products.csv")
print("4. pricing_inefficiencies.csv")
print("5. products_needing_repricing.csv")
print("6. products_needing_cost_renegotiation.csv")
print("7. products_for_discontinuation_review.csv")
print("8. cost_structure_flagged_summary.csv")