'''
python课设
'''
import sys#加速!加速!
import time#计时
import random#random_dfs打乱方向列表
import pygame#神金音效
import keyboard#为什么要任意按键 ...
import subprocess#用自运行做下一关
from queue import PriorityQueue#优先队列 A*要用 懒得自己做
import tkinter as tk#窗口 菜单创建
from datetime import datetime#获取日期
from PIL import Image, ImageDraw, ImageTk#pillow库 绘图 将PIL的图片转为tkinter格式
from tkinter import colorchooser, simpledialog, messagebox, StringVar#取色器 文本组件输入 输出 更新文本

input = sys.stdin.readline
log_write_open = open("design of class/maze/text/log.txt", "a", encoding = 'UTF-8')#存储路径 时间..
default_setting_read_open = open("design of class/maze/text/default setting.txt", "r", encoding = 'UTF-8')#默认设置 玩家不可修改 只用于恢复默认设置
player_default_setting_read_open = open("design of class/maze/text/player default setting.txt", "r", encoding = 'UTF-8')
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
record_time = [0, 0]#记录玩家0:开始 1:结束游戏时间
position = [0, 0]#玩家当前位置
sound_effect_list = ["explosion 1.mp3", "explosion 2.mp3", "coin received1.mp3", "wild_flower_Hardcore.mp3", "Daisuke.wav"]#神金音效 哎 LDP
sound_effect_apply = [3, 2]#0:玩家移动音效 1:玩家通关音效

class two_queue:
    def __init__(self, rows, cols, num = 0):#num设置初始化为墙:0 路:1
        self.data = [[num for _ in range(cols)] for _ in range(rows)]
    def show(self):
        for i in self.data:
            print(i)
        print()

def load_image(im):
    tk_image = ImageTk.PhotoImage(im)#将PIL的Image对象转换为Tkinter可以识别的格式
    if(record_time[0]):
        label = tk.Label(root, image = tk_image, text="用时:{}".format(round(time.time() - record_time[0], 2)), font=("Arial", 20), compound="bottom")#将label组件的父组件设置为root(要放在的位置) 
    else:
        label = tk.Label(root, image = tk_image)
    '''
    text-compound('top'、'bottom'、'left'、'right'、'center')一起用才能在图形上显示文字
    fg 和 bg: 分别用于设置前景色（文本颜色）和背景色。
    font: 用于设置字体样式。
    '''
    label.image = tk_image#图像对象需要保持引用 否则图像可能会被垃圾回收机制回收 导致显示不出来(坑)
    label.pack()#将组件放到父组件中

def update_root(im):
    root.update()
    for widget in root.pack_slaves():
        widget.destroy()#清除缓存画布！
    load_image(im)

def game_loop():
    if(True):
        update_root(im)
        if(break_move):#重新开始
            root.config(cursor="arrow")  # 恢复默认箭头光标
            record_changed_setting()
            root.destroy()
            sys.exit()
        root.after(5, game_loop)#每隔0.2秒更新一次GUI

def init_maze():
    draw = ImageDraw.Draw(im)#在im上绘画
    draw.rectangle((0, 0, (width + 2) * size_list[0], (hight + 2) * size_list[0]), fill = color_list[3])#填充中间

def init_setting():
    global color_list, size_list, hight, width
    color_list_index = player_default_setting_read.index("color_list\n") + 1
    color_list = player_default_setting_read[color_list_index].strip().split(',')

    list_index = player_default_setting_read.index("size_list\n") + 1
    size_list = [*map(int, player_default_setting_read[list_index].strip().split(','))]

    list_index = player_default_setting_read.index("hight,width\n") + 1
    hight, width = map(int, player_default_setting_read[list_index].strip().split(','))
    
    sys.setrecursionlimit(10000)#小心递归深度爆了 默认1000

def reset_setting(event = 0):#event给个默认值不然只能响应快捷键
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
    player_default_setting_write = open("design of class/maze/text/player default setting.txt", "w", encoding = 'UTF-8')#玩家可修改的默认设置 覆盖写直接
    player_default_setting_write.writelines(player_default_setting_read)
    player_default_setting_write.close()

def destory_window():
    try:
        size_setting_window.destroy()
    except:
        pass
    try:
        color_setting_window.destroy()
    except:
        pass
    try:
        effect_sound_setting_window.destroy()
    except:
        pass
    try:
        choose_fog_mode_window.destroy()
    except:
        pass
    try:
        astar_sound_setting_window.destroy()
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

