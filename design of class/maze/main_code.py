import sys#加速!加速!
import time#计时
import random#random_dfs打乱方向列表
import pygame#神金音效
import keyboard#为什么要任意按键 ...
import subprocess#用自运行做下一关
from queue import PriorityQueue#优先队列 A*要用 懒得自己做
import tkinter as tk#窗口 菜单创建
import customtkinter
from customtkinter import CTkToplevel
from datetime import datetime#获取日期
from PIL import Image, ImageDraw, ImageTk#pillow库 绘图 将PIL的图片转为tkinter格式
from tkinter import colorchooser, messagebox, StringVar#取色器 文本组件输入 输出 更新文本

prefix = 'design of class/text/'
log_path = prefix + 'log.txt'
default_setting_path = prefix + 'default setting.txt'
player_default_setting = prefix + 'player default setting.txt'

log_write_open = open(log_path, "a", encoding = 'UTF-8')#存储路径 时间..
default_setting_read_open = open(default_setting_path, "r", encoding = 'UTF-8')#默认设置 玩家不可修改 只用于恢复默认设置
player_default_setting_read_open = open(player_default_setting, "r", encoding = 'UTF-8')
default_setting_read = default_setting_read_open.readlines()
player_default_setting_read = player_default_setting_read_open.readlines()

color_list = []
#0:玩家路径颜色 1:玩家当前位置颜色 2:A*路径颜色 3:迷宫背景颜色 4:迷宫墙颜色
size_list = [0, 0, 3]#0:迷宫晶格边长 1:玩家路径边长 2:迷雾可见半径

flag = [0, 0, 0, 0, 0, 0]
'''0:是否已生成迷宫(1:随机dfs 2:随机prim 3:kruskal 4:递归分割) 
1:是否已经按下下一关按键 
2:当前游玩模式(0:未设置游戏模式 1:普通模式 2:迷雾模式 3:自动模式) 
3:迷雾模式(0:当前周围可见 1:路径周围可见) 
4:更改什么地方的音效(0:玩家移动音效 1:玩家通关音效)
5:A*显示哪个路径 (0:不显示 1:显示最终路径 2:显示探索路径 3:显示所有路径)
'''
code_path = 'design of class/main_code.py'
record_time = [0, 0]#记录玩家0:开始 1:结束游戏时间
position = [0, 0]#玩家当前位置
sound_effect_list = ["爆炸1.mp3", "爆炸2.mp3", "获得金币.mp3", "野!花!香!.mp3", "浴霸.wav"]#神金音效 哎 LDP
sound_effect_apply = [3, 2]#0:玩家移动音效 1:玩家通关音效
ctext_font = '华文楷体'; ctitle_font = '仿宋'

def refresh(event):
    try:
        root.destroy()
        subprocess.run(['python', code_path])#下一关
    except:
        pass

class two_queue:
    def __init__(self, rows, cols, num = 0):#num设置初始化为墙:0 路:1
        self.data = [[num for _ in range(cols)] for _ in range(rows)]
    def show(self):
        for i in self.data:
            print(i)
        print()

class ctktoplevel_frame(customtkinter.CTkToplevel):
    def __init__(self, master, title):
        super().__init__(master)
        self.title(title)
        def destroy_window(event):
            self.destroy()
        self.bind("<Escape>", destroy_window)
    
    def set_size(self, x, y, dx = 0, dy = 0):
        self.width = x
        self.high = y
        self.geometry("{}x{}+{}+{}".format(x, y, dx, dy))

class radiobutton_frame(customtkinter.CTkFrame):#单选框
    def __init__(self, master, title, values, default_value = ''):
        super().__init__(master)
        self.values = values
        self.title = title
        self.radiobuttons = []
        self.variable = customtkinter.StringVar(value=default_value)

        self.title = customtkinter.CTkLabel(self, text=self.title, fg_color="gray70", corner_radius=6, font=(ctitle_font, 24))
        self.title.grid(row=0, column=0, padx=10, pady=5, sticky="w")

        for i, value in enumerate(self.values):
            radiobutton = customtkinter.CTkRadioButton(
                self,
                text=value, 
                value=value,
                font=(ctext_font, 24),
                variable=self.variable,
                fg_color = '#BBFFFF',#选中颜色
                hover_color='#F0FFF0',
                border_color = '#7FFFD4',#未选中
            )
            radiobutton.grid(row = 0, column = i + 1, padx=10, pady=5, sticky="w")
            self.radiobuttons.append(radiobutton)

    def get(self):
        return self.variable.get()

    def set(self, value):
        self.variable.set(value)

class entry_frame(customtkinter.CTkFrame):#单选框
    def __init__(self, master, title, placeholder_text = '', default_value = ''):
        super().__init__(master)
        self.configure(fg_color = 'transparent')
        self.title = title

        self.title = customtkinter.CTkLabel(self, text=self.title, fg_color="gray70", corner_radius=6)
        self.title.grid(row=0, column=0, padx=10, pady=5, sticky="w")

        self.ctkentry = customtkinter.CTkEntry(self, placeholder_text = placeholder_text)
        if default_value != '': self.ctkentry.insert(0, default_value)
        self.ctkentry.grid(row = 0, column = 1, padx=10, pady=5, sticky="nsew")

    def get(self):
        return self.ctkentry.get()
    
    def set_size(self, width = 140, height = 28):
        self.ctkentry.configure(width = width, height = height)

