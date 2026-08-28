import os

import psycopg
from dotenv import load_dotenv


load_dotenv()


def get_db_connection():
    """Create and return a PostgreSQL database connection."""

    return psycopg.connect(
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT"),
        dbname=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
    )
    
if __name__ == "__main__":
    try:
        connection = get_db_connection()
        print("Database connection successful.")
        connection.close()

    except Exception as error:
        print(f"Database connection failed: {error}")