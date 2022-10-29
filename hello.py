from flask import Flask, render_template

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
    favorite_pizza=favorite_pizza,
    )

@app.route('/user/<name>')
def user(name):
    #return "<h1>Hello {}!!!</h1>".format(name)
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


