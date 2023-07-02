from datetime import datetime
import re
import csv
from io import StringIO
from flask import redirect, render_template, request, session, flash, make_response
from app import app
from services.user_service import user_service
from services.task_service import task_service
from services.customer_service import customer_service


def _get_customers_and_projects() -> set:
    """Gets customers and their related projects.

    Returns:
        set of customers and projects:  customers consists of a set
        of customer id and name tuples. projects is a list of dictionaries
        with project id, name and customer id of the project.
    """
    customers_and_projects = []
    customers_and_projects = customer_service.get_customers_and_projects()
    customers_ = {
        (cap.customer_id, cap.customer_name) for cap in customers_and_projects
    }
    projects_ = [
        {
            "project_id": cap.project_id,
            "customer_id": cap.customer_id,
            "project_name": cap.project_name,
        }
        for cap in customers_and_projects
    ]
    return customers_, projects_


@app.route("/", methods=["GET", "POST"])
def index():
    """Render home page with a week view of users tasks.
    There is also an option open a separate card that can
    be used to create a new task or edit/delete existing one.
    """
    if "user_id" not in session or not session["user_id"]:
        return redirect("/login")
    if request.method == "GET":
        customers_, projects_ = _get_customers_and_projects()
        task_types = task_service.get_all_task_types()
        tasks = task_service.get_weeks_tasks(session["user_id"])
        task_form_display = (
            "none" if session.get("chosen_task", None) is None else "block"
        )
        return render_template(
            "index.html",
            chosen_week=f'{session["chosen_week"][0]}-W{session["chosen_week"][1]}',
            tasks=tasks,
            projects=projects_,
            customers=customers_,
            task_types=task_types,
            chosen_task=session.get("chosen_task", None),
            task_form_display=task_form_display,
        )


@app.route("/login", methods=["GET", "POST"])
def login():
    """Render login page where you can either sign in
    from or navigate to a sign up -page.
    """
    if request.method == "GET":
        return render_template("login.html")
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        if user_service.login(username, password):
            return redirect("/")
        flash("Incorrect username or password.")
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Perform logout in user_service and redirect to index."""
    user_service.logout()
    return redirect("/")


@app.route("/signup", methods=["GET", "POST"])
def signup():
    """Render a signup page and handle attempts to create new credentials."""
    min_un_len = 3
    min_pw_len = 4
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        role_id = request.form["role"]
        if user_service.create_credentials(
            username, password, role_id, min_un_len, min_pw_len
        ):
            return redirect("/")
    return render_template(
        "signup.html",
        roles=user_service.roles,
        min_un_len=min_un_len,
        min_pw_len=min_pw_len,
    )


@app.route("/create-task", methods=["POST"])
def create_task():
    """Create/edit/delete a task depending if a task was
    selected, and what button was pressed when submitting
    the form on home page."""
    if "cancel_button" in request.form:
        return redirect("/deselect-task")

    user_service.check_csrf(request.form["csrf_token"])
    if "delete_button" in request.form:
        task_service.delete_task(session["chosen_task"]["id"])
        return redirect("/deselect-task")
    if "save_button" in request.form:
        if session.get("chosen_task", None) is not None:
            task_service.edit_task(request.form)
            return redirect("/deselect-task")
        task_service.create_task(request.form)
    return redirect("/")


@app.route("/change-week", methods=["GET"])
def change_week():
    """Change session's chosen_week to user selection.
    Done on home page with the weekly task view."""
    try:
        year_and_week = re.match("(\d*)-W(\d{1,2})", request.args["chosen_week"])
        session["chosen_week"] = (
            int(year_and_week.group(1)),
            int(year_and_week.group(2)),
        )
    except ValueError:
        session["chosen_week"] = (
            datetime.today().year,
            datetime.today().isocalendar()[1],
        )
    return redirect("/")


@app.route("/customers", methods=["GET", "POST"])
def customers():
    """Render page for Customer management and handle
    requests to create/edit/delete customers."""
    user_service.check_user_role_level(1)
    if request.method == "POST":
        user_service.check_csrf(request.form["csrf_token"])
        if (
            "delete_button" in request.form
            and session.get("chosen_customer", None) is not None
        ):
            customer_service.delete_customer(request.form["customer_id"])
            return redirect("/deselect-customer")

        if "save_button" in request.form:
            if session.get("chosen_customer", None) is not None:
                customer_service.edit_customer(request.form)
            else:
                customer_service.create_customer(request.form)
            return redirect("/deselect-customer")
        return redirect("/deselect-customer")

    managers = user_service.get_users(1)
    customers_, _ = _get_customers_and_projects()
    return render_template(
        "customers.html",
        managers=managers,
        customers=customers_,
        chosen_customer=session.get("chosen_customer", None),
    )


@app.route("/select-customer")
def select_customer():
    """Set session's chosen_customer so that it
    can be edited or deleted on Customer Management page."""
    user_service.check_user_role_level(1)
    session["chosen_customer"] = customer_service.get_customer_details(
        request.args["customer_id"]
    )._asdict()
    return redirect("/customers")


@app.route("/deselect-customer")
def deselect_customer():
    """Undo session's chosen_customer selection."""
    if session.get("chosen_customer", None) is not None:
        del session["chosen_customer"]
    return redirect("/customers")


