from datetime import date
from typing import Any

from .connection import get_db_connection


def create_task(
    title: str,
    description: str | None = None,
    due_date: date | None = None,
) -> dict[str, Any]:
    """Create a new task and return the inserted row."""

    connection = get_db_connection()

    try:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                INSERT INTO tasks (
                    title,
                    description,
                    due_date
                )
                VALUES (%s, %s, %s)
                RETURNING
                    id,
                    title,
                    description,
                    due_date,
                    completed,
                    created_at,
                    updated_at;
                """,
                (title, description, due_date),
            )

            row = cursor.fetchone()

        connection.commit()

        return {
            "id": row[0],
            "title": row[1],
            "description": row[2],
            "due_date": row[3],
            "completed": row[4],
            "created_at": row[5],
            "updated_at": row[6],
        }

    except Exception:
        connection.rollback()
        raise

    finally:
        connection.close()


def list_tasks() -> list[dict[str, Any]]:
    """Return all study tasks ordered by creation time."""

    connection = get_db_connection()

    try:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                SELECT
                    id,
                    title,
                    description,
                    due_date,
                    completed,
                    created_at,
                    updated_at
                FROM tasks
                ORDER BY created_at DESC;
                """
            )

            rows = cursor.fetchall()

        return [
            {
                "id": row[0],
                "title": row[1],
                "description": row[2],
                "due_date": row[3],
                "completed": row[4],
                "created_at": row[5],
                "updated_at": row[6],
            }
            for row in rows
        ]

    finally:
        connection.close()


def complete_task(task_id: int) -> dict[str, Any] | None:
    """Mark a task as completed and return the updated task."""

    connection = get_db_connection()

    try:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                UPDATE tasks
                SET
                    completed = TRUE,
                    updated_at = CURRENT_TIMESTAMP
                WHERE id = %s
                RETURNING
                    id,
                    title,
                    description,
                    due_date,
                    completed,
                    created_at,
                    updated_at;
                """,
                (task_id,),
            )

            row = cursor.fetchone()

        connection.commit()

        if row is None:
            return None

        return {
            "id": row[0],
            "title": row[1],
            "description": row[2],
            "due_date": row[3],
            "completed": row[4],
            "created_at": row[5],
            "updated_at": row[6],
        }

    except Exception:
        connection.rollback()
        raise

    finally:
        connection.close()


def reopen_task(task_id: int) -> dict[str, Any] | None:
    """Mark a task as incomplete and return the updated task."""

    connection = get_db_connection()

    try:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                UPDATE tasks
                SET
                    completed = FALSE,
                    updated_at = CURRENT_TIMESTAMP
                WHERE id = %s
                RETURNING
                    id,
                    title,
                    description,
                    due_date,
                    completed,
                    created_at,
                    updated_at;
                """,
                (task_id,),
            )

            row = cursor.fetchone()

        connection.commit()

        if row is None:
            return None

        return {
            "id": row[0],
            "title": row[1],
            "description": row[2],
            "due_date": row[3],
            "completed": row[4],
            "created_at": row[5],
            "updated_at": row[6],
        }

    except Exception:
        connection.rollback()
        raise

    finally:
        connection.close()
        
def update_task_due_date(
    task_id: int,
    due_date: date | None,
) -> dict[str, Any] | None:
    """Update a task due date and return the updated task."""

    connection = get_db_connection()

    try:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                UPDATE tasks
                SET
                    due_date = %s,
                    updated_at = CURRENT_TIMESTAMP
                WHERE id = %s
                RETURNING
                    id,
                    title,
                    description,
                    due_date,
                    completed,
                    created_at,
                    updated_at;
                """,
                (due_date, task_id),
            )

            row = cursor.fetchone()

        connection.commit()

        if row is None:
            return None

        return {
            "id": row[0],
            "title": row[1],
            "description": row[2],
            "due_date": row[3],
            "completed": row[4],
            "created_at": row[5],
            "updated_at": row[6],
        }

    except Exception:
        connection.rollback()
        raise

    finally:
        connection.close()
        
def get_task(task_id: int) -> dict[str, Any] | None:
    """Return a task by its ID."""

    connection = get_db_connection()

    try:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                SELECT
                    id,
                    title,
                    description,
                    due_date,
                    completed,
                    created_at,
                    updated_at
                FROM tasks
                WHERE id = %s;
                """,
                (task_id,),
            )

            row = cursor.fetchone()

        if row is None:
            return None

        return {
            "id": row[0],
            "title": row[1],
            "description": row[2],
            "due_date": row[3],
            "completed": row[4],
            "created_at": row[5],
            "updated_at": row[6],
        }

    finally:
        connection.close()


def update_task(
    task_id: int,
    title: str | None = None,
    description: str | None = None,
    due_date: date | None = None,
) -> dict[str, Any] | None:
    """Update task fields and return the updated task."""

    connection = get_db_connection()

    try:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                UPDATE tasks
                SET
                    title = COALESCE(%s, title),
                    description = COALESCE(%s, description),
                    due_date = COALESCE(%s, due_date),
                    updated_at = CURRENT_TIMESTAMP
                WHERE id = %s
                RETURNING
                    id,
                    title,
                    description,
                    due_date,
                    completed,
                    created_at,
                    updated_at;
                """,
                (
                    title,
                    description,
                    due_date,
                    task_id,
                ),
            )

            row = cursor.fetchone()

        connection.commit()

        if row is None:
            return None

        return {
            "id": row[0],
            "title": row[1],
            "description": row[2],
            "due_date": row[3],
            "completed": row[4],
            "created_at": row[5],
            "updated_at": row[6],
        }

    except Exception:
        connection.rollback()
        raise

    finally:
        connection.close()


def delete_task(task_id: int) -> dict[str, Any] | None:
    """Delete a task and return the deleted task."""

    connection = get_db_connection()

    try:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                DELETE FROM tasks
                WHERE id = %s
                RETURNING
                    id,
                    title,
                    description,
                    due_date,
                    completed,
                    created_at,
                    updated_at;
                """,
                (task_id,),
            )

            row = cursor.fetchone()

        connection.commit()

        if row is None:
            return None

        return {
            "id": row[0],
            "title": row[1],
            "description": row[2],
            "due_date": row[3],
            "completed": row[4],
            "created_at": row[5],
            "updated_at": row[6],
        }

    except Exception:
        connection.rollback()
        raise

    finally:
        connection.close()