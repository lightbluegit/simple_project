import pyautogui
import easyocr
import time
#从微信打开词达人 宽为930px 长拉满 放在屏幕最右边
def move_click(x, y):
    pyautogui.moveTo(x, y)
    pyautogui.click()

def choose(x, y, step):
    move_click(x, y)
    time.sleep(1.5)#万一点错了 响应要大概1.5S
    move_click(x, y + step)#点下一个选项
    time.sleep(1.5)
    move_click(x, y + step * 2)#防止第一次识别定位出问题 多点一次
    time.sleep(0.3)#给错误页面加载出来一下
    move_click(2450, 1450)#确认
    time.sleep(0.1)#防止点快了
    move_click(2450, 1450)

def solve():
    screenshot = pyautogui.screenshot(region = (2048, 531, 170, 170))#截取一小部分判定选项文字位置
    screenshot.save('test.png')
    reader = easyocr.Reader(['ch_sim', 'en'])
    result = reader.readtext('test.png')
    for i in result:
        choose(2048 + (i[0][1][0] + i[0][1][1])/2, 531 + (i[0][2][0] + i[0][2][1])/2, 90)#对于第一个文字(选项) 找到位置作为初始位置

move_click(2450, 1450)#全选完单词 设置完快速模式 运行程序
time.sleep(1)#等加载一下题
move_click(2490, 117)#跳过背诵题
time.sleep(0.2)#等加载
move_click(2085, 1488)
for i in range(125):#30个单词大概循环125次可以完成 有可能多 要手动暂停 基本没啥bug 能蒙个40~50分左右
    solve()