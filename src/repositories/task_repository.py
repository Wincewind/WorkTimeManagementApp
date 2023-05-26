from db import db
from sqlalchemy import text
from datetime import datetime

class TaskRepository:
    def __init__(self, db) -> None:
        self._db = db

    def get_weeks_tasks(self,user_id: int, week_num: int):
        sql = text("SELECT * FROM tasks" \
                   "LEFT JOIN customers ON customer_id=customers.id" \
                   "LEFT JOIN projects ON project_id=projects.id" \
                   "LEFT JOIN task_types ON task_type_id=task_types.id" \
                   "WHERE user_id =:user_id AND WEEK(task_date)=:week_num" \
                    "GROUP BY tasks.id;")
        tasks = self._db.session.execute(sql, {"user_id":user_id,"week_num":week_num}).fetchall()

task_repository = TaskRepository(db)