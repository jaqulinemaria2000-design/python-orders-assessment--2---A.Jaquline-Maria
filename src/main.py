from ingestion import load_data
from cleaning import run_cleaning
from transformation import transform_data, generate_aggregations
from run_sqlite import run_sql_analysis
import os
import pandas as pd
from ingestion import load_data

def main():
    # Setup paths
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    data_dir = os.path.join(base_dir, 'data')
    output_dir = os.path.join(base_dir, 'outputs')
    agg_dir = os.path.join(output_dir, 'aggregates')
    
    # 1. Ingestion
    print("--- Part 1: Ingestion ---")
    df_customers, df_orders, df_payments = load_data(data_dir)
    
    # 2. Cleaning
    print("\n--- Part 2: Cleaning ---")
    customers_clean, orders_clean, payments_clean = run_cleaning(df_customers, df_orders, df_payments)
    
    # Save cleaned data
    customers_clean.to_csv(os.path.join(output_dir, 'customers_clean.csv'), index=False)
    orders_clean.to_csv(os.path.join(output_dir, 'orders_clean.csv'), index=False)
    payments_clean.to_csv(os.path.join(output_dir, 'payments_clean.csv'), index=False)
    
    # 3. Transformation
    print("\n--- Part 3: Transformation ---")
    final_df = transform_data(customers_clean, orders_clean, payments_clean)
    final_df.to_csv(os.path.join(output_dir, 'final_fact_orders.csv'), index=False)
    
    aggs = generate_aggregations(final_df)
    aggs['revenue_by_country'].to_csv(os.path.join(agg_dir, 'revenue_by_country.csv'), index=False)
    aggs['avg_order_value'].to_csv(os.path.join(agg_dir, 'avg_order_value_by_customer.csv'), index=False)
    aggs['monthly_revenue'].to_csv(os.path.join(agg_dir, 'monthly_revenue_trend.csv'), index=False)
    aggs['pivot_country_status'].to_csv(os.path.join(agg_dir, 'pivot_revenue_country_status.csv'))
    
    print(f"Transformation complete. Files saved to {output_dir}")
    
    # 4. SQL Analysis
    print("\n--- Part 4: SQL Analysis ---")
    db_path = os.path.join(output_dir, 'analysis.db')
    run_sql_analysis(customers_clean, orders_clean, payments_clean, db_path)

if __name__ == "__main__":
    main()