def get_now_algorithm():
    if(flag[0] == 1):
        now_algorithm = "随机dfs算法"
    elif(flag[0] == 2):
        now_algorithm = "随机prim算法"
    elif(flag[0] == 3):
        now_algorithm = "kruskal算法"
    elif(flag[0] == 4):
        now_algorithm = "递归分割算法"
    messagebox.showwarning("流程错误", "迷宫已经用{}初始化 该选择模式了".format(now_algorithm))

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

def random_dfs(event = 0):
    if(flag[0] == 0):
        global hight, width
        if(width * hight < 6e3):
            destory_window()
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
                subprocess.run(['python', 'design of class/maze/main_code.py'])#下一关

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
            subprocess.run(['python', 'design of class/maze/main_code.py'])#下一关
    else:
        get_now_algorithm()

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

def run_recursive_division(event = 0):
    if(flag[0] == 0):
        global visit
        destory_window()
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
    else:
        get_now_algorithm()

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

def run_kruskal(event = 0):
    if(flag[0] == 0):
        global visit
        destory_window()
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
    else:
        get_now_algorithm()

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

def run_prim(event = 0):
    if(flag[0] == 0):
        global hight, width
        if(hight * width < 6e3):
            global visit
            destory_window()
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
            subprocess.run(['python', 'design of class/maze/main_code.py'])#下一关
    else:
        get_now_algorithm()
        

def init_mode_menu():
    mode_menu.add_command(label = "普通模式", command = commen_mode, accelerator = "Ctrl + n")
    root.bind("<Control-n>", commen_mode)
    mode_menu.add_separator() # 添加分隔线
    mode_menu.add_command(label = "迷雾模式", command = fog_mode, accelerator = "Ctrl + f")
    root.bind("<Control-f>", fog_mode)
    mode_menu.add_separator() # 添加分隔线
    mode_menu.add_command(label = "A*速通", command = astar, accelerator = "Ctrl + a")
    root.bind("<Control-a>", astar)

def on_key_event(event = 0):
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
            sound = pygame.mixer.Sound('design of class/maze/sound effect set/{}'.format(sound_effect_list[sound_effect_apply[1]]))
            sound.play()
            flag[1] = True
            record_time[1] = time.time()
            log_write_open.write("通关时间:{:.3f}\n".format(record_time[1] - record_time[0]))
            score = round(min((width * hight * 0.28) / len(move_path), 1) * 100, 2)#得分函数
            log_write_open.write("得分:{:.3f}\n".format(score))
            im.save('design of class/maze/map set/map_record.png')
            messagebox.showinfo("恭喜过关", "你过关!\n得分:{}\n弹窗关闭后按下任意键进入下一关".format(score))
            root.config(cursor="arrow")#恢复鼠标光标
            keyboard.hook(on_key_event)
            while(flag[1] == False):#等待直到玩家按下任意按键
                time.sleep(0.2)
            root.destroy()
            record_changed_setting()
            subprocess.run(['python', 'design of class/maze/main_code.py'])#下一关
        
        if(0 < position[0] + 1 <= (width + 1) and 0 < position[1] <= hight and visit.data[position[1]][position[0] + 1] == 1):
            draw.rectangle((position[0] * size_list[0] + decrease, position[1] * size_list[0] + decrease, (position[0] + 1) * size_list[0] + plus, position[1] * size_list[0] + plus), fill = color_list[0])
            position[0] += 1
    if(flag[1] == False):
        log_write_open.write("x = {}, y = {}\n".format(position[0], position[1]))
    move_path.append((position[0], position[1]))
    sound = pygame.mixer.Sound('design of class/maze/sound effect set/{}'.format(sound_effect_list[sound_effect_apply[0]]))#玩家移动音效
    sound.play(loops=0, maxtime=800)
    if(flag[2] == 2):
        draw_no_fog_circle()
    if (flag[1] == False):
        draw.rectangle((position[0] * size_list[0] + decrease, position[1] * size_list[0] + decrease, position[0] * size_list[0] + plus, position[1] * size_list[0] + plus), fill = color_list[1])#表示当前位置
    

