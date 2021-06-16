import argparse
from flask import Flask, render_template, request, redirect
from flask.helpers import url_for
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
def index(project_result=None, select_result=None) -> str:
    return render_template("index.html", project_result=project_result, select_result=select_result)


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

@app.route("/select_series", methods=["GET"])
def select_series():

    # If the get button is pressed, obtain data from database
    if request.args.get("project_get", None):
        criteria = None

        if request.args.get("select_criteria", None):
            criteria = request.args["select_criteria"]

        # If criteria are None, query will throw error. So redirect to index.html
        if criteria == None:
            return redirect("/")

        project_result = f"[('showname')] : {bs.select_series(criteria)}"

        return render_template("index.html", project_result=project_result)

    # If reset button is pressed, simply redirect to home
    elif request.args.get("project_reset", None):
        return redirect("/")

    return redirect("/")

@app.route("/project_series", methods=["GET"])
def project_series():

    # If the get button is pressed, obtain data from database
    if request.args.get("project_get", None):
        seasons = None
        episodes = None

        if request.args.get("project_seasons", None):
            seasons = request.args["project_seasons"]
        if request.args.get("project_episodes", None):
            episodes = request.args["project_episodes"]

        # If both are None, query will throw error. So redirect to index.html
        if seasons == None and episodes == None:
            return redirect("/")

        # Project based on selected checkboxes
        if seasons != None and episodes != None:
            project_result = f"[('showname', 'seasons', 'episodes')] : \
                {bs.project_series(seasons=True, episodes=True)}"
        elif seasons != None and episodes == None:
            project_result = f"[('showname', 'seasons')] : {bs.project_series(seasons=True, episodes=False)}"
        elif seasons == None and episodes != None:
            project_result = f"[('showname', 'episodes')] : {bs.project_series(seasons=False, episodes=True)}"

        return render_template("index.html", project_result=project_result)

    # If reset button is pressed, simply redirect to home
    elif request.args.get("project_reset", None):
        return redirect("/")

    return redirect("/")


try:
    app.run(host="localhost", port=8080, debug=True)
finally:
    bs.end_session()
