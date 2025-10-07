import os 
import sqlite3 
import pandas as pd 
import logging 

DATA_DIR = "../data"
DB_PATH = "../history.db"
LOG_PATH = "../import_log.txt"

# setup logging 
logging.basicConfig(filename=LOG_PATH, level=logging.INFO, filemode="w", format="%(asctime)s - %(levelname)s - %(message)s")

def clean_column_names(df):
    df.columns = [col.strip().replace(" ", "_").replace("-", "_").lower() for col in df.columns]
    return df 

def import_csv_to_sqlite(csv_file, conn):
    table_name = os.path.splitext(csv_file)[0].lower()
    file_path = os.path.join(DATA_DIR, csv_file) 

    try:
        df = pd.read_csv(file_path)
        df = clean_column_names(df)

        df.to_sql(table_name, conn, if_exists='replace', index=False)

        logging.info(f"Imported '{csv_file}' as table '{table_name}' with {len(df)} rows.")
        print(f"{csv_file} -> {table_name} ({len(df)} rows)")
    
    except Exception as e:
        logging.error(f"Failed to import '{csv_file}': {e}")
        print(f"Failed to import {csv_file}: {e}")

def main():
    if not os.path.exists(DATA_DIR):
        print(f"Data directory not found: {DATA_DIR}")
        return 
    
    conn = sqlite3.connect(DB_PATH)
    print(f"Connected to database: {DB_PATH}")

    for file in os.listdir(DATA_DIR):
        if file.endswith(".csv"):
            import_csv_to_sqlite(file, conn)
    
    conn.close()
    print("CSV files processed.")
    logging.info("All CSV imports completed.")

if __name__ == "__main__":
    main()
    