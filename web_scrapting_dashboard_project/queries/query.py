import sqlite3 
import argparse
import pandas as pd 
from tabulate import tabulate 

DB_PATH = "../history.db"

def connect_db():
    return sqlite3.connect(DB_PATH)

def run_query(conn, sql, params=None):
    try:
        df = pd.read_sql_query(sql, conn, params=params)
        if df.empty:
            print("No results found.")
        else:
            print(tabulate(df, headers='keys', tablefmt='grid'))
    except Exception as e:
        print(f"Query failed: {e}")

def query_events_by_year(conn, year):
    sql = "SELECT * FROM events WHERE year = ?"
    run_query(conn, sql, (year,))

# 🔒 Commented out - no player/stats data available
# def query_player_stats(conn, player_name):
#     sql = """
#         SELECT p.name, s.*
#         FROM players p 
#         JOIN stats s ON p.player_id = s.player_id 
#         WHERE p.name LIKE ?
#     """
#     run_query(conn, sql, (f"%{player_name}%",))

def query_events_by_type(conn, keyword):
    sql = """
        SELECT * FROM events 
        WHERE LOWER(event) LIKE ?
        OR LOWER(description) LIKE ?
    """
    run_query(conn, sql, (f"%{keyword.lower()}%", f"%{keyword.lower()}%"))

def list_tables(conn):
    sql = "SELECT name FROM sqlite_master WHERE type='table';"
    run_query(conn, sql)

def main():
    parser = argparse.ArgumentParser(description="Query the history database")
    parser.add_argument("--year", type=int, help="Filter events by year")
    
    # 🔒 Commented out - no player data
    # parser.add_argument("--player", type=str, help="Filter stats by player name")

    parser.add_argument("--event", type=str, help="Search events by keyword")
    parser.add_argument("--list-tables", action="store_true", help="List all tables")

    args = parser.parse_args()
    conn = connect_db()

    if args.list_tables:
        list_tables(conn)
    elif args.year:
        query_events_by_year(conn, args.year)

    # 🔒 Commented out - no player query function
    # elif args.player:
    #     query_player_stats(conn, args.player)

    elif args.event:
        query_events_by_type(conn, args.event)
    else:
        parser.print_help()

    conn.close()

if __name__ == "__main__":
    main()
