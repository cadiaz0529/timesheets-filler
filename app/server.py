from flask import Flask, render_template, request, jsonify, redirect
from pymongo import MongoClient

app = Flask(__name__)

client = MongoClient()
db = client["open_air"]
timesheet_activities = db["timesheet_activities"]
timesheets = db["timesheets"]


@app.route("/")
def home():
    try:
        timesheets_list = [{"name": "Timesheet 1", "timesheet_id": "1"},
                           {"name": "Timesheet 2", "timesheet_id": "2"},
                           {"name": "Timesheet 3", "timesheet_id": "3"}]
        """
        for doc in timesheets.find():
            timesheets_list.append(doc)
        """
        return render_template("home.html", timesheets=timesheets_list)
    except ConnectionError as error:
        print(error)
        return jsonify(message="No se pudieron encontrar timesheets")


@app.route("/timesheet", methods=["GET", "POST"])
def create_timesheet():
    if request.method == "GET":
        return render_template("timesheet.html")
    elif request.method == "POST":
        try:
            timesheet_name = request.form["name"]
            new_timesheet = {"name": timesheet_name}
            #timesheets.insert_one(new_timesheet)
            return redirect("http://localhost:5000/")
        except AttributeError as error:
            print(error)
            return jsonify(message="No se recibieron datos!")
    else:
        return jsonify(message="El método del request no es aceptable")


@app.route("/activity/<timesheet_id>", methods=["GET", "POST"])
def create_activity(timesheet_id):
    if request.method == "GET":
        return render_template("activity.html", timesheet_id=timesheet_id)
    elif request.method == "POST":
        try:
            activity_type = request.form["activity_type"]
            activity_name = request.form["activity_name"]
            hours = float(request.form["hours"])
            description = request.form["description"]
            new_activity = {
                "timesheet_id": timesheet_id,
                "type": activity_type,
                "name": activity_name,
                "hours": hours,
                "description": description
            }
            #timesheet_activities.insert_one(new_activity)
            print(new_activity)
            return redirect("http://localhost:5000/")
        except ValueError as error:
            print(error)
            return jsonify(message="El número de horas trabajadas está en un formato inválido")
    else:
        return jsonify(message="El método del request no es aceptable")


if __name__ == "__main__":
    app.run(debug=True)
