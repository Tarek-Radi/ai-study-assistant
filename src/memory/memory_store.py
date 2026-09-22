from typing import Any

from src.database.connection import get_db_connection


def save_memory(
    key: str,
    value: str,
) -> dict[str, Any]:
    """Create or update a memory value."""

    connection = get_db_connection()

    try:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                INSERT INTO memories (key, value)
                VALUES (%s, %s)
                ON CONFLICT (key)
                DO UPDATE SET
                    value = EXCLUDED.value,
                    updated_at = CURRENT_TIMESTAMP
                RETURNING
                    id,
                    key,
                    value,
                    created_at,
                    updated_at;
                """,
                (
                    key,
                    value,
                ),
            )

            memory = cursor.fetchone()

        connection.commit()

        return {
            "id": memory[0],
            "key": memory[1],
            "value": memory[2],
            "created_at": memory[3].isoformat(),
            "updated_at": memory[4].isoformat(),
        }

    except Exception:
        connection.rollback()
        raise

    finally:
        connection.close()


def get_memory(
    key: str,
) -> dict[str, Any] | None:
    """Get a memory by key."""

    connection = get_db_connection()

    try:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                SELECT
                    id,
                    key,
                    value,
                    created_at,
                    updated_at
                FROM memories
                WHERE key = %s;
                """,
                (key,),
            )

            memory = cursor.fetchone()

        if memory is None:
            return None

        return {
            "id": memory[0],
            "key": memory[1],
            "value": memory[2],
            "created_at": memory[3].isoformat(),
            "updated_at": memory[4].isoformat(),
        }

    finally:
        connection.close()


def list_memories() -> list[dict[str, Any]]:
    """Return all saved memories."""

    connection = get_db_connection()

    try:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                SELECT
                    id,
                    key,
                    value,
                    created_at,
                    updated_at
                FROM memories
                ORDER BY id;
                """
            )

            memories = cursor.fetchall()

        return [
            {
                "id": memory[0],
                "key": memory[1],
                "value": memory[2],
                "created_at": memory[3].isoformat(),
                "updated_at": memory[4].isoformat(),
            }
            for memory in memories
        ]

    finally:
        connection.close()


def delete_memory(
    key: str,
) -> bool:
    """Delete a memory by key."""

    connection = get_db_connection()

    try:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                DELETE FROM memories
                WHERE key = %s;
                """,
                (key,),
            )

            deleted = cursor.rowcount > 0

        connection.commit()

        return deleted

    except Exception:
        connection.rollback()
        raise

    finally:
        connection.close()
        
        
if __name__ == "__main__":
    print(
        save_memory(
            key="preferred_language",
            value="English",
        )
    )

    print(
        get_memory(
            key="preferred_language"
        )
    )

    print(
        delete_memory(
            key="preferred_language"
        )
    )

    print(
        get_memory(
            key="preferred_language"
        )
    )