def commen_mode(event = 0):
    if(flag[0]):
        if(flag[2] == 0):
            destory_window()
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
        else:
            messagebox.showwarning("流程错误", "选定模式无法更改")
    else:
        messagebox.showwarning("流程错误", "迷宫还没初始好 你先不要急着跑")

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

def mouse_click_left(event = 0):
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

def fog_mode(event = 0):
    if(flag[0] != 0):
        if(flag[2] == 0):
            flag[2] = 2
            destory_window()
            global choose_fog_mode_window
            choose_fog_mode_window = tk.Toplevel(root)
            choose_fog_mode_window.title("迷雾模式设置")
            choose_fog_mode_window.geometry('600x220')
            def choose_fog_mode_window_destroy(event = 0):
                choose_fog_mode_window.destroy()
            choose_fog_mode_window.bind("<Escape>", choose_fog_mode_window_destroy)
            def flag3_1():
                flag[3] = 1
                choose_fog_mode_window.destroy()
                record_time[0] = time.time()#防止还在选类型就开始计时
            torch_style = tk.Button(choose_fog_mode_window, text="探索型", command = flag3_1, fg = '#11FBFF', font = ('华文楷体', 22))
            torch_style.place(x = 50, y = 20)#22号字体大约40px/字 两个text间隔60px
            explor_explain = tk.Label(choose_fog_mode_window, text="照亮路径上所有格子的迷雾", fg = '#11FBFF', font = ('华文宋体', 20))
            explor_explain.place(x = 170, y = 35)#解释性文字 y上的偏移量为15
            def flag3_0():
                flag[3] = 0
                choose_fog_mode_window.destroy()
                record_time[0] = time.time()

            explor_style = tk.Button(choose_fog_mode_window, text="火把型(默认)", command = flag3_0, fg = '#11FBFF', font = ('华文楷体', 22))
            explor_style.place(x = 50, y = 80)
            torch_explain = tk.Label(choose_fog_mode_window, text="只照亮当前格子周围的迷雾", fg = '#11FBFF', font = ('华文宋体', 20))
            torch_explain.place(x = 250, y = 95)

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
        else:
            messagebox.showwarning("流程错误", "选定模式无法更改")
    else:
        messagebox.showwarning("流程错误", "迷宫还没初始好 你先不要急着跑")

def astar_search(x, y, current_cost, pos_and_total_cost, go_back):
    global width, hight, astar_visit
    draw = ImageDraw.Draw(im)#在im上绘画
    astar_visit.append((x, y))
    plus = (size_list[0] + size_list[1]) / 2
    decrease = (size_list[0] - size_list[1]) / 2
    if(flag[5] == 2 or flag[5] == 3):
        draw.rectangle((x * size_list[0] + decrease, y * size_list[0] + decrease, x * size_list[0] + plus, y * size_list[0] + plus), fill = color_list[0])#以玩家路径颜色绘画A*探索路径
        update_root(im)
    if (x == width and y == hight):
        back_x = x; back_y = y
        while(back_x != 0 or back_y != 1):
            if(flag[5] == 1 or flag[5] == 3):
                update_root(im)
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

        im.save('design of class/maze/map set/map_record.png')
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
        subprocess.run(['python', 'design of class/maze/main_code.py'])
    
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

def astar(event = 0):
    if(flag[0]):
        global astar_visit
        destory_window()
        astar_visit = []
        current_cost = {(0, 1) : 0}#走到(x, y)需要的步数为x
        go_back = {}
        pos_and_total_cost = PriorityQueue()#(x, y)处总花费为x
        astar_search(0, 1, current_cost, pos_and_total_cost, go_back)
    else:
        messagebox.showwarning("流程错误", "迷宫还没初始好 你先不要急着跑")
    

def init_other_menu():
    other_menu.add_command(label = "查看最好成绩", command = best_score, accelerator = "Alt + b")
    root.bind("<Alt-b>", best_score)#严格区分大小写
    other_menu.add_separator() # 添加分隔线

    def clean_log(event = 0):#记得加event = 0,不用都行
        _ = open("design of class/maze/text/log.txt", 'w', encoding = "UTF-8")
    other_menu.add_command(label = "重置得分记录表", command = clean_log, accelerator = "Alt + c")
    root.bind("<Alt-c>", clean_log)
    other_menu.add_separator() # 添加分隔线

    other_menu.add_command(label = "退出游戏", command = Break_move, accelerator = "Esc")#加入快捷键(只是个提示 实际效果要自己做)
    root.bind("<Escape>", Break_move)

