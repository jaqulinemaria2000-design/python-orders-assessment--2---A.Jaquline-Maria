import pandas as pd
import os
import json

def load_data(data_dir='data'):
    """
    Loads customers (CSV), orders (JSON), and payments (Excel) datasets.
    
    Args:
        data_dir (str): Path to the data directory.
        
    Returns:
        tuple: (df_customers, df_orders, df_payments)
    """
    print("Loading datasets...")
    
    # Load Customers (CSV)
    customers_path = os.path.join(data_dir, 'customers.csv')
    try:
        # Handling potential encoding issues with 'latin1' if 'utf-8' fails, 
        # though sample data is generated in default encoding.
        df_customers = pd.read_csv(customers_path, encoding='utf-8')
    except UnicodeDecodeError:
        print(f"Warning: UnicodeDecodeError encountered reading {customers_path}. Trying 'latin1'.")
        df_customers = pd.read_csv(customers_path, encoding='latin1')
    except FileNotFoundError:
        print(f"Error: {customers_path} not found.")
        df_customers = pd.DataFrame()

    # Load Orders (JSON)
    orders_path = os.path.join(data_dir, 'orders.json')
    try:
        df_orders = pd.read_json(orders_path)
        # Ensure date columns are datetime objects
        if 'order_date' in df_orders.columns:
            # handle mixed formats and invalid dates
            df_orders['order_date'] = pd.to_datetime(df_orders['order_date'], errors='coerce', dayfirst=True)
            
            # Report invalid dates
            invalid_dates = df_orders['order_date'].isnull().sum()
            if invalid_dates > 0:
                print(f"Warning: {invalid_dates} records have invalid or missing 'order_date'. They will be set to NaT.")
    except ValueError as e:
        print(f"Error reading JSON {orders_path}: {e}")
        df_orders = pd.DataFrame()
    except FileNotFoundError:
        print(f"Error: {orders_path} not found.")
        df_orders = pd.DataFrame()

    # Load Payments (Excel)
    # Load Payments (Excel)
    payments_path = os.path.join(data_dir, 'payments.xlsx')
    try:
        df_payments = pd.read_excel(payments_path)
        if 'payment_date' in df_payments.columns:
            # handle mixed formats
            df_payments['payment_date'] = pd.to_datetime(df_payments['payment_date'], errors='coerce', dayfirst=True)
            
            # Report invalid dates
            invalid_dates = df_payments['payment_date'].isnull().sum()
            if invalid_dates > 0:
                print(f"Warning: {invalid_dates} payment records have invalid 'payment_date'. They will be set to NaT.", flush=True)
    # except Exception as e:
    #     print(f"Error reading Excel {payments_path}: {e}")
    #     df_payments = pd.DataFrame()
    except FileNotFoundError:
        print(f"Error: {payments_path} not found.")
        df_payments = pd.DataFrame()

    print("Data ingestion complete.")
    return df_customers, df_orders, df_payments

if __name__ == "__main__":
    c, o, p = load_data('../data')
    print("Customers shape:", c.shape)
    print("Orders shape:", o.shape)
    print("Payments shape:", p.shape)
