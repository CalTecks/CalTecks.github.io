from flask import Flask, render_template
import yaml

with open("./posts/example.yaml", "r") as f:
    data = yaml.safe_load(f)


print(data)

app = Flask(__name__)


@app.route('/_site/')
def index():
    author_name = "Thomas"
    return render_template("index.html", author_name=author_name)


@app.route('/_site/user/<name>')
def user(name):
    return render_template("user.html", user_name=name)


@app.route('/_site/pizza')
def pizza():
    ingedrients = ["zout", "peper", "zalm",
                   "heilbot", "sliptong", "tomaat", "deeg"]
    return render_template("pizza.html", title="Pizza's!", pizza_type="Vispizza", ingedrients=ingedrients)
