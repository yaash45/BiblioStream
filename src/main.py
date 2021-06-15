import argparse
from flask import Flask, render_template, request, redirect
from bibliostream import BiblioStream
from database import Database

app = Flask(__name__)


@app.route("/")
def index() -> str:
    return render_template("index.html")


@app.route("/insert_user", methods=["POST"])
def insert_user():
    user_name = request.form.get("username")
    user_email = request.form.get("email")
    user_phone = request.form.get("phone")

    print(f"name = {user_name}, email = {user_email}, phone = {user_phone}")

    return redirect("/")


def main() -> None:
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
        print(bs.insert_user("Yaash", "abc@ubc.ca", "1234567890"))
        bs.end_session()


if __name__ == "__main__":
    app.run(host="localhost", port=8080, debug=True)
