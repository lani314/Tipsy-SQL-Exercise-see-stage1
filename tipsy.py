"""
tipsy.py -- A flask-based todo list
"""
from flask import Flask, render_template, redirect, request, session, g
import model

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html", user_name="chriszf")

@app.route("/save_task", methods=["POST"])
def save_task():
    # db = model.connect_db()
    title = request.form['title']
    model.new_task(db, title)
    return redirect("/tasks")

@app.route("/tasks")
def list_tasks():
    # db = model.connect_db()
    tasks_from_db = model.get_tasks(db, None)
    return render_template("list_tasks.html", tasks=tasks_from_db)

@app.route("/task/<int:id>", methods=["GET"])
def view_task(id):
    # db = model.connect_db()
    task_from_db = model.get_task(g.db, id)
    return render_template("view_task.html", task=task_from_db)

@app.route('/login')
def login():
    return render_template("login.html")

@app.route('/logout')
def logout():
    # remove the username from the session if it's there
    session.pop('username', None)
    return redirect(url_for('index'))

# set the secret key.  keep this really secret:
app.secret_key = 'askmeaboutpython'

@app.route("/authenticate", methods=["POST"])
def authenticate():
    email = request.form['email']
    password = request.form['password']
    user_id = model.authenticate(g.db, email, password)
    session['user_id'] = user_id
    return redirect("/")

@app.route("/task/<int:id>", methods=["POST"])
def complete_task(id):
    # db = model.connect_db()
    model.complete_task(db, id)
    return redirect("/tasks")

@app.before_request
def set_up_db():
    g.db = model.connect_db()

@app.teardown_request
def disconnect_db(e): #waht is the variable e from?
    g.db.close()

@app.route("/set_date") #set date for start of session
def set_date():
    session['date'] = datetime.datetime.now()
    return "Date set"

@app.route("/get_date") #return date of session start
def get_date():
    return str(session['date'])

if __name__ == "__main__":
    app.run(debug=True)
