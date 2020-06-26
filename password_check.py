import requests
import sys
import hashlib
from tkinter import *

window = Tk()
window.title("password checker")
window.geometry("400x150")

def search_command():
    tb.delete("1.0","end")
    tb.insert("end",mainf(e1_value.get()))


def request_api(querry):
    murl = "https://api.pwnedpasswords.com/range/" + querry
    response = requests.get(murl)
    if response.status_code != 200:
        raise RuntimeError (f'error{response.status_code} please check again')
    else:
        return response

def pwned_api_check(mypass):
    sha1pass = hashlib.sha1(mypass.encode('utf-8')).hexdigest().upper()
    first5, last5 = sha1pass[:5] , sha1pass[5:]
    res = request_api(first5)
    return(get_pass_count(res,last5))

def get_pass_count(hashed,my_pass_hash):
    hashed = (line.split(':') for line in hashed.text.splitlines())
    for h, count in hashed:
        if h == my_pass_hash:
            return count
    return 0

def mainf(args):
    count = pwned_api_check(e1_value.get())
    if count:
        return(f"{e1_value.get()} was hacked {count} times.\n better choose another one")
    else :
        return(f"{e1_value.get()} is good")

l1 = Label(window,text="Enter Password")
l1.grid(row=0,column=0)

e1_value = StringVar()
e1 = Entry(window,textvariable = e1_value)
e1.grid(row=0, column=1)

b1 = Button(window,text='search',command=search_command)
b1.grid(row=0, column=3)

tb = Text(window, height = 7, width = 50)
tb.grid(row=1, column=0, rowspan = 3, columnspan = 7)

#scroll bar will be added another try

if __name__== "__main__":
    window.mainloop()