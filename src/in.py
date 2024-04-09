#    /$$$$$$  /$$$$$$  /$$$$$$  /$$   /$$       /$$$$$$ /$$   /$$
#   /$$__  $$|_  $$_/ /$$__  $$| $$$ | $$      |_  $$_/| $$$ | $$
#  | $$  \__/  | $$  | $$  \__/| $$$$| $$        | $$  | $$$$| $$
#  |  $$$$$$   | $$  | $$ /$$$$| $$ $$ $$        | $$  | $$ $$ $$
#   \____  $$  | $$  | $$|_  $$| $$  $$$$        | $$  | $$  $$$$
#   /$$  \ $$  | $$  | $$  \ $$| $$\  $$$        | $$  | $$\  $$$
#  |  $$$$$$/ /$$$$$$|  $$$$$$/| $$ \  $$       /$$$$$$| $$ \  $$
#   \______/ |______/ \______/ |__/  \__/      |______/|__/  \__/
#                                                                
#                                                                
#                                                                
#    /$$$$$$  /$$$$$$$  /$$$$$$$                                 
#   /$$__  $$| $$__  $$| $$__  $$                                
#  | $$  \ $$| $$  \ $$| $$  \ $$                                
#  | $$$$$$$$| $$$$$$$/| $$$$$$$/                                
#  | $$__  $$| $$____/ | $$____/                                 
#  | $$  | $$| $$      | $$                                      
#  | $$  | $$| $$      | $$                                      
#  |__/  |__/|__/      |__/                                      
#                                                                
#                                                                
#  

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
        self.active = True
    
    def view(self):
        list = "{'name': '" + str(self.name) + "', 'hour_in': " + str(self.hour_in) + ", 'min_in': " + str(self.min_in) + ", 'hour_out': " + str(self.hour_out) + ", 'min_out': " + str(self.min_out) + ", 'active': " + str(self.active) + "}"
        return list


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
    m_day = int(date.today().strftime("%d"))
    lets_check(1, current_year_int, m_date_int, m_date, m_day)


#
#SignIn and Out fully month
#

def month_check(m_date):
    m_date_int = date_to_int(m_date)
    current_year_int = int(date.today().strftime("%Y"))

    #First we check if the month selected is the actually month, if it is, we will SignIn still today
    if date.today().strftime("%m") == m_date:
        month_day_int = int(date.today().strftime("%d"))

    #If the month selected is pasted, we will do the SignIn and Out of this month.
    else:
        month_day_int = assign_days(m_date)
    
    lets_check(month_day_int, current_year_int, m_date_int, m_date, 1)



def lets_check(days:int, current_year_int:int, m_date_int:int, m_date:str, m_day:int):

    #Reset de month day at 1st
    m_day = m_day

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


#
#SIGN ACTIONS
#


def user_new(name:str, hour_in:int, min_in:int, hour_out:int, min_out:int):
    usuari_nou = {'name': name, 'hour_in': hour_in, 'min_in': min_in, 'hour_out': hour_out, 'min_out': min_out, 'active': True}
    with open("data/data.json") as file_json:
        data = json.loads(file_json.read())
        users = data["users"]
        users.append(usuari_nou)

    users = {"users": users}
    with open("data/data.json", "w") as file_json:
        json.dump(users, file_json, indent=4)


def users_show():
    with open("data/data.json") as file_json:
        data = json.loads(file_json.read())
        users = data["users"]
        for i in range(len(users)):
            print("Name: {} \nTime In: {}:{} \nTime Out: {}:{}\n________________________________".format(users[i]["name"], users[i]["hour_in"], users[i]["min_in"], users[i]["hour_out"], users[i]["min_out"], users[i]["min_out"]))


def user_drop():
    with open("data/data.json") as file_json:
        data = json.loads(file_json.read())
        users = data["users"]
        print("¿Qué usuario quieres eliminar? (introduce el número del usuario)")
        for i in range(len(users)):
            print("{} - {}".format(i, users[i]["name"]))
        
        to_drop = int(input())
        print("¿Estás seguro que quieres eliminar a {}? S/N".format(users[to_drop]["name"]))
        respuesta2 = input()
    if respuesta2 == "S":
        with open("data/data.json") as file_json:
            data = json.loads(file_json.read())
            users = data["users"]
            del users[to_drop]
            for i in range(len(users)):
                print("{} - {}".format(i, users[i]["name"]))

    elif respuesta2 == "N":
        print("No se ha eliminado ningún usuario")
        

