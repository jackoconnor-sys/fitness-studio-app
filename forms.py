from flask_wtf import FlaskForm
from wtforms import SubmitField, RadioField, StringField, PasswordField
from wtforms.validators import InputRequired, EqualTo

class RegistrationForm(FlaskForm):
    user_id = StringField("UserID:", validators=[InputRequired()])
    password = PasswordField("Password:", validators=[InputRequired()])
    password2 = PasswordField("Repeat password:", validators=[InputRequired(), EqualTo("password")])
    submit = SubmitField("Submit")

class LoginForm(FlaskForm):
    user_id = StringField("UserID:", validators=[InputRequired()])
    password = PasswordField("Password:", validators=[InputRequired()])
    submit = SubmitField("Submit") 

class AdminRegistrationForm(FlaskForm):
    admin_id = StringField("AdminID:", validators=[InputRequired()])
    password = PasswordField("Password:", validators=[InputRequired()])
    password2 = PasswordField("Repeat Password:", validators=[InputRequired(), EqualTo("password")])
    special_admin_code = StringField("Special Admin Code:", validators=[InputRequired()])
    submit = SubmitField("Register Admin")

class AdminLoginForm(FlaskForm):
    admin_id = StringField("AdminID:", validators=[InputRequired()])
    password = PasswordField("Password", validators=[InputRequired()])
    special_admin_code = StringField("Special Admin Code", validators=[InputRequired()])
    submit = SubmitField("Login as Admin")

class ClassForm(FlaskForm):
    name = StringField('Class Name', validators=[InputRequired()])
    day = StringField('Day', validators=[InputRequired()])
    time = StringField('Time', validators=[InputRequired()])
    duration = StringField('Duration', validators=[InputRequired()])
    trainer = StringField('Trainer', validators=[InputRequired()])
    description = StringField('Description', validators=[InputRequired()])
    submit = SubmitField('Add Class')


class SignupOtherUserClassForm(FlaskForm):
    user_id = StringField("User ID", validators=[InputRequired()])
    class_name = RadioField("Class", choices=["Pilates", "HIIT", "Yoga Flow", "Strength & Conditioning", "Spin Class", "Zumba", "Boxing Fundamentals", "Mobility & Stretch"], default="Pilates")
    submit = SubmitField("Sign Up")

class FreeTrialForm(FlaskForm):
    name = StringField("Name", validators=[InputRequired()])
    email = StringField("Email", validators=[InputRequired()])
    phone = StringField("Phone Number", validators=[InputRequired()])
    preferred_class = RadioField("Class", choices=["Pilates", "HIIT", "Yoga Flow", "Strength & Conditioning", "Spin Class", "Zumba", "Boxing Fundamentals", "Mobility & Stretch"], default="Pilates")
    submit = SubmitField("Sign Up for Free Trial")