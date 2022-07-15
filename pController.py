from pynput.mouse import Controller
from pynput.keyboard import Controller
# we cannot use both function at time

def mouseController():
    mouse = Controller()
    mouse.position = (10, 100)

# mouseController()

def keywordController():
    keyword = Controller()
    keyword.type("Courser position is here\n")
keywordController()
# Courser position is here
#
# pyinstaller --onefile pController.py
# pip install pyinstaller
