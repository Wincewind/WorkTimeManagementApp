from datetime import datetime
from sqlalchemy import text
from db import db


class TaskRepository:
    def __init__(self, db_) -> None:
        self._db = db_

    def get_weeks_tasks(self, user_id: int, week_num: int):
        sql = text(
            """SELECT tasks.id as task_id, task_date, duration_hours,
            duration_minutes, customers.name as customer_name,
            projects.name as project_name, task_types.description as task_desc FROM tasks
            LEFT JOIN customers ON customer_id=customers.id
            LEFT JOIN projects ON project_id=projects.id
            LEFT JOIN task_types ON task_type_id=task_types.id
            WHERE user_id =:user_id AND DATE_PART('week',task_date)=:week_num
            GROUP BY tasks.id, customers.id, projects.id, task_types.id;"""
        )
        tasks = self._db.session.execute(
            sql, {"user_id": user_id, "week_num": week_num}
        ).fetchall()
        return tasks

    def get_customers_and_projects(self):
        sql = text(
            """SELECT customers.id as customer_id, customers.name as customer_name,
                   projects.id as project_id, projects.name as project_name FROM customers
                   LEFT JOIN projects ON customer_id=customers.id
                   WHERE customers.visible = TRUE AND projects.visible = TRUE
                    GROUP BY customers.id, projects.id;"""
        )
        return self._db.session.execute(sql).fetchall()

    def get_types(self):
        return self._db.session.execute(text("SELECT * FROM task_types;"))

    def create(self, task_values: dict):
        sql = text(
            """INSERT INTO tasks (user_id, duration_hours, duration_minutes,
                   task_date, customer_id, project_id, task_type_id, invoiceable, note)
                    VALUES (:user_id, :duration_hours, :duration_minutes,
                    :task_date, :customer_id, :project_id, :task_type_id, :invoiceable, :note);"""
        )
        self._db.session.execute(sql, task_values)
        self._db.session.commit()

    def get_task(self, task_id, user_id):
        sql = text(
            """SELECT id, task_date, duration_hours, duration_minutes, customer_id,
        project_id, task_type_id, invoiceable, note FROM tasks
        WHERE user_id =:user_id AND tasks.id=:task_id;"""
        )
        return self._db.session.execute(
            sql, {"task_id": task_id, "user_id": user_id}
        ).fetchone()

    def delete(self, task_id, user_id):
        sql_sel = text("SELECT FROM tasks WHERE user_id=:user_id AND id=:task_id;")
        if (
            len(
                self._db.session.execute(
                    sql_sel, {"task_id": task_id, "user_id": user_id}
                ).fetchall()
            )
            == 0
        ):
            return False
        sql_del = text("DELETE FROM tasks WHERE user_id=:user_id AND id=:task_id;")
        self._db.session.execute(sql_del, {"task_id": task_id, "user_id": user_id})
        self._db.session.commit()
        if (
            len(
                self._db.session.execute(
                    sql_sel, {"task_id": task_id, "user_id": user_id}
                ).fetchall()
            )
            != 0
        ):
            return False
        return True

    def edit(self, task_values: dict):
        sql = text(
            """UPDATE tasks SET duration_hours=:duration_hours,
                    duration_minutes=:duration_minutes, task_date=:task_date,
                    customer_id=:customer_id, project_id=:project_id,
                    task_type_id=:task_type_id, invoiceable=:invoiceable, note=:note
                    WHERE user_id=:user_id AND id=:task_id;"""
        )
        self._db.session.execute(sql, task_values)
        self._db.session.commit()


task_repository = TaskRepository(db)
