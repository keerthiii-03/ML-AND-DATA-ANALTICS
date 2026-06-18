import pandas as pd

# =====================================================
# LOAD DATASET
# =====================================================

file_path = "Nassau Candy Distributor (1).csv"
df = pd.read_csv(file_path)

print("Dataset Loaded Successfully")

# =====================================================
# CREATE TOTAL PROFIT COLUMN
# =====================================================

# Nassau Candy dataset already contains Gross Profit
df['Total_Profit'] = df['Gross Profit']

# =====================================================
# KPI ANALYSIS
# =====================================================

kpi_analysis = df.groupby('Product Name').agg({
    'Sales': 'sum',
    'Units': 'sum',
    'Total_Profit': 'sum'}).reset_index()

# -----------------------------------------------------
# KPI 1: Gross Margin (%)
# -----------------------------------------------------

kpi_analysis['Gross_Margin_%'] = (
    kpi_analysis['Total_Profit']
    / kpi_analysis['Sales']) * 100

# -----------------------------------------------------
# KPI 2: Profit Per Unit
# -----------------------------------------------------

kpi_analysis['Profit_per_Unit'] = (
    kpi_analysis['Total_Profit']
    / kpi_analysis['Units'])

# -----------------------------------------------------
# KPI 3: Revenue Contribution (%)
# -----------------------------------------------------

total_sales = kpi_analysis['Sales'].sum()

kpi_analysis['Revenue_Contribution_%'] = (
    kpi_analysis['Sales']
    / total_sales) * 100

# -----------------------------------------------------
# KPI 4: Profit Contribution (%)
# -----------------------------------------------------

total_profit = kpi_analysis['Total_Profit'].sum()

kpi_analysis['Profit_Contribution_%'] = (
    kpi_analysis['Total_Profit']
    / total_profit) * 100

# =====================================================
# MARGIN VOLATILITY KPI
# =====================================================

# Convert Order Date correctly
df['Order Date'] = pd.to_datetime(
    df['Order Date'],
    dayfirst=True,
    errors='coerce')

# Remove invalid dates
df = df.dropna(subset=['Order Date'])

# Monthly Margin Analysis
monthly_margin = df.groupby(
    df['Order Date'].dt.to_period('M')).agg({
    'Sales': 'sum',
    'Total_Profit': 'sum'}).reset_index()

monthly_margin['Margin_%'] = (
    monthly_margin['Total_Profit'] /
    monthly_margin['Sales']) * 100

# Margin Volatility
margin_volatility = monthly_margin[
    'Margin_%'].std()
print("\nMargin Volatility:")
print(round(margin_volatility, 2))
# Save Output
margin_volatility_df = pd.DataFrame({
    'Metric': ['Margin Volatility'],
    'Value': [round(margin_volatility, 2)]})

margin_volatility_df.to_csv(
    ".margin_volatility_kpi.csv",
    index=False)

monthly_margin.to_csv(
    "k6.monthly_margin_analysis.csv",
    index=False)

print("Margin Volatility KPI Generated")

# =====================================================
# SAVE KPI OUTPUT FILES
# =====================================================

# Gross Margin
gross_margin = kpi_analysis[
    ['Product Name', 'Gross_Margin_%']
].sort_values(
    by='Gross_Margin_%',
    ascending=False
)

gross_margin.to_csv(
    'k1.gross_margin_kpi.csv',
    index=False
)

# Profit Per Unit
profit_per_unit = kpi_analysis[
    ['Product Name', 'Profit_per_Unit']
].sort_values(
    by='Profit_per_Unit',
    ascending=False
)

profit_per_unit.to_csv(
    'k2.profit_per_unit_kpi.csv',
    index=False
)

# Revenue Contribution
revenue_contribution = kpi_analysis[
    ['Product Name', 'Revenue_Contribution_%']
].sort_values(
    by='Revenue_Contribution_%',
    ascending=False
)

revenue_contribution.to_csv(
    'k3.revenue_contribution_kpi.csv',
    index=False
)

# Profit Contribution
profit_contribution = kpi_analysis[
    ['Product Name', 'Profit_Contribution_%']
].sort_values(
    by='Profit_Contribution_%',
    ascending=False
)

profit_contribution.to_csv(
    'k4.profit_contribution_kpi.csv',
    index=False
)

# Margin Volatility
margin_volatility_df.to_csv(
    'k5.margin_volatility_kpi.csv',
    index=False
)

# Complete KPI Analysis
kpi_analysis.to_csv(
    'k7.complete_kpi_analysis.csv',
    index=False
)

# =====================================================
# DISPLAY RESULTS
# =====================================================

print("\n===================================")
print("KEY PERFORMANCE INDICATORS")
print("===================================")

print("\nTop 10 Products by Gross Margin")
print(
    gross_margin.head(10)
)

print("\nTop 10 Products by Profit Contribution")
print(
    profit_contribution.head(10)
)

print("\nMargin Volatility:")
print(round(margin_volatility, 2))

print("\nGenerated Files:")
print("1. gross_margin_kpi.csv")
print("2. profit_per_unit_kpi.csv")
print("3. revenue_contribution_kpi.csv")
print("4. profit_contribution_kpi.csv")
print("5. margin_volatility_kpi.csv")
print("6. complete_kpi_analysis.csv")

print("\n KPI Analysis Completed Successfully")