from datetime import date
import random
import time

def CheckVersion ():
    today = date.today()
    today == date.fromtimestamp(time.time())
    month = random.randint(1,6)
    day = random.randint(1,28)
    fin = date(2024, month, day)
    if today<fin :
        return True
    else :
        return False



def StrEnd(val):
    if val>6000 & val<6999:
        return""
    else :
        return "\\\\\r\n"