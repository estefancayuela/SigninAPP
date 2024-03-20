import random
import json
import csv


file_json = open('data/data.json')
data = json.loads(file_json.read())

#Get the name from the 1st user example: user = data["users"][1]["name"]



#
#USERS LOGIN
#

class Employee:

    def random_oclock(hour:int ):
        hour_before = hour-1
        current_hour = random.choice([hour, hour_before])
        if current_hour == hour:
            minutes = random.randint(0,5)
            return "{}:0{}".format(current_hour, minutes)
        
        elif current_hour == hour_before:
            return "{}:{}".format(current_hour, random.randint(55,59))



    def random_half(hour:int):
        minutes = random.randint(28,35)
        return "{}:{}".format(hour, minutes)



with open("prova.csv", 'a', newline='') as file:
    csvwriter = csv.writer(file)
    for user in data["users"]:
        csvwriter.writerow([user["name"], Employee.random_oclock(user["hour_in"]), Employee.random_half(user["hour_out"])])


