import random
import json
import csv
from datetime import date
import holidays


#Dict with holidays from your country
cat_holidays = holidays.ES(subdiv="CT")


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
months_with_31 = ["01","03","05","07","08","10","12"]
months_with_28 = ["02"]



#
#SIGNIN TODAY
#To chenge the location/file we have to modify the open() function
#Get the name from the 1st user example: user = data["users"][0]["name"]
#
def today_check():
    m_date = date.today().strftime("%m")
    m_date_int = date_to_int(m_date)
    current_year_int = int(date.today().strftime("%Y"))
    lets_check(1, current_year_int, m_date_int, m_date)


#
#SignIn and Out fully month
#

def month_check(m_date):
    m_date_int = date_to_int(m_date)
    current_year_int = int(date.today().strftime("%Y"))

    #First we check if the month selected is the actually month, if it is, we will SignIn still today
    if date.today().strftime("%m") == m_date:
        month_day_int = int(date.today().strftime("%d"))
        lets_check(month_day_int, current_year_int, m_date_int, m_date)

    #If the month selected is pasted, we will do the SignIn and Out of this month.
    else:
        days = assign_days(m_date)
        lets_check(days, current_year_int, m_date_int, m_date)



def lets_check(days:int, current_year_int:int, m_date_int:int, m_date:str):

    #Reset de month day at 1st
    m_day = 1

    with open("data/data.json") as file_json:
        data = json.loads(file_json.read())
        #We will check day for day to do the Sign
        for i in range(days):
            current_date = date(year=current_year_int, month=m_date_int, day=m_day)
            if not current_date in cat_holidays and current_date.weekday() != 6:
                with open("docs/{}_{}.csv".format(current_year_int, m_date), 'a', newline='') as file:
                    csvwriter = csv.writer(file)
                
                    #SignIn log
                    for user in data["users"]:
                        if user["min_in"] == 0:
                            csvwriter.writerow([user["name"], Employee.random_oclock(user["hour_in"]), current_date, "CheckIn"])
                        
                        elif user["min_in"] == 30:
                            csvwriter.writerow([user["name"],Employee.random_half(user["hour_in"]), current_date, "CheckIn"])
                        
                        else:
                            print("Incorrect value range: the user {} only can SignIn at {}:0, or at {}:30".format(user["name"], user["hour_in"], user["hour_in"]))
                        
                    #SignOut log
                    for user in data["users"]:
                        if user["min_out"] == 0:
                            csvwriter.writerow([user["name"], Employee.random_oclock(user["hour_out"]), current_date, "CheckOut"])
                            
                        elif user["min_out"] == 30:
                            csvwriter.writerow([user["name"],Employee.random_half(user["hour_out"]), current_date, "CheckOut"])
                            
                        else:
                            print("Incorrect value range: the user {} only can SignOut at {}:0, or at {}:30".format(user["name"], user["hour_out"], user["hour_out"]))   
            m_day = m_day + 1




#Doing all Singns still today (at the same year)
def check_still_today():
    m_date = date.today().strftime("%m")
    m_date_int = date_to_int(m_date)

    for i in range(m_date_int-1):
        m_date_int = m_date_int -1
        if m_date_int < 9:
            month_check("0{}".format(str(m_date_int))) #We need to give it as string to operate with it
        else:
            month_check(str(m_date_int))
    
    month_check(m_date)



def assign_days(m_date:object):
    #Assigning the selected month the days it will have.
    if m_date in months_with_31:
        m_date = Month_31()
    elif m_date in months_with_30:
        m_date = Month_30()
    elif m_date in months_with_28:
        m_date = Months()
    
    return(m_date.days)



#Convert m_date:str into m_date int, to operate with it
def date_to_int(m_date:str):
    if m_date == "01" or m_date == "02" or m_date == "03" or m_date == "04" or m_date == "05" or m_date == "06" or m_date == "07" or m_date == "08" or m_date == "09":
        m_date_int = int(m_date[-1])
    else:
        m_date_int = int(m_date)
    
    return m_date_int



#check_still_today()
#today_check()
#month_check("01")
