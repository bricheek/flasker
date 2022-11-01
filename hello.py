from flask import Flask, render_template, request, flash
from flask_wtf import FlaskForm
from wtforms import SubmitField, StringField
from wtforms.validators import DataRequired, input_required

#create flask instance
app = Flask(__name__)

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

app.config['SECRET_KEY'] = "secret key ###"

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

@app.route('/user/<name>')
def user(name):
    return render_template("user.html", user_name=name)

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

