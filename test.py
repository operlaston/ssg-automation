import pyautogui
import time
import sys

def tab():
    pyautogui.press('tab')
def enter():
    pyautogui.press('enter')

inX = 1000


pyautogui.click(clicks=2, x=inX, y=269)
pyautogui.write("operlaston21@gmail.com")
tab()
pyautogui.write('a')
tab()
pyautogui.write('a')
conf = pyautogui.confirm("Add contact?", "Check", ["Yes", "No"])
if(conf == "No"):
    pyautogui.click(clicks=2, x=1405, y=146)
    time.sleep(1.5)
    pyautogui.click(1327, 197)
    sys.exit()
pyautogui.click(clicks=2, x=inX, y=536)
pyautogui.write("position")
tab()
pyautogui.write("company")
tab()
# City
pyautogui.write("n/a")
tab()
enter()
# State
pyautogui.write("n/a")
enter()
tab()
enter()
# Country
pyautogui.write("n/a")
enter()
# pyautogui.moveTo(1133, 481)
# pyautogui.scroll(-2000)
tab()
tab()
enter()
# Industry
pyautogui.write("technology")
enter()
tab()
enter()
# Sub-Industry
time.sleep(1)
pyautogui.write("it service")
enter()
pyautogui.press('esc')
tab()
tab()
enter()
# Project
pyautogui.write("royal")
enter()
pyautogui.press('esc')
time.sleep(0.5)
pyautogui.moveTo(1082, 799)
time.sleep(0.4)