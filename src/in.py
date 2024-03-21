import random
import json
import csv
from datetime import date
import holidays

#
#USERS LOGIN
#
class Employee:

    def random_oclock(hour):
        hour_before = hour-1
        current_hour = random.choice([hour, hour_before])
        if current_hour == hour:
            minutes = random.randint(0,5)
            return "{}:0{}".format(current_hour, minutes)
        
        elif current_hour == hour_before:
            return "{}:{}".format(current_hour, random.randint(55,59))



    def random_half(hour):
        minutes = random.randint(28,35)
        return "{}:{}".format(hour, minutes)


#
#HOLDAY CHECK
#To chenge the location/file we have to modify the open() function
#Get the name from the 1st user example: user = data["users"][0]["name"]
#

with open("data/data.json") as file_json:
    data = json.loads(file_json.read())
    year = data["year"][0]["current"]
    if not date.today() in sorted(holidays.ES(subdiv='CT', years=year).items()):
        with open("docs/march.csv", 'a', newline='') as file:
            csvwriter = csv.writer(file)
            #SignIn log
            for user in data["users"]:
                if user["min_in"] == 0:
                    csvwriter.writerow([user["name"], Employee.random_oclock(user["hour_in"]), date.today(), "CheckIn"])
                elif user["min_in"] == 30:
                    csvwriter.writerow([user["name"],Employee.random_half(user["hour_in"]), date.today(), "CheckIn"])
                else:
                    print("Incorrect value range: the user {} only can SignIn at {}:0, or a {}:30".format(user["name"], user["hour_in"], user["hour_in"]))
            #SignOut log
            for user in data["users"]:
                if user["min_out"] == 0:
                    csvwriter.writerow([user["name"], Employee.random_oclock(user["hour_out"]), date.today(), "CheckOut"])
                elif user["min_out"] == 30:
                    csvwriter.writerow([user["name"],Employee.random_half(user["hour_out"]), date.today(), "CheckOut"])
                else:
                    print("Incorrect value range: the user {} only can SignOut at {}:0, or a {}:30".format(user["name"], user["hour_out"], user["hour_out"]))
