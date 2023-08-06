#This is the TerminalPyAPI, This can be used to fork TerminalPy easly and edit using TerminalPyAPI!
#Windows EDITION!

import os
import json

def init(name_of_the_app):
    print("Welcome to", name_of_the_app, "!")
def startTerminalPyAutomatedUserSetup(file, loadTime, IdUser):
    if loadTime == True:
        import time
    elif loadTime == False:
        pass
    else:
        pass
    if IdUser == True:
        import random
    elif IdUser == False:
        pass
    else:
        pass
    print("You'll be asked some questions...")
    print("Setting up the file...")
    try:
        time.sleep(2.5)
    except NameError:
        pass
    print("Doing the finishing touches...")
    try:
        time.sleep(1.5)
    except NameError:
        pass
    with open(file) as file:
        file.write('{Test : "test"}')
        data = json.load(file)
        TerminalAutomatedSetupName = input("Enter your name: ")
        data['User_Name'] = TerminalAutomatedSetupName
        TerminalAutomatedSetupPass = input("Enter a password(If you don't want leave it empty): ")
        data["User_Password"] = TerminalAutomatedSetupPass
        try:
            TerminalMainID = random.randint(1000, 999999)
            data["User_ID"] = TerminalMainID
        except NameError:
            pass
            
        del data['TEST']
        with open('UserInfo.json', 'w') as file:
            json.dump(data, file)
def run_your_app(file, running, input):
    #It's not the whole code of TerminalPy!
    #This only includes the print, exit and Reading a file
    def file_reading(file):
        try:
            TerminalMainFile = open(file, "r")
            c = 0
            ct = file.read()
            cl = ct.split("\n")
            for i in cl:
                if i:
                    c += 1
            print(f"Lines in the file are {c}")
        except FileNotFoundError:
            print("No Such File Found")
        except UnicodeDecodeError:
            print("Unsupported File")
    def print(input):
        print(input)
    def exit():
        os.system("cls")
        exit()