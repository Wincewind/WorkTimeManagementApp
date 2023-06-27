from sqlalchemy import text
from db import db


class CustomerRepository:
    def __init__(self, db_) -> None:
        self._db = db_

    def get_customers_and_projects(self):
        sql = text(
            """SELECT customers.id as customer_id, customers.name as customer_name,
            projects.id as project_id, projects.name as project_name FROM customers
            LEFT JOIN projects ON customer_id=customers.id
            WHERE customers.visible = TRUE AND
            (projects.visible = TRUE OR projects.id IS NULL)
            GROUP BY customers.id, projects.id;"""
        )
        return self._db.session.execute(sql).fetchall()

    def create(self, customer_values: dict):
        sql = text(
            "INSERT INTO customers (name, manager_id) VALUES (:customer_name, :manager_id);"
        )
        self._db.session.execute(sql, customer_values)
        self._db.session.commit()

    def delete(self, customer_id: int):
        try:
            sql = text("UPDATE customers SET visible = False WHERE id = :customer_id;")
            self._db.session.execute(sql, {"customer_id": customer_id})
            sql = text(
                "UPDATE projects SET visible = False WHERE customer_id = :customer_id;"
            )
            self._db.session.execute(sql, {"customer_id": customer_id})
            self._db.session.commit()
        except Exception as ex:
            print("Failed to remove customer entry: ", str(ex))

    def edit(self, customer_values):
        sql = text(
            """UPDATE customers SET name=:customer_name,
            manager_id=:manager_id WHERE id=:customer_id;"""
        )
        self._db.session.execute(sql, customer_values)
        self._db.session.commit()

    def get_customer(self, customer_id: int):
        try:
            sql = text(
                """SELECT customers.id as customer_id, customers.name as customer_name,
                        users.id as user_id, username FROM customers LEFT JOIN
                        users ON users.id = manager_id
                        WHERE customers.id = :customer_id
                        GROUP BY customers.id, users.id;"""
            )
            return self._db.session.execute(
                sql, {"customer_id": customer_id}
            ).fetchone()
        except Exception as ex:
            print("Failed to get specific customer details: ", str(ex))

    def get_project(self, project_id: int):
        try:
            sql = text(
                """SELECT id, customer_id, name, cost_limit, hour_limit,
                        use_cost_limit, use_hour_limit FROM projects
                        WHERE id = :project_id AND visible = TRUE;"""
            )
            return self._db.session.execute(sql, {"project_id": project_id}).fetchone()
        except Exception as ex:
            print("Failed to get specific project details: ", str(ex))

    def create_project(self, project_values: dict):
        sql = text(
            """INSERT INTO projects (name, customer_id, hour_limit, cost_limit,
                    use_hour_limit, use_cost_limit) VALUES (:project_name, :project_customer,
                    :hour_limit, :cost_limit, :use_hour_limit, :use_cost_limit);"""
        )
        self._db.session.execute(sql, project_values)
        self._db.session.commit()

    def edit_project(self, project_values):
        sql = text(
            """UPDATE projects SET name=:project_name, hour_limit=:hour_limit,
            cost_limit=:cost_limit, use_hour_limit=:use_hour_limit,
            use_cost_limit=:use_cost_limit WHERE id=:project_id
            AND customer_id=:project_customer;"""
        )
        self._db.session.execute(sql, project_values)
        self._db.session.commit()

    def delete_project(self, project_id: int):
        try:
            sql = text("UPDATE projects SET visible = False WHERE id = :project_id;")
            self._db.session.execute(sql, {"project_id": project_id})
            self._db.session.commit()
        except Exception as ex:
            print("Failed to remove project entry: ", str(ex))


customer_repository = CustomerRepository(db)