class optionmenu_frame(customtkinter.CTkFrame):
    def __init__(self, master, title, button_name, values, default_value = ''):
        super().__init__(master)
        self.values = values
        self.default_value = default_value
        self.title = title
        self.radiobuttons = []
        self.variable = customtkinter.StringVar(value = default_value)

        self.title = customtkinter.CTkLabel(self, text=self.title, fg_color="gray70", corner_radius=6)
        self.title.grid(row=0, column=0, padx=10, pady=5, sticky="w")

        self.option_menu = customtkinter.CTkOptionMenu(self, values = self.values, variable = self.variable, command= lambda x: self.click(button_name))
        self.option_menu.grid(row = 0, column = 1, padx=10, pady=5)

    def get(self):
        return self.variable.get()
    
    def set_size(self, width = 140, height = 28):
        self.option_menu.configure(width = width, height = height)
    
    def click(self, button_name):
        if(button_name == '改音效'):
            relyi = 0.4; dy = 0.15
            if(self.get() == '更改玩家移动音效'):
                current_sound_effect.configure(text="当前移动音效:{}".format(sound_effect_list[sound_effect_apply[0]][:-4:]))
            if(self.get() == '更改玩家通关音效'):
                current_sound_effect.configure(text="当前通关音效:{}".format(sound_effect_list[sound_effect_apply[1]][:-4:]))
            sound = optionmenu_frame(effect_sound_page, "音效选择:",'选音效', ["爆炸1", "爆炸2", "获得金币", "野 花 香", "浴霸"], "野 花 香")
            sound.place(relx=0.5, rely=relyi, anchor="center")
            relyi += dy

            def confirm():
                effect_sound_attri = self.get()
                if(effect_sound_attri == '更改玩家移动音效'):
                    flag[4] = 0
                if(effect_sound_attri == '更改玩家通关音效'):
                    flag[4] = 1
                sound_dic = {"爆炸1":0, "爆炸2":1, "获得金币":2, "野 花 香":3, "浴霸":4}
                sound_effect_apply[flag[4]] = sound_dic[sound.get()]

            confirm_buttom = customtkinter.CTkButton(effect_sound_page, command = confirm, text='修改选中音效属性')
            confirm_buttom.place(relx=0.5, rely=relyi, anchor="center")
            relyi += dy
        
        if(button_name == '改大小'):#更改路径线条大小
            if(self.get() == '更改迷宫大小'):
                size_entry = entry_frame(size_page, '输入迷宫大小:', '长(最多81)宽(最多135) 输入奇数空格分隔)当前迷宫长:{} 宽{}'.format(hight, width))

            if(self.get() == '更改迷宫晶格大小'):
                size_entry = entry_frame(size_page, '输入迷宫晶格大小:', '(范围6~15)\n当前路径尺寸大小:{} 当前迷宫晶格大小:{}'.format(size_list[1], size_list[0]))

            if(self.get() == '更改路径线条大小'):
                size_entry = entry_frame(size_page, '输入玩家路径大小:', '(范围5~14)\n当前路径尺寸大小:{} 当前迷宫晶格大小:{}'.format(size_list[1], size_list[0]))

            if(self.get() == '更改迷雾可见半径大小'):
                size_entry = entry_frame(size_page, '输入迷雾可见半径:', "(范围1~3)\n当前可见半径:{}".format(size_list[2]))

            size_entry.set_size(200)
            size_entry.place(relx=0.5, rely=0.3, anchor="center")

            def confirm():
                size_get = size_entry.get()#
                if(self.get() == '更改迷宫大小'):
                    global im,hight, width
                    hight, width = map(int, size_get.strip().split())
                    if(hight & 1 == 0 or width & 1 == 0):
                        messagebox.showwarning("输入错误", "请输入奇数 否则迷宫会很奇怪")
                        return
                    if(hight > 81 or hight < 3 or width < 3 or width > 135):
                        messagebox.showwarning("输入错误", "请输入合适范围的数字")
                        return
                    im = Image.new("RGB", ((width + 2) * size_list[0], (hight + 2) * size_list[0]), color_list[3])#创建一个背景图片white +2作为边界
                    root.set_size(str(max((width + 2) * (size_list[0] - 4) + 50, 600)), str(max((hight + 2) * (size_list[0] - 4) + 50, 600)) ,800, 200)

                if(self.get() == '更改迷宫晶格大小'):
                    size_get = int(size_get)
                    if(size_get <= size_list[1] or size_get > 15):
                        messagebox.showwarning("输入错误", "请输入合适范围的数字")
                        return
                    size_list[0] = size_get

                if(self.get() == '更改路径线条大小'):
                    size_get = int(size_get)
                    if(size_get < 5 or size_get >= size_list[0]):
                        messagebox.showwarning("输入错误", "请输入合适范围的数字")
                        return
                    size_list[1] = size_get
                
                if(self.get() == '更改迷雾可见半径大小'):
                    size_get = int(size_get)
                    if(size_get < 1 or size_get > 3):
                        messagebox.showwarning("输入错误", "请输入合适范围的数字")
                        return
                    size_list[2] = size_get

            confirm_buttom = customtkinter.CTkButton(size_page, command = confirm, text='修改选中大小属性')
            confirm_buttom.place(relx=0.5, rely=0.45, anchor="center")

class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        self.title("迷 宫 游 戏")
        self.bind('<F5>', refresh)
        self.bind("<Escape>", self.root_destroy)
    
    def root_destroy(self, event=None):
        self.destroy()
    
    def set_size(self, x, y, dx, dy):
        self.width = x
        self.high = y
        self.geometry("{}x{}+{}+{}".format(x, y, dx, dy))

def update_root():
    root.update()
    for widget in root.pack_slaves():
        widget.destroy()#清除缓存画布
    global im
    tk_image = ImageTk.PhotoImage(im)#将PIL的Image对象转换为Tkinter可以识别的格式
    if(record_time[0]):
        label = tk.Label(root, image = tk_image, text="用时:{}".format(round(time.time() - record_time[0], 2)), font=("Arial", 20), compound="bottom")#将label组件的父组件设置为root(要放在的位置) 
    else:
        label = tk.Label(root, image = tk_image)
    label.image = tk_image#图像对象需要保持引用 否则图像可能会被垃圾回收机制回收 导致显示不出来(坑)
    label.pack()#将组件放到父组件中

def game_loop():
    if(True):
        update_root()
        if(break_move):#重新开始
            root.config(cursor="arrow")  # 恢复默认箭头光标
            record_changed_setting()
            root.destroy()
            sys.exit()
        root.after(50, game_loop)#每隔0.2秒更新一次GUI

def init_setting():
    global color_list, size_list, hight, width
    color_list_index = player_default_setting_read.index("color_list\n") + 1
    color_list = player_default_setting_read[color_list_index].strip().split(',')

    list_index = player_default_setting_read.index("size_list\n") + 1
    size_list = [*map(int, player_default_setting_read[list_index].strip().split(','))]

    list_index = player_default_setting_read.index("hight,width\n") + 1
    hight, width = map(int, player_default_setting_read[list_index].strip().split(','))
    
    sys.setrecursionlimit(5000)#小心递归深度爆了 默认1000

def reset_setting(event = None):#event给个默认值不然只能响应快捷键
    global color_list, size_list, hight, width
    color_list_index = default_setting_read.index("color_list\n") + 1
    color_list = default_setting_read[color_list_index].strip().split(',')

    list_index = player_default_setting_read.index("size_list\n") + 1
    size_list = default_setting_read[list_index].strip().split(',')
    for i in range(len(size_list)):
        size_list[i] = int(size_list[i])

    maze_size_index = default_setting_read.index("hight,width\n") + 1
    hight, width = map(int, default_setting_read[maze_size_index].strip().split(','))

def record_changed_setting():
    global color_list, size_list, hight, width
    list_index = player_default_setting_read.index("color_list\n") + 1
    player_default_setting_read[list_index] = ','.join(color_list) + '\n'

    list_index = player_default_setting_read.index("size_list\n") + 1
    player_default_setting_read[list_index] = ''
    for i in range(len(size_list) - 1):
        player_default_setting_read[list_index] += str(size_list[i]) + ','
    player_default_setting_read[list_index] += str(size_list[len(size_list) - 1]) + '\n'

    list_index = player_default_setting_read.index("hight,width\n") + 1
    player_default_setting_read[list_index] = str(hight) + ',' + str(width) + '\n'
    #print("更改后的设置为{}".format(player_default_setting_read))
    player_default_setting_write = open(player_default_setting, "w", encoding = 'UTF-8')#玩家可修改的默认设置 覆盖写直接
    player_default_setting_write.writelines(player_default_setting_read)
    player_default_setting_write.close()

