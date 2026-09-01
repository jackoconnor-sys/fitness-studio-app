# to sign in as an admin, you can go to the regular login route
# here it will prompt to login as an admin, click that and you can register as an admin
# to register, and then eventually login as an admin, you need the special admin code which is: 123
# this will then bring you the admin home, where you can add workouts, see the users who have registered, and also see who has signed up for the free trial 


import os
from flask import Flask, render_template, request, session, redirect, url_for, g
from forms import RegistrationForm, LoginForm, AdminRegistrationForm, AdminLoginForm, ClassForm, SignupOtherUserClassForm, FreeTrialForm
from database import get_db, close_db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_session import Session
from functools import wraps


app = Flask(__name__)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)
app.teardown_appcontext(close_db)
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "this_is_my_secret_key")

# Shared code required to register or log in as an admin
ADMIN_SPECIAL_CODE = os.environ.get("ADMIN_SPECIAL_CODE", "bloodsweatandtears")


@app.before_request
def load_logged_in_user():
    g.user = session.get("user_id", None)

def login_required(view):
    @wraps(view)
    def wrapped_view(*args, **kwargs):
        if g.user is None:
            return redirect(url_for("login", next=request.url))
        return(view(*args, **kwargs))
    return wrapped_view


def admin_required(view):
    @wraps(view)
    def wrapped_view(*args, **kwargs):
        if 'admin_id' not in session:
            return redirect(url_for('admin_login', next=request.url)) 
        
        return view(*args, **kwargs)  
    return wrapped_view


@app.route("/register", methods=["GET", "POST"])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user_id = form.user_id.data
        password = form.password.data
        db = get_db()
        clash = db.execute("""SELECT * FROM users WHERE user_id = ?;""", (user_id,)).fetchone()
        
        if clash is not None:
            form.user_id.errors.append("User ID already taken")
        else:
            db.execute("""INSERT INTO users (user_id, password) VALUES (?, ?);""", 
                       (user_id, generate_password_hash(password)))
            db.commit()
        
            return redirect(url_for("login")) 
    return render_template("register.html", form=form)


@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user_id = form.user_id.data
        password = form.password.data
        db = get_db()

        user_in_db = db.execute("""SELECT * FROM users WHERE user_id = ?;""", (user_id,)).fetchone()
        
        if user_in_db is None:
            form.user_id.errors.append("No such user name!")

        elif not check_password_hash(user_in_db["password"], password): form.password.errors.append("Incorrect password!")
        else:
            session.clear()
            session["user_id"] = user_id
            session.modified = True 
            next_page = request.args.get("next")
            if not next_page:
                next_page = url_for("index")
            
            return redirect(next_page) 
    return render_template("login.html", form=form)

@app.route("/logout")
def logout():
    session.clear()
    session.modified = True
    return redirect(url_for("index"))


@app.route("/")
def index():
    return render_template("index.html")

@app.route("/classes")
@login_required 
def classes():
  db = get_db()
  classes = db.execute("""SELECT * FROM classes;""").fetchall()
  return render_template("classes.html", classes=classes)

@app.route("/add_to_sign_ups/<int:class_id>")
def add_to_sign_ups(class_id):
    if "your_sign_ups" not in session:
        session["your_sign_ups"] = {} 

    if class_id not in session["your_sign_ups"]:
        session["your_sign_ups"][class_id] = 1 
    else: 
        session["your_sign_ups"][class_id] += 1 

    session.modified = True  
    print("Updated sign-ups:", session["your_sign_ups"]) 

    return redirect(url_for("your_sign_ups"))


@app.route("/your_sign_ups")
def your_sign_ups():
    if "your_sign_ups" not in session:
        session["your_sign_ups"] = {}
        session.modified = True

    class_details = {}  
    db = get_db()

    for class_id in session["your_sign_ups"]:
        class_info = db.execute(
            """SELECT * FROM classes WHERE class_id = ?;""", (class_id,)
        ).fetchone()

        if class_info:
            class_details[class_id] = {
                "name": class_info["name"],
                "day": class_info["day"],
                "time": class_info["time"],
                "signups": session["your_sign_ups"][class_id],
            }

    return render_template(
        "your_sign_ups.html",
        class_details=class_details
    )


@app.route("/admin_register", methods=["GET", "POST"])
def admin_register():
    form = AdminRegistrationForm()
    message = ""
    
    if form.validate_on_submit():
        admin_id = form.admin_id.data
        password = form.password.data
        special_admin_code = form.special_admin_code.data
        
        
        expected_code = ADMIN_SPECIAL_CODE
        
        if special_admin_code != expected_code:     
            form.special_admin_code.errors.append("Invalid special code.")
        else:
            db = get_db()
            clash = db.execute("""SELECT * FROM admins WHERE admin_id = ?;""", (admin_id,)).fetchone()
            if clash:
                form.admin_id.errors.append("Username already taken.")
            else:
                db.execute("""INSERT INTO admins (admin_id, password) VALUES (?, ?);""", 
                           (admin_id, generate_password_hash(password)))
                db.commit()
                message = "Admin account successfully created!"

                return redirect(url_for("admin_login"))
    
    return render_template("admin_register.html", form=form, message=message)

