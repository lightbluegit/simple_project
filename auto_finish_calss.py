import pyautogui
import time
#打开网页版雨课堂 全屏
for _ in range(83):#页数
    time.sleep(3.1)#3.05可不可以？
    pyautogui.moveTo(1880, 1150)
    pyautogui.click()
pyautogui.moveTo(1000, 1000)#提示已经刷完