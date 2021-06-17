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
def index(project_result=None, agg_result=None, select_result=None, join_result=None, division_result=None) -> str:
    return render_template(
        "index.html", project_result=project_result, agg_result=agg_result, select_result=select_result, join_result=join_result, division_result=None
    )


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
    if request.args.get("select_get", None):
        criteria = None

        if request.args.get("select_criteria", None):
            criteria = request.args["select_criteria"]

        # If criteria are None, query will throw error. So redirect to index.html
        if criteria == None:
            return redirect("/")

        select_result = f"[('showname')] : {bs.select_series(criteria)}"

        return render_template("index.html", select_result=select_result)

    # If reset button is pressed, simply redirect to home
    elif request.args.get("select_reset", None):
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


@app.route("/aggregate_movie_length")
def aggregate_movie_length():
    if request.args.get("agg_get", None):
        if request.args.get("agg_func", None):
            agg_func = request.args.get("agg_func")

            # Check for valid aggregation function
            if agg_func.lower() in ["min", "max", "count", "avg"]:
                # Calculate aggregation result
                agg_result = bs.aggregate_movie_length(agg_func=agg_func)

                # Render template with agg_result set
                return render_template(
                    "index.html", agg_result=f"{agg_func} movie length is {agg_result}"
                )
            else:
                redirect("/")

    elif request.args.get("agg_reset", None):
        return redirect("/")

    return redirect("/")

@app.route("/join_video_cert", methods=["GET"])
def join_video_cert():

    # If the get button is pressed, obtain data from database
    if request.args.get("join_get", None):
        certificate = None

        if request.args.get("get_cert", None):
            certificate = request.args["get_cert"]

        # If criteria are None, query will throw error. So redirect to index.html
        if certificate == None:
            return redirect("/")

        join_result = f"[('videomedia_name')] : {bs.select_certification(certificate)}"

        return render_template("index.html", join_result=join_result)

    # If reset button is pressed, simply redirect to home
    elif request.args.get("join_reset", None):
        return redirect("/")

    return redirect("/")
   
@app.route("/division_streaming", methods=["GET"])
def division_streaming():

    # If the get button is pressed, obtain data from database
    if request.args.get("division_get", None):
        user = None
        email = None

        if request.args.get("division_user", None):
            user = request.args["division_user"]
        if request.args.get("division_email", None):
            email = request.args["division_email"]

        # If both are None, query will throw error. So redirect to index.html
        if user == None and email == None:
            return redirect("/")

        # Project based on selected checkboxes
        if user != None and email != None:
            division_result = f"'name', 'email' : \
                {bs.has_all_streaming(user=True, email=True)}"
        elif user != None and email == None:
            division_result = f"'name' : {bs.has_all_streaming(user=True, email=False)}"
        elif user == None and email != None:
            division_result = f"'email' : {bs.has_all_streaming(user=False, email=True)}"

        return render_template("index.html", division_result=division_result)

    # If reset button is pressed, simply redirect to home
    elif request.args.get("division_reset", None):
        return redirect("/")

    return redirect("/")



try:
    app.run(host="localhost", port=8080, debug=True)
finally:
    bs.end_session()