@app.route("/select-task")
def select_task():
    """Set session's chosen_task so that it
    can be edited or deleted on Home page."""
    task_service.get_task(request.args.get("task_id"))
    return redirect("/")


@app.route("/deselect-task")
def deselect_task():
    """Undo session's chosen_task selection."""
    if session.get("chosen_task", None) is not None:
        del session["chosen_task"]
    return redirect("/")


@app.route("/projects", methods=["GET", "POST"])
def projects():
    """Render page for Project management and handle
    requests to create/edit/delete projects."""
    user_service.check_user_role_level(1)
    if request.method == "POST":
        user_service.check_csrf(request.form["csrf_token"])
        if (
            "delete_button" in request.form
            and session.get("chosen_project", None) is not None
        ):
            customer_service.delete_project(request.form["project_id"])
            return redirect("/deselect-project")

        if "save_button" in request.form:
            if session.get("chosen_project", None) is not None:
                customer_service.edit_project(request.form)
            else:
                customer_service.create_project(request.form)
            return redirect("/deselect-project")
        return redirect("/deselect-project")

    customers_, projects_ = _get_customers_and_projects()
    return render_template(
        "projects.html",
        customers=customers_,
        projects=projects_,
        chosen_customer=session.get("chosen_customer", None),
        chosen_project=session.get("chosen_project", None),
    )


@app.route("/select-project")
def select_project():
    """Set session's chosen_project so that it
    can be edited or deleted on Project Management page."""
    user_service.check_user_role_level(1)
    if "selected_project" in request.args:
        session["chosen_project"] = customer_service.get_project_details(
            request.args["selected_project"]
        )._asdict()
    return redirect("/projects")


@app.route("/deselect-project")
def deselect_project():
    """Undo session's chosen_project selection."""
    if session.get("chosen_project", None) is not None:
        del session["chosen_project"]
    return redirect("/projects")


@app.route("/queries")
def queries():
    """Render page for displaying saved tasks in table format and filtering/searching for them from specific customers, projects or date period."""
    customers_, projects_ = _get_customers_and_projects()
    if "select_button" not in request.args:
        tasks = task_service.query_task_details()
    else:
        tasks = task_service.query_task_details(request.args)
    return render_template(
        "query_page.html", tasks=tasks, customers=customers_, projects=projects_
    )


@app.route("/export")
def export():
    """Export the selected tasks on task query page to a csv file.

    Returns:
        A response that redirects back to queries and a tasks.csv attachment.
    """
    si = StringIO()
    cw = csv.writer(si, delimiter=";")
    cw.writerow(
        [
            "Customer",
            "Project",
            "Submitted by",
            "Task date",
            "Duration hours",
            "Duration minutes",
            "Task type",
            "Task note",
            "Invoiceable",
        ]
    )
    cw.writerows(
        [
            (
                task["customer_name"],
                task["project_name"],
                task["username"],
                task["task_date"],
                task["duration_hours"],
                task["duration_minutes"],
                task["type_desc"],
                task["note"],
                task["invoiceable"],
            )
            for task in session["selected_tasks"]
        ]
    )
    response = make_response(si.getvalue())
    response.headers["Content-Disposition"] = "attachment; filename=tasks.csv"
    response.headers["Content-type"] = "text/csv"
    response.location = "/queries"
    return response