def destory_window():
    try:
        change_menu_window.destroy()
    except:
        pass
    try:
        choose_fog_mode_window.destroy()
    except:
        pass


def init_algorithm_menu():
    algorithm_menu.add_command(label = "随机深搜算法", command = random_dfs, accelerator = "Ctrl + d")#编写实例选项
    root.bind("<Control-d>", random_dfs)
    algorithm_menu.add_separator() # 添加分隔线

    algorithm_menu.add_command(label = "prim算法", command = run_prim, accelerator = "Ctrl + p")
    root.bind("<Control-p>", run_prim)
    algorithm_menu.add_separator() # 添加分隔线

    algorithm_menu.add_command(label = "Kruskal最小生成树算法", command = run_kruskal, accelerator = "Ctrl + k")
    root.bind("<Control-k>", run_kruskal)
    algorithm_menu.add_separator() # 添加分隔线

    algorithm_menu.add_command(label = "递归分割算法", command = run_recursive_division, accelerator = "Ctrl + r")
    root.bind("<Control-r>", run_recursive_division)

def check_bound(x, y):
    if(0 <= x <= width and 0 <= y <= hight and visit.data[x][y] == 0):
        return True
    return False

def random_dfs_search(x, y, M):
    visit.data[x][y] = 1
    search_direction = [(2, 0), (-2, 0), (0, 2), (0, -2)]
    random.shuffle(search_direction)
    for dx, dy in search_direction:
        if(check_bound(x + dx, y + dy)):
            midx = (2 * x + dx) // 2; midy = (2 * y + dy) // 2
            visit.data[midx][midy] = 1
            M[midx][midy] = ' '
            random_dfs_search(x + dx, y + dy, M)

def random_dfs(event = None):
    global hight, width
    if(width * hight < 6e3):
        destory_window()
        menu_bar.delete('选择算法')
        menu_bar.delete('自定义设置')
        menu_bar.insert_cascade(0, label = "选择模式", menu = mode_menu)
        flag[0] = 1#标记已经生成迷宫
        draw = ImageDraw.Draw(im)#在im上绘画
        M = [[' ' for _ in range(width + 4)] for _ in range(hight + 4)]
        global visit
        visit = two_queue(hight + 2, width + 2)
        for i in range(hight + 2):
            if(i & 1):
                for j in range(0, width + 2, 2):
                    M[i][j] = '#'
            else:
                for j in range(width + 2):
                    M[i][j] = '#'
        for i in range(width + 2):
            M[0][i] = '#'
            M[hight + 1][i] = '#'
        try:
            random_dfs_search(1, 1, M)
        except IndexError:
            messagebox.showwarning("越界错误", "越界了越界了")
            hight = 15; width = 15
            root.destroy()
            record_changed_setting()
            subprocess.run(['python', 'design of class/main_code.py'])#下一关
        M[1][0] = ' '
        visit.data[1][0] = 1
        M[hight][width + 1] = ' '
        visit.data[hight][width + 1] = 1
        for i in range(len(M)):
            for j in range(len(M[0])):
                if(M[i][j] == '#'):
                    draw.rectangle(((j) * size_list[0], (i) * size_list[0] + 1, (j + 1) * size_list[0], (i + 1) * size_list[0]), fill = color_list[4])
                else:
                    draw.rectangle(((j) * size_list[0], (i) * size_list[0] + 1, (j + 1) * size_list[0], (i + 1) * size_list[0]), fill = color_list[3])
    else:
        messagebox.showwarning("可能越界","迷宫太大，可能越界")
        hight = 15; width = 15
        root.destroy()
        record_changed_setting()
        subprocess.run(['python', 'design of class/main_code.py'])#下一关

def recursive_division(start_x, start_y, end_x, end_y, M):
    global visit
    if start_x < end_x and start_y < end_y:
        split_x = random.choice(range(start_x + 1, end_x , 2))
        split_y = random.choice(range(start_y + 1, end_y, 2))
        left_x = random.choice(range(start_x, split_x, 2))
        right_x = random.choice(range(split_x + 1, end_x + 1, 2))
        up_y = random.choice(range(start_y, split_y, 2))
        down_y = random.choice(range(split_y + 1, end_y + 1, 2))
        d = random.randint(1,4)
        for i in range(start_y, end_y + 1):
            M[i][split_x] = '#'
            visit.data[i][split_x] = 0
        for i in range(start_x, end_x + 1):
            M[split_y][i] = '#'
            visit.data[split_y][i] = 0
        if d != 1:#左
            M[split_y][left_x] = ' '
            visit.data[split_y][left_x] = 1
        if d != 2:#右
            M[split_y][right_x] = ' '
            visit.data[split_y][right_x] = 1
        if d != 3:#上
            M[up_y][split_x] = ' '
            visit.data[up_y][split_x] = 1
        if d != 4:#下
            M[down_y][split_x] = ' '
            visit.data[down_y][split_x] = 1

        recursive_division(start_x, start_y, split_x - 1, split_y - 1, M)
        recursive_division(split_x + 1, start_y, end_x, split_y - 1, M)
        recursive_division(start_x, split_y + 1, split_x - 1, end_y, M)
        recursive_division(split_x + 1, split_y + 1, end_x, end_y, M)

def run_recursive_division(event = None):
    global visit
    destory_window()
    menu_bar.delete('选择算法')
    menu_bar.delete('自定义设置')
    menu_bar.insert_cascade(0, label = "选择模式", menu = mode_menu)
    visit = two_queue(hight + 2, width + 2, 1)#初始化值设为1 因为后续添加的是墙
    flag[0] = 4
    draw = ImageDraw.Draw(im)#在im上绘画
    M = [[' ' for _ in range(width + 2)] for _ in range(hight + 2)]
    for i in range(hight + 2):
        M[i][0] = '#'
        visit.data[i][0] = 0
        M[i][width + 1] = '#'
        visit.data[i][width + 1] = 0#visit.data = 0
    for i in range(width + 2):
        M[0][i] = '#'
        visit.data[0][i] = 0
        M[hight + 1][i] = '#'
        visit.data[hight + 1][i] = 0
    recursive_division(1, 1, width, hight, M)
    M[1][0] = ' '
    visit.data[1][0] = 1
    M[hight][width + 1] = ' '
    visit.data[hight][width + 1] = 1
    for i in range(len(M)):
        for j in range(len(M[0])):
            if(M[i][j] == '#'):
                draw.rectangle(((j) * size_list[0], (i) * size_list[0] + 1, (j + 1) * size_list[0], (i + 1) * size_list[0]), fill = color_list[4])