def best_score(event = 0):
    log_read_open = open("design of class/maze/text/log.txt", 'r', encoding = "UTF-8")
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

def Break_move(event = 0):
    global break_move
    break_move = 1


def init_change_menu():
    change_menu.add_cascade(label="更改大小", command=size_settings_window, accelerator = "Shift + S")
    root.bind("<Shift-S>", size_settings_window)
    change_menu.add_separator()

    change_menu.add_cascade(label="更改颜色", command=color_settings_window, accelerator = "Shift + C")
    root.bind("<Shift-C>", color_settings_window)
    change_menu.add_separator()

    change_menu.add_cascade(label="更改音效", command=effect_sound_settings_window, accelerator = "Shift + E")
    root.bind("<Shift-E>", effect_sound_settings_window)
    change_menu.add_separator()

    change_menu.add_cascade(label="更改A*显示", command=astar_settings_window, accelerator = "Shift + A")
    root.bind("<Shift-A>", astar_settings_window)
    change_menu.add_separator()

    change_menu.add_command(label = "恢复默认设置", command = reset_setting, accelerator = "Shift + R")
    root.bind("<Shift-R>", reset_setting)

def size_settings_window(event = 0):
    if(flag[0] == 0):#玩家没有生成迷宫
        # 创建设置窗口
        destory_window()
        global size_setting_window
        size_setting_window = tk.Toplevel(root)
        size_setting_window.title("大小设置")
        size_setting_window.geometry('400x350')
        def size_setting_window_destroy(event = 0):
            size_setting_window.destroy()
        size_setting_window.bind("<Escape>", size_setting_window_destroy)
        change_hig_wid_button = tk.Button(size_setting_window, text="更改迷宫大小", command = change_hig_wid, fg = '#11FBFF', font = ('华文楷体', 22))#只用height会出现有点按钮无法显示文字 有点按钮长度明显过长
        change_hig_wid_button.place(x = 50, y = 20)
        # 创建一个变量来保存设置

        change_cell_button = tk.Button(size_setting_window, text="更改迷宫晶格大小", command = change_cell, fg = '#11FBFF', font = ('华文楷体', 22))
        change_cell_button.place(x = 50, y = 80)

        change_line_size_button = tk.Button(size_setting_window, text="更改路径线条大小", command = change_line_size, fg = '#11FBFF', font = ('华文楷体', 22))
        change_line_size_button.place(x = 50, y = 140)

        change_view_fog_size_button = tk.Button(size_setting_window, text="更改迷雾可见半径大小", command = change_view_fog_size, fg = '#11FBFF', font = ('华文楷体', 22))
        change_view_fog_size_button.place(x = 50, y = 200)
    else:
        messagebox.showwarning("流程错误", "无法在生成迷宫后修改迷宫大小")

def change_hig_wid():
    try:#如果用户没有输入或输入错误 会报错
        if(flag[0] == 0):#玩家没有生成迷宫
            global hight, width, im
            user_input = simpledialog.askstring("长宽设置", "请输入自定义的长(最多81)宽(最多135) 输入必须为正奇数 用空格分隔)\n当前迷宫长:{} 宽{}".format(hight, width), initialvalue="")
            hight, width = map(int, user_input.strip().split())
            while((hight & 1 == 0 or width & 1 == 0) or (hight > 81 or hight < 3 or width < 3 or width > 135 )):
                if(hight & 1 == 0 or width & 1 == 0):
                    messagebox.showwarning("输入错误", "请输入奇数 否则迷宫会很奇怪")
                if(hight > 81 or hight < 3 or width < 3 or width > 135):
                    messagebox.showwarning("输入错误", "请输入合适范围的数字")
                user_input = simpledialog.askstring("长宽设置", "请输入自定义的长(最多135)宽(最多81) 输入必须为正奇数 用空格分隔)\n当前迷宫长:{} 宽{}".format(hight, width), initialvalue="")
                hight, width = map(int, user_input.strip().split())
            im = Image.new("RGB", ((width + 2) * size_list[0], (hight + 2) * size_list[0]), color_list[3])#创建一个背景图片white +2作为边界
            root.geometry(str(max((width + 2) * size_list[0] + 50, 600)) + 'x' + str(max((hight + 2) * size_list[0] + 50, 600)) + '+600' + '+200')
        else:
            messagebox.showwarning("流程错误", "无法在生成迷宫后修改迷宫大小")
    except:
        pass

