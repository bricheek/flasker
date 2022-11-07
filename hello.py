from flask import Flask, render_template, request, flash
from flask_wtf import FlaskForm
from wtforms import SubmitField, StringField
from wtforms.validators import DataRequired, input_required
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

#create flask instance
app = Flask(__name__)
# old Sqlite db
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
# new MySQL db
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:password123@localhost/my_users'
app.config['SECRET_KEY'] = "secret key ###"

db = SQLAlchemy(app)
db.init_app(app)


# Create Model
class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    email =db.Column(db.String(120), nullable=False, unique=True)
    date_added =db.Column(db.DateTime, default=datetime.utcnow)

    #create a string
    def __repr__(self):
        return '<Name %r>' % self.name

# database already created
# with app.app_context():
    # db.create_all()

#create a route decorator
@app.route('/')
def index():
    first_name = "John"
    stuff = "This is bold text."
    favorite_pizza = ["Pepperoni", "Cheese", "Mushroom", 41]
    return render_template("index.html", 
    given_name = first_name, 
    stuff=stuff,
    favorite_pizza=favorite_pizza
    )


#create form class
class NamerForm(FlaskForm):
    name = StringField("What's Your Name?", validators=[DataRequired()])
    submit = SubmitField("Submit")

#create form class
class UserForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired()])
    email = StringField("Email", validators=[DataRequired()])
    submit = SubmitField("Submit")


@app.route('/user/<name>')
def user(name):
    return render_template("user.html", user_name=name)

#create user page
@app.route('/user/add', methods=['GET', 'POST'])
def add_user():
    name = None
    form = UserForm()
    if form.validate_on_submit():
        user = Users.query.filter_by(email=form.email.data).first()
        if user is None:
            user = Users(name=form.name.data, email=form.email.data)
            db.session.add(user)
            db.session.commit
        name=form.name.data
        form.name.data=""
        form.email.data=""
        flash("User Added Successfully")
    our_users = Users.query.order_by(Users.date_added)
    return render_template("add_user.html", form=form, name=name, our_users=our_users)

# custom error pages
# Invalid URL
@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404

#internal server error
@app.errorhandler(500)
def page_not_found(e):
    return render_template("500.html"), 500

#Create name page
@app.route('/name', methods=['GET', 'POST'])
def name():
    name = None
    form = NamerForm()
    if form.validate_on_submit():
        name=form.name.data
        form.name.data = ''
        flash("Form Submitted Successfully")
    return render_template("name.html", name=name, form=form)