def kruskal(M):
    wall_list = []; path_list = [[()]]
    for i in range(1,hight + 1):
        for j in range(1, width + 1):#横向
            if(i & 1):
                if(j & 1):
                    path_list.append([(i, j)])
                    visit.data[i][j] = 1
                else:
                    M[i][j] = '#'
                    if(0 < j <= width):
                        wall_list.append((i, j, 'x'))#x轴延展
            else:
                M[i][j] = '#'
                if(j & 1):
                    wall_list.append((i, j, 'y'))#y轴延展
    while(len(wall_list)):
        random_index = random.randint(0,len(wall_list) - 1)
        random_wall = wall_list[random_index]
        index1 = 0; index2 = 0
        if(random_wall[2] == 'x'):
            cell1 = (random_wall[0], random_wall[1] + 1)
            cell2 = (random_wall[0], random_wall[1] - 1)
        elif(random_wall[2] == 'y'):
            cell1 = (random_wall[0] + 1, random_wall[1])
            cell2 = (random_wall[0] - 1, random_wall[1])
        flag = False
        for i in range(len(path_list)):
            if((cell1 in path_list[i]) and (cell2 in path_list[i])):
                flag = True
                del wall_list[random_index]
                break
            if(cell1 in path_list[i]):
                index1 = i
            if(cell2 in path_list[i]):
                index2 = i
        
        if(flag == False):
            M[random_wall[0]][random_wall[1]] = ' '
            visit.data[random_wall[0]][random_wall[1]] = 1
            del wall_list[random_index]
            for i in path_list[index2]:
                path_list[index1].append(i)
            del path_list[index2]

def run_kruskal(event = None):
    global visit
    destory_window()
    menu_bar.delete('选择算法')
    menu_bar.delete('自定义设置')
    menu_bar.insert_cascade(0, label = "选择模式", menu = mode_menu)
    visit = two_queue(hight + 2, width + 2)#初始化值设为0 因为后续清除的是墙
    flag[0] = 3
    draw = ImageDraw.Draw(im)#在im上绘画
    M = [[' ' for _ in range(width + 2)] for _ in range(hight + 2)]
    kruskal(M)
    for i in range(hight + 2):
        M[i][0] = '#'
        M[i][width + 1] = '#'
    for i in range(width + 2):
        M[0][i] = '#'
        M[hight + 1][i] = '#'
    M[1][0] = ' '
    visit.data[1][0] = 1
    M[hight][width + 1] = ' '
    visit.data[hight][width + 1] = 1
    #visit.show()
    for i in range(len(M)):
        for j in range(len(M[0])):
            if(M[i][j] == ' '):
                draw.rectangle(((j) * size_list[0], (i) * size_list[0] + 1, (j + 1) * size_list[0], (i + 1) * size_list[0]), fill = color_list[3])#填充中间
            elif(M[i][j] == '#'):
                draw.rectangle(((j) * size_list[0], (i) * size_list[0] + 1, (j + 1) * size_list[0], (i + 1) * size_list[0]), fill = color_list[4])#填充中间

def check_wall(x, y, wall_list):
    if(visit.data[x][y] == 0 and 0 < x <= width and 0 < y <= hight and (x, y) not in wall_list):
        return True
    return False
    
def prim(M):
    wall_list = [(1, 2, 'x'), (2, 1, 'y')]
    for i in range(1,hight + 1):
        for j in range(1, width + 1):#横向
            if(i & 1):
                if(j & 1 == 0):
                    M[i][j] = '#'
            else:
                M[i][j] = '#'
    while(len(wall_list)):
        random_index = random.randint(0,len(wall_list) - 1)
        random_wall = wall_list[random_index]
        if(random_wall[2] == 'x'):
            cell1 = (random_wall[0], random_wall[1] + 1)
            cell2 = (random_wall[0], random_wall[1] - 1)
        elif(random_wall[2] == 'y'):
            cell1 = (random_wall[0] + 1, random_wall[1])
            cell2 = (random_wall[0] - 1, random_wall[1])
        visit1 = False; visit2 = False
        if(visit.data[cell1[0]][cell1[1]]):
            visit1 = True
        if(visit.data[cell2[0]][cell2[1]]):
            visit2 = True
        if(visit1 & visit2):
            del wall_list[random_index]
        else:
            if(visit1):
                visit.data[cell2[0]][cell2[1]] = 1
                if(check_wall(cell2[0] + 1, cell2[1], wall_list)):
                    wall_list.append((cell2[0] + 1, cell2[1], 'y'))
                if(check_wall(cell2[0] - 1, cell2[1], wall_list)):
                    wall_list.append((cell2[0] - 1, cell2[1], 'y'))
                if(check_wall(cell2[0], cell2[1] + 1, wall_list)):
                    wall_list.append((cell2[0], cell2[1] + 1, 'x'))
                if(check_wall(cell2[0], cell2[1] - 1, wall_list)):
                    wall_list.append((cell2[0], cell2[1] - 1, 'x'))
            if(visit2):
                visit.data[cell1[0]][cell1[1]] = 1
                if(check_wall(cell1[0] + 1, cell1[1], wall_list)):
                    wall_list.append((cell1[0] + 1, cell1[1], 'y'))
                if(check_wall(cell1[0] - 1, cell1[1], wall_list)):
                    wall_list.append((cell1[0] - 1, cell1[1], 'y'))
                if(check_wall(cell1[0], cell1[1] + 1, wall_list)):
                    wall_list.append((cell1[0], cell1[1] + 1, 'x'))
                if(check_wall(cell1[0], cell1[1] - 1, wall_list)):
                    wall_list.append((cell1[0], cell1[1] - 1, 'x'))
            del wall_list[random_index]
            visit.data[random_wall[0]][random_wall[1]] = 1
            M[random_wall[0]][random_wall[1]] = ' '

def run_prim(event = None):
    global hight, width
    if(hight * width < 6e3):
        global visit
        destory_window()
        menu_bar.delete('选择算法')
        menu_bar.delete('自定义设置')
        menu_bar.insert_cascade(0, label = "选择模式", menu = mode_menu)
        visit = two_queue(hight + 2, width + 2)#初始化值设为0 因为后续清除的是墙
        visit.data[1][1] = 1
        flag[0] = 2
        draw = ImageDraw.Draw(im)#在im上绘画
        M = [[' ' for _ in range(width + 2)] for _ in range(hight + 2)]
        prim(M)
        for i in range(hight + 2):
            M[i][0] = '#'
            M[i][width + 1] = '#'
        for i in range(width + 2):
            M[0][i] = '#'
            M[hight + 1][i] = '#'
        M[1][0] = ' '
        visit.data[1][0] = 1
        M[hight][width + 1] = ' '
        visit.data[hight][width + 1] = 1
        for i in range(len(M)):
            for j in range(len(M[0])):
                if(M[i][j] == ' '):
                    draw.rectangle(((j) * size_list[0], (i) * size_list[0] + 1, (j + 1) * size_list[0], (i + 1) * size_list[0]), fill = color_list[3])#填充中间
                elif(M[i][j] == '#'):
                    draw.rectangle(((j) * size_list[0], (i) * size_list[0] + 1, (j + 1) * size_list[0], (i + 1) * size_list[0]), fill = color_list[4])#填充中间
    else:
        messagebox.showwarning("可能越界","迷宫太大，可能越界")
        hight = 15; width = 15
        root.destroy()
        record_changed_setting()
        subprocess.run(['python', 'design of class/main_code.py'])#下一关
        

