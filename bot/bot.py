import os
from subprocess import check_output
import time
import sys
from config import credentials
from model import get_tasks


params_tasks = {
    "colsubsidio": {
        "name": "Colsubsidio : Cliente 360",
        "role": "15: Consultor Sintec Digital",
        "status": "Asignado"
    },
    "internal": {
        "name": "Sintec : Internal Time",
        "role": "3: Internal:Practice Activities",
        "status": "Internal"
    },
    "holiday": {
        "name": "Sintec : Time Off",
        "role": "1: Time off:Holidays",
        "status": "Time off"
    },
    "vacations": {
        "name": "Sintec : Time Off",
        "role": "1: Time off:Vacations",
        "status": "Time off"
    }
}

coordinates = {
    "timesheet_options_button_x": 28,
    "timesheet_options_button_y": 572,
    "new_timesheet_button_x": 762,
    "new_timesheet_button_y": 670,
    "base_task_x": 607,
    "base_role_x": 1177,
    "base_status_x": 1575,
    "base_hours_x": 1692,
    "first_row_y": 939,
    "hour_cells_distance": 163,
    "row_vertical_distance": 86,
    "submit_button_x": 2021,
    "submit_button_y": 641
}


def login(credentials):
    wid = os.system("xdotool search 'Mozilla Firefox'")
    os.system("xdotool windowactivate --sync {}".format(wid))
    os.system("xdotool key ctrl+t")
    os.system("xdotool type 'https://www.openair.com/index.pl'")
    os.system("xdotool key Return")
    time.sleep(2)

    os.system("xdotool type '{}'".format(credentials["company"]))
    os.system("xdotool key Tab")
    time.sleep(2)
    os.system("xdotool type '{}'".format(credentials["user"]))
    os.system("xdotool key Tab")
    time.sleep(2)
    os.system("xdotool type '{}'".format(credentials["password"]))
    time.sleep(2)
    os.system("xdotool key Return")
    time.sleep(3)


def new_timesheet():
    os.system("xdotool mousemove {} {} click 1".format(coordinates["timesheet_options_button_x"],
                                                       coordinates["timesheet_options_button_y"]))
    time.sleep(3)
    os.system("xdotool type 'Timesheets'")
    time.sleep(3)

    os.system("xdotool key Tab")
    os.system("xdotool key Tab")
    os.system("xdotool key Tab")
    os.system("xdotool key Return")
    time.sleep(3)

    os.system("xdotool mousemove {} {} click 1".format(coordinates["new_timesheet_button_x"],
                                                       coordinates["new_timesheet_button_y"]))
    time.sleep(3)


def fill_timesheet(tasks):
    wid = check_output("xdotool search --name 'Mozilla Firefox'", shell=True)
    wid = int(wid.decode())
    os.system("xdotool windowactivate --sync {}".format(wid))
    # Fill hours and descriptions of activities
    for task_index in range(len(tasks)):
        activities = tasks[task_index]["activities"]
        for i in range(len(activities)):
            weekday = activities[i]["weekday"]
            hours_cell_x = coordinates["base_hours_x"] + coordinates["hour_cells_distance"] * weekday
            hours_cell_y = coordinates["first_row_y"] + coordinates["row_vertical_distance"] * task_index
            hours = activities[i]["hours"]
            activity_name = activities[i]["name"]
            activity_description = activities[i]["description"]

            os.system("xdotool mousemove {} {} click 1".format(hours_cell_x, hours_cell_y))
            os.system("xdotool type '{}'".format(hours))
            os.system("xdotool key Tab")
            os.system("xdotool key Return")
            time.sleep(2)
            os.system("xdotool type '{}'".format(activity_name))
            os.system("xdotool key Tab")
            os.system("xdotool type '{}'".format(activity_description))
            os.system("xdotool key Tab")
            os.system("xdotool key Return")
            time.sleep(2)

    # Fill tasks, roles and statuses
    for task_index in range(len(tasks)):
        task_type = tasks[task_index]["type"]
        task_y = coordinates["first_row_y"] + coordinates["row_vertical_distance"] * task_index

        task_name_x = coordinates["base_task_x"]
        task_name = params_tasks[task_type]["name"]

        task_role_x = coordinates["base_role_x"]
        task_role = params_tasks[task_type]["role"]

        task_status_x = coordinates["base_status_x"]
        task_status = params_tasks[task_type]["status"]

        os.system("xdotool mousemove {} {} click 1".format(task_name_x, task_y))
        time.sleep(2)
        os.system("xdotool type '{}'".format(task_name))
        os.system("xdotool key Tab")
        time.sleep(2)
        os.system("xdotool mousemove {} {} click 1".format(task_role_x, task_y))
        os.system("xdotool type '{}'".format(task_role))
        os.system("xdotool key Tab")
        time.sleep(2)
        os.system("xdotool mousemove {} {} click 1".format(task_status_x, task_y))
        os.system("xdotool type '{}'".format(task_status))
        os.system("xdotool key Tab")
        time.sleep(2)
        os.system("xdotool mousemove {} {}".format(coordinates["submit_button_x"],
                                                           coordinates["submit_button_y"]))


def main():
    if len(sys.argv) != 3:
        print("Error: Los parámetros indicados son incorrectos")
        return 1
    if sys.argv[1] != "--timesheet-option":
        print("Error: Por favor indicar el parámetro 'timesheet-option' mediante el flag --timesheet-option")
        return 1
    timesheet_option = sys.argv[2]
    tasks = get_tasks()
    if timesheet_option == "new":
        login(credentials=credentials)
        new_timesheet()
        fill_timesheet(tasks=tasks)
    elif timesheet_option == "open":
        fill_timesheet(tasks=tasks)
    return 0


if __name__ == "__main__":
    main()
