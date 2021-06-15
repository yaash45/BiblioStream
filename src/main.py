import argparse
from flask import Flask, render_template, request, redirect
from bibliostream import BiblioStream
from database import Database

app = Flask(__name__)


# Create instance of argument parser
parser = argparse.ArgumentParser(description="Pass database config")

# Define argument for database config file path
parser.add_argument("DatabaseConfigPath", metavar="path", type=str)

# Parse provided argument from CLI
args = parser.parse_args()

if args.DatabaseConfigPath != None:
    # Create an instance of the Database
    db = Database(args.DatabaseConfigPath)
    bs = BiblioStream(db)


@app.route("/")
def index() -> str:
    return render_template("index.html")


@app.route("/insert_user", methods=["POST"])
def insert_user():
    user_name = request.form.get("username")
    user_email = request.form.get("email")
    user_phone = request.form.get("phone")

    result = bs.insert_user(user_name, user_email, user_phone)

    if result != None:
        return redirect("/")
    else:
        return "Failed operation"


@app.route("/delete_user", methods=["POST"])
def delete_user():
    user_email = request.form.get("delete_email")

    result = bs.delete_user(user_email)

    if result != None:
        return redirect("/")
    else:
        return "Failed operation"


@app.route("/update_user_phone", methods=["POST"])
def update_user_phone():
    user_email = request.form.get("update_email")
    user_phone = request.form.get("update_phone")

    result = bs.update_user_phone(user_email, user_phone)

    if result != None:
        return redirect("/")
    else:
        return "Failed operation"


try:
    app.run(host="localhost", port=8080, debug=True)
finally:
    bs.end_session()
