from flask import Flask, render_template, request, flash
from flask_wtf import FlaskForm
from wtforms import SubmitField, StringField
from wtforms.validators import DataRequired, input_required
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

#create flask instance
app = Flask(__name__)
app.config['SECRET_KEY'] = "secret key ###"
#add database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
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

with app.app_context():
    db.create_all()

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


# class SignupForm(Form):
#     age = IntegerField('Age')

# def validate_age(form, field):
#     if field.data < 13:
#         raise ValidationError("We're sorry, you must be 13 or older to register")

# class MyForm(Form):
#     first_name = StringField('First Name', validators=[validators.input_required()])
#     last_name  = StringField('Last Name', validators=[validators.optional()])

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


# def register(request):
#     form = RegistrationForm(request.POST)
#     if request.method == 'POST' and form.validate():
#         user = User()
#         user.username = form.username.data
#         user.email = form.email.data
#         user.save()
#         redirect('register')
#     return render_response('register.html', form=form)

# app.route('/name', methods=['GET', 'POST'])
# def name():
#     name = None
#     form = NamerForm()
#     #validate form
#     if form.validate_on_submit():
#         name=form.name.data
#         form.name.data = ''
#     return render_template('name.html',
#     name = name,
#     form = form)

# def create_app():
#     app = Flask(__name__)
#     with app.app_context():
#         db.create_all()
#     return app