import pandas as pd
import sqlite3

def load_data_to_sqlite(csv_path="data/grants_contacts.csv"):
    df = pd.read_csv(csv_path)
    conn = sqlite3.connect(":memory:")
    df.to_sql("grants_contacts", conn, index=False, if_exists="replace")
    return conn, df

def run_sql_audits(conn):
    results = {}
    
    # 1. Missing Metadata (Null or Empty Names / Amounts)
    missing_query = """
        SELECT record_id, contact_name, email, grant_amount, region
        FROM grants_contacts
        WHERE contact_name IS NULL OR contact_name = '' 
           OR grant_amount IS NULL OR grant_amount <= 0
           OR region IS NULL OR region = 'Unknown';
    """
    results["missing_data"] = pd.read_sql(missing_query, conn)
    
    # 2. Duplicate Records (Exact email + amount + region matches or duplicate record IDs)
    dup_query = """
        SELECT contact_name, email, grant_amount, COUNT(*) as duplicate_count
        FROM grants_contacts
        GROUP BY contact_name, email, grant_amount
        HAVING COUNT(*) > 1;
    """
    results["duplicates"] = pd.read_sql(dup_query, conn)
    
    # 3. Formatting Errors (Invalid email formats missing '@')
    formatting_query = """
        SELECT record_id, contact_name, email
        FROM grants_contacts
        WHERE email NOT LIKE '%@%';
    """
    results["formatting_errors"] = pd.read_sql(formatting_query, conn)
    
    return results
