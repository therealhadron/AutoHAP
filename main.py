from time import sleep

import pywinauto
from pywinauto.application import Application

PROGRAM_PATH = 'C:\E20-II\HAP42\CODE\hap42.exe'
# represents the HAP application object
applicationHAP = None
mainForm = None

# Starts the carrier HAP application
def start_HAP(program_path = PROGRAM_PATH):
    global applicationHAP
    try:
        applicationHAP = Application(backend="win32").start(program_path)
    except:
        print("Path not found")

# Clicks OK
def dimiss_start_screen():
    global mainForm
    try:
        applicationHAP.ThunderRT6FormDC['AfxWnd40'].OK.click()
        mainForm = applicationHAP.ThunderRT6FormDC
    except:
        print("Application does not exist")

def main():
    start_HAP()
    dimiss_start_screen()
    # Clicks into "Spaces"
    mainForm.ListView.select(1).click_input(double=True)

    # Clicks into "New default space"
    mainForm.ListView.select(0).click_input(double=True)

main()

