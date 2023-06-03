from flask import session
from repositories.customer_repository import customer_repository

class CustomerService:
    def __init__(self) -> None:
        self.repository = customer_repository
        self._roles = None

    def get_customers_and_projects(self):
        return self.repository.get_customers_and_projects()
    
    def create_customer(self,customer):
        self.repository.create(customer)

    def delete_customer(self,customer_id):
        self.repository.delete(customer_id)

    def edit_customer(self,customer):
        self.repository.edit(customer)

    def get_customer_details(self,customer_id):
        return self.repository.get_customer(customer_id)


customer_service = CustomerService()