def change_cell():
    try:
        global size_list
        user_input = simpledialog.askstring("迷宫晶格大小设置", "请输入迷宫晶格大小(范围6~15)\n当前路径尺寸大小:{} 当前迷宫晶格大小:{}".format(size_list[1], size_list[0]), initialvalue="")
        new_size = int(user_input.strip())
        while(new_size <= size_list[1] or new_size > 15):
            messagebox.showwarning("输入错误", "请输入合适范围的数字")
            user_input = simpledialog.askstring("迷宫晶格大小设置", "请输入迷宫晶格大小(范围6~15)\n当前路径尺寸大小:{} 当前迷宫晶格大小:{}".format(size_list[1], size_list[0]), initialvalue="")
            new_size = int(user_input.strip())
        size_list[0] = new_size
    except:
        pass

def change_line_size():
    try:
        global size_list
        user_input = simpledialog.askstring("路径尺寸设置", "请输入玩家路径尺寸(范围5~15)\n当前路径尺寸大小:{} 当前迷宫晶格大小:{}".format(size_list[1], size_list[0]), initialvalue="")
        new_size = int(user_input.strip())
        while(new_size < 5 or new_size >= size_list[0]):
            messagebox.showwarning("输入错误", "请输入合适范围的数字")
            user_input = simpledialog.askstring("路径尺寸设置", "请输入玩家路径尺寸(范围1~15)\n当前路径尺寸大小:{} 当前迷宫晶格大小:{}".format(size_list[1], size_list[0]), initialvalue="")
            new_size = int(user_input.strip())
        size_list[1] = new_size
    except:
        pass

def change_view_fog_size():
    try:
        global size_list, hight, width
        max_r = int(min(hight, width) / 2 - 0.5)
        user_input = simpledialog.askstring("迷雾可见半径设置", "请输入迷雾可见半径(范围1~{})\n当前可见半径:{}".format(max_r, size_list[2]), initialvalue="")
        new_size = int(user_input.strip())

        while(new_size < 1 or new_size > max_r):
            messagebox.showwarning("输入错误", "请输入合适范围的数字")
            user_input = simpledialog.askstring("迷雾可见半径设置", "请输入迷雾可见半径(范围1~{})\n当前可见半径:{}".format(max_r, size_list[2]), initialvalue="")
            new_size = int(user_input.strip())
        size_list[2] = new_size
    except:
        pass

def color_settings_window(event = 0):
    if(flag[0] == 0):
        # 创建设置窗口
        destory_window()
        global color_setting_window
        color_setting_window = tk.Toplevel(root)
        color_setting_window.title("颜色设置")
        color_setting_window.geometry('420x420')
        def color_setting_window_destroy(event = 0):
            color_setting_window.destroy()
        color_setting_window.bind("<Escape>", color_setting_window_destroy)
        change_window_backgroud_colors = tk.Button(color_setting_window, text="更改窗口背景颜色", command = change_root_backgroud_color, fg = '#11FBFF', font = ('华文楷体', 22))
        change_window_backgroud_colors.place(x = 50, y = 20)
        
        change_player_point_colors =tk.Button(color_setting_window, text="更改玩家当前位置颜色", command = change_player_point_color, fg = '#11FBFF', font = ('华文楷体', 22))
        change_player_point_colors.place(x = 50, y = 80)

        change_player_path_colors =tk.Button(color_setting_window, text="更改玩家路径颜色", command = change_player_path_color, fg = '#11FBFF', font = ('华文楷体', 22))
        change_player_path_colors.place(x = 50, y = 140)

        change_astar_path_colors = tk.Button(color_setting_window, text="更改A*路径颜色", command = change_astar_path_color, fg = '#11FBFF', font = ('华文楷体', 22))
        change_astar_path_colors.place(x = 50, y = 200)
        
        change_labyrinth_backgroud_colors = tk.Button(color_setting_window, text="更改迷宫背景颜色", command = change_labyrinth_backgroud_color, fg = '#11FBFF', font = ('华文楷体', 22))
        change_labyrinth_backgroud_colors.place(x = 50, y = 260)

        change_labyrinth_wall_colors = tk.Button(color_setting_window, text="更改迷宫墙壁颜色", command = change_labyrinth_wall_color, fg = '#11FBFF', font = ('华文楷体', 22))
        change_labyrinth_wall_colors.place(x = 50, y = 320)
    else:
        messagebox.showwarning("流程错误", "无法在生成迷宫后修改迷宫颜色")

