from datetime import datetime
from flask import session
from repositories.task_repository import task_repository
from services.user_service import user_service


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

    def _prepare_query_input(self, form_data):
        filter_values = {}
        for val in form_data:
            if val in ["from_date", "to_date", "customer_id", "project_id"]:
                if form_data[val] != "":
                    filter_values[val] = form_data[val]
        return filter_values

    def get_weeks_tasks(self, user_id: int):
        return self.repository.get_weeks_tasks(
            user_id, session["chosen_week"][1], session["chosen_week"][0]
        )

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
        return True

    def delete_task(self, task_id):
        return self.repository.delete(task_id, session["user_id"])

    def edit_task(self, form_data):
        task = self._prepare_task_input(form_data)
        self.repository.edit(task)

    def query_task_details(self, query_data=None):
        """Parse form arguments into a query and fetch data from
        task repository. If the user doesn't have a manager role,
        only their tasks will be returned.
        """
        if query_data is None:
            now = datetime.now()
            from_date = datetime(now.year, 1, 1)
            to_date = datetime(now.year, 12, 31)
            filters = {"from_date": from_date, "to_date": to_date}
        else:
            filters = self._prepare_query_input(query_data)
        if not user_service.check_user_role_level(1, False):
            filters["user_id"] = session["user_id"]
        return task_repository.select_task_details(filters)


task_service = TaskService()
