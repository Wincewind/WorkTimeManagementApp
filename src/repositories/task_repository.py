from datetime import datetime
from sqlalchemy import text
from db import db


class TaskRepository:
    def __init__(self, db_) -> None:
        self._db = db_

    def get_weeks_tasks(self, user_id: int, week_num: int, year: int):
        """Get a week's tasks for a specific user.

        Args:
            user_id (int): user_id of the owner of the task.
            week_num (int): number of the week.
            year (int): year from which the week is checked."""
        sql = text(
            """SELECT tasks.id as task_id, task_date, duration_hours,
            duration_minutes, customers.name as customer_name,
            projects.name as project_name, task_types.description as task_desc FROM tasks
            LEFT JOIN customers ON customer_id=customers.id
            LEFT JOIN projects ON project_id=projects.id
            LEFT JOIN task_types ON task_type_id=task_types.id
            WHERE user_id =:user_id AND DATE_PART('week',task_date)=:week_num
            AND DATE_PART('year',task_date)=:year GROUP BY tasks.id,
            customers.id, projects.id, task_types.id;"""
        )
        tasks = self._db.session.execute(
            sql, {"user_id": user_id, "week_num": week_num, "year": year}
        ).fetchall()
        return tasks

    def get_types(self):
        """Get available task type information from repository.

        Returns:
            sqlalchemy result object: task type ids, descriptions and hourly costs
        """
        return self._db.session.execute(
            text("SELECT id, description, hourly_cost FROM task_types;")
        )

    def create(self, task_values: dict):
        """Add a new task to repository."""
        sql = text(
            """INSERT INTO tasks (user_id, duration_hours, duration_minutes,
                   task_date, customer_id, project_id, task_type_id, invoiceable, note)
                    VALUES (:user_id, :duration_hours, :duration_minutes,
                    :task_date, :customer_id, :project_id, :task_type_id, :invoiceable, :note);"""
        )
        self._db.session.execute(sql, task_values)
        self._db.session.commit()

    def get_task(self, task_id, user_id):
        """Get a specific task's details."""
        sql = text(
            """SELECT id, task_date, duration_hours, duration_minutes, customer_id,
        project_id, task_type_id, invoiceable, note FROM tasks
        WHERE user_id =:user_id AND tasks.id=:task_id;"""
        )
        return self._db.session.execute(
            sql, {"task_id": task_id, "user_id": user_id}
        ).fetchone()

    def delete(self, task_id, user_id):
        "Remove task from repository."
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
        "Edit a task's details."
        sql = text(
            """UPDATE tasks SET duration_hours=:duration_hours,
                    duration_minutes=:duration_minutes, task_date=:task_date,
                    customer_id=:customer_id, project_id=:project_id,
                    task_type_id=:task_type_id, invoiceable=:invoiceable, note=:note
                    WHERE user_id=:user_id AND id=:task_id;"""
        )
        self._db.session.execute(sql, task_values)
        self._db.session.commit()

    def select_task_details(self, filter_values: dict):
        """Select tasks based on filtering. If no filters
        were provided, all possible tasks are selected. The query
        is built dynamically based on what filter vailues were provided."""
        select_part = """SELECT tasks.id as task_id, task_date, duration_hours,
            duration_minutes, note, customers.name as customer_name, 
            projects.name as project_name, username, task_types.description as type_desc, invoiceable
            FROM tasks LEFT JOIN customers ON customer_id=customers.id 
            LEFT JOIN projects ON project_id=projects.id LEFT JOIN users ON user_id=users.id
            LEFT JOIN task_types ON task_type_id=task_types.id"""
        groupby_part = (
            "GROUP BY tasks.id, customers.id, projects.id, users.id, task_types.id"
        )
        where_part = " "
        if len(filter_values) > 0:
            where_parts = []
            for filter_key in filter_values:
                if filter_key == "customer_id":
                    part = "customers.id =:"
                if filter_key == "project_id":
                    part = "projects.id =:"
                if filter_key == "from_date":
                    part = "task_date >=:"
                if filter_key == "to_date":
                    part = "task_date <=:"
                if filter_key == "user_id":
                    part = "users.id =:"
                where_parts.append(part + filter_key)
            where_part = f' WHERE {" AND ".join(where_parts)} '
        sql = text(select_part + where_part + groupby_part)
        tasks = self._db.session.execute(sql, filter_values).fetchall()
        return tasks


task_repository = TaskRepository(db)
