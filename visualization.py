import streamlit as st
import pandas as pd
import plotly.express as px
df = pd.read_csv("2"
".A.final_profit_data.csv")
product_analysis = pd.read_csv("3.A.product_level_profitability_analysis.csv")
division_analysis = pd.read_csv("4.A.division_performance_analysis.csv")
pareto_analysis = pd.read_csv("5.D.pareto_profit_analysis.csv")
cost_analysis = pd.read_csv("6.A.cost_structure_analysis.csv")

st.title("📊 Nassau Candy Analytics Dashboard")

# =====================================================
# KPI CARDS
# =====================================================

st.header("Key Performance Indicators")

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Total Sales",
    f"${df['Sales'].sum():,.0f}"
)

col2.metric(
    "Total Profit",
    f"${df['Total_Profit'].sum():,.0f}"
)

col3.metric(
    "Gross Margin %",
    f"{df['Gross_Margin_%'].mean():.2f}%"
)

col4.metric(
    "Units Sold",
    f"{df['Units'].sum():,.0f}"
)

# =====================================================
# PRODUCT PROFITABILITY OVERVIEW
# =====================================================

st.header("📦 Product Profitability Overview")

fig1 = px.bar(
    product_analysis.sort_values(
        by="Gross_Margin_%",
        ascending=False
    ).head(10),
    x="Product Name",
    y="Gross_Margin_%",
    title="Top 10 Products by Gross Margin"
)

st.plotly_chart(fig1, width="stretch")

# =====================================================
# PRODUCT PROFIT CHART
# =====================================================

fig2 = px.bar(
    product_analysis.sort_values(
        by="Total_Profit",
        ascending=False
    ).head(10),
    x="Product Name",
    y="Total_Profit",
    title="Top 10 Products by Profit"
)

st.plotly_chart(fig2, width="stretch")

# =====================================================
# DIVISION PERFORMANCE
# =====================================================

st.header("🏢 Division Performance Dashboard")

fig3 = px.bar(
    division_analysis,
    x="Division",
    y=["Sales", "Total_Profit"],
    barmode="group",
    title="Revenue vs Profit Comparison"
)

st.plotly_chart(fig3, width="stretch")

# =====================================================
# MARGIN DISTRIBUTION
# =====================================================

fig4 = px.bar(
    division_analysis,
    x="Division",
    y="Average_Margin_%",
    title="Average Margin by Division"
)

st.plotly_chart(fig4, width="stretch")

# =====================================================
# COST VS SALES DIAGNOSTICS
# =====================================================

st.header("💰 Cost Structure Diagnostics")

fig5 = px.scatter(
    cost_analysis,
    x="Cost",
    y="Sales",
    color="Gross_Margin_%",
    hover_name="Product Name",
    title="Cost vs Sales Scatter Plot"
)

st.plotly_chart(fig5, width="stretch")

# =====================================================
# COST HEAVY PRODUCTS
# =====================================================

fig6 = px.bar(
    cost_analysis.sort_values(
        by="Cost_to_Sales_%",
        ascending=False
    ).head(10),
    x="Product Name",
    y="Cost_to_Sales_%",
    title="Cost Heavy Products"
)

st.plotly_chart(fig6, width="stretch")

# =====================================================
# PARETO ANALYSIS
# =====================================================

st.header("📈 Profit Concentration Analysis")

fig7 = px.line(
    pareto_analysis,
    x="Product Name",
    y="Cumulative_Profit_%",
    markers=True,
    title="Pareto Profit Analysis"
)

st.plotly_chart(fig7, width="stretch")

# =====================================================
# DEPENDENCY INDICATOR
# =====================================================

profit_80 = pareto_analysis[
    pareto_analysis["Cumulative_Profit_%"] <= 80
]

dependency = (
    len(profit_80)
    /
    len(pareto_analysis)
) * 100

st.metric(
    "Dependency Indicator",
    f"{dependency:.2f}% of Products Generate 80% Profit"
)

# =====================================================
# DATA PREVIEW
# =====================================================

st.header("Dataset Preview")

st.dataframe(df.head(50))