def change_root_backgroud_color():
    chosed_color = colorchooser.askcolor(title = "猛男就该用猛男粉!")
    root.configure(bg = chosed_color[1])

def change_player_path_color():
    chosed_color = colorchooser.askcolor(title = "猛男就该用猛男粉!")
    color_list[0] = chosed_color[1]

def change_player_point_color():
    chosed_color = colorchooser.askcolor(title = "猛男就该用猛男粉!")
    color_list[1] = chosed_color[1]

def change_astar_path_color():
    chosed_color = colorchooser.askcolor(title = "猛男就该用猛男粉!")
    color_list[2] = chosed_color[1]

def change_labyrinth_backgroud_color():
    chosed_color = colorchooser.askcolor(title = "猛男就该用猛男粉!")
    color_list[3] = chosed_color[1]

def change_labyrinth_wall_color():
    chosed_color = colorchooser.askcolor(title = "猛男就该用猛男粉!")
    color_list[4] = chosed_color[1]

def effect_sound_settings_window(event = 0):
    global effect_sound_setting_window
    if(flag[0] == 0):
        # 创建设置窗口
        destory_window()
        effect_sound_setting_window = tk.Toplevel(root)
        effect_sound_setting_window.title("音效设置")
        effect_sound_setting_window.geometry('380x220')
        def effect_sound_setting_window_destroy(event = 0):
            effect_sound_setting_window.destroy()
        effect_sound_setting_window.bind("<Escape>", effect_sound_setting_window_destroy)
        
        def change_move_sound():
            flag[4] = 0
            get_sound()
        change_window_backgroud_colors = tk.Button(effect_sound_setting_window, text="更改玩家移动音效", command = change_move_sound, fg = '#11FBFF', font = ('华文楷体', 22))
        change_window_backgroud_colors.place(x = 50, y = 20)
        
        def change_pass_sound():
            flag[4] = 1
            get_sound()
        change_player_point_colors =tk.Button(effect_sound_setting_window, text="更改玩家通关音效", command = change_pass_sound, fg = '#11FBFF', font = ('华文楷体', 22))
        change_player_point_colors.place(x = 50, y = 80)

    else:
        messagebox.showwarning("流程错误", "无法在生成迷宫后修改音效")

def get_sound():
    global var
    effect_sound_get = tk.Toplevel(root)
    effect_sound_get.title("音效选择")
    effect_sound_get.geometry('420x420')
    def confirm_sound():
        sound_effect_apply[flag[4]] = var.get()
        effect_sound_get.destroy()

    if(flag[4] == 0):
        current_sound_effect = tk.Label(effect_sound_get, text="当前玩家移动音效为:{}".format(sound_effect_list[sound_effect_apply[0]]), font=("华文楷体", 20)).place(x = 50, y = 20)
    if(flag[4] == 1):
        current_sound_effect = tk.Label(effect_sound_get, text="当前玩家通关音效为:{}".format(sound_effect_list[sound_effect_apply[1]]), font=("华文楷体", 20)).place(x = 50, y = 20)
    var = tk.IntVar()
    content_y = 60
    tk.Radiobutton(effect_sound_get, text="爆炸1", variable=var, value=0,font = ('华文楷体', 22)).place(x = 50, y = content_y)
    tk.Radiobutton(effect_sound_get, text="爆炸2", variable=var, value=1, font = ('华文楷体', 22)).place(x = 50, y = content_y + 60)
    tk.Radiobutton(effect_sound_get, text="获得金币", variable=var, value=2, font = ('华文楷体', 22)).place(x = 50, y = content_y + 120)
    tk.Radiobutton(effect_sound_get, text="野 花 香", variable=var, value=3, font = ('华文楷体', 22)).place(x = 50, y = content_y + 180)
    tk.Radiobutton(effect_sound_get, text="浴霸", variable=var, value=4, font = ('华文楷体', 22)).place(x = 50, y = content_y + 240)
    tk.Button(effect_sound_get, text="确认", command= confirm_sound, font = ('华文楷体', 22)).place(x = 50, y = content_y + 300)

