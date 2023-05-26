from flask import session
from werkzeug.security import check_password_hash, generate_password_hash
from repositories.task_repository import task_repository
from secrets import token_hex
from datetime import date, datetime

class TaskService:
    def __init__(self) -> None:
        self.repository = task_repository
        self._roles = None

    def get_weeks_tasks(self,user_id: int):
        week_num = date(datetime.now()).isocalendar()[1]
        return self.repository.get_weeks_tasks(user_id,week_num)

task_service = TaskService()