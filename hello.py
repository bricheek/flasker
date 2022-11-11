from flask import Flask, render_template, request, flash
from flask_wtf import FlaskForm
from wtforms import SubmitField, StringField, PasswordField, BooleanField, ValidationError
from wtforms.validators import DataRequired, input_required, EqualTo, Length
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import date
from wtforms.widgets import TextArea

#create flask instance
app = Flask(__name__)
# old Sqlite db
#app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
# new MySQL db
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:password123@localhost/my_users'
app.config['SECRET_KEY'] = "secret key ###"

db = SQLAlchemy(app)
migrate = Migrate(app, db)
db.init_app(app)

#blog post model
class Posts(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255))
    content = db.Column(db.Text)
    author = db.Column(db.String(255))
    date_posted = db.Column(db.DateTime, default=datetime.utcnow)
    slug = db.Column(db.String(255))

# Create Model
class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    email =db.Column(db.String(120), nullable=False, unique=True)
    favorite_color = db.Column(db.String(120))
    date_added =db.Column(db.DateTime, default=datetime.utcnow)
    #integrating passwords
    password_hash = db.Column(db.String(128))

    @property
    def password(self):
        raise AttributeError('pasword is not a readable attribute')
    
    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)
        
    #create a string
    def __repr__(self):
        return '<Name %r>' % self.name

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

#delete user class
@app.route('/delete/<int:id>')
def delete(id):
    user_to_delete=Users.query.get_or_404(id)
    Name = None
    form = UserForm()
    try:
        db.session.delete(user_to_delete)
        db.session.commit()
        flash("User Deleted Successfully")
        our_users = Users.query.order_by(Users.id)
        return render_template("add_user.html", form=form, name=name, our_users=our_users)
    except:
        flash("There was an error deleting, please try again")
        our_users = Users.query.order_by(Users.id)
        return render_template("add_user.html", form=form, name=name, our_users=our_users)
        
#create a posts form
class PostForm(FlaskForm):
    title = StringField("title", validators=[DataRequired()])
    content = StringField("Content", validators=[DataRequired()], widget=TextArea())
    author = StringField("Author", validators=[DataRequired()])
    slug = StringField("Slug", validators=[DataRequired()])
    submit = SubmitField("Submit")

#create form class
class PasswordForm(FlaskForm):
    email = StringField("What's Your Email?", validators=[DataRequired()])
    password_hash = PasswordField("What's Your password?", validators=[DataRequired()])
    submit = SubmitField("Submit")

#create form class
class NamerForm(FlaskForm):
    name = StringField("What's Your Name?", validators=[DataRequired()])
    submit = SubmitField("Submit")

#create form class
class UserForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired()])
    email = StringField("Email", validators=[DataRequired()])
    favorite_color = StringField("Favorite Color")
    password_hash = PasswordField(
        'Password', validators=[DataRequired(), 
        EqualTo('password_hash2', 
        message='passwords must match')]
        )
    password_hash2 = PasswordField('Confirm Password', validators=[DataRequired()])
    submit = SubmitField("Submit")

@app.route('/user/<name>')
def user(name):
    return render_template("user.html", user_name=name)

#individual post page
@app.route('/posts/<int:id>')
def post(id):
    post = Posts.query.get_or_404(id)
    return render_template('post.html', post=post)

#add post page
@app.route('/add_post', methods=['GET', 'POST'])
def add_post():
    form = PostForm()
    if form.validate_on_submit():
        post = Posts(
            title=form.title.data,
            content=form.content.data,
            author=form.author.data,
            slug=form.slug.data
        )
        form.title.data = ''
        form.content.data = ''
        form.author.data = ''
        form.slug.data = ''
        db.session.add(post)
        db.session.commit()
        flash("Blog post submitted successfully")
    return render_template("add_post.html", form=form)

#display blog post (future home page of app)
@app.route('/posts')
def posts():
    posts = Posts.query.order_by(Posts.date_posted)
    return render_template("posts.html", posts=posts)


#create user page
@app.route('/user/add', methods=['GET', 'POST'])
def add_user():
    name = None
    form = UserForm()
    if form.validate_on_submit():
        user = Users.query.filter_by(email=form.email.data).first()
        if user is None:
            #hash the password
            hashed_pw = generate_password_hash(form.password_hash.data, "sha256")
            user = Users(
                name=form.name.data, 
                email=form.email.data, 
                favorite_color=form.favorite_color.data,
                password_hash=hashed_pw
                )
            db.session.add(user)
            db.session.commit()
            name=form.name.data
            email=form.email.data
        form.name.data=""
        form.email.data=""
        form.favorite_color.data=""
        form.password_hash = ""
        flash("User Added Successfully")
    our_users = Users.query.order_by(Users.id)
    return render_template("add_user.html", form=form, name=name, our_users=our_users)

#update database record
@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    form=UserForm()
    name_to_update=Users.query.get_or_404(id)
    if request.method == "POST":
        name_to_update.name = request.form['name']
        name_to_update.email = request.form['email']
        name_to_update.favorite_color = request.form['favorite_color']
        try:
            db.session.commit()
            flash("User Updated Successfully")
            return render_template (
            "update.html", 
            form=form,
            name_to_update = name_to_update
            )
        except:
            flash("Error! Try Again Please")
            return render_template (
            "update.html", 
            form=form,
            name_to_update = name_to_update,
            )
    else:
        return render_template (
            "update.html", 
            form=form,
            name_to_update = name_to_update,
            id = id
            )

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

#Create password test page
@app.route('/test_pw', methods=['GET', 'POST'])
def test_pw():
    email = None
    password = None
    pw_to_check = None
    passed = None
    form = PasswordForm()
    if form.validate_on_submit():
        email=form.email.data
        password=form.password_hash.data
        form.email.data = ''
        form.password_hash.data = ''
        #lookup user by email address
        pw_to_check = Users.query.filter_by(email=email).first()
        #check hashed password
        passed = check_password_hash(pw_to_check.password_hash, password)

    return render_template(
        "test_pw.html", 
        email=email, 
        password=password, 
        pw_to_check = pw_to_check,
        passed = passed,
        form=form
        )

@app.route('/date')
def get_current_date():
    return {"Date" : date.today()}
