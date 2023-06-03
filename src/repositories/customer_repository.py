from db import db
from sqlalchemy import text

class CustomerRepository:
    def __init__(self, db) -> None:
        self._db = db

    def get_customers_and_projects(self):
        sql = text("SELECT customers.id as customer_id, customers.name as customer_name, " \
                   "projects.id as project_id, projects.name as project_name FROM customers " \
                   "LEFT JOIN projects ON customer_id=customers.id " \
                   "WHERE customers.visible = TRUE AND COALESCE(projects.visible,'TRUE') <> 'FALSE' " \
                    "GROUP BY customers.id, projects.id;")
        return self._db.session.execute(sql).fetchall()
    
    def create(self, customer_values: dict):
        sql = text("INSERT INTO customers (name, manager_id) VALUES (:customer_name, :manager_id);")
        self._db.session.execute(sql, customer_values)
        self._db.session.commit()

    def delete(self, customer_id: int):
        try:
            sql = text("UPDATE customers SET visible = False WHERE id = :customer_id;")
            self._db.session.execute(sql, {'customer_id':customer_id})
            sql = text("UPDATE projects SET visible = False WHERE customer_id = :customer_id;")
            self._db.session.execute(sql, {'customer_id':customer_id})
            self._db.session.commit()
        except Exception as ex:
            print('Failed to remove customer entry: ',str(ex))

    def edit(self, customer_values):
        sql = text("UPDATE customers SET name=:customer_name, manager_id=:manager_id WHERE id=:customer_id;")
        self._db.session.execute(sql, customer_values)
        self._db.session.commit()

    def get_customer(self, customer_id: int):
        try:
            sql = text("SELECT customers.id as customer_id, customers.name as customer_name, " \
                       "users.id as user_id, username FROM customers LEFT JOIN " \
                        "users ON users.id = manager_id " \
                        "WHERE customers.id = :customer_id " \
                        "GROUP BY customers.id, users.id;")
            return self._db.session.execute(sql, {'customer_id':customer_id}).fetchone()
        except Exception as ex:
            print('Failed to get specific customer details: ',str(ex))

customer_repository = CustomerRepository(db)