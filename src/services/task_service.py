from datetime import datetime
from flask import session
from repositories.task_repository import task_repository


class TaskService:
    """Service for handling interaction with the tasks repository."""

    def __init__(self) -> None:
        self.repository = task_repository
        self._roles = None

    def _prepare_task_input(self, form_data):
        task = {"user_id": session["user_id"], "invoiceable": False}
        for val in form_data:
            if val in [
                "duration",
                "task_date",
                "customer_id",
                "project_id",
                "task_type_id",
                "invoiceable",
                "note",
            ]:
                if val == "duration":
                    task["duration_hours"], task["duration_minutes"] = form_data[
                        val
                    ].split(":")
                else:
                    task[val] = form_data[val]
        if session.get("chosen_task", None) is not None:
            task["task_id"] = session["chosen_task"]["id"]
        return task

    def get_weeks_tasks(self, user_id: int, chosen_date=datetime.now()):
        week_num = chosen_date.isocalendar()[1]
        return self.repository.get_weeks_tasks(user_id, week_num, chosen_date.year)

    def get_all_task_types(self):
        return self.repository.get_types()

    def create_task(self, form_data):
        task = self._prepare_task_input(form_data)
        self.repository.create(task)

    def get_task(self, task_id):
        task = self.repository.get_task(task_id, session["user_id"])
        if task is None:
            return False
        session["chosen_task"] = task._asdict()
        print(session["chosen_task"])
        return True

    def delete_task(self, task_id):
        return self.repository.delete(task_id, session["user_id"])

    def edit_task(self, form_data):
        task = self._prepare_task_input(form_data)
        self.repository.edit(task)


task_service = TaskService()
