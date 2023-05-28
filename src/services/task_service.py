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
        week_num = datetime.now().isocalendar()[1]
        return self.repository.get_weeks_tasks(user_id,week_num)

    def get_customers_and_projects(self):
        return self.repository.get_customers_and_projects()
    
    def get_all_task_types(self):
        return self.repository.get_types()
    
    def create_task(self,task):
        self.repository.create(task)

task_service = TaskService()