def init_mode_menu():
    mode_menu.add_command(label = "普通模式", command = commen_mode, accelerator = "Ctrl + n")
    root.bind("<Control-n>", commen_mode)
    mode_menu.add_separator() # 添加分隔线
    mode_menu.add_command(label = "迷雾模式", command = fog_mode, accelerator = "Ctrl + f")
    root.bind("<Control-f>", fog_mode)
    mode_menu.add_separator() # 添加分隔线
    mode_menu.add_command(label = "A*速通", command = astar, accelerator = "Ctrl + a")
    root.bind("<Control-a>", astar)

def on_key_event(event = None):
    if event.event_type == keyboard.KEY_DOWN:
        flag[1] = True

def press_move(event : tk.Event):
    global move_path
    destory_window()
    draw = ImageDraw.Draw(im)#在im上绘画
    plus = (size_list[0] + size_list[1]) / 2
    decrease = (size_list[0] - size_list[1]) / 2
    if(event.keysym == "Up"):
        if( 0 <= position[0] <= width and 0 < position[1] - 1 <= hight and visit.data[position[1] - 1][position[0]] == 1):
            draw.rectangle((position[0] * size_list[0] + decrease, (position[1] - 1) * size_list[0] + decrease, position[0]  * size_list[0] + plus, position[1] * size_list[0] + plus), fill = color_list[0])
            position[1] -= 1

    if(event.keysym == "Down"):
        if(0 <= position[0] <= width and 0 < position[1] + 1 <= hight and visit.data[position[1] + 1][position[0]] == 1):
            draw.rectangle((position[0] * size_list[0] + decrease, position[1] * size_list[0] + decrease, position[0] * size_list[0] + plus, (position[1] + 1) * size_list[0] + plus), fill = color_list[0])
            position[1] += 1

    if(event.keysym == "Left"):
        if(0 <= position[0] - 1 <= width and 0 < position[1] <= hight and visit.data[position[1]][position[0] - 1] == 1):
            draw.rectangle(((position[0] - 1) * size_list[0] + decrease, position[1] * size_list[0] + decrease, position[0] * size_list[0] + plus, position[1] * size_list[0] + plus), fill = color_list[0])
            position[0] -= 1

    if(event.keysym == "Right"):
        if (position[0] == width and position[1] == hight):#结束状态
            if(flag[2]!=2):#不是迷雾模式 只需要用路径覆盖掉之前的位置颜色就好
                draw.rectangle((position[0] * size_list[0] + decrease, position[1] * size_list[0] + decrease, (position[0] + 1) * size_list[0] + plus, position[1] * size_list[0] + plus), fill = color_list[0])
            if(flag[2] == 2):#迷雾模式由于检测逻辑是在这个位置而且向右走 会有2个这个地方的颜色残留 即使这里以及destroy了 也会继续执行完这一部分 所以要额外吧当前位置变成迷宫墙的颜色
                draw.rectangle((position[0] * size_list[0] + decrease, position[1] * size_list[0] + decrease, position[0] * size_list[0] + plus, position[1] * size_list[0] + plus), fill = color_list[3])#
            draw.rectangle(((position[0] + 1) * size_list[0] + decrease, position[1] * size_list[0] + decrease, (position[0] + 1) * size_list[0] + plus, position[1] * size_list[0] + plus), fill = color_list[1])#表示当前位置
            flag[2] = 0
            sound = pygame.mixer.Sound('design of class/sound effect set/{}'.format(sound_effect_list[sound_effect_apply[1]]))
            sound.play()
            flag[1] = True
            record_time[1] = time.time()
            log_write_open.write("通关时间:{:.3f}\n".format(record_time[1] - record_time[0]))
            score = round(min((width * hight * 0.28) / len(move_path), 1) * 100, 2)#得分函数
            log_write_open.write("得分:{:.3f}\n".format(score))
            im.save('design of class/map set/map_record.png')
            messagebox.showinfo("恭喜过关", "你过关!\n得分:{}\n弹窗关闭后按下任意键进入下一关".format(score))
            root.config(cursor="arrow")#恢复鼠标光标
            keyboard.hook(on_key_event)
            while(flag[1] == False):#等待直到玩家按下任意按键
                time.sleep(0.2)
            root.destroy()
            record_changed_setting()
            subprocess.run(['python', 'design of class/main_code.py'])#下一关
        
        if(0 < position[0] + 1 <= (width + 1) and 0 < position[1] <= hight and visit.data[position[1]][position[0] + 1] == 1):
            draw.rectangle((position[0] * size_list[0] + decrease, position[1] * size_list[0] + decrease, (position[0] + 1) * size_list[0] + plus, position[1] * size_list[0] + plus), fill = color_list[0])
            position[0] += 1
    if(flag[1] == False):
        log_write_open.write("x = {}, y = {}\n".format(position[0], position[1]))
    move_path.append((position[0], position[1]))
    sound = pygame.mixer.Sound('design of class/sound effect set/{}'.format(sound_effect_list[sound_effect_apply[0]]))#玩家移动音效
    sound.play(loops=0, maxtime=800)
    if(flag[2] == 2):
        draw_no_fog_circle()
    if (flag[1] == False):
        draw.rectangle((position[0] * size_list[0] + decrease, position[1] * size_list[0] + decrease, position[0] * size_list[0] + plus, position[1] * size_list[0] + plus), fill = color_list[1])#表示当前位置
    

def commen_mode(event = None):
    destory_window()
    menu_bar.delete('选择模式')
    flag[2] = 1
    root.config(cursor="none")  # 隐藏鼠标光标
    draw = ImageDraw.Draw(im)#在im上绘画
    plus = (size_list[0] + size_list[1]) / 2
    decrease = (size_list[0] - size_list[1]) / 2
    draw.rectangle((decrease, size_list[0] + decrease, plus, size_list[0] + plus), fill = color_list[0])#画一下起点
    #visit.show()
    root.bind('<Up>', press_move)
    root.bind('<Down>', press_move)
    root.bind('<Left>', press_move)
    root.bind('<Right>', press_move)
    record_time[0] = time.time()#获取开始时间
    log_write_open.write("普通模式闯关 记录日期:{}\n".format(str(datetime.now())[:19]))

