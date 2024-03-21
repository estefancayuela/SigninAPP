import random
import json
import csv
from datetime import date
import holidays

#
#USERS LOGIN
#
class Employee:
    def __init__(self, name:str, hour_in:int, min_in:int, hour_out:int, min_out:int):
        self.name = name
        self.hour_in = hour_in
        self.min_in = min_in
        self.hour_out = hour_out
        self.min_out = min_out

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

"""
class Months():
    def __init__(self):
        self.days = 28
        
    def month_days(self):
        for i in range(self.days):
            print(i)


class Month_30(Months):
    def __init__(self):
        self.days = 30
        
        

class Month_31(Months):
    def __init__(self):
        self.days = 31


months_with_30 = ["04","06","09","11"]
months_with_31 = ["01","03","05","07","08",10,12]
months_with_28 = ["02"]
"""

current_day = date.today().weekday()
current_month = date.today().strftime("%m")
current_year = date.today().strftime("%Y")
def dia_avui():
    if current_day == 0:
        print("Dilluns")
    elif current_day == 1:
        print("Dimarts")
    elif current_day == 2:
        print("Dimecres")
    elif current_day == 3:
        print("Dijous")
    elif current_day == 4:
        print("Divendres")
    elif current_day == 5:
        print("Dissabte")
    elif current_day == 6:
        print("Diumenge")


"""
if current_mes in months_with_30:
    current_mes = Month_30()
    print(current_mes.days)

elif current_mes in months_with_31:
    current_mes = Month_31()
    print(current_mes.days)

elif current_mes in months_with_28:
    current_mes = Months()
    print(current_mes.days)

else:
    print("Error: couldn't get the date")

"""

#
#SIGNIN TODAY
#To chenge the location/file we have to modify the open() function
#Get the name from the 1st user example: user = data["users"][0]["name"]
#
def today_check():
    with open("data/data.json") as file_json:
        data = json.loads(file_json.read())
        year = data["year"][0]["current"]
        if not date.today() in sorted(holidays.ES(subdiv='CT', years=year).items()):
            with open("docs/{}_{}.csv".format(current_year, current_month), 'a', newline='') as file:
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



today_check()
