import psycopg2
from datetime import datetime
from config import config 

def connect():
    try:
        conn = psycopg2.connect(**config)
        return conn
    except Exception as e:
        print(f"Error connecting to database: {e}")
        return None

def parse_date(date_str):
    if not date_str or not isinstance(date_str, str):
        return None
    try:
        return datetime.strptime(date_str.strip(), "%Y-%m-%d").date()
    except ValueError:
        print(f"Invalid date format: {date_str}. Expected YYYY-MM-DD.")
        return None