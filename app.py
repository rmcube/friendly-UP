from flask import Flask, request
from query.user import getUsers

app = Flask(__name__)


@app.route("/users/<user_id>", methods=["GET"])
def show_user_profile(user_id):
    # show the user profile for that user
    return "User %s" % user_id


@app.route("/users")
def get_users_by_condition():
    name = request.args.get("name")
    school = request.args.get("school")

    query = getUsers.query1
    where = ""
    if name is not None:
        where += "where name = %s"

    if school is not None:
        if where == "":
            where += "where school = %s"
        else:
            where += " and school = %s"

    # You need to establish a connection to the database and create a cursor here
    # For example:
    # connection = your_database_connection
    # cur = connection.cursor()

    cur.execute(query + where, (name, school))

    # Add logic here to fetch the result and convert it to a dictionary

    return "User %s" % name


@app.route("/users/by/grade", methods=["GET"])
def get_user_by_grade():
    school = request.args.get("school")
    grade = request.args.get("grade")

    query = getUsers.query1

    where = ""
    if grade is not None:
        where += "where grade = %s"

    if school is not None:
        if where == "":
            where += "where school = %s"
        else:
            where += " and school = %s"

    # You need to establish a connection to the database and create a cursor here
    # For example:
    # connection = your_database_connection
    # cur = connection.cursor()

    cur.execute(query + where, (grade, school))

    # Add logic here to fetch the result and convert it to a dictionary

    return "users %s" % grade


@app.route("/users/by/school", methods=["GET"])
def get_user_by_school():
    school = request.args.get("school")

    query = getUsers.query1

    where = ""

    if school is not None:
        if where == "":
            where += "where school = %s"
        else:
            where += " and school = %s"

    # You need to establish a connection to the database and create a cursor here
    # For example:
    # connection = your_database_connection
    # cur = connection.cursor()

    cur.execute(query + where, (school,))

    # Add logic here to fetch the result and convert it to a dictionary

    return "users %s" % school


if __name__ == "__main__":
    app.debug = True
    app.run(host="127.0.0.1", port=5000)