def astar_settings_window(event = 0):
    global astar_sound_setting_window
    if(flag[0] == 0):
        # 创建设置窗口
        destory_window()
        astar_sound_setting_window = tk.Toplevel(root)
        astar_sound_setting_window.title("A*设置")
        astar_sound_setting_window.geometry('480x220')
        def astar_sound_setting_window_destroy(event = 0):
            astar_sound_setting_window.destroy()
        astar_sound_setting_window.bind("<Escape>", astar_sound_setting_window_destroy)
        def confirm_astar(event = 0):
            if(var1.get()):
                flag[5] = 2
            if(var2.get()):
                flag[5] = 1
            if(var1.get() and var2.get()):
                flag[5] = 3
            astar_sound_setting_window.destroy()
        var1 = tk.IntVar()
        var2 = tk.IntVar()
        content_y = 60
        if(flag[5] == 0):
            tk.Label(astar_sound_setting_window, text="当前状态:不显示动画", font=("华文楷体", 20)).place(x = 50, y = 20)
        elif(flag[5] == 1):
            tk.Label(astar_sound_setting_window, text="当前状态:显示回溯动画", font=("华文楷体", 20)).place(x = 50, y = 20)
        elif(flag[5] == 2):
            tk.Label(astar_sound_setting_window, text="当前状态:显示探索动画", font=("华文楷体", 20)).place(x = 50, y = 20)
        elif(flag[5] == 3):
            tk.Label(astar_sound_setting_window, text="当前状态:显示所有动画", font=("华文楷体", 20)).place(x = 50, y = 20)
        tk.Checkbutton(astar_sound_setting_window, text="启用探索动画", variable=var1, font = ('华文楷体', 22)).place(x = 50, y = content_y)
        tk.Checkbutton(astar_sound_setting_window, text="启用回溯动画", variable=var2,  font = ('华文楷体', 22)).place(x = 50, y = content_y + 60)
        tk.Button(astar_sound_setting_window, text="确认", command= confirm_astar, font = ('华文楷体', 22)).place(x = 50, y = content_y + 120)
    else:
        messagebox.showwarning("流程错误", "无法在生成迷宫后修改A*可见性")


def solve():
    pygame.init()#神币音效
    pygame.mixer.init()
    global hight, width, im, root, break_move, move_path
    move_path = [(0, 1)]#81*135的迷宫 size_list[0]控制每一个方块大小
    init_setting()#初始化设置
    im = Image.new("RGB", ((width + 2) * size_list[0], (hight + 2) * size_list[0]), color_list[3])#创建一个背景图片white +2作为边界
    break_move = False; position[0] = 0; position[1] = 1#初始化起点
    root = tk.Tk()#创建[根组件/窗口](空)
    root.title("迷 宫 游 戏")#窗口名称
    root.geometry(str(max((width + 2) * size_list[0] + 50, 600)) + 'x' + str(max((hight + 2) * size_list[0] + 50, 600)) + '+600' + '+200')#调整窗口大小('x') 位置('+' 第一个表示x 第二个表示y)
    menu_bar = tk.Menu(root)#创建菜单栏(空)
    global algorithm_menu
    algorithm_menu = tk.Menu(menu_bar, tearoff = 0)#创建菜单上的项目
    init_algorithm_menu()#初始化项目
    menu_bar.add_cascade(label = "选择算法", menu = algorithm_menu)#添加显示
    global mode_menu
    mode_menu = tk.Menu(menu_bar, tearoff = 0)
    init_mode_menu()
    menu_bar.add_cascade(label = "选择模式", menu = mode_menu)

    global other_menu
    other_menu = tk.Menu(menu_bar, tearoff = 0)
    init_other_menu()
    menu_bar.add_cascade(label = "其他设置", menu = other_menu)

    global change_menu
    change_menu = tk.Menu(menu_bar, tearoff = 0)
    init_change_menu()
    menu_bar.add_cascade(label = "自定义设置", menu = change_menu)

    root.config(menu = menu_bar)#启用菜单栏
    game_loop()#启动更新循环
    root.mainloop()#展示根组件
    pygame.quit()
    log_write_open.close()
    default_setting_read_open.close()

def main():
    solve()

if __name__ == '__main__':
    main()
