from flask import session
from repositories.customer_repository import customer_repository


class CustomerService:
    """Service for handling interaction with the customers and projects repositories."""

    def __init__(self) -> None:
        self.repository = customer_repository
        self._roles = None

    def _prepare_project_input(self, form_data):
        project = {"use_cost_limit": False, "use_hour_limit": False}
        for val in form_data:
            if val in [
                "project_customer",
                "project_name",
                "hour_limit",
                "cost_limit",
                "use_hour_limit",
                "use_cost_limit",
            ]:
                if val in ["hour_limit", "cost_limit"]:
                    try:
                        limit_val = int(float(form_data[val]))
                        if limit_val < 0:
                            raise ValueError
                        project[val] = limit_val
                    except ValueError:
                        project[val] = 0
                else:
                    project[val] = form_data[val]
        if session.get("chosen_project", None) is not None:
            project["project_id"] = form_data["project_id"]
        return project

    def _prepare_customer_input(self, form_data):
        customer = {}
        for val in form_data:
            if val in ["customer_name", "manager_id"]:
                customer[val] = form_data[val]
        if session.get("chosen_customer", None) is not None:
            customer["customer_id"] = form_data["customer_id"]
        return customer

    def get_customers_and_projects(self):
        """Get visible customers and related projects from repository."""
        return self.repository.get_visible_customers_and_projects()

    def create_customer(self, form_data):
        customer = self._prepare_customer_input(form_data)
        self.repository.create(customer)

    def delete_customer(self, customer_id):
        self.repository.delete(customer_id)

    def edit_customer(self, form_data):
        customer = self._prepare_customer_input(form_data)
        self.repository.edit(customer)

    def get_customer_details(self, customer_id):
        return self.repository.get_customer(customer_id)

    def get_project_details(self, project_id):
        return self.repository.get_project(project_id)

    def create_project(self, form_data):
        project = self._prepare_project_input(form_data)
        self.repository.create_project(project)

    def delete_project(self, project_id):
        self.repository.delete_project(project_id)

    def edit_project(self, form_data):
        project = self._prepare_project_input(form_data)
        self.repository.edit_project(project)


customer_service = CustomerService()
