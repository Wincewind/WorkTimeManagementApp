from flask import session
from werkzeug.security import check_password_hash, generate_password_hash
from repositories.task_repository import task_repository
from secrets import token_hex
from datetime import date, datetime

class TaskService:
    def __init__(self) -> None:
        self.repository = task_repository
        self._roles = None

    def get_weeks_tasks(self,user_id: int, chosen_date=datetime.now()):
        week_num = chosen_date.isocalendar()[1]
        return self.repository.get_weeks_tasks(user_id,week_num)

    def get_customers_and_projects(self):
        return self.repository.get_customers_and_projects()
    
    def get_all_task_types(self):
        return self.repository.get_types()
    
    def create_task(self,task):
        self.repository.create(task)

    def get_task(self, task_id):
        task = self.repository.get_task(task_id, session['user_id'])
        if task is None:
            return False
        session["chosen_task"] = task._asdict()
        print(session["chosen_task"])
        return True
    
    def delete_task(self, task_id):
        return self.repository.delete(task_id, session['user_id'])
    
    def edit_task(self, task):
        self.repository.edit(task)

task_service = TaskService()