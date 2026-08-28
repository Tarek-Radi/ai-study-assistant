from .task_tools import (
    add_task,
    list_tasks,
    get_task,
    complete_task,
    reopen_task,
    update_task,
    update_task_due_date,
    delete_task,
)


def run_tests():
    print("\n1) Add task")
    task_result = add_task(
        title="Study RAG",
        description="Review embeddings",
        due_date="2026-09-02",
    )
    print(task_result)

    task_id = task_result["task"]["id"]

    print("\n2) Get task")
    print(get_task(task_id))

    print("\n3) List tasks")
    print(list_tasks())

    print("\n4) Complete task")
    print(complete_task(task_id))

    print("\n5) Reopen task")
    print(reopen_task(task_id))

    print("\n6) Update task")
    print(
        update_task(
            task_id=task_id,
            title="Study Advanced RAG",
            description="Review retrieval and embeddings",
        )
    )

    print("\n7) Update due date")
    print(update_task_due_date(task_id, "2026-09-05"))

    print("\n8) Delete task")
    print(delete_task(task_id))


if __name__ == "__main__":
    run_tests()