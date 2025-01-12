import time
import pygame
import subprocess#用自运行做下一关
import random
from tkinter import messagebox, simpledialog

pygame.init()
pygame.mixer.init()
sudoku_play = [[0 for _ in range(9)] for _ in range(9)]
class two_dimension():
    def __init__(self, x = 9, y = 9, init_num = 0):
        self.x = x
        self.y = y
        self.data = [[init_num for _ in range(y)] for _ in range(x)]
    def reset(self, reset_num = 0):
        self.data = [[reset_num for _ in range(self.y)] for _ in range(self.x)]
error_map = two_dimension()
flag=[0, '', 0, 0, 0, 0]
'''
0:数独是否已经创建完成 1是 0否
1:填充状态 ''(空):擦除
2:游戏难度 0简单 1中等 2困难
3:已消去数字数量
4:是否已经初始化难度
5:是否已经通关
'''
path = []#(x,y,num)
def build_sudoku(x, y, sudoku):#竖x 横y
    if(sudoku[x][y] == 0):#需要寻找合适数字
        valid_num = [i for i in range(1, 10)]
        for i in range(x//3*3, x//3*3 + 3):
            for j in range(y//3*3, y//3*3 + 3):
                if(sudoku[i][j] in valid_num):#检查晶格
                    valid_num.remove(sudoku[i][j])
        for i in range(9):
            if(sudoku[i][y] in valid_num):
                valid_num.remove(sudoku[i][y])
            if(sudoku[x][i] in valid_num):
                valid_num.remove(sudoku[x][i])
        random.shuffle(valid_num)#保证随机
        for i in valid_num:
            if(flag[0]):
                return
            sudoku[x][y] = i
            #x//3 * 3+ y//3 确定第几个方格区  x % 3 * 3 + y % 3确定在方格转列表的下标
            if(x == y == 8 and flag[0] == 0):#已经遍历完成
                for i in range(9):
                    for j in range(9):
                        sudoku_play[i][j] = sudoku[i][j]#继承数据
                flag[0] = 1
                return
            x = x if y + 1 <= 8 else x + 1#模拟遍历下一步
            y = y + 1 if y + 1 <= 8 else 0
            build_sudoku(x, y, sudoku)
            x = x if y != 0 else x - 1
            y = y - 1 if y != 0 else 8
            if(flag[0] == 0):
                sudoku[x][y] = 0#没有生成完成才需要回溯
    else:#已经填充完成
        x = x if y + 1 <= 8 else x + 1
        y = y + 1 if y + 1 <= 8 else 0
        if(x == y == 8 and flag[0] == 0):
            for i in range(9):
                for j in range(9):
                    sudoku_play[i][j] = sudoku[i][j]
            flag[0] = 1
            return
        build_sudoku(x, y, sudoku)

delete_num_pos = [i for i in range(81)]
deleted_num_pos = []
random.shuffle(delete_num_pos)#保证随机排列

class images():
    def __init__(self, path):
        self.path = path
        self.image = pygame.image.load(path)#首先加载路径

    def set_size(self, size = (100, 100)):
        self.image = pygame.transform.scale(self.image, size)
    
    def put_image(self, put_place = (0, 0)):
        self.put_place = put_place
        image_rect = self.image.get_rect()  # 获取图片的矩形区域
        image_rect.topleft = put_place  # 设置图片位置(tuple)
        return image_rect

    def show_image(self):
        screen.blit(self.image, self.put_place)  # 将图片绘制在屏幕

class rectangulars():
    def __init__(self, color = (255, 255, 255)):
        self.color = color

    def set_position(self, left_up, size, outline_size = 0):
        pygame.draw.rect(screen, self.color, pygame.Rect(left_up, size), outline_size)

def show_long_text(text, line_num, pos, dy):
    pygame.init()
    font = pygame.font.Font('design of class/Sudoku/fonts/ZCOOLKuaiLe-Regular.ttf', 40)
    #font = pygame.font.Font('design of class\Sudoku\fonts\NotoSerifSC-VariableFont_wght.ttf', 40)
    text_color = (0, 0, 0)  # black
    cnt = 0
    sentence_list = text.split('\n')#适配\n换行
    for one_text in sentence_list:
        for i in range(0, len(one_text), line_num):
            text_surface = font.render(one_text[i:i + line_num], True, text_color)
            screen.blit(text_surface, (pos[0], pos[1] + cnt * dy))
            cnt += 1

def difficulty_set():
    try:#如果用户没有输入或输入错误 会报错
        difficult_input = simpledialog.askinteger("难度设置", "输入希望留出的空位数:(1~81)", initialvalue="")
        while(81 < difficult_input or difficult_input < 1):
            messagebox.showwarning("输入错误", "请输入正确的数字")
            difficult_input = simpledialog.askinteger("难度设置", "输入希望留出的空位数:(1~81)", initialvalue="")
        flag[3] = flag[2] =int(difficult_input)
        flag[4] = 1
        for _ in range(flag[3]):
            sudoku_play[delete_num_pos[0] // 9][delete_num_pos[0] % 9] = 0
            deleted_num_pos.append((delete_num_pos[0] // 9, delete_num_pos[0] % 9))
            del delete_num_pos[0]
    except:#如果没有输入 直接退出就行
        pass
       
def welcome_part():
    global screen
    pygame.mixer.music.load("design of class/Sudoku/musics/bgm/clock paradox.mp3")
    pygame.mixer.music.play(-1)
    pygame.display.set_caption('数独游戏-欢迎页面')
    screen = pygame.display.set_mode((1400, 1000))# 创建屏幕
    welcome_bgimage = images('design of class/Sudoku/images/backgrounds/welcom_background.png')
    welcome_bgimage.set_size((1400, 1000))
    welcome_bgimage.put_image()
    welcome_bgimage.show_image()
    
    text_contain = "规则:\n在数独中填入合适数字 使得每一行、每一列以及每一个3x3的宫内数字1到9只出现一次\n \n游戏支持的操作有:\n1.重新开始当前数独\n2.重新生成数独\n3.悔棋\n4.擦除指定位置数字\n5.给出其中一个正确答案(如果无响应代表当前状态无解)\n6.自动判断是否成功(如果填充失败告诉玩家违反哪个规则)\n \ntips:按Esc以退出游戏"
    show_long_text(text_contain, 32, (100, 50), 45)

    running = True
    while running:# 事件处理
        start_image = images('design of class/Sudoku/images/icons/start_game.png')
        start_image_rect = start_image.put_image((1000, 700))
        start_image_motion = images('design of class/Sudoku/images/icons/start_game_motion.png')
        start_image_rect_motion = start_image_motion.put_image((1000, 700))

        difficulty_image = images('design of class/Sudoku/images/icons/difficulty_set.png')
        difficulty_image.set_size()
        difficulty_image_rect = difficulty_image.put_image((800, 750))
        difficulty_image_motion = images('design of class/Sudoku/images/icons/difficulty_set_motion.png')
        difficulty_image_motion.set_size()
        difficulty_image_motion_rect = difficulty_image_motion.put_image((800, 750))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.MOUSEMOTION:
                mouse_pos = event.pos#difficulty
                if start_image_rect.collidepoint(mouse_pos):
                    start_image_motion.show_image()
                else:
                    start_image.show_image()
                if difficulty_image_rect.collidepoint(mouse_pos):
                    difficulty_image_motion.show_image()
                else:
                    difficulty_image.show_image()
                
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos= event.pos
                if start_image_rect.collidepoint(mouse_pos):
                    if(flag[4] == 0):
                        difficulty_set()
                    start_time = time.time()
                    game_part()
                    record_log = open("design of class/Sudoku/texts/record.txt", "a+")
                    record_log.write("game time:{:.3f}\ndifficulty:{} blank(s)\n".format(time.time() - start_time, flag[2]))
                    record_log.close()
                    pygame.quit()#从game里面出来一定意味着已经结束游戏了
                if difficulty_image_rect.collidepoint(mouse_pos):
                    difficulty_set()
            if event.type == pygame.KEYDOWN:# 检测特定键
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    
        pygame.display.flip()
 

def draw_sudoku_background():
    #铺底层白色
    background_rect = rectangulars()
    background_rect.set_position((50, 50), (880, 880))
    line_color = (0, 0, 0)  # black
    # 绘制黑色粗线条
    for gap in range(55,55 + 4 * 290, 290):#55:留下间隔给宽度
        pygame.draw.line(screen, line_color, (55, gap), (930, gap), 10)  # 最后的2表示线条宽度 向两侧延伸的宽度
        pygame.draw.line(screen, line_color, (gap, 55), (gap, 930), 10)
    gap = 153
    for _ in range(3):#3行/列
        for _ in range(2):#中间细线
            pygame.draw.line(screen, line_color, (60, gap), (930, gap), 5)
            pygame.draw.line(screen, line_color, (gap, 60), (gap, 930), 5)
            gap += 95
        gap += 100

def transform_xy(x, y):
    left_x = x // 3
    dx = x % 3
    up_y = y // 3
    dy = y % 3
    return left_x, dx, up_y, dy

def draw_player_put_num(x, y, num):
    left_x, dx, up_y, dy = transform_xy(x, y)
    num_background_rect = rectangulars()
    num_background_rect.set_position((1 + 60 + 290 * left_x + 95 * dx, 1 + 60 + 290 * up_y + 95 * dy), (89, 89))
    if(error_map.data[x][y] != 0):
        error_x_outline = rectangulars((127, 255, 212))
        error_x_outline.set_position((6 + 60 + 290 * left_x + 95 * dx, 6 + 60 + 290 * up_y + 95 * dy), (80, 80), 4)
    if(num == flag[1]):#所有相同的数
        outline_pos = (2 + 60 + 290 * left_x + 95 * dx, 2 + 60 + 290 * up_y + 95 * dy)  # 左上角坐标
        pygame.draw.rect(screen, (255, 127, 80), pygame.Rect(outline_pos, (88, 88)),2)
    if(num != '0'):
        font = pygame.font.Font(None, 110)
        text_color = (0, 0, 0) if (y, x) not in deleted_num_pos else (140, 255, 255)
        text_surface = font.render(num, True, text_color)
        screen.blit(text_surface, (22 + 60 + 290 * left_x + 95 * dx, 10 + 60 + 290 * up_y + 95 * dy))

def draw_fix_num():
    for y in range(9):#遍历大晶格找到所在晶格 确定起始位置
        for x in range(9):
            draw_player_put_num(x, y, str(sudoku_play[y][x]))

def show_now_num():
    white_rect = pygame.Rect(1225, 100, 130, 50)
    pygame.draw.rect(screen, (255, 255, 255), white_rect)
    
    font = pygame.font.Font(None, 70)
    text_color = (0, 0, 0)
    if(flag[1] == ''):
        num_text = "erase"
    else:
        num_text = flag[1]
    text_surface = font.render("now num:" + num_text, True, text_color)
    screen.blit(text_surface, (1000, 100))

def show_error_message(text):
    white_rect = pygame.Rect(1030, 150, 290, 35)
    pygame.draw.rect(screen, (255, 255, 255), white_rect)
    
    font = pygame.font.Font('design of class/Sudoku/fonts/ZCOOLKuaiLe-Regular.ttf', 30)
    text_color = (0, 0, 0)
    text_surface = font.render("错误:" + text, True, text_color)
    screen.blit(text_surface, (1000, 150))

def get_num_pos(x, y):
    for dy_cell in range(3):#遍历大晶格找到所在晶格 确定起始位置晶格坐标
        for dx_cell in range(3):
            if(60 + 290 * dx_cell <= x <= 60 + 290 * (dx_cell + 1) and 60 + 290 * dy_cell <= y <= 60 + 290 * (dy_cell + 1)):
                left_x = 60 + 290 * dx_cell
                cell_x = dx_cell * 3
                up_y = 60 + 290 * dy_cell
                cell_y = dy_cell * 3
                for dy in range(3):
                    for dx in range(3):
                        if(left_x + 95 * dx <= x <= left_x + 95 * (dx + 1) and up_y + 95 * dy <= y <= up_y + 95 * (dy + 1)):
                            return (cell_y + dy, cell_x + dx)

def check_changeable(x, y):
    if((x, y) not in deleted_num_pos):
        show_error_message("已有数字{}".format(sudoku_play[x][y]))
        return False
    return True

def check_put(x, y):
    result = True
    for i in range(9):
        if(int(flag[1]) == sudoku_play[i][y]):
            show_error_message("纵向已有该数字")
            error_map.data[y][i] = 1
            print(i, y)
            result = False
        if(int(flag[1]) == sudoku_play[x][i]):
            show_error_message("横向已有该数字")
            error_map.data[i][x] = 1
            print(x, i)
            result = False
    for i in range(x // 3 * 3, x // 3 * 3 + 3):
        for j in range(y // 3 * 3, y // 3 * 3 + 3):
            if(int(flag[1]) == sudoku_play[i][j]):
                show_error_message("当前晶胞已有该数字")
                error_map.data[j][i] = 1
                result = False
    return result & check_changeable(x, y)#其他都过了 检测当前数字可变如果过了就过了 不过就不过

def game_part():
    pygame.display.set_caption('数独游戏')
    play_bgimage = images('design of class/Sudoku/images/backgrounds/play_background.png')
    play_bgimage.set_size((1400, 1000))
    play_bgimage.put_image()
    play_bgimage.show_image()
    draw_sudoku_background()
    running = True
    while running:# 事件处理
        restart_image = images('design of class/Sudoku/images/icons/restart.png')
        restart_image.set_size()
        restart_image_rect = restart_image.put_image((1000, 500))
        restart_image_motion = images('design of class/Sudoku/images/icons/restart_motion.png')
        restart_image_motion.set_size()
        restart_image_motion_rect = restart_image_motion.put_image((1000, 500))

        answer_image = images('design of class/Sudoku/images/icons/answer.png')
        answer_image.set_size()
        answer_image_rect = answer_image.put_image((1200, 700))
        answer_image_motion = images('design of class/Sudoku/images/icons/answer_motion.png')
        answer_image_motion.set_size()
        answer_image_motion_rect = answer_image_motion.put_image((1200, 700))
        
        erase_image = images('design of class/Sudoku/images/icons/erase.png')
        erase_image.set_size()
        erase_image_rect = erase_image.put_image((1000, 700))
        erase_image_motion = images('design of class/Sudoku/images/icons/erase_motion.png')
        erase_image_motion.set_size()
        erase_image_motion_rect = erase_image_motion.put_image((1000, 700))
        
        last_step_image = images('design of class/Sudoku/images/icons/last_step.png')
        last_step_image.set_size()
        last_step_image_rect = last_step_image.put_image((1200, 300))
        last_step_image_motion = images('design of class/Sudoku/images/icons/last_step_motion.png')
        last_step_image_motion.set_size()
        last_step_image_motion_rect = last_step_image_motion.put_image((1200, 300))

        regame_image = images('design of class/Sudoku/images/icons/regame.png')
        regame_image.set_size()
        regame_image_rect = regame_image.put_image((1200, 500))
        regame_image_motion = images('design of class/Sudoku/images/icons/regame_motion.png')
        regame_image_motion.set_size()
        regame_image_motion_rect = regame_image_motion.put_image((1200, 500))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            
            if event.type == pygame.MOUSEMOTION:
                mouse_pos = event.pos
                if restart_image_rect.collidepoint(mouse_pos):
                    restart_image_motion.show_image()
                else:
                    restart_image.show_image()

                if regame_image_rect.collidepoint(mouse_pos):
                    regame_image_motion.show_image()
                else:
                    regame_image.show_image()

                if answer_image_rect.collidepoint(mouse_pos):
                    answer_image_motion.show_image()
                else:
                    answer_image.show_image()

                if erase_image_rect.collidepoint(mouse_pos):
                    erase_image_motion.show_image()
                else:
                    erase_image.show_image()

                if last_step_image_rect.collidepoint(mouse_pos):
                    last_step_image_motion.show_image()
                else:
                    last_step_image.show_image()
            if event.type == pygame.MOUSEBUTTONDOWN:
                error_map.reset()
                x, y = event.pos
                if(0<=x<=1e3 and 0<=y<=1e3):
                    num_pos = get_num_pos(x, y)
                    if(flag[1] != '' and check_put(num_pos[0], num_pos[1])):
                        show_error_message("")
                        flag[3] -= 1
                        sudoku_play[num_pos[0]][num_pos[1]] = int(flag[1])
                        path.append((num_pos[0], num_pos[1], int(flag[1])))
                    elif(flag[1] == '' and check_changeable(num_pos[0], num_pos[1])):
                        show_error_message("")
                        flag[3] += 1
                        sudoku_play[num_pos[0]][num_pos[1]] = 0
                        path.append((num_pos[0], num_pos[1], 0))
                
                if erase_image_rect.collidepoint((x, y)):
                    flag[1] = ''
                if restart_image_rect.collidepoint((x, y)):
                    flag[3] = flag[2]
                    for pos in deleted_num_pos:
                        sudoku_play[pos[0]][pos[1]] = 0
                if regame_image_rect.collidepoint((x, y)):
                    pygame.quit()
                    subprocess.run(['python', 'design of class/Sudoku/sudoku.py'])
                if answer_image_rect.collidepoint((x, y)):
                    flag[0] = 0
                    build_sudoku(0, 0,sudoku_play)
                    if(sudoku_play[8][8] == 0):
                        valid_num = [i for i in range(1, 10)]
                        for i in range(6, 9):
                            for j in range(6, 9):
                                if(sudoku_play[i][j] in valid_num):
                                    valid_num.remove(sudoku_play[i][j])
                        sudoku_play[8][8] = valid_num[0]
                if last_step_image_rect.collidepoint((x, y)):
                    if(len(path)):
                        flag[3] = flag[2]
                        path.pop()
                        for pos in deleted_num_pos:
                            sudoku_play[pos[0]][pos[1]] = 0
                        for i in path:
                            sudoku_play[i[0]][i[1]] = i[2]
                            flag[3] -= 1 if i[2] else -1
                
            if event.type == pygame.KEYDOWN:# 检测特定数字键
                error_map.reset()
                if event.key == pygame.K_1:
                    flag[1] = '1'
                elif event.key == pygame.K_2:
                    flag[1] = '2'
                elif event.key == pygame.K_3:
                    flag[1] = '3'
                elif event.key == pygame.K_4:
                    flag[1] = '4'
                elif event.key == pygame.K_5:
                    flag[1] = '5'
                elif event.key == pygame.K_6:
                    flag[1] = '6'
                elif event.key == pygame.K_7:
                    flag[1] = '7'
                elif event.key == pygame.K_8:
                    flag[1] = '8'
                elif event.key == pygame.K_9:
                    flag[1] = '9'
                elif event.key == pygame.K_ESCAPE:
                    pygame.quit()
        draw_fix_num()
        show_now_num()

        pygame.display.flip()
        if(flag[3] == 0):
            sound = pygame.mixer.Sound('design of class/Sudoku/musics/sound_effect/coin received1.mp3')#玩家移动音效
            sound.play(loops=0, maxtime=500)
            messagebox.showinfo("通关!", "您已经完成数独!")
            flag[5] = 1
            running = False

def solve():
    build_sudoku(0, 0, sudoku_play)
    welcome_part()
solve()