def draw_no_fog_circle_pos(now_x, now_y):
    draw = ImageDraw.Draw(im)#在im上绘画
    for x in range(max(0, now_x - size_list[2]), min(hight + 2, now_x + size_list[2])):
        for y in range(max(0, now_y - size_list[2]), min(width + 2, now_y + size_list[2])):
            if(visit.data[y][x] == 1):
                draw.rectangle(((x) * size_list[0], (y) * size_list[0] + 1, (x + 1) * size_list[0], (y + 1) * size_list[0]), fill = color_list[3])#填充中间
            elif(visit.data[y][x] == 0):
                draw.rectangle(((x) * size_list[0], (y) * size_list[0] + 1, (x + 1) * size_list[0], (y + 1) * size_list[0]), fill = color_list[4])#填充中间

def draw_no_fog_circle():
    if(flag[3] == 0):
        draw = ImageDraw.Draw(im)#在im上绘画
        draw.rectangle((0, 0, (width + 2) * size_list[0], (hight + 2) * size_list[0]), fill = "black")#重新覆盖
        draw_no_fog_circle_pos(position[0], position[1])
    elif(flag[3] == 1):
        draw = ImageDraw.Draw(im)#在im上绘画
        draw.rectangle((0, 0, (width + 2) * size_list[0], (hight + 2) * size_list[0]), fill = "black")#重新覆盖
        for x, y in move_path:
            draw_no_fog_circle_pos(x, y)

def mouse_click_left(event = None):
    if(flag[2] == 2):
        draw = ImageDraw.Draw(im)#在im上绘画
        plus = (size_list[0] + size_list[1]) / 2
        decrease = (size_list[0] - size_list[1]) / 2
        for i in range(1, len(move_path)):
            x = move_path[i][0]
            y = move_path[i][1]
            if(move_path[i][1] - move_path[i - 1][1] == 1):
                draw.rectangle((x * size_list[0] + decrease, (y - 1) * size_list[0] + decrease, x  * size_list[0] + plus, y * size_list[0] + plus), fill = color_list[0])

            if(move_path[i][1] - move_path[i - 1][1] == -1):
                draw.rectangle((x * size_list[0] + decrease, y * size_list[0] + decrease, x * size_list[0] + plus, (y + 1) * size_list[0] + plus), fill = color_list[0])

            if(move_path[i][0] - move_path[i - 1][0] == 1):
                draw.rectangle(((x - 1) * size_list[0] + decrease, y * size_list[0] + decrease, x * size_list[0] + plus, y * size_list[0] + plus), fill = color_list[0])

            if(move_path[i][0] - move_path[i - 1][0] == -1):
                draw.rectangle((x * size_list[0] + decrease, y * size_list[0] + decrease, (x + 1) * size_list[0] + plus, y * size_list[0] + plus), fill = color_list[0])

def fog_mode(event = None):
    flag[2] = 2
    destory_window()
    menu_bar.delete('选择模式')
    global choose_fog_mode_window
    choose_fog_mode_window = ctktoplevel_frame(root, "迷雾模式设置")
    choose_fog_mode_window.set_size(600, 220)
    def flag3_1():
        flag[3] = 1
        choose_fog_mode_window.destroy()
        record_time[0] = time.time()#防止还在选类型就开始计时
    title_size = 25
    torch_style = customtkinter.CTkButton(choose_fog_mode_window, text="探索型", command = flag3_1, font = (title_font, title_size))
    torch_style.place(x = 50, y = 20)#22号字体大约40px/字 两个text间隔60px
    explor_explain = customtkinter.CTkLabel(choose_fog_mode_window, text="照亮路径上所有格子的迷雾", font = ('华文宋体', 20))
    explor_explain.place(x = 200, y = 20)#解释性文字 y上的偏移量为15
    def flag3_0():
        flag[3] = 0
        choose_fog_mode_window.destroy()
        record_time[0] = time.time()
    explor_style = customtkinter.CTkButton(choose_fog_mode_window, text="火把型(默认)", command = flag3_0, font = (title_font, title_size))
    explor_style.place(x = 50, y = 80)
    torch_explain = customtkinter.CTkLabel(choose_fog_mode_window, text="只照亮当前格子周围的迷雾", font = ('华文宋体', 20))
    torch_explain.place(x = 190, y = 80)
    root.config(cursor="none")  # 隐藏鼠标光标
    draw = ImageDraw.Draw(im)#在im上绘画
    plus = (size_list[0] + size_list[1]) / 2
    decrease = (size_list[0] - size_list[1]) / 2
    draw.rectangle((decrease, size_list[0] + decrease, plus, size_list[0] + plus), fill = color_list[0])#画一下起点
    root.bind('<Up>', press_move)
    root.bind('<Down>', press_move)
    root.bind('<Left>', press_move)
    root.bind('<Right>', press_move)
    root.bind("<Button-1>", mouse_click_left)
    log_write_open.write("迷雾模式闯关 记录日期:{}\n".format(str(datetime.now())[:19]))

