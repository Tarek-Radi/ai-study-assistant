from datetime import date

from .task_repository import (
    create_task,
    list_tasks,
    get_task,
    complete_task,
    reopen_task,
    update_task_due_date,
    update_task,
    delete_task,
)


def run_tests():
    print("\n1) Creating task...")
    task = create_task(
        title="Study Embeddings",
        description="Focus on cosine similarity",
        due_date=date(2026, 9, 1),
    )
    print(task)

    task_id = task["id"]

    print("\n2) Getting task...")
    print(get_task(task_id))

    print("\n3) Listing tasks...")
    print(list_tasks())

    print("\n4) Completing task...")
    print(complete_task(task_id))

    print("\n5) Reopening task...")
    print(reopen_task(task_id))

    print("\n6) Updating due date...")
    print(update_task_due_date(task_id, date(2026, 9, 5)))

    print("\n7) Updating task...")
    print(
        update_task(
            task_id=task_id,
            title="Study Embeddings and Vector Search",
            description="Focus on cosine similarity and vector retrieval",
        )
    )

    print("\n8) Deleting task...")
    print(delete_task(task_id))

    print("\n9) Checking deleted task...")
    print(get_task(task_id))


if __name__ == "__main__":
    run_tests()