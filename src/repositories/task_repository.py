from db import db
from sqlalchemy import text
from datetime import datetime

class TaskRepository:
    def __init__(self, db) -> None:
        self._db = db

    def get_weeks_tasks(self, user_id: int, week_num: int):
        sql = text("SELECT * FROM tasks " \
                   "LEFT JOIN customers ON customer_id=customers.id " \
                   "LEFT JOIN projects ON project_id=projects.id " \
                   "LEFT JOIN task_types ON task_type_id=task_types.id " \
                   "WHERE user_id =:user_id AND DATE_PART('week',task_date)=:week_num " \
                    "GROUP BY tasks.id, customers.id, projects.id, task_types.id;")
        tasks = self._db.session.execute(sql, {"user_id":user_id,"week_num":week_num}).fetchall()
        return tasks

    def get_customers_and_projects(self):
        sql = text("SELECT customers.id as customer_id, customers.name as customer_name, " \
                   "projects.id as project_id, projects.name as project_name FROM customers " \
                   "LEFT JOIN projects ON customer_id=customers.id " \
                   "WHERE customers.visible = TRUE AND projects.visible = TRUE " \
                    "GROUP BY customers.id, projects.id;")
        return self._db.session.execute(sql).fetchall()

task_repository = TaskRepository(db)