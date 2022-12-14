from flask import Flask, render_template, request, flash, redirect, url_for
from flask_wtf import FlaskForm
from wtforms import SubmitField, StringField, PasswordField, BooleanField, ValidationError
from wtforms.validators import DataRequired, input_required, EqualTo, Length
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import date
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user
from webforms import LoginForm, PostForm, UserForm, PasswordForm, NamerForm, SearchForm
from flask_ckeditor import CKEditor
from werkzeug.utils import secure_filename
import uuid as uuid
import os
import click



#create flask instance
app = Flask(__name__)

ckeditor = CKEditor(app)
# old Sqlite db
#app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
# local MySQL db
#app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:password123@localhost/my_users'
#Postgres Dbase on heroku
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://lbizylwmzaxzer:982422db8ff3cd35c3dc42dc07d745a9a3e3e345c440144452f02e360a190f4e@ec2-52-1-17-228.compute-1.amazonaws.com:5432/deu19ae0foeuj9"

app.config['SECRET_KEY'] = "secret key ###"

UPLOAD_FOLDER = "/Users/brian/Documents/flasker/static/images/"
app.config['UPLOAD_FOLDER']=UPLOAD_FOLDER

db = SQLAlchemy(app)
migrate = Migrate(app, db)
#def init_app(app):
    #db.init_app(app)

# def create_db(self):
#     """Creates database"""
#     db.create_all()
    
# def drop_db():
#     """Cleans database"""
#     db.drop_all()

# def create_model_table():
#     """ Create table model in the database """
#     Posts.__table__.create(db.engine)
#     Users.__table__.create(db.engine)
    
# def init_app(app):
#     # add multiple commands in a bulk
#     for command in [create_db, drop_db, create_model_table]:
#         app.cli.add_command(app.cli.command()(command))

db.init_app(app)

# Flask Login setup
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(int(user_id))

#Pass into navbar
@app.context_processor
def base():
    form = SearchForm()
    return dict(form=form)

@app.route('/admin')
@login_required
def admin():
    id = current_user.id 
    if id == 3:
        return render_template("admin.html")
    else:
        flash("Sorry, page restricted to admin users only")
        return redirect(url_for('dashboard'))


# create search function
@app.route('/search', methods=['POST'])
def search():
    form = SearchForm()
    posts = Posts.query
    if form.validate_on_submit():
        post_searched = form.searched.data
        posts = posts.filter(Posts.content.like('%' + post_searched + '%'))
        posts = posts.order_by(Posts.title).all()
        return render_template('search.html', form=form, searched=post_searched, posts=posts)
        

# create login page
@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = Users.query.filter_by(username=form.username.data).first()
        if user:
            #check the hash
            if check_password_hash(user.password_hash, form.password.data):
                login_user(user)
                flash("Login Successful")
                return redirect(url_for('dashboard'))
            else:
                flash("Login unsuccessful, try again")
        else:
            flash("User does not exist, try again")
    return render_template('login.html', form=form)

#Create logout function
@app.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    flash("You are logged out")
    return redirect(url_for('login'))

