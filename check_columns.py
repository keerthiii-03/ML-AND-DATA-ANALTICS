import pandas as pd

files = [
    "2.A.final_profit_data.csv",
    "3.A.product_level_profitability_analysis.csv",
    "4.A.division_performance_analysis.csv",
    "5.D.pareto_profit_analysis.csv",
    "6.A.cost_structure_analysis.csv"
]

for file in files:
    print("\n" + "="*50)
    print(file)
    print("="*50)

    df = pd.read_csv(file)

    print("\nColumns:")
    print(df.columns.tolist())