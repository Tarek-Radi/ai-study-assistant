
from .connection import get_db_connection

CREATE_TASKS_TABLE = """
CREATE TABLE IF NOT EXISTS tasks (
    id SERIAL PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    description TEXT,
    due_date DATE,
    completed BOOLEAN NOT NULL DEFAULT FALSE,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);
"""


def init_db():
    """Initialize the database schema."""

    connection = get_db_connection()

    try:
        with connection.cursor() as cursor:
            cursor.execute(CREATE_TASKS_TABLE)

        connection.commit()
        print("Database initialized successfully.")

    except Exception as error:
        connection.rollback()
        print(f"Database initialization failed: {error}")

    finally:
        connection.close()


if __name__ == "__main__":
    init_db()