#create dashboard page
@app.route('/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():
    form=UserForm()
    id=current_user.id
    name_to_update=Users.query.get_or_404(id)
    if request.method == "POST":
        name_to_update.name = request.form['name']
        name_to_update.username = request.form['username']
        name_to_update.email = request.form['email']
        name_to_update.favorite_color = request.form['favorite_color']
        name_to_update.about_author = request.form['about_author']

        # Check for profile pic
        if request.files['profile_pic']:
            name_to_update.profile_pic = request.files['profile_pic']
            # get image name
            pic_filename=secure_filename(name_to_update.profile_pic.filename)
            # Save image
            saver = request.files['profile_pic']
            pic_name = str(uuid.uuid1())+ "_" +pic_filename
            name_to_update.profile_pic = pic_name


            try:
                db.session.commit()
                saver.save(os.path.join(app.config['UPLOAD_FOLDER'], pic_name))
                flash("User Updated Successfully")
                return render_template (
                "dashboard.html", 
                form=form,
                name_to_update = name_to_update
                )
            except:
                flash("Error! Try Again Please")
                return render_template (
                "dashboard.html", 
                form=form,
                name_to_update = name_to_update,
                )
        else:
            db.session.commit()
            flash("User Updated Successfully")
            return render_template (
            "dashboard.html", 
            form=form,
            name_to_update = name_to_update
            )

    else:
        return render_template (
            "dashboard.html", 
            form=form,
            name_to_update = name_to_update,
            id = id
            )
    #return render_template('dashboard.html')

#create a route decorator
@app.route('/')
def index():
    return redirect("/login",)

#delete user class
@app.route('/delete/<int:id>')
@login_required
def delete(id):
    if id == current_user.id or current_user.id == 1:
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
    else:
        flash("You do not have permission to delete that user")
        return redirect(url_for('dashboard'))

# @app.route('/user/<name>')
# def user(name):
#     return render_template("user.html", user_name=name)

#individual post page
@app.route('/posts/<int:id>')
def post(id):
    post = Posts.query.get_or_404(id)
    return render_template('post.html', post=post)

@app.route('/posts/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_post(id):
    post = Posts.query.get_or_404(id)
    form = PostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        #post.author = form.author.data
        post.slug = form.slug.data
        post.content = form.content.data
        db.session.add(post)
        db.session.commit()
        flash("Post has been updated")
        return redirect(url_for('post', id=post.id))
    if current_user.id == post.poster_id or current_user.id == 1:
        form.title.data = post.title
        #form.author.data = post.author
        form.slug.data = post.slug
        form.content.data = post.content
        return render_template('edit_post.html', form=form)
    else:
        flash("You cannot edit the post of another user")
        posts = Posts.query.order_by(Posts.date_posted)
        return render_template("posts.html", posts=posts)



@app.route('/posts/delete/<int:id>')
@login_required
def delete_post(id):
    post_to_delete = Posts.query.get_or_404(id)
    val_id = current_user.id
    if val_id == post_to_delete.poster.id or val_id == 1:
        try:
            db.session.delete(post_to_delete)
            db.session.commit()
            flash("Blog post was deleted successfully")
            posts = Posts.query.order_by(Posts.date_posted)
            return render_template("posts.html", posts=posts)
        except:
            flash("Whoops, there was a problem deleting. Try again")
            posts = Posts.query.order_by(Posts.date_posted)
            return render_template("posts.html", posts=posts)
    else:
        flash("You cannot delete post of another user")
        posts = Posts.query.order_by(Posts.date_posted)
        return render_template("posts.html", posts=posts)

#add post page
@app.route('/add_post', methods=['GET', 'POST'])
@login_required
def add_post():
    form = PostForm()
    if form.validate_on_submit():
        poster = current_user.id
        post = Posts(
            title=form.title.data,
            content=form.content.data,
            poster_id=poster,
            slug=form.slug.data
        )
        form.title.data = ''
        form.content.data = ''
        #form.author.data = ''
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
                username=form.username.data,
                email=form.email.data, 
                favorite_color=form.favorite_color.data,
                password_hash=hashed_pw
                )
            db.session.add(user)
            db.session.commit()
            name=form.name.data
            email=form.email.data
        form.name.data=""
        form.username.data=""
        form.email.data=""
        form.favorite_color.data=""
        form.password_hash = ""
        flash("User Added Successfully")
    our_users = Users.query.order_by(Users.id)
    return render_template("add_user.html", form=form, name=name, our_users=our_users)

#update database record
@app.route('/update/<int:id>', methods=['GET', 'POST'])
@login_required
def update(id):
    form=UserForm()
    name_to_update=Users.query.get_or_404(id)
    if request.method == "POST":
        name_to_update.name = request.form['name']
        name_to_update.username = request.form['username']
        name_to_update.email = request.form['email']
        name_to_update.favorite_color = request.form['favorite_color']
        name_to_update.about_author = request.form['about_author']
        try:
            db.session.commit()
            flash("User Updated Successfully")
            return render_template (
            "update.html", 
            form=form,
            id=id,
            name_to_update = name_to_update
            )
        except:
            flash("Error! Try Again Please")
            return render_template (
            "update.html", 
            form=form,
            id=id,
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
# @app.route('/name', methods=['GET', 'POST'])
# def name():
#     name = None
#     form = NamerForm()
#     if form.validate_on_submit():
#         name=form.name.data
#         form.name.data = ''
#         flash("Form Submitted Successfully")
#     return render_template("name.html", name=name, form=form)

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

#blog post model
class Posts(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255))
    content = db.Column(db.Text)
    #author = db.Column(db.String(255))
    date_posted = db.Column(db.DateTime, default=datetime.utcnow)
    slug = db.Column(db.String(255))
    # Foreign Key link to p key in Users
    poster_id = db.Column(db.Integer, db.ForeignKey('users.id'))

# Create Model
class Users(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), nullable=False, unique=True)
    name = db.Column(db.String(200), nullable=False)
    email =db.Column(db.String(120), nullable=False, unique=True)
    favorite_color = db.Column(db.String(120))
    about_author = db.Column(db.Text(), nullable=True)
    date_added =db.Column(db.DateTime, default=datetime.utcnow)
    profile_pic=db.Column(db.String(255), nullable=True)
    #integrating passwords
    password_hash = db.Column(db.String(128))
    # user can have many posts
    posts = db.relationship('Posts', backref='poster')

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

with app.app_context():
    db.create_all()