@app.route("/admin_login", methods=["GET", "POST"])
def admin_login():
    form = AdminLoginForm()  
    
    if form.validate_on_submit():
        admin_id = form.admin_id.data
        password = form.password.data
        special_admin_code = form.special_admin_code.data 
        db = get_db()

        
        admin_in_db = db.execute("""SELECT * FROM admins WHERE admin_id = ?;""", (admin_id,)).fetchone()
        
        
        if admin_in_db is None:
            form.admin_id.errors.append("No such admin username!")
        
        elif not check_password_hash(admin_in_db["password"], password):
            form.password.errors.append("Incorrect password!")
        
        elif special_admin_code != ADMIN_SPECIAL_CODE:
            form.special_admin_code.errors.append("Incorrect special code!")
        
        else:
            
            session.clear()
            session["admin_id"] = admin_id
            session.modified = True
            next_page = request.args.get("next")
            if not next_page:
                next_page = url_for("admin_home")  
            
            return redirect(next_page)
    
    return render_template("admin_login.html", form=form)



@app.route('/admin_logout')
def admin_logout():
    session.clear()
    return redirect(url_for('admin_login'))


@app.route("/admin_home")
@admin_required 
def admin_home():
    db = get_db()
    classes = db.execute("SELECT * FROM classes;").fetchall()
    
    free_trials = db.execute("SELECT * FROM free_trial_signups").fetchall()

    
    users = db.execute("SELECT * FROM users").fetchall()

    return render_template("admin_home.html", free_trials=free_trials, users=users, classes=classes)

@app.route("/add_class", methods=["GET", "POST"])
@admin_required  
def add_class():
    form = ClassForm() 
    if form.validate_on_submit():
        
        name = form.name.data
        day = form.day.data
        time = form.time.data
        duration = form.duration.data
        trainer = form.trainer.data
        description = form.description.data
        
        db = get_db()
        db.execute("""INSERT INTO classes (name, day, time, duration, trainer, description) VALUES (?, ?, ?, ?, ?, ?);""",
                   (name, day, time, duration, trainer, description))
        db.commit()

        return redirect(url_for("admin_home"))  
    
    return render_template("add_class.html", form=form)


@app.route("/signup_class", methods=["GET", "POST"])
@login_required
def signup_class():
    form = SignupOtherUserClassForm()
    db = get_db()
    message = ""

   
    classes = db.execute("SELECT name, day, time FROM classes").fetchall()

    if form.validate_on_submit():
        user_id = form.user_id.data
        class_name = form.class_name.data

        
        class_info = db.execute("SELECT class_id FROM classes WHERE name = ?", (class_name,)).fetchone()

        if class_info is None:
            form.class_name.errors.append("Class not found.")
        else:
            class_id = class_info["class_id"]

            
            existing_signup = db.execute(
                "SELECT * FROM class_signups WHERE user_id = ? AND class_id = ?", 
                (user_id, class_id)
            ).fetchone()

            if existing_signup:
                form.user_id.errors.append("User is already signed up for this class.")
            else:
                db.execute("INSERT INTO class_signups (user_id, class_id) VALUES (?, ?)", (user_id, class_id))
                db.commit()

                
                message = "User successfully signed up for the class!"

                return render_template("signup_class.html", form=form, classes=classes, message=message)

    return render_template("signup_class.html", form=form, classes=classes, message=message)


@app.route("/free_trial", methods=["GET", "POST"])
def free_trial():
    form = FreeTrialForm()
    db = get_db()
    message = ""

    
    classes = db.execute("SELECT name, day, time, duration, trainer, description FROM classes").fetchall()

    if form.validate_on_submit():
        name = form.name.data
        email = form.email.data
        phone = form.phone.data
        preferred_class = form.preferred_class.data

        
        class_info = db.execute("SELECT class_id FROM classes WHERE name = ?", (preferred_class,)).fetchone()

        if class_info is None:
            form.preferred_class.errors.append("Class not found.")
        else:
            class_id = class_info["class_id"]

           
            db.execute(
                "INSERT INTO free_trial_signups (name, email, phone, preferred_class) VALUES (?, ?, ?, ?)",
                (name, email, phone, preferred_class),
            )
            db.commit()

            message = "Thank you for signing up! A member of staff will be in touch shortly."

            
            return render_template("free_trial.html", form=form, classes=classes, message=message)

    return render_template("free_trial.html", form=form, classes=classes, message=message)