def astar_search(x, y, current_cost, pos_and_total_cost, go_back):
    global width, hight, astar_visit
    draw = ImageDraw.Draw(im)#在im上绘画
    astar_visit.append((x, y))
    plus = (size_list[0] + size_list[1]) / 2
    decrease = (size_list[0] - size_list[1]) / 2
    if(flag[5] == 2 or flag[5] == 3):
        draw.rectangle((x * size_list[0] + decrease, y * size_list[0] + decrease, x * size_list[0] + plus, y * size_list[0] + plus), fill = color_list[0])#以玩家路径颜色绘画A*探索路径
        update_root()
    if (x == width and y == hight):
        back_x = x; back_y = y
        while(back_x != 0 or back_y != 1):
            if(flag[5] == 1 or flag[5] == 3):
                update_root()
            now_x = back_x; now_y = back_y
            back_x, back_y = go_back[(back_x, back_y)]
            if(now_x - back_x == 1):#l
                draw.rectangle(((now_x - 1) * size_list[0] + decrease, now_y * size_list[0] + decrease, now_x * size_list[0] + plus, now_y * size_list[0] + plus), fill = color_list[2])
            if(now_x - back_x == -1):
                draw.rectangle((now_x * size_list[0] + decrease, now_y * size_list[0] + decrease, (now_x + 1) * size_list[0] + plus, now_y * size_list[0] + plus), fill = color_list[2])
            if(now_y - back_y == 1):#up
                draw.rectangle((now_x * size_list[0] + decrease, (now_y - 1) * size_list[0] + decrease, now_x * size_list[0] + plus, now_y * size_list[0] + plus), fill = color_list[2])
            if(now_y - back_y == -1):
                draw.rectangle((now_x * size_list[0] + decrease, now_y * size_list[0] + decrease, now_x * size_list[0] + plus, (now_y + 1) * size_list[0] + plus), fill = color_list[2])
        draw.rectangle((width * size_list[0] + decrease, hight * size_list[0] + decrease, (width + 1) * size_list[0] + plus, hight * size_list[0] + plus), fill = color_list[2])#补齐最后一格到出口的线条
        draw.rectangle((0 * size_list[0] + decrease, 1 * size_list[0] + decrease, (0 + 1) * size_list[0] + plus, 1 * size_list[0] + plus), fill = color_list[2])

        im.save('design of class/map set/map_record.png')
        messagebox.showinfo("<del>过关提示</del>", "你过关!\n?什么地方不太对?")
        root.config(cursor = "arrow")  # 恢复默认箭头光标
        keyboard.hook(on_key_event)
        while(flag[1] == False):#等待直到玩家按下任意按键
            time.sleep(0.2)
        flag[2] = 0
        #log_write_open.write("A*通关\n")
        draw.rectangle((0, 0, width * size_list[0], hight * size_list[0]), fill = "white")#重置空白画布
        root.destroy()
        record_changed_setting()
        subprocess.run(['python', 'design of class/main_code.py'])
    
    def manhattan_distance(start, end):#曼哈顿距离
        return abs(start[0] - end[0]) + abs(start[1] - end[1])
    
    #4向搜索 计算总花费和可走路径
    if(0 < x <= width and 0 < y + 1 <= hight and visit.data[y + 1][x] == 1 and (x, y + 1) not in astar_visit):
        pos_and_total_cost.put((manhattan_distance((x, y + 1), (width, hight)) + current_cost[(x, y)] + 1, (x, y + 1)))
        current_cost[(x, y + 1)] = current_cost[(x, y)] + 1
        go_back[(x, y + 1)] = (x, y)
    if(0 < x + 1 <= width and 0 < y <= hight and visit.data[y][x + 1] == 1 and (x + 1, y) not in astar_visit):
        pos_and_total_cost.put((manhattan_distance((x + 1, y), (width, hight)) + current_cost[(x, y)] + 1, (x + 1, y))) 
        current_cost[(x + 1, y)] = current_cost[(x, y)] + 1
        go_back[(x + 1, y)] = (x, y)
    if(0 < x <= width and 0 < (y - 1) <= hight and visit.data[y - 1][x] == 1 and (x, (y - 1)) not in astar_visit):
        pos_and_total_cost.put((manhattan_distance((x, y - 1), (width, hight)) + current_cost[(x, y)] + 1, (x, y - 1)))
        current_cost[(x, y - 1)] = current_cost[(x, y)] + 1
        go_back[(x, y - 1)] = (x, y)
    if(0 < (x - 1) <= width and 0 < y <= hight and visit.data[y][x - 1] == 1 and ((x - 1), y) not in astar_visit):
        pos_and_total_cost.put((manhattan_distance((x - 1, y), (width, hight)) + current_cost[(x, y)] + 1, (x - 1, y))) 
        current_cost[(x - 1, y)] = current_cost[(x, y)] + 1
        go_back[(x - 1, y)] = (x, y)

    next_place = pos_and_total_cost.get()
    x = next_place[1][0]
    y = next_place[1][1]
    try:
        astar_search(x, y, current_cost, pos_and_total_cost, go_back)
    except RecursionError:
        messagebox.showwarning("递归错误", "爆深度了!")
        pass
    '''    if(dir == 'd'):
            draw.rectangle((x * size_list[0] + decrease, y * size_list[0] + decrease, x * size_list[0] + plus, (y + 1) * size_list[0] + plus), fill = color_list[2])
            astar_search(x, y + 1)
        if(dir == 'u'):
            draw.rectangle((x * size_list[0] + decrease, (y - 1) * size_list[0] + decrease, x  * size_list[0] + plus, y * size_list[0] + plus), fill = color_list[2])
            astar_search(x, y - 1)
        if(dir == 'l'):
            draw.rectangle(((x - 1) * size_list[0] + decrease, y * size_list[0] + decrease, x * size_list[0] + plus, y * size_list[0] + plus), fill = color_list[2])
            astar_search(x - 1, y)'''

def astar(event = None):
    global astar_visit
    destory_window()
    try:
        menu_bar.delete('选择模式')
    except:
        pass
    astar_visit = []
    current_cost = {(0, 1) : 0}#走到(x, y)需要的步数为x
    go_back = {}
    pos_and_total_cost = PriorityQueue()#(x, y)处总花费为x
    astar_search(0, 1, current_cost, pos_and_total_cost, go_back)


def init_other_menu():
    other_menu.add_command(label = "查看最好成绩", command = best_score, accelerator = "Alt + b")
    root.bind("<Alt-b>", best_score)#严格区分大小写
    other_menu.add_separator() # 添加分隔线

    def clean_log(event = None):
        _ = open(log_path, 'w', encoding = "UTF-8")
    other_menu.add_command(label = "重置得分记录表", command = clean_log, accelerator = "Alt + c")
    root.bind("<Alt-c>", clean_log)
    other_menu.add_separator() # 添加分隔线

    other_menu.add_command(label = "退出游戏", command = Break_move, accelerator = "Esc")#加入快捷键(只是个提示 实际效果要自己做)
    root.bind("<Escape>", Break_move)

def best_score(event = None):
    log_read_open = open(log_path, 'r', encoding = "UTF-8")
    contents = log_read_open.readlines()
    max_score = 0
    if(len(contents)):
        for line in contents:
            if(line[:3] == "得分:"):
                max_score = max(max_score, float(line[3:].strip()))
        messagebox.showinfo("查找最高分", "最高分是:{}\n".format(max_score))
    else:
        messagebox.showinfo("查找最高分", "暂无成绩")
    log_read_open.close()

def Break_move(event = None):
    global break_move
    break_move = 1


def init_change_menu():
    global change_menu_window, effect_sound_page, size_page, color_page, astar_page
    change_menu_window = ctktoplevel_frame(root, "自定义设置")
    change_menu_window.set_size(400, 350, 150, 521)
    def refresh_init_change_menu(event):
        change_menu_window.destroy()
        init_change_menu()
    change_menu_window.bind("<F5>", refresh_init_change_menu)

    tab_window = customtkinter.CTkTabview(change_menu_window, width=300, height=200, corner_radius=10, fg_color="lightblue")
    tab_window.pack(fill="both", expand=True, padx=20, pady=20)

    size_page = tab_window.add('大小')
    color_page = tab_window.add('颜色')
    effect_sound_page = tab_window.add('音效')
    astar_page = tab_window.add('A*显示')
    size_settings_window(size_page)
    color_settings_window(color_page)
    effect_sound_settings_window(effect_sound_page)
    astar_settings_window(astar_page)
    
    reset_buttom = customtkinter.CTkButton(tab_window, command = reset_setting, text='重置所有设置')
    reset_buttom.place(relx=0.15, rely=0.8, anchor="center")

def size_settings_window(master):
    size_change = optionmenu_frame(master, "选择要改变的大小属性:",'改大小', ["更改迷宫大小", "更改迷宫晶格大小", "更改路径线条大小", "更改迷雾可见半径大小"])
    size_change.configure(fg_color = 'transparent')
    size_change.place(relx=0.5, rely=0.1, anchor="center")