def user_update():
    with open("data/data.json") as file_json:
        data = json.loads(file_json.read())
        users = data["users"]
        print("¿Qué usuario quieres modificar? (introduce el número del usuario)")
        for i in range(len(users)):
            print("{} - {}".format(i, users[i]["name"]))
        
        to_modi = int(input())
        print("¿Qué campo quieres modificar de {}? nombre/entrada/salida/activo".format(users[to_modi]["name"]))
    campo = input()
    if campo == "nombre":
        with open("data/data.json") as file_json:
            data = json.loads(file_json.read())
            users = data["users"][to_modi]["name"]
            print("¿Qué nombre quieres ponerle al usuario seleccionado?")
            nombre = input()
            data["users"][to_modi]["name"] = nombre

        with open("data/data.json", "w") as file_json:
            json.dump(data, file_json, indent=4)

    elif campo == "entrada":
        with open("data/data.json") as file_json:
            data = json.loads(file_json.read())
            users = data["users"][to_modi]["name"]
            print("¿Qué hora de entrada quieres ponerle al usuario seleccionado? (Formato 24h)")
            hora = int(input())
            data["users"][to_modi]["hour_in"] = hora
            print("¿Qué minuto de entrada quieres ponerle al usuario seleccionado? (Si es en punto pon un único 0)")
            min = int(input())
            data["users"][to_modi]["min_in"] = min

        with open("data/data.json", "w") as file_json:
            json.dump(data, file_json, indent=4)


    elif campo == "salida":
        with open("data/data.json") as file_json:
            data = json.loads(file_json.read())
            users = data["users"][to_modi]["name"]
            print("¿Qué hora de entrada quieres ponerle al usuario seleccionado? (Formato 24h)")
            hora = int(input())
            data["users"][to_modi]["hour_out"] = hora
            print("¿Qué minuto de entrada quieres ponerle al usuario seleccionado? (Si es en punto pon un único 0)")
            min = int(input())
            data["users"][to_modi]["min_out"] = min

        with open("data/data.json", "w") as file_json:
            json.dump(data, file_json, indent=4)

    elif campo == "activo":
        with open("data/data.json") as file_json:
            data = json.loads(file_json.read())
            users = data["users"][to_modi]["name"]

            if data["users"][to_modi]["active"]:
                data["users"][to_modi]["active"] = False
                print("El usuario se ha desactivado")
            
            else:
                data["users"][to_modi]["active"] = True
                print("El usuario se ha activado")

        with open("data/data.json", "w") as file_json:
            json.dump(data, file_json, indent=4)
    
    else:
        print("Lo siento, no te he entendido")


#MAIN MENU
print('   SSSSSSSSSSSSSSS IIIIIIIIII      GGGGGGGGGGGGGNNNNNNNN        NNNNNNNN     IIIIIIIIIINNNNNNNN        NNNNNNNN\n SS:::::::::::::::SI::::::::I   GGG::::::::::::GN:::::::N       N::::::N     I::::::::IN:::::::N       N::::::N\nS:::::SSSSSS::::::SI::::::::I GG:::::::::::::::GN::::::::N      N::::::N     I::::::::IN::::::::N      N::::::N\nS:::::S     SSSSSSSII::::::IIG:::::GGGGGGGG::::GN:::::::::N     N::::::N     II::::::IIN:::::::::N     N::::::N\nS:::::S              I::::I G:::::G       GGGGGGN::::::::::N    N::::::N       I::::I  N::::::::::N    N::::::N\nS:::::S              I::::IG:::::G              N:::::::::::N   N::::::N       I::::I  N:::::::::::N   N::::::N\n S::::SSSS           I::::IG:::::G              N:::::::N::::N  N::::::N       I::::I  N:::::::N::::N  N::::::N\n  SS::::::SSSSS      I::::IG:::::G    GGGGGGGGGGN::::::N N::::N N::::::N       I::::I  N::::::N N::::N N::::::N\n    SSS::::::::SS    I::::IG:::::G    G::::::::GN::::::N  N::::N:::::::N       I::::I  N::::::N  N::::N:::::::N\n       SSSSSS::::S   I::::IG:::::G    GGGGG::::GN::::::N   N:::::::::::N       I::::I  N::::::N   N:::::::::::N\n            S:::::S  I::::IG:::::G        G::::GN::::::N    N::::::::::N       I::::I  N::::::N    N::::::::::N\n            S:::::S  I::::I G:::::G       G::::GN::::::N     N:::::::::N       I::::I  N::::::N     N:::::::::N\nSSSSSSS     S:::::SII::::::IIG:::::GGGGGGGG::::GN::::::N      N::::::::N     II::::::IIN::::::N      N::::::::N\nS::::::SSSSSS:::::SI::::::::I GG:::::::::::::::GN::::::N       N:::::::N     I::::::::IN::::::N       N:::::::N\nS:::::::::::::::SS I::::::::I   GGG::::::GGG:::GN::::::N        N::::::N     I::::::::IN::::::N        N::::::N\n SSSSSSSSSSSSSSS   IIIIIIIIII      GGGGGG   GGGGNNNNNNNN         NNNNNNN     IIIIIIIIIINNNNNNNN         NNNNNNN\n\n\nQué quieres hacer hoy?\n0 - Hacer el fichaje de hoy\n1 - Hacer el fichaje de un mes a elección\n2 - Hacer todos los fichajes del año hasta hoy\n3 - Crear un usuario\n4 - Modificar un usuario existente\n5 - Eliminar un usuario\n6 - Mostrar todos los usuarios\n')
main_answer = int(input(""))
if main_answer == 0:
    today_check()

elif main_answer == 1:
    print("¿De qué mes quieres hacer el fichaje? 01 - Enero, 02 - Febrero, (...), 12 - Diciembre")
    mont = input()
    month_check(mont)

elif main_answer == 2:
    check_still_today()

elif main_answer == 3:
    user_new()

elif main_answer == 4:
    user_update()

elif main_answer == 5:
    user_drop()

elif main_answer == 6:
    users_show()

else:
    print("Oh oh... Algo ha salido mal")