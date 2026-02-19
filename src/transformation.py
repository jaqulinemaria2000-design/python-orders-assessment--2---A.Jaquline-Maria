import pandas as pd
import numpy as np

def transform_data(df_customers, df_orders, df_payments):
    """
    Transforms data:
    - Joins customers, orders, and payments.
    - Creates derived columns.
    - Performs aggregations.
    - Generates pivot tables.
    """
    print("Joining datasets...")

    # Join Orders with Customers
    orders_enriched = pd.merge(df_orders, df_customers, on='customer_id', how='left')
    
    # Join with Payments
    final_df = pd.merge(orders_enriched, df_payments, on='order_id', how='left')
    
    # Ensure date columns are datetime
    final_df['order_date'] = pd.to_datetime(final_df['order_date'])
    final_df['payment_date'] = pd.to_datetime(final_df['payment_date'])
    
    print("Creating derived columns...")
    # Derived Columns
    final_df['order_year'] = final_df['order_date'].dt.year
    final_df['payment_delay_days'] = (final_df['payment_date'] - final_df['order_date']).dt.days
    
    # Handle NaN in paid_amount (for unpaid/cancelled orders)
    final_df['paid_amount'] = final_df['paid_amount'].fillna(0)
    
    # Is fully paid? (Check if paid amount matches or exceeds order amount, considering float precision)
    final_df['is_fully_paid'] = final_df['paid_amount'] >= final_df['amount'] - 0.01

    return final_df

def generate_aggregations(df):
    """
    Generates summary aggregations.
    """
    aggs = {}
    
    # Total revenue per country
    aggs['revenue_by_country'] = df.groupby('country')['amount'].sum().reset_index().sort_values(by='amount', ascending=False)
    
    # Average order value per customer
    aggs['avg_order_value'] = df.groupby(['customer_id', 'name'])['amount'].mean().reset_index().rename(columns={'amount': 'avg_order_value'})
    
    # Monthly revenue trend
    df['order_month'] = df['order_date'].dt.to_period('M')
    aggs['monthly_revenue'] = df.groupby('order_month')['amount'].sum().reset_index()
    aggs['monthly_revenue']['order_month'] = aggs['monthly_revenue']['order_month'].astype(str) # Convert to string for better CSV output
    
    # Pivot: Revenue by country vs order status
    aggs['pivot_country_status'] = df.pivot_table(index='country', columns='status', values='amount', aggfunc='sum', fill_value=0)
    
    return aggs