def color_settings_window(master):
    color_change = optionmenu_frame(master, "选择要改变的颜色属性:",'改颜色', ["更改窗口背景颜色", "更改玩家当前位置颜色", "更改玩家路径颜色", "更改A*路径颜色", '更改迷宫背景颜色', '更改迷宫墙壁颜色'], "更改窗口背景颜色")
    color_change.configure(fg_color = 'transparent')
    color_change.place(relx=0.5, rely=0.1, anchor="center")

    def confirm():
        color_attri = color_change.get()
        if(color_attri == '更改窗口背景颜色'):
            change_root_backgroud_color()
        if(color_attri == '更改玩家当前位置颜色'):
            change_player_point_color()
        if(color_attri == '更改玩家路径颜色'):
            change_player_path_color()
        if(color_attri == '更改A*路径颜色'):
            change_astar_path_color()
        if(color_attri == '更改迷宫背景颜色'):
            change_labyrinth_backgroud_color()
        if(color_attri == '更改迷宫墙壁颜色'):
            change_labyrinth_wall_color()

    confirm_buttom = customtkinter.CTkButton(master, command = confirm, text='修改选中颜色属性')
    confirm_buttom.place(relx=0.5, rely=0.3, anchor="center")

def change_root_backgroud_color():
    chosed_color = colorchooser.askcolor(title = "猛男就该用猛男粉!")
    if(chosed_color[1] != None):
        root.configure(bg = chosed_color[1])

def change_player_path_color():
    chosed_color = colorchooser.askcolor(title = "猛男就该用猛男粉!")
    print(chosed_color)
    if(chosed_color[1] != None):
        color_list[0] = chosed_color[1]

def change_player_point_color():
    chosed_color = colorchooser.askcolor(title = "猛男就该用猛男粉!")
    if(chosed_color[1] != None):
        color_list[1] = chosed_color[1]

def change_astar_path_color():
    chosed_color = colorchooser.askcolor(title = "猛男就该用猛男粉!")
    if(chosed_color[1] != None):
        color_list[2] = chosed_color[1]

def change_labyrinth_backgroud_color():
    chosed_color = colorchooser.askcolor(title = "猛男就该用猛男粉!")
    if(chosed_color[1] != None):
        color_list[3] = chosed_color[1]

def change_labyrinth_wall_color():
    chosed_color = colorchooser.askcolor(title = "猛男就该用猛男粉!")
    if(chosed_color[1] != None):
        color_list[4] = chosed_color[1]

def effect_sound_settings_window(master):
    global effect_sound_change, current_sound_effect
    effect_sound_change = optionmenu_frame(master, "选择要改变的音效属性:",'改音效', ["更改玩家移动音效", "更改玩家通关音效"])
    effect_sound_change.configure(fg_color = 'transparent')
    effect_sound_change.place(relx=0.5, rely=0.1, anchor="center")
    
    current_sound_effect = customtkinter.CTkLabel(effect_sound_page, text="当前移动音效:{}".format(sound_effect_list[sound_effect_apply[0]][:-4:]), font=(title_font, 23))
    current_sound_effect.place(relx=0.5, rely=0.25, anchor="center")

def astar_settings_window(master):
    def confirm():
        flag[5] = explor_var.get() + back_var.get()
        print(flag[5])
        master.destroy()
    rowi = 0
    title_size = 25
    if(flag[5] == 0):
        customtkinter.CTkLabel(master, text="当前状态:不显示动画", font=(title_font, title_size)).grid(row = rowi, column = 0, padx=10, pady=10)
    elif(flag[5] == 1):
        customtkinter.CTkLabel(master, text="当前状态:显示回溯动画", font=(title_font, title_size)).grid(row = rowi, column = 0, padx=10, pady=10)
    elif(flag[5] == 2):
        customtkinter.CTkLabel(master, text="当前状态:显示探索动画", font=(title_font, title_size)).grid(row = rowi, column = 0, padx=10, pady=10)
    elif(flag[5] == 3):
        customtkinter.CTkLabel(master, text="当前状态:显示所有动画", font=(title_font, title_size)).grid(row = rowi, column = 0, padx=10, pady=10)
    rowi += 1
    
    explor_var = customtkinter.IntVar()
    explor = customtkinter.CTkCheckBox(master, text="启用探索动画", variable=explor_var, font = (title_font, title_size), onvalue=2, offvalue=0)
    explor.grid(row = rowi, column = 0, padx=10, pady=10)
    rowi += 1

    back_var = customtkinter.IntVar()
    back = customtkinter.CTkCheckBox(master, text="启用回溯动画", variable=back_var, font = (title_font, title_size), onvalue=1, offvalue=0)
    back.grid(row = rowi, column = 0, padx=10, pady=10)
    rowi += 1

    confrim_button = customtkinter.CTkButton(master, text="确定", command=confirm)
    confrim_button.grid(row = rowi, column = 0, padx=10, pady=10)
    rowi+=1


def solve():
    pygame.init()#神币音效
    pygame.mixer.init()
    global hight, width, im, root, break_move, move_path, menu_bar
    move_path = [(0, 1)]#81*135的迷宫 size_list[0]控制每一个方块大小
    init_setting()#初始化设置
    im = Image.new("RGB", ((width + 2) * size_list[0], (hight + 2) * size_list[0]), color_list[3])#创建一个背景图片white +2作为边界
    break_move = False; position[0] = 0; position[1] = 1#初始化起点
    root = App()
    root.set_size(str(max((width + 2) * (size_list[0] - 4) + 50, 600)), str(max((hight + 2) * (size_list[0] - 4) + 50, 600)) ,800, 200)

    global title_font, text_font, english_font
    title_font = "design of class/fonts/NotoSerifSC-VariableFont_wght.ttf"
    text_font = "华文楷体"
    english_font = "design of class/fonts/Exo-VariableFont_wght.ttf"

    menu_bar = tk.Menu(root)#创建菜单栏(空)
    global algorithm_menu
    algorithm_menu = tk.Menu(menu_bar, tearoff = 0, font=(english_font, 14))#创建菜单上的项目
    algorithm_menu.config(font=(title_font, 16))
    init_algorithm_menu()#初始化项目
    menu_bar.add_cascade(label = "选择算法", menu = algorithm_menu)#添加显示
    global mode_menu
    mode_menu = tk.Menu(menu_bar, tearoff = 0, font=(english_font, 14))
    mode_menu.config(font=(title_font, 16))
    init_mode_menu()

    global other_menu
    other_menu = tk.Menu(menu_bar, tearoff = 0, font=(english_font, 14))
    other_menu.config(font=(title_font, 16))
    init_other_menu()
    menu_bar.add_cascade(label = "其他设置", menu = other_menu)

    menu_bar.add_command(label = "自定义设置", command = init_change_menu)

    root.config(menu = menu_bar)#启用菜单栏
    game_loop()#启动更新循环
    root.mainloop()#展示根组件bott
    pygame.quit()
    log_write_open.close()
    default_setting_read_open.close()

def main():
    solve()

main()
