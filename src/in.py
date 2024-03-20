import random

def random_oclock(hour):
    hour_before = hour-1
    current_hour = random.choice([hour, hour_before])
    if current_hour == hour:
        minutes = random.randint(0,5)
        print("{}:0{}".format(current_hour, minutes))
    
    elif current_hour == hour_before:
        minutes = random.randint(55,59)
        print("{}:{}".format(current_hour, minutes))


def random_half(hour):
    minutes = random.randint(28,35)
    print("{}:{}".format(hour, minutes))


