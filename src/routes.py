from flask import redirect, render_template, request, session, flash
from datetime import datetime
from app import app
from services.user_service import user_service
from services.task_service import task_service
from services.customer_service import customer_service

@app.route("/",methods=["GET","POST"])
def index():
    if 'user_id' not in session or not session['user_id']:
        return redirect("/login")
    if request.method == "GET":
        customers_and_projects = []
        #user_service.check_user_role_level(2)
        customers_and_projects = customer_service.get_customers_and_projects()
        customers = {(cap.customer_id,cap.customer_name) for cap in customers_and_projects}
        projects = [{'project_id':cap.project_id,
                     'customer_id':cap.customer_id,
                     'project_name':cap.project_name} for cap in customers_and_projects]
        task_types = task_service.get_all_task_types()
        tasks = task_service.get_weeks_tasks(session['user_id'],session["chosen_date"])
        task_form_display = 'none' if session.get("chosen_task", None) is None else 'block'
        return render_template("index.html", chosen_date=session["chosen_date"].strftime('%Y-%m-%d'),
                               tasks=tasks,
                               projects=projects,
                               customers=customers,
                               task_types=task_types,
                               chosen_task=session.get("chosen_task", None),
                               task_form_display=task_form_display)

@app.route("/login",methods=["GET","POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        if user_service.login(username,password):
            return redirect("/")
        flash('Incorrect username or password.')
        return render_template("login.html")
    
@app.route("/logout")
def logout():
    user_service.logout()
    return redirect('/')

@app.route("/signup",methods=["GET","POST"])
def signup():
    min_un_len = 3
    min_pw_len = 4
    if request.method == "GET":
        return render_template("signup.html", roles=user_service.roles,
                               min_un_len=min_un_len, min_pw_len=min_pw_len)
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        role_id = request.form["role"]
        print('got so far')
        if len(username) < min_un_len or len(password) < min_pw_len:
            flash(f'Username needs to be atleast {min_un_len} characters long' \
                  f'and password {min_pw_len} characters.')
        elif user_service.create_credentials(username,password,role_id):
            user_service.login(username, password)
            flash('New credentials created.')
            return redirect("/")
        else:
            flash('Username is already in use.')
        return render_template("signup.html", roles=user_service.roles,
                               min_un_len=min_un_len, min_pw_len=min_pw_len)
    
@app.route("/create-task",methods=["POST"])
def create_task():
    if 'cancel_button' in request.form:
        return redirect('/deselect-task')
    user_service.check_csrf(request.form["csrf_token"])
    if 'delete_button' in request.form:
        task_service.delete_task(session['chosen_task']['id'])
        return redirect('/deselect-task')

    if 'save_button' in request.form:
        task = {'user_id':session["user_id"],'invoiceable':False}
        for val in request.form:
            if val in ['duration','task_date','customer_id','project_id',
                    'task_type_id','invoiceable','note']:
                if val == 'duration':
                    task['duration_hours'], task['duration_minutes'] = request.form[val].split(':')
                else:
                    task[val] = request.form[val]

        if session.get("chosen_task", None) is not None:
            task['task_id'] = session['chosen_task']['id']
            task_service.edit_task(task)
            return redirect('/deselect-task')
        task_service.create_task(task)
        return redirect('/')

@app.route("/change-week",methods=["GET"])
def change_week():
    try:
        session["chosen_date"] = datetime.fromisoformat(request.args['chosen_date'])
    except AttributeError:
        session["chosen_date"] = datetime.today()
    return redirect('/')

@app.route("/customers",methods=["GET","POST"])
def customers():
    user_service.check_user_role_level(1)
    managers = user_service.get_users(1)
    customers_and_projects = customer_service.get_customers_and_projects()
    customers_ = {(cap.customer_id,cap.customer_name) for cap in customers_and_projects}

    if request.method == "POST":
        user_service.check_csrf(request.form["csrf_token"])
        if 'delete_button' in request.form and session.get("chosen_customer", None) is not None:
            customer_service.delete_customer(request.form["customer_id"])
            return redirect("/deselect-customer")

        if 'save_button' in request.form:
            customer = {}
            for val in request.form:
                if val in ['customer_name','manager_id']:
                    customer[val] = request.form[val]
            if session.get("chosen_customer", None) is not None:
                customer['customer_id'] = request.form['customer_id']
                customer_service.edit_customer(customer)
            else:
                customer_service.create_customer(customer)
            return redirect("/deselect-customer")
        return redirect('/deselect-customer')

    return render_template('customers.html', managers=managers,
                           customers_=customers,
                           chosen_customer=session.get("chosen_customer", None))

@app.route("/select-customer",methods=["POST"])
def select_customer():
    user_service.check_user_role_level(1)
    session["chosen_customer"] = customer_service.get_customer_details(
        request.form["customer_id"])._asdict()
    return redirect("/customers")

@app.route("/deselect-customer")
def deselect_customer():
    if session.get("chosen_customer", None) is not None:
        del session["chosen_customer"]
    return redirect('/customers')

@app.route("/select-task")
def select_task():
    task_service.get_task(
        request.args.get("task_id"))
    return redirect('/')

@app.route("/deselect-task")
def deselect_task():
    if session.get("chosen_task", None) is not None:
        del session["chosen_task"]
    return redirect('/')
