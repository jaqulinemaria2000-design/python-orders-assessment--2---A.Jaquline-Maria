import pandas as pd
import numpy as np

def clean_customers(df):
    """
    Cleans customer data.
    - Handles missing emails (flagged).
    - Removes duplicates.
    - Standardizes country names.
    - Ensures correct data types.
    """
    if df.empty: return df
    
    # Remove duplicates
    initial_count = len(df)
    df = df.drop_duplicates(subset=['customer_id'])
    print(f"Removed {initial_count - len(df)} duplicate customers.")
    
    # Handle missing emails
    df['email_missing'] = df['email'].isnull()
    df['email'] = df['email'].fillna('MISSING')
    
    # Standardize country names
    df['country'] = df['country'].str.title().str.strip()
    # Handle USA variations specifically if needed, though title() covers usa -> Usa.
    # We want 'Usa' -> 'USA' or 'United States'. Let's standardise to 'United States' for this example
    country_map = {
        'Usa': 'United States',
        'Uk': 'United Kingdom'
    }
    df['country'] = df['country'].replace(country_map)
    
    # Convert signup_date to datetime if not already
    try:
        df['signup_date'] = pd.to_datetime(df['signup_date'])
    except Exception as e:
        print(f"Error converting signup_date: {e}")

    return df

def clean_orders(df):
    """
    Cleans orders data.
    - Flags invalid amounts (<= 0).
    - Normalizes status.
    - Identifies outliers.
    """
    if df.empty: return df

    # Normalize status
    df['status'] = df['status'].str.title().str.strip()
    
    # Ensure amount is numeric
    df['amount'] = pd.to_numeric(df['amount'], errors='coerce')
    
    # Handle invalid amounts
    df['is_valid_amount'] = df['amount'] > 0
    invalid_count = (~df['is_valid_amount']).sum()
    if invalid_count > 0:
        print(f"Found {invalid_count} orders with invalid amounts.")
        
    # Identify outliers (Simple Z-score approach or IQR)
    # Using IQR for robustness
    Q1 = df['amount'].quantile(0.25)
    Q3 = df['amount'].quantile(0.75)
    IQR = Q3 - Q1
    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR
    
    df['is_outlier'] = ~df['amount'].between(lower_bound, upper_bound)
    outlier_count = df['is_outlier'].sum()
    print(f"Identified {outlier_count} outlier orders.")
    
    return df

def clean_payments(df):
    """
    Cleans payments data.
    - Removes duplicate payment records.
    - Ensures valid payment amounts.
    """
    if df.empty: return df
    
    # Remove duplicates
    initial_count = len(df)
    df = df.drop_duplicates() 
    print(f"Removed {initial_count - len(df)} duplicate payments.")
    
    # Ensure payment_date is datetime
    try:
        df['payment_date'] = pd.to_datetime(df['payment_date'])
    except Exception as e:
        print(f"Error converting payment_date: {e}")
        
    # Ensure paid_amount is numeric
    if 'paid_amount' in df.columns:
        df['paid_amount'] = pd.to_numeric(df['paid_amount'], errors='coerce')

    return df

def run_cleaning(df_customers, df_orders, df_payments):
    print("Cleaning customers...")
    customers_clean = clean_customers(df_customers.copy())
    
    print("Cleaning orders...")
    orders_clean = clean_orders(df_orders.copy())
    
    print("Cleaning payments...")
    payments_clean = clean_payments(df_payments.copy())
    
    return customers_clean, orders_clean, payments_clean
