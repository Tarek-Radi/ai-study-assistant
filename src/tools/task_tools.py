from datetime import date, datetime
from typing import Any

from pydantic import BaseModel, Field

from src.database import task_repository

# ---------------------------------------------------------
# Input validation models
# ---------------------------------------------------------


class AddTaskInput(BaseModel):
    """Validate input for creating a task."""

    title: str = Field(min_length=1, max_length=255)
    description: str | None = None
    due_date: date | None = None


class TaskIdInput(BaseModel):
    """Validate a task ID."""

    task_id: int = Field(gt=0)


class UpdateTaskInput(BaseModel):
    """Validate input for updating a task."""

    task_id: int = Field(gt=0)
    title: str | None = Field(default=None, min_length=1, max_length=255)
    description: str | None = None
    due_date: date | None = None


class UpdateDueDateInput(BaseModel):
    """Validate input for updating or removing a due date."""

    task_id: int = Field(gt=0)
    due_date: date | None = None


# ---------------------------------------------------------
# Helpers
# ---------------------------------------------------------


def _serialize_task(task: dict[str, Any] | None) -> dict[str, Any] | None:
    """Convert database values into JSON-friendly values."""

    if task is None:
        return None

    serialized_task = task.copy()

    for key, value in serialized_task.items():
        if isinstance(value, (date, datetime)):
            serialized_task[key] = value.isoformat()

    return serialized_task


# ---------------------------------------------------------
# Agent-facing tools
# ---------------------------------------------------------


def add_task(
    title: str,
    description: str | None = None,
    due_date: str | None = None,
) -> dict[str, Any]:
    """Create a new study task."""

    data = AddTaskInput(
        title=title,
        description=description,
        due_date=due_date,
    )

    task = task_repository.create_task(
        title=data.title.strip(),
        description=data.description,
        due_date=data.due_date,
    )

    return {
        "task": _serialize_task(task),
    }


def list_tasks() -> dict[str, Any]:
    """Return all study tasks."""

    tasks = task_repository.list_tasks()

    return {
        "count": len(tasks),
        "tasks": [_serialize_task(task) for task in tasks],
    }


def get_task(task_id: int) -> dict[str, Any]:
    """Return a study task by ID."""

    data = TaskIdInput(task_id=task_id)

    task = task_repository.get_task(data.task_id)

    if task is None:
        raise ValueError(f"Task with ID {data.task_id} was not found.")

    return {
        "task": _serialize_task(task),
    }


def complete_task(task_id: int) -> dict[str, Any]:
    """Mark a study task as completed."""

    data = TaskIdInput(task_id=task_id)

    task = task_repository.complete_task(data.task_id)

    if task is None:
        raise ValueError(f"Task with ID {data.task_id} was not found.")

    return {
        "task": _serialize_task(task),
    }


def reopen_task(task_id: int) -> dict[str, Any]:
    """Mark a completed study task as incomplete."""

    data = TaskIdInput(task_id=task_id)

    task = task_repository.reopen_task(data.task_id)

    if task is None:
        raise ValueError(f"Task with ID {data.task_id} was not found.")

    return {
        "task": _serialize_task(task),
    }


def update_task(
    task_id: int,
    title: str | None = None,
    description: str | None = None,
    due_date: str | None = None,
) -> dict[str, Any]:
    """Update one or more fields of a study task."""

    data = UpdateTaskInput(
        task_id=task_id,
        title=title,
        description=description,
        due_date=due_date,
    )

    if (
        data.title is None
        and data.description is None
        and data.due_date is None
    ):
        raise ValueError("At least one task field must be provided.")

    task = task_repository.update_task(
        task_id=data.task_id,
        title=data.title.strip() if data.title is not None else None,
        description=data.description,
        due_date=data.due_date,
    )

    if task is None:
        raise ValueError(f"Task with ID {data.task_id} was not found.")

    return {
        "task": _serialize_task(task),
    }


def update_task_due_date(
    task_id: int,
    due_date: str | None = None,
) -> dict[str, Any]:
    """Update or remove the due date of a study task."""

    data = UpdateDueDateInput(
        task_id=task_id,
        due_date=due_date,
    )

    task = task_repository.update_task_due_date(
        task_id=data.task_id,
        due_date=data.due_date,
    )

    if task is None:
        raise ValueError(f"Task with ID {data.task_id} was not found.")

    return {
        "task": _serialize_task(task),
    }


def delete_task(task_id: int) -> dict[str, Any]:
    """Delete a study task."""

    data = TaskIdInput(task_id=task_id)

    task = task_repository.delete_task(data.task_id)

    if task is None:
        raise ValueError(f"Task with ID {data.task_id} was not found.")

    return {
        "deleted_task": _serialize_task(task),
    }