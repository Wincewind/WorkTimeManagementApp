from flask import redirect, render_template, request, session, flash
from sqlalchemy import text
from app import app
from services.user_service import user_service

@app.route("/")
def index():
    if 'user_id' not in session or not session['user_id']:
        return redirect("/login")
    return render_template("index.html")

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
        role_id = request.form["roles"]
        if len(username) < min_un_len or len(password) < min_pw_len:
            flash(f'Username needs to be atleast {min_un_len} characters long' \
                  'and password {min_pw_len} characters.')
        elif user_service.create_credentials(username,password,role_id):
            flash('New credentials created.')
            return redirect("/login")
        else:
            flash('Username is already in use.')
        return render_template("signup.html", roles=user_service.roles,
                               min_un_len=min_un_len, min_pw_len=min_pw_len)
    