from flask import redirect, render_template, request, session, flash
from datetime import date, datetime
from sqlalchemy import text
from app import app
from services.user_service import user_service
from services.task_service import task_service

CHOSEN_DATE = datetime.now()

@app.route("/",methods=["GET","POST"])
def index():
    global CHOSEN_DATE
    if 'user_id' not in session or not session['user_id']:
        return redirect("/login")
    if request.method == "GET":
        customers_and_projects = []
        #user_service.check_user_role_level(2)
        customers_and_projects = task_service.get_customers_and_projects()
        customers = {(cap.customer_id,cap.customer_name) for cap in customers_and_projects}
        projects = [{'project_id':cap.project_id,
                     'customer_id':cap.customer_id,
                     'project_name':cap.project_name} for cap in customers_and_projects]
        task_types = task_service.get_all_task_types()
        tasks = task_service.get_weeks_tasks(session['user_id'],CHOSEN_DATE)
        return render_template("index.html", chosen_date=CHOSEN_DATE.strftime('%Y-%m-%d'),
                               tasks=tasks,
                               projects=projects,
                               customers=customers,
                               task_types=task_types)

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
    global CHOSEN_DATE
    user_service.logout()
    CHOSEN_DATE = datetime.now()
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
            flash('New credentials created.')
            return redirect("/login")
        else:
            flash('Username is already in use.')
        return render_template("signup.html", roles=user_service.roles,
                               min_un_len=min_un_len, min_pw_len=min_pw_len)
    
@app.route("/create-task",methods=["POST"])
def create_task():
    user_service.check_csrf(request.form["csrf_token"])
    task = {'user_id':session["user_id"],'invoiceable':False}
    for val in request.form:
        if val in ['duration','task_date','customer_id','project_id', 'task_type_id','invoiceable','note']:
            if val == 'duration':
                task['duration_hours'], task['duration_minutes'] = request.form[val].split(':')
            else:
                task[val] = request.form[val]
    task_service.create_task(task)
    return redirect('/')

@app.route("/change-week",methods=["GET"])
def change_week():
    global CHOSEN_DATE
    CHOSEN_DATE = datetime.fromisoformat(request.args['chosen_date'])
    return redirect('/')