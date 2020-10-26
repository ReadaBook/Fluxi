import os
import re
from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session, url_for, jsonify
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions
from werkzeug.security import check_password_hash, generate_password_hash
import urllib.parse

from flask import redirect, render_template, request, session
from functools import wraps


def apology(message, code=400):
    """Render message as an apology to user."""
    def escape(s):
        """
        Escape special characters.
        """
        for old, new in [("-", "--"), ("_", "__"), ("?", "~q"),
                         ("%", "~p"), ("#", "~h"), ("\"", "''")]:
            s = s.replace(old, new)
        return s
    return render_template("apology.html", top=code, bottom=escape(message)), code


def login_required(f):
    """
    Decorate routes to require login.
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///project.db")


@app.route("/")
def index():
    return redirect(url_for("user"))


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = :username",
                          username=request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect(url_for("user"))

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
@login_required
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect(url_for("index"))


@app.route("/register", methods=["POST"])
def register():
    """Register user"""

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        # Ensure name was submitted
        if not request.form.get("name"):
            return apology("must provide name", 400)

        # Ensure surname was submitted
        elif not request.form.get("surname"):
            return apology("must provide surname", 400)

        # Ensure username was submitted
        elif not request.form.get("username"):
            return apology("must provide username", 400)

        # Ensure username has at least six characters
        elif len(request.form.get("username")) < 6:
            return apology("username must be longer than six (6) characters", 400)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 400)

        # Ensure password has at least eight characters
        elif len(request.form.get("password")) < 8:
            return apology("password must be longer than eight (8) characters", 400)

       # hash the password and insert a new user in the database
        hash = generate_password_hash(request.form.get("password"))
        new_user_id = db.execute("INSERT INTO users (name, surname, username, hash) VALUES(:name, :surname, :username, :hash)",
                                 name=request.form.get("name"),
                                 surname=request.form.get("surname"),
                                 username=request.form.get("username"),
                                 hash=hash)

        # unique username constraint violated?
        if not new_user_id:
            return apology("username taken", 400)

        # Remember which user has logged in
        session["user_id"] = new_user_id

        # Display a flash message
        flash("Registered!")

        # Redirect user to home page
        return redirect(url_for("user"))


@app.route("/check", methods=["GET"])
def check():
    """Check if username is available"""

    username = request.args.get("username")
    users = db.execute("SELECT username FROM 'users' WHERE username=:username;", username=username)
    if users and username:
        return jsonify(False)
    elif not users and username:
        return jsonify(True)
    else:
        return jsonify(False)


@app.route("/user")
@login_required
def user():
    users = db.execute("SELECT * FROM users WHERE id = :user_id", user_id=session["user_id"])
    boards = db.execute("SELECT * FROM boards WHERE user_id = :user_id", user_id=session["user_id"])
    user = users[0]
    return render_template("user.html", user=user, boards=boards)


@app.route("/board/new", methods=["POST"])
@login_required
def board_new():
    """Add board"""

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        # Ensure title was submitted
        if not request.form.get("name"):
            return apology("must provide title", 400)

        db.execute("INSERT INTO boards (name, user_id) VALUES(:name, :user_id)",
                   name=request.form.get("name"), user_id=session["user_id"])

        # Display a flash message
        flash("Board Added!")

        # Redirect user to home page
        return redirect(url_for("user"))


@app.route("/board/<idx>", methods=["GET"])
@login_required
def board(idx):
    """View Board Page"""
    users = db.execute("SELECT * FROM users WHERE id = :user_id", user_id=session["user_id"])
    boards = db.execute("SELECT * FROM boards WHERE id = :board_id", board_id=int(idx))
    todos = db.execute("SELECT * FROM tasks WHERE board_id = :board_id AND status = 'todo'", board_id=int(idx))
    doings = db.execute("SELECT * FROM tasks WHERE board_id = :board_id AND status = 'doing'", board_id=int(idx))
    dones = db.execute("SELECT * FROM tasks WHERE board_id = :board_id AND status = 'done'", board_id=int(idx))
    comments = db.execute("SELECT * FROM comments WHERE board_id = :board_id", board_id=int(idx))
    user = users[0]
    board = boards[0]
    return render_template("board.html", user=user, board=board, todos=todos, doings=doings, dones=dones, comments=comments)


@app.route("/board/<idx>/new", methods=["POST"])
@login_required
def task_new(idx):
    """Add task"""

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        # Ensure title was submitted
        if not request.form.get("name"):
            return apology("must provide task", 400)
        db.execute("INSERT INTO tasks (name, board_id) VALUES(:name, :board_id)",
                   name=request.form.get("name"),
                   board_id=int(idx))

        # Display a flash message
        flash("Task Added!")

        # Redirect user to home page
        return redirect("/board/" + idx)


@app.route("/board/<idx>/comment/<task_idx>", methods=["POST"])
@login_required
def comment_new(idx, task_idx):
    """Add comment"""

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        # Ensure title was submitted
        if not request.form.get("text"):
            return apology("must provide text", 400)
        db.execute("INSERT INTO comments (task_id, text, board_id) VALUES(:task_id, :text, :board_id)",
                   task_id=int(task_idx), text=request.form.get("text"), board_id=int(idx))

        # Display a flash message
        flash("Comment Added!")

        # Redirect user to home page
        return redirect("/board/" + idx)


@app.route("/board/update/<idx>", methods=["POST"])
@login_required
def board_edit(idx):
    """Edit board"""
    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        # Ensure title was submitted
        if not request.form.get("name"):
            return apology("must provide name", 400)
        db.execute("UPDATE boards SET name = :name WHERE id = :idx;", name=request.form.get("name"), idx=int(idx))

        # Display a flash message
        flash("Board Updated!")

        # Redirect user to home page
        return redirect("/user")


@app.route("/board/<idx>/delete")
@login_required
def board_delete(idx):
    boards = db.execute("SELECT user_id, id FROM boards WHERE user_id = :user_id AND id = :board_id",
                        user_id=session["user_id"], board_id=idx)
    user_id = session["user_id"]
    if user_id != boards[0]["user_id"]:
        return redirect(url_for("user"))
    else:
        db.execute("DELETE FROM boards WHERE user_id = :user_id AND id = :board_id", user_id=session["user_id"], board_id=idx)
        db.execute("DELETE FROM tasks WHERE board_id = :board_id", board_id=idx)
        db.execute("DELETE FROM comments WHERE board_id = :board_id", board_id=idx)
        # Display a flash message
        flash("Board Deleted!")
        return redirect(url_for("user"))


@app.route("/board/<idx>/task/<task_idx>/delete")
@login_required
def task_delete(idx, task_idx):
    db.execute("DELETE FROM tasks WHERE id = :task_idx", task_idx=task_idx)
    db.execute("DELETE FROM comments WHERE task_id = :task_id", task_id=task_idx)
    flash("Task Deleted!")
    return redirect("/board/" + idx)


@app.route("/delete/comment", methods=["POST"])
@login_required
def comment_delete():
    idx = request.form.get('idx')
    db.execute("DELETE FROM comments WHERE id = :idx", idx=int(idx))
    flash("Comment Deleted!")
    return (jsonify(idx))


@app.route("/update/tasks/<idx>", methods=["POST"])
@login_required
def tasks_edit(idx):
    """Edit tasks"""
    status = request.form.get('new_status')
    print(status)
    tasks = db.execute("SELECT * FROM tasks WHERE id = :idx", idx=int(idx))
    task = tasks[0]
    print(task['id'])
    db.execute("UPDATE tasks SET status = :status WHERE id = :idx;",
               status=status,
               idx=task['id'])
    return(jsonify(task))


@app.route("/update/name/<idx>", methods=["POST"])
@login_required
def name_edit(idx):
    """Edit name"""
    name = request.form.get('name')
    print(name)
    tasks = db.execute("SELECT * FROM tasks WHERE id = :idx", idx=int(idx))
    task = tasks[0]
    print(task['id'])
    db.execute("UPDATE tasks SET name = :name WHERE id = :idx;",
               name=name,
               idx=task['id'])
    return(jsonify(task))


@app.route("/update/desc/<idx>", methods=["POST"])
@login_required
def desc_edit(idx):
    """Edit desc"""
    desc = request.form.get('desc')
    print(desc)
    tasks = db.execute("SELECT * FROM tasks WHERE id = :idx", idx=int(idx))
    task = tasks[0]
    print(task['id'])
    db.execute("UPDATE tasks SET description = :desc WHERE id = :idx;",
               desc=desc,
               idx=task['id'])
    return(jsonify(task))


@app.route("/update/due/<idx>", methods=["POST"])
@login_required
def due_edit(idx):
    """Edit due"""
    due = request.form.get('due')
    print(due)
    tasks = db.execute("SELECT * FROM tasks WHERE id = :idx", idx=int(idx))
    task = tasks[0]
    print(task['id'])
    db.execute("UPDATE tasks SET due = :due WHERE id = :idx;",
               due=due,
               idx=task['id'])
    return (jsonify(task))


@app.route("/update/comment/<idx>", methods=["POST"])
@login_required
def comment_edit(idx):
    """Edit comment"""
    text = request.form.get('text')
    print(text)
    comments = db.execute("SELECT * FROM comments WHERE id = :idx", idx=int(idx))
    comment = comments[0]
    print(comment['id'])
    db.execute("UPDATE comments SET text = :text WHERE id = :idx;",
               text=text,
               idx=comment['id'])
    return(jsonify(comment))


def errorhandler(e):
    """Handle error"""
    return apology(e.name, e.code)


# listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)

port = int(os.environ.get("PORT", 5000))
app.run(debug=True, host='0.0.0.0', port=port)