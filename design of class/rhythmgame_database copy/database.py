import re  # 正则表达式处理爬取数据时的跳转编号
import os
import time  # 计时器
import queue  # 异步
import heapq
import requests
import threading
import subprocess
import tkinter as tk
from PIL import Image
import customtkinter as ctk
from selenium import webdriver
from tkinter import messagebox
from CTkToolTip import CTkToolTip
import xml.etree.ElementTree as ET
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

py_path = 'rhythmgame_database/database.py'
xmlpath = 'rhythmgame_database/phigros_data.xml'
image_path_prefix = 'rhythmgame_database/images/'
ctitle_font = '仿宋'


class ctktoplevel_frame(ctk.CTkToplevel):  # 副窗口
    def __init__(self, master, title):
        super().__init__(master)
        self.title(title)

        def destroy_window(event):
            self.destroy()
        self.bind("<Escape>", destroy_window)

    def set_size(self, x, y, dx, dy):
        self.geometry("{}x{}+{}+{}".format(x, y, dx, dy))


class combobox_frame(ctk.CTkFrame):  # 下拉框+输入
    def __init__(self, master, title, button_name, values, default_value=''):
        super().__init__(master)

        self.grid_columnconfigure(0, weight=1)
        self.configure(height=32, fg_color="transparent")
        self.values = values
        self.default_value = default_value
        self.title = title
        self.variable = ctk.StringVar(value=default_value)
        self.title = ctk.CTkLabel(self, text=self.title, fg_color="#F0FFFF",
                                  corner_radius=6, font=(ctitle_font, 20))  # 提示标签
        self.title.grid(row=0, column=0, padx=10, pady=2, sticky="w")

        self.option_menu = ctk.CTkComboBox(self, values=self.values, variable=self.variable, command=lambda x: self.click(button_name), font=(ctext_font, 20))  # 下拉框+输入
        self.option_menu.grid(row=0, column=1, padx=10, pady=2)
        self.option_menu.configure(width=300)

    def get(self):
        return self.option_menu.get()

    def set_size(self, width=300, height=32):
        self.option_menu.configure(width=width, height=height)

    def click(self, button_name):  # 响应选择选项 只起到一个根据输入更新控件内容的作用
        if (button_name == '添加歌曲'):
            complex_name = self.get()
            bracket_idx = complex_name.rindex('(')
            composer = complex_name[bracket_idx + 1: -1:]
            # click拿到的数据 所以一定能找到
            song_info = phigros_root.get_song_data('name', complex_name)
            avaliable_diff_list = []
            for diffi in phigros_root.diff_list:  # 按照频率排序 加进去的时候就是同样的顺序
                if diffi not in song_info.keys():
                    avaliable_diff_list.append(diffi)
            diff_var = ctk.StringVar(value=avaliable_diff_list[0])
            phigros_root.contain_item['增']['难度'].option_menu.configure(values=avaliable_diff_list, variable=diff_var)

            composer_var = ctk.StringVar(value=composer)
            phigros_root.contain_item['增']['曲师'].option_menu.configure(variable=composer_var)

        elif (button_name == '更改歌曲'):
            song_name = phigros_root.valid_test('名称', self.get())
            if (song_name == '无'):
                return
            phigros_root.tip_song = song_name
            song_info = phigros_root.get_song_data('name', song_name)
            if (song_info is None):
                return
            avaliable_diff_list = []

            for diffi in phigros_root.diff_list:  # 按照频率排序 加进去的时候就是同样的顺序
                if diffi in song_info.keys():
                    avaliable_diff_list.append(diffi)

            phigros_root.tip_diff = avaliable_diff_list[0]
            phigros_root.contain_item['改']['难度'].option_menu.configure(values=avaliable_diff_list, variable=ctk.StringVar(value=phigros_root.tip_diff))
            phigros_root.change_current_info()

            try:
                for widget in phigros_root.grid_item['改']['曲绘窗口'].winfo_children():
                    widget.destroy()
                song_image = ctk.CTkImage(light_image=Image.open(image_path_prefix + f'{song_info['歌曲id']}.png'), size=(454, 240))
                image_label = ctk.CTkLabel(phigros_root.grid_item['改']['曲绘窗口'], text='', image=song_image)
                image_label.grid(row=0, column=0, pady=5, padx=10, sticky='nsew')
            except:
                messagebox.showwarning('更改歌曲页面', f'{song_info['名称']}未找到对应图片')

        elif (button_name == '删除歌曲'):
            complex_name = self.get()
            song_info = phigros_root.get_song_data('name', complex_name)
            diff = []
            for diffi in phigros_root.diff_list:
                if (diffi in song_info.keys()):
                    diff.append(diffi)
            phigros_root.contain_item['删']['难度'].option_menu.configure(values=tuple(diff))
            try:
                for widget in phigros_root.grid_item['删']['曲绘窗口'].winfo_children():
                    widget.destroy()
                song_image = ctk.CTkImage(light_image=Image.open(image_path_prefix + f'{song_info['歌曲id']}.png'), size=(454, 240))
                image_label = ctk.CTkLabel(phigros_root.grid_item['删']['曲绘窗口'], text='', image=song_image)
                image_label.grid(row=0, column=0, pady=5, padx=10, sticky='nsew')
            except:
                messagebox.showwarning('删除歌曲页面', f'{song_info['名称']}未找到对应图片')

        elif (button_name == '查找歌曲'):
            song_name = self.get()
            if (phigros_root.contain_item['查']['属性'].get() in ('名称', '俗称')):
                song_name = phigros_root.valid_test('名称', song_name)
            song_index = phigros_root.song_list.index(song_name)
            song_info = phigros_root.get_song_data('index', song_index)
            diff = []
            for diffi in phigros_root.diff_list:
                if (diffi in song_info.keys()):
                    diff.append(diffi)
            phigros_root.contain_item['查']['名称-难度'].option_menu.configure(values=diff, variable=ctk.StringVar(value=diff[0]))
            # print(song_info)

        elif (button_name == '展示数量'):
            phigros_root.show_num_perpage = int(self.get())
            phigros_root.grid_find_rst()


class optionmenu_frame(ctk.CTkFrame):  # 下拉框
    def __init__(self, master, title, button_name, values, default_value=''):
        super().__init__(master)
        self.grid_columnconfigure(0, weight=1)
        self.configure(height=32, fg_color="transparent")
        self.values = values
        self.default_value = default_value
        self.title = title
        self.radiobuttons = []
        self.variable = ctk.StringVar(value=default_value)

        self.title = ctk.CTkLabel(self, text=self.title, fg_color="#F0FFFF", corner_radius=6, font=(ctitle_font, 20))
        self.title.grid(row=0, column=0, padx=10, pady=5, sticky="w")

        self.option_menu = ctk.CTkOptionMenu(self, values=self.values, variable=self.variable, command=lambda x: self.click(button_name), font=(ctext_font, 20))
        self.option_menu.grid(row=0, column=1, padx=10, pady=5)

    def get(self):
        return self.option_menu.get()

    def set_size(self, width=140, height=28):
        self.option_menu.configure(width=width, height=height)

    def click(self, button_name):
        if (button_name == '查找属性'):
            seek_type = self.get()
            print(f"查找属性:指定{seek_type}")
            phigros_root.change_find_window(seek_type)

        if (button_name == '更改属性'):
            phigros_root.tip_attri = self.get()
            phigros_root.change_current_info()

        if (button_name == '更改难度'):
            phigros_root.tip_diff = self.get()
            phigros_root.change_current_info()


class entry_frame(ctk.CTkFrame):  # 单行输入框
    def __init__(self, master, title, placeholder_text='', default_value=''):
        super().__init__(master)
        self.grid_columnconfigure(0, weight=1)
        self.configure(height=32, fg_color="transparent")
        self.title = title

        self.title = ctk.CTkLabel(self, text=self.title, fg_color="#F0FFFF", font=(ctitle_font, 20), corner_radius=6)
        self.title.grid(row=0, column=0, padx=10, pady=5, sticky="w")

        self.ctkentry = ctk.CTkEntry(self, placeholder_text=placeholder_text, font=(ctext_font, 20))
        if default_value != '':
            self.ctkentry.insert(0, default_value)
        self.ctkentry.configure(width=150, height=32)
        self.ctkentry.grid(row=0, column=1, padx=10, pady=5, sticky="nsew")
        self.ctkentry.configure(width=300)

    def get(self):
        return self.ctkentry.get()

    def set_size(self, width=300, height=32):
        self.ctkentry.configure(width=width, height=height)


class muti_entry_frame(ctk.CTkFrame):  # 多行输入框
    def __init__(self, master, title, placeholder_text=''):
        super().__init__(master)
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.configure(height=32, fg_color="transparent")

        self.title = title
        self.placeholder = placeholder_text
        self.title_label = ctk.CTkLabel(self, text=self.title, fg_color="#F0FFFF", font=(ctitle_font, 20), corner_radius=6)
        self.title_label.grid(row=0, column=0, padx=10, pady=5, sticky="w")

        self.ctktext = ctk.CTkTextbox(self, wrap="word", font=(ctext_font, 20), height=70, width=300, activate_scrollbars=True, border_width=2, corner_radius=8)  # 自动换行模式：word/char/none

        # 输入提示文字
        if placeholder_text:
            self.ctktext.insert("0.0", placeholder_text)
            self.ctktext.bind("<FocusIn>", self.clear_placeholder)

        self.ctktext.bind("<FocusOut>", self.restore_placeholder)  # 光标移开
        self.ctktext.grid(row=0, column=1, padx=10, pady=5, sticky="nsew")

    def get(self):
        content = self.ctktext.get("0.0", "end-1c")
        return content.strip()

    def clear_placeholder(self, event):  # 清除提示文字
        if (self.get() == self.placeholder):
            self.ctktext.delete("1.0", "end")  # 删除所有文字

    def restore_placeholder(self, event):
        if (not self.get()):
            self.ctktext.insert("0.0", self.placeholder)

    def set_size(self, x, y, dx, dy):
        self.width = x
        self.high = y
        self.geometry("{}x{}+{}+{}".format(x, y, dx, dy))


class expand_frame(ctk.CTkFrame):
    def __init__(self, master, title, is_expanded=False, text_color='black'):
        super().__init__(master)

        self.is_expanded = is_expanded
        self.title = title
        self.configure(border_width=4, border_color='#FFF5EE', fg_color='#fffef5')

        self.grid_columnconfigure(0, weight=1)  # 主窗口第0列可扩展
        self.header_button = ctk.CTkButton(
            self,
            text=f"▶{self.title}",
            command=self.change_expand,
            anchor="w",
            fg_color="transparent",
            text_color=text_color,
            font=(ctitle_font, 25),
            hover=False  # 鼠标悬停不变色
        )
        self.header_button.grid(row=0, column=0, sticky="ew", padx=2, pady=2)

        self.content_frame = ctk.CTkFrame(self, fg_color='#E0FFFF', corner_radius=0)  # 内容部分
        self.content_frame.grid(row=1, column=0, sticky="ew", padx=2, pady=2)
        if (not is_expanded):
            self.content_frame.grid_remove()

    def change_expand(self):
        self.is_expanded = not self.is_expanded
        if self.is_expanded:
            self.header_button.configure(text=f"▼ {self.title}")
            self.content_frame.grid()
        else:
            self.header_button.configure(text=f"▶ {self.title}")
            self.content_frame.grid_remove()

    def set_color(self, fg_color):
        self.configure(fg_color=fg_color)


class phigros_data(ctk.CTk):
    def __init__(self):
        super().__init__()
        global ctext_font
        ctext_font = 'rhythmgame_database/fonts/NotoSerifSC-VariableFont_wght.ttf'
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.configure(fg_color='#FFF5EE')
        self.title("phigros数据库")

        def refresh_root(event):
            self.destroy()

            subprocess.run(['python', py_path])
        self.bind('<F5>', refresh_root)

        def phigros_destroy(event):
            self.destroy()
        self.bind("<Escape>", phigros_destroy)

        self.grid_item = {'增': {}, '删': {}, '改': {}, '查': {}, '更': {}}  # 记录主窗口 用来快捷隐藏/展示
        self.contain_item = {'增': {}, '删': {}, '改': {}, '查': {}, '更': {}, '侧': {}}  # 记录内容 便于在class外用
        self.create_sidebar()
        self.content_frame = ctk.CTkFrame(self)
        self.content_frame.grid(row=0, column=1, sticky="nsew", padx=3, pady=0)
        self.content_frame.configure(fg_color='#F0FFF0')
        self.now_page_name = -1  # 当前在主页面展示的页面

        self.MAX_LEVEL = 17.6  # 最高定数
        self.sidebar_expanded = True
        self.tip_song = ''
        self.tip_attri = ''
        self.tip_diff = ''  # 查找时生成提示部分必备属性
        self.addable_song = {}
        self.diff_list = ['AT', 'IN', 'HD', 'EZ']
        self.diff_color = {'AT': '#ff8aba', 'IN': '#ff6a5c', 'HD': '#3D71B2', 'EZ': '#5ffe5d'}
        self.commen_attri = ['歌曲id', '名称', '曲师', '俗称', '章节', 'bpm', '时长', '画师']  # 通用属性
        self.diff_attri = ['定数', 'acc', '单曲rks', '简评', '物量', '谱师']  # 难度差分属性
        self.ban_hid_attri = ['歌曲id', '章节', 'bpm', '时长', '画师', '物量', '谱师']  # 默认不在查找页面布局的属性

        tree = ET.parse(xmlpath)
        xmlroot = tree.getroot()
        for idx in range(len(xmlroot)):
            avali_diff_list = []
            song_info = self.get_song_data('index', idx)
            if (song_info):
                for diffi in self.diff_list:
                    if (diffi not in song_info.keys()):
                        avali_diff_list.append(diffi)
            else:
                messagebox.showerror('', '无法获取歌曲信息')
                continue
            if (avali_diff_list):
                self.addable_song[f'{song_info['名称']}({song_info['曲师']})'] = avali_diff_list
                if (song_info['俗称'] != '无'):
                    self.addable_song[f'{song_info['俗称']}'] = avali_diff_list
        # print(f'可添加难度歌曲:{self.addable_song}')
        # print(song_values)

        self.get_song_list()
        self.content_frame.grid_rowconfigure(0, weight=1)
        self.content_frame.grid_columnconfigure(0, weight=1)

        self.load_queue = queue.Queue()  # ?
        load_tasks = [
            (self.init_find_window, 40),
            (self.init_add_window, 20),
            (self.init_delete_window, 20),
            (self.init_change_window, 20),
        ]
        threading.Thread(
            target=self._background_loader,  # 指定后台执行函数
            args=(load_tasks,),              # 传入任务列表
            daemon=True                      # 随主线程退出终止（安全机制）
        ).start()
        self._poll_loading_updates()

    def set_size(self, x, y, dx, dy):
        self.geometry("{}x{}+{}+{}".format(x, y, dx, dy))

    def _background_loader(self, tasks):
        for func, weight in tasks:
            func()  # 执行实际加载任务
            # 将进度更新放入队列
            self.load_queue.put(('progress', weight))

        # 加载完成信号
        self.load_queue.put(('complete', None))
        self.change_hide_statue_btn.configure(command=self.change_hide_statue_sidebar)

    def _poll_loading_updates(self):
        try:
            while True:
                msg_type, data = self.load_queue.get_nowait()  # 非阻塞获取消息
                # 处理消息...
        except queue.Empty:
            self.after(50, self._poll_loading_updates)  # 关键调度

    def create_sidebar(self):  # 创建侧边栏
        self.sidebar_frame = ctk.CTkFrame(self)
        self.sidebar_frame.grid(row=0, column=0, sticky="nsew")
        self.sidebar_frame.configure(fg_color='#F0FFFF')

        rowi = 0
        self.change_hide_statue_btn = ctk.CTkButton(self.sidebar_frame, text="☰")
        self.change_hide_statue_btn.grid(row=rowi, column=0, pady=10, padx=10, sticky='nsew')
        self.change_hide_statue_btn.grid_remove()
        rowi += 1
        tooltip = CTkToolTip(self.change_hide_statue_btn, message="折叠侧边栏", bg_color="gray90", font=(ctext_font, 18))
        self.contain_item['侧']['折叠提示'] = tooltip

        pages = {  # 侧边栏按钮 关键字:提示内容
            "增": " 新增项目",
            "删": " 删除项目",
            "改": " 修改项目",
            '查': ' 查询项目',
            '更': ' 更新数据',
            '测': '测试模块'
        }

        icon_prefix = 'rhythmgame_database/icons/'
        icon_path = ['add song.png', 'delete song.png', 'change song.png', 'find song.png', 'grab.png', 'test.png']
        tip_text = ['新增曲目或对已有曲子进行难度差分', '删除曲子或某个难度', '更改曲子的属性', 'rks及各种属性查询', '通过萌娘百科中的内容更新数据库', '这是…测开?']
        idx = 0
        self.nav_buttons = {}  # 导航按钮
        for page_id, text in pages.items():
            icon_image = ctk.CTkImage(light_image=Image.open(icon_prefix + icon_path[idx]), size=(20, 20))
            btn = ctk.CTkButton(self.sidebar_frame, text=text, command=lambda pid=page_id: self.switch_page(pid), anchor="w", image=icon_image, compound="left")  # 图片在文字左侧
            btn.grid(row=rowi, column=0, pady=10, padx=10, sticky='nsew')
            rowi += 1
            self.nav_buttons[page_id] = btn  # 记录按钮地址 方便后续调用

            tooltip = CTkToolTip(btn, message=tip_text[idx], bg_color="gray90", font=(ctext_font, 18))
            idx += 1

        for i in self.nav_buttons.values():
            i.grid_remove()  # 默认全隐藏 初始化好一个显示一个

        self.nav_buttons['更'].grid()
        self.show_test = False

        def show_test_part(event):
            if (self.show_test):
                self.nav_buttons['测'].grid_remove()
            else:
                self.nav_buttons['测'].grid()
            self.show_test = not self.show_test
        self.bind("<Shift-L>", show_test_part)  # 切换测试按钮可见性

    def change_hide_statue_sidebar(self):  # 切换侧边栏状态
        if self.sidebar_expanded:
            self.sidebar_frame.configure(width=20)
            self.contain_item['侧']['折叠提示'].configure(message='展开侧边栏')
            self.change_hide_statue_btn.configure(width=20)
            for keyi, vali in self.nav_buttons.items():
                if (keyi == '测'):
                    continue
                vali.grid_remove()
        else:
            self.sidebar_frame.configure(width=250)
            self.contain_item['侧']['折叠提示'].configure(message='折叠侧边栏')
            self.change_hide_statue_btn.configure(width=140)
            for keyi, vali in self.nav_buttons.items():
                if (keyi == '测'):
                    continue
                vali.grid()

        self.sidebar_expanded = not self.sidebar_expanded

    def switch_page(self, page_id):  # 切换主窗口显示页面
        if (self.now_page_name != page_id and page_id != '测'):
            self.view_page(self.now_page_name)  # 隐藏当前页
            # print(f"隐藏{self.now_page_name}")
            self.now_page_name = page_id
            self.view_page(page_id, True)
            # print(f"显示{page_id}")
            self.contain_item['查']['设置按钮'].place_forget()
            if (page_id == '查'):
                self.change_find_window(self.find_now_page)
                self.contain_item['查']['设置按钮'].place(
                    relx=0.25,
                    rely=0.95,
                    anchor="s",
                    relwidth=0.7  # 相对宽度
                )
                self.contain_item['查']['设置窗口'].withdraw()
            # self.pages[page_id]()
        if (page_id == '测'):
            self.test()
        if (page_id == '更'):
            self.grab_info()

    def get_song_data(self, get_type, data):
        '''{
        '歌曲id': '2',
        '名称': 'IndelibleScar',
        '曲师': 'Noah',
        '俗称': '无',
        '章节': 'Chapter EX-Paradigm:Reboot 精选集',
        'bpm': '223',
        '时长': '2:17',
        '画师': '兜',
        'AT': {
        '定数': '16.5',
        'acc': '99.08',
        '单曲rks': '15.8322',
        '简评': '无',
        '物量': '1207',
        '谱师': '上班睡大觉_Sleepyhead'_Sleepyhead'
        },
        'IN': {'定数': '15.3', 'acc': '99.11', '单曲rks': '14.7008', '简评': '无', '物量': '844', '谱师': 'Likey affected by Ancestral Xhronicle'},
        'HD': {'定数': '11.5', 'acc': '0', '单曲rks': '0', '简评': '无', '物量': '733', '谱师': 'Salt & Barbarianerman'},
        'EZ': {'定数': '7.0', 'acc': '0', '单曲rks': '0', '简评': '无', '物量': '316', '谱师': 'Clutter & Barbarianerman'}
        }'''
        tree = ET.parse(xmlpath)
        xmlroot = tree.getroot()
        song_info = {}
        if (get_type == 'name'):
            complex_name = data
            # print(name, '\n',composer)
            try:
                song_idx = self.song_list.index(complex_name)
            except:
                return None
        elif (get_type == 'index'):
            song_idx = data

        songi = xmlroot[song_idx]

        song_info['歌曲id'] = songi.attrib['id']

        name_elm = songi.find('名称')
        song_info['名称'] = name_elm.text if name_elm is not None else '无'

        composer_elm = songi.find('曲师')
        song_info['曲师'] = composer_elm.text if composer_elm is not None else '无'

        nickname_elm = songi.find('俗称')
        song_info['俗称'] = nickname_elm.text if nickname_elm is not None else '无'

        chapter_elm = songi.find('章节')
        song_info['章节'] = chapter_elm.text if chapter_elm is not None else '无'

        bpm_elm = songi.find('bpm')
        song_info['bpm'] = bpm_elm.text if bpm_elm is not None else '0'

        time_span_elm = songi.find('时长')
        song_info['时长'] = time_span_elm.text if time_span_elm is not None else '0:0'

        drawer_elm = songi.find('画师')
        song_info['画师'] = drawer_elm.text if drawer_elm is not None else '无'

        for diffi in self.diff_list:
            avaliable_diff_elm = songi.find(diffi)
            if (avaliable_diff_elm is not None):
                diff_attri = {}
                level_elm = avaliable_diff_elm.find('定数')
                diff_attri['定数'] = level_elm.text if level_elm is not None else '0'

                acc_elm = avaliable_diff_elm.find('acc')
                diff_attri['acc'] = acc_elm.text if acc_elm is not None else '0'

                singal_rks_elm = avaliable_diff_elm.find('单曲rks')
                diff_attri['单曲rks'] = singal_rks_elm.text if singal_rks_elm is not None else '0'

                comment_elm = avaliable_diff_elm.find('简评')
                diff_attri['简评'] = comment_elm.text if comment_elm is not None else '无'

                note_cnt_elm = avaliable_diff_elm.find('物量')
                diff_attri['物量'] = note_cnt_elm.text if note_cnt_elm is not None else '0'

                noter_elm = avaliable_diff_elm.find('谱师')
                diff_attri['谱师'] = noter_elm.text if noter_elm is not None else '无'

                song_info[diffi] = diff_attri

        # print(song_info)

        return song_info

    def get_song_list(self):
        tree = ET.parse(xmlpath)
        xmlroot = tree.getroot()
        self.song_list = []
        self.nickname_list = []
        self.nickname_dic = {}  # 俗称:名称
        self.composer_list = []
        self.chapter_list = ['无']
        for songi in xmlroot:
            composer = songi.find('曲师')
            if (composer.text and composer.text != '无'):
                self.composer_list.append(composer.text)
            name = songi.find('名称')
            self.song_list.append(f'{name.text}({composer.text})')
            nickname = songi.find('俗称')
            if (nickname.text and nickname.text != '无'):
                self.nickname_list.append(nickname.text)
                self.nickname_dic[nickname.text] = f'{name.text}({composer.text})'

            chapter = songi.find('章节')
            if (chapter.text and chapter.text != '无'):
                self.chapter_list.append(chapter.text)
        # print(self.nickname_dic)
        self.composer_list = list(set(self.composer_list))
        self.chapter_list = list(set(self.chapter_list))

    def valid_test(self, s_type, val):
        val = val.strip()
        if (not val):
            return '无'

        def valid_float(attri_type, val, minn, maxx):
            try:
                rst = eval(val)
                if (minn <= rst <= maxx):
                    return str(rst)
                else:
                    messagebox.showerror(f'{attri_type}非法范围', f'哪有数值为{rst}的歌啊?')
                    return 'error'
            except:
                valid_char = [str(i) for i in range(10)] + ['.']
                error_char = ''
                for i in val:
                    if (i not in valid_char):
                        error_char += i
                messagebox.showerror(f'{attri_type}报错', f'输入中包含 {set(error_char)} 等非法字符')
                return 'error'

        if (s_type == '名称'):
            if (val in self.nickname_list):
                val = self.nickname_dic[val]
                # print(f'俗称转名称:{val}')

        elif (s_type in ['定数', '单曲rks']):
            return valid_float(s_type, val, 0, self.MAX_LEVEL)

        elif (s_type == 'acc'):
            return valid_float(s_type, val, 0, 100)

        elif (s_type == '物量'):
            if (val.isdigit()):
                return str(int(val))
            messagebox.showerror(f'{s_type}非法输入', f'{s_type}必须是纯数字')
            return 'error'

        elif (s_type == 'bpm'):
            valid_char = [str(i) for i in range(10)] + ['~', '.']
            for chari in val:
                if (chari not in valid_char):
                    messagebox.showerror(f'{s_type}非法输入', f'含有非法字符{chari}')
                    return 'error'
            try:
                return str(eval(val))
            except:
                return val

        elif (s_type == '时长'):
            try:
                if (':' in val):
                    val = val.replace(':', '.')  # 适应网页读取
                val = str(eval(val))
                if ('.' in val):
                    temp_val = val
                    temp_val = temp_val.split('.')
                    if (60 < int(temp_val[1]) or int(temp_val[1]) < 0):
                        messagebox.showerror(f'{s_type}非法输入', f'哪有{temp_val[1]}秒啊?')
                        return 'error'

            except:
                valid_char = [str(i) for i in range(10)] + ['.']
                error_char = ''
                for i in val:
                    if (i not in valid_char):
                        error_char += i
                messagebox.showerror(f'{s_type}非法输入', f'时长输入中包含 {set(error_char)} 等非法字符')
                return 'error'

        return val

    def view_page(self, page_name, viewable=False):
        if (page_name not in ['增', '删', '改', '查', '更']):
            return
        for itemi in self.grid_item[page_name].values():
            if (viewable):
                itemi.grid()
            else:
                itemi.grid_remove()

    def init_add_window(self):
        rowi = 0
        song_values = list(self.addable_song.keys())
        add_content_frame = ctk.CTkFrame(self.content_frame)
        add_content_frame.configure(fg_color='transparent')
        self.grid_item['增']['窗口'] = add_content_frame

        add_name_choose = combobox_frame(add_content_frame, '歌曲名称*', '添加歌曲', song_values)
        add_name_choose.grid(row=rowi, column=0, pady=5, padx=10, sticky='nsew')
        self.contain_item['增']['名称'] = add_name_choose
        rowi += 1

        def filter_values(event):  # 模糊搜索 过滤结果
            input_text = add_name_choose.get().strip().lower().replace(' ', '')
            if not input_text:
                add_name_choose.option_menu.configure(values=song_values)
                return
            filtered = [item for item in song_values if input_text in item.lower()]
            add_name_choose.option_menu.configure(values=filtered)
        add_name_choose.option_menu.bind("<KeyRelease>", filter_values)

        nickname_entry = entry_frame(add_content_frame, '歌曲俗称:', '儿童鞋垫')
        nickname_entry.grid(row=rowi, column=0, pady=5, padx=10, sticky='nsew')
        self.contain_item['增']['俗称'] = nickname_entry
        rowi += 1

        composer_choose = combobox_frame(add_content_frame, '曲师*', '增加曲师', self.composer_list)
        composer_choose.grid(row=rowi, column=0, pady=5, padx=10, sticky='nsew')
        self.contain_item['增']['曲师'] = composer_choose
        rowi += 1

        bpm_entry = entry_frame(add_content_frame, '歌曲bpm:', '2333')
        bpm_entry.grid(row=rowi, column=0, pady=5, padx=10, sticky='nsew')
        self.contain_item['增']['bpm'] = bpm_entry
        rowi += 1

        time_span_entry = entry_frame(add_content_frame, '歌曲时长:', '7.21 or 07:21')
        time_span_entry.grid(row=rowi, column=0, pady=5, padx=10, sticky='nsew')
        self.contain_item['增']['时长'] = time_span_entry
        rowi += 1

        drawer_entry = entry_frame(add_content_frame, '曲绘画师:', '笔记RE')
        drawer_entry.grid(row=rowi, column=0, pady=5, padx=10, sticky='nsew')
        self.contain_item['增']['画师'] = drawer_entry
        rowi += 1

        chapter_choose = optionmenu_frame(add_content_frame, '章节名称', '增加章节', self.chapter_list, '无')
        chapter_choose.grid(row=rowi, column=0, pady=5, padx=10, sticky='nsew')
        self.contain_item['增']['章节'] = chapter_choose
        rowi += 1

        difficulty_choose = optionmenu_frame(add_content_frame, '歌曲难度*', '增加难度', self.diff_list, 'IN')
        difficulty_choose.grid(row=rowi, column=0, pady=5, padx=10, sticky='nsew')
        self.contain_item['增']['难度'] = difficulty_choose
        rowi += 1

        level_entry = entry_frame(add_content_frame, '歌曲定数*', '11.3')
        level_entry.grid(row=rowi, column=0, pady=5, padx=10, sticky='nsew')
        self.contain_item['增']['定数'] = level_entry
        rowi += 1

        accuracy_entry = entry_frame(add_content_frame, 'acc*', '66.6')
        accuracy_entry.grid(row=rowi, column=0, pady=5, padx=10, sticky='nsew')
        self.contain_item['增']['acc'] = accuracy_entry
        rowi += 1

        note_cnt_entry = entry_frame(add_content_frame, '歌曲物量:', '2085')
        note_cnt_entry.grid(row=rowi, column=0, pady=5, padx=10, sticky='nsew')
        self.contain_item['增']['物量'] = note_cnt_entry
        rowi += 1

        noter_entry = entry_frame(add_content_frame, '歌曲谱师:', '百九十八')
        noter_entry.grid(row=rowi, column=0, pady=5, padx=10, sticky='nsew')
        self.contain_item['增']['谱师'] = noter_entry
        rowi += 1

        comment_placeholder_text = '先生 买朵花吗~?'
        comment_entry = muti_entry_frame(add_content_frame, '简评一下:', comment_placeholder_text)
        comment_entry.grid(row=rowi, column=0, pady=5, padx=10, sticky='nsew')
        self.contain_item['增']['简评'] = comment_entry
        rowi += 1

        def add_confirm():
            tree = ET.parse(xmlpath)
            xmlroot = tree.getroot()

            add_name = self.valid_test('名称', add_name_choose.get())
            nickname = self.valid_test('俗名', nickname_entry.get())  # self.valid_test('', )
            composer = self.valid_test('曲师', composer_choose.get())
            bpm = self.valid_test('bpm', bpm_entry.get())
            time_span = self.valid_test('时长', time_span_entry.get())
            drawer = self.valid_test('画师', drawer_entry.get())
            chapter = self.valid_test('章节', chapter_choose.get())

            difficulty = difficulty_choose.get()
            # print(difficulty)
            level = self.valid_test('定数', level_entry.get())
            accuracy = self.valid_test('acc', accuracy_entry.get())
            comment = self.valid_test('简评', comment_entry.get())
            note_cnt = self.valid_test('物量', note_cnt_entry.get())
            noter = self.valid_test('谱师', noter_entry.get())
            if ('无' in (add_name, composer) or 'error' in (add_name, nickname, composer, bpm, time_span, drawer, chapter, level, accuracy, comment, note_cnt, noter)):
                return
            if (comment == comment_placeholder_text):
                comment = '无'

            if (add_name in self.song_list):  # 已有歌曲新差分
                print(f'{add_name}已经在列表中,差分')
                index = self.song_list.index(add_name)
                # print('index = ', index)
                add_song = xmlroot[index]
                if (add_song.find(difficulty) is not None):
                    print(f'{difficulty}难度已经存在')
                    return
            else:
                print(f'新建歌曲{add_name}')
                new_id = len(xmlroot)
                index = new_id

                add_song = ET.SubElement(xmlroot, 'song')  # 若是在下面len的话会多算已经创建的这个 导致id多+1
                add_song.attrib['id'] = f'{new_id}'
                ET.SubElement(add_song, '名称').text = add_name
                ET.SubElement(add_song, '俗称').text = nickname
                if (nickname != '无'):
                    self.nickname_list.append(nickname)
                    self.nickname_dic[nickname] = f'{add_name}({composer})'

                ET.SubElement(add_song, '曲师').text = composer
                self.song_list.append(f'{add_name}({composer})')
                if (composer not in self.composer_list):
                    self.composer_list.append(composer)

                ET.SubElement(add_song, '章节').text = chapter
                if (chapter not in self.chapter_list):
                    self.chapter_list.append(chapter)

                ET.SubElement(add_song, 'bpm').text = bpm
                ET.SubElement(add_song, '时长').text = time_span
                ET.SubElement(add_song, '画师').text = drawer

            chafen = ET.SubElement(add_song, f'{difficulty}')
            ET.SubElement(chafen, '定数').text = level
            ET.SubElement(chafen, 'acc').text = accuracy
            if (float(accuracy) < 70):
                singal_rks = '0'
            else:
                singal_rks = str(round(float(level) * pow((float(accuracy) - 55) / 45, 2), 4))
            ET.SubElement(chafen, '单曲rks').text = singal_rks
            ET.SubElement(chafen, '简评').text = comment
            ET.SubElement(chafen, '物量').text = note_cnt
            ET.SubElement(chafen, '谱师').text = noter

            messagebox.showinfo("", f'{add_name}({composer})成功加入数据库')
            tree.write(xmlpath, encoding='utf-8', xml_declaration=True)
            singal_rks = float(singal_rks)
            change = False
            if (self.b27_list[-1][0] < singal_rks):  # 更新b27
                song_info = self.get_song_data('index', index)
                self.b27_list = self.b27_list[:len(self.b27_list) - 1:]
                self.b27_list.append([singal_rks, song_info, difficulty])
                self.b27_list.sort(reverse=True, key=lambda x: x[0])  # 降序排列
                change = True

            if (int(eval(accuracy)) == 100 and self.phi3_list[-1][0] < float(level)):
                song_info = self.get_song_data('index', index)
                self.phi3_list = self.phi3_list[:len(self.phi3_list) - 1:]
                self.phi3_list.append((float(level), song_info, difficulty))
                self.phi3_list.sort(reverse=True, key=lambda x: x[0])  # 降序排列
                change = True

            if (change):
                self.generate_rks_conpound(self.contain_item['查']['滚动页面'])

        confirm_button = ctk.CTkButton(add_content_frame, text='写入数据库', command=add_confirm)
        confirm_button.grid(row=rowi + 1, column=0, pady=10, padx=10)
        self.contain_item['增']['确认'] = confirm_button
        rowi += 1
        add_content_frame.grid(row=0, column=0, sticky="nsew", padx=0, pady=0)
        self.view_page('增')  # 设为不可见
        self.nav_buttons['增'].grid()

    def init_delete_window(self):
        delete_content_frame = ctk.CTkFrame(self.content_frame)
        delete_content_frame.configure(fg_color='transparent')
        self.grid_item['删']['窗口'] = delete_content_frame
        rowi = 0

        select_song = combobox_frame(delete_content_frame, '选择要删除的歌曲', '删除歌曲', self.song_list)

        def filter_values(event):
            input_text = select_song.get().strip().lower().replace(' ', '')
            if not input_text:
                select_song.option_menu.configure(values=self.song_list)
                return
            filtered = [item for item in (self.song_list + self.nickname_list) if input_text in item.lower()]
            select_song.option_menu.configure(values=filtered)
        select_song.option_menu.bind("<KeyRelease>", filter_values)
        select_song.grid(row=rowi, column=0, pady=10, padx=10, sticky='nsew')
        self.contain_item['删']['歌曲'] = select_song
        rowi += 1

        difficulty_choose = optionmenu_frame(delete_content_frame, '选择难度(留空则删掉整首歌)', '删除难度', [''] + self.diff_list, '')
        difficulty_choose.grid(row=rowi, column=0, pady=10, padx=10, sticky='nsew')
        self.contain_item['删']['难度'] = difficulty_choose
        rowi += 1

        def delete_confirm():
            tree = ET.parse(xmlpath)
            xmlroot = tree.getroot()
            delete_song = select_song.get()  # 玩家可能选择后又进行了输入
            if (delete_song in self.nickname_list):
                delete_song = self.nickname_dic[delete_song]
            if (delete_song not in self.song_list):
                messagebox.showwarning('名称错误', f'无法找到曲名为{delete_song}的歌曲')
                return
            else:
                song_idx = self.song_list.index(delete_song)
            song = xmlroot[song_idx]
            diff = difficulty_choose.get()
            complex_name = f'{song.find('名称').text}({song.find('曲师').text})'
            if (diff == ''):  # 没有指定难度 直接删掉整首歌
                messagebox.showinfo('删除歌曲', f"删除歌曲{delete_song}")
                diff_exise = False
                for diffi in self.diff_list:
                    if (song.find(diffi) is not None):  # 根据从高到低的顺序找第一个存在的就是最高的rks
                        diff_exise = True
                        diff_elm = song.find(diffi)
                        singal_rks = float(diff_elm.find('单曲rks').text)
                        # print(diff_exise)
                        break
                if (not diff_exise):  # 无难度存在 只剩个基本信息力…
                    singal_rks = 0
                    diff_elm = None
                xmlroot.remove(song)
                for index in range(song_idx, len(xmlroot)):  # 更新索引
                    xmlroot[index].attrib['id'] = f'{index}'
                self.song_list.remove(complex_name)
                nickname = song.find('俗称').text
                if (nickname != '无'):
                    self.nickname_list.remove(nickname)
                    del self.nickname_dic[nickname]
            else:
                diff_elm = song.find(diff)  # 指定删除的难度
                singal_rks = float(diff_elm.find('单曲rks').text)
                if (diff_elm is None):
                    messagebox.showwarning("难度不存在", f'{delete_song} 没有{diff}难度')
                    return
                else:
                    messagebox.showinfo('删除难度', f'删除难度{diff}')
                    song.remove(diff_elm)

            # print(diff_elm.find('acc').text)
            tree.write(xmlpath, encoding='utf-8', xml_declaration=True)
            # print(singal_rks, self.b27_list[-1][0])
            if (not diff_exise):
                return  # 都无难度存在了不可能需要更新rks了
            if (singal_rks >= self.b27_list[-1][0] or (diff_elm is not None and int(eval(diff_elm.find('acc').text)) == 100 and singal_rks >= self.phi3_list[-1][0])):
                # print('进入')
                index_counter = 0
                self.b27_list = []
                self.phi3_list = []
                for index in range(len(xmlroot)):
                    song_info = self.get_song_data('index', index)
                    for diffi in self.diff_list:
                        if (diffi in song_info.keys()):
                            acc = float(song_info[diffi]['acc'])
                            singal_rks = float(song_info[diffi]['单曲rks'])
                            index_counter += 1
                            item = [singal_rks, index_counter, song_info, diffi]
                            if len(self.b27_list) < 27:
                                heapq.heappush(self.b27_list, item)
                            else:
                                heapq.heappushpop(self.b27_list, item)

                            if (int(acc) == 100):
                                # print(name)
                                if len(self.phi3_list) < 3:
                                    heapq.heappush(self.phi3_list, item)
                                else:
                                    heapq.heappushpop(self.phi3_list, item)

                self.b27_list = [[item[0], item[2], item[3]] for item in self.b27_list]
                self.b27_list.sort(reverse=True, key=lambda x: x[0])  # 降序排列

                self.phi3_list = [[item[0], item[2], item[3]] for item in self.phi3_list]
                self.phi3_list.sort(reverse=True, key=lambda x: x[0])  # 降序排列
                self.generate_rks_conpound(self.contain_item['查']['滚动页面'])

        confirm_button = ctk.CTkButton(delete_content_frame, text='删除选中歌曲的所选属性', command=delete_confirm)
        confirm_button.grid(row=rowi, column=0, pady=10, padx=10)
        self.contain_item['删']['确认'] = confirm_button
        rowi += 1

        image_frame = ctk.CTkFrame(delete_content_frame)
        image_frame.configure(fg_color='transparent')
        image_frame.grid(row=rowi, column=0, sticky="nsew", padx=50, pady=0)
        self.grid_item['删']['曲绘窗口'] = image_frame
        rowi += 1

        delete_content_frame.grid(row=0, column=0, sticky="nsew", padx=0, pady=0)
        self.view_page('删')  # 设为不可见
        self.nav_buttons['删'].grid()

    def init_change_window(self):
        change_content_frame = ctk.CTkFrame(self.content_frame)
        change_content_frame.configure(fg_color='transparent')
        self.grid_item['改']['窗口'] = change_content_frame
        rowi = 0

        select_song_choose = combobox_frame(change_content_frame, '选择更改的歌曲:', '更改歌曲', self.song_list)
        select_song_choose.set_size(width=500)
        select_song_choose.grid(row=rowi, column=0, pady=10, padx=10, sticky='nsew')
        self.contain_item['改']['歌曲'] = select_song_choose
        rowi += 1

        def filter_values(event=None):
            input_text = select_song_choose.get().strip().lower().replace(' ', '')
            if not input_text:
                select_song_choose.option_menu.configure(values=self.song_list)
                return
            filtered = [item for item in (self.song_list + self.nickname_list) if input_text in item.lower()]
            select_song_choose.option_menu.configure(values=filtered)
        select_song_choose.option_menu.bind("<KeyRelease>", filter_values)

        change_difficulty_choose = optionmenu_frame(change_content_frame, '选择更改的难度:', '更改难度', self.diff_list, self.diff_list[0])
        change_difficulty_choose.grid(row=rowi, column=0, pady=10, padx=10, sticky='nsew')
        self.contain_item['改']['难度'] = change_difficulty_choose
        rowi += 1

        self.tip_attri = 'acc'
        attribution_choose = optionmenu_frame(change_content_frame, '选择更改的属性:', '更改属性', ('名称', '俗称', '曲师', '章节', 'bpm', '时长', '画师', '定数', 'acc', '简评', '物量', '谱师'), self.tip_attri)
        attribution_choose.grid(row=rowi, column=0, pady=10, padx=10, sticky='nsew')
        self.contain_item['改']['属性'] = attribution_choose
        rowi += 1

        attribution_entry = muti_entry_frame(change_content_frame, '输入更改值:')
        attribution_entry.grid(row=rowi, column=0, pady=10, padx=10, sticky='nsew')
        self.contain_item['改']['值'] = attribution_entry
        rowi += 1

        tips = ctk.CTkLabel(change_content_frame, text='', font=(ctext_font, 25), fg_color="transparent")
        tips.grid(row=rowi, column=0, pady=5, padx=10)
        self.contain_item['改']['提示'] = tips
        rowi += 1

        def change_confirm():
            song_name = self.valid_test('名称', select_song_choose.get())
            if (song_name == '无' or song_name not in self.song_list):
                messagebox.showerror('无效名称', f'{song_name}不存在')
                return

            tree = ET.parse(xmlpath)
            xmlroot = tree.getroot()
            song_idx = self.song_list.index(song_name)
            song = xmlroot[song_idx]
            difficulty = change_difficulty_choose.get()
            diff_elm = song.find(difficulty)
            singal_rks = diff_elm.find('单曲rks').text
            attribution_type = attribution_choose.get()
            if (attribution_type in self.diff_attri and diff_elm is None):
                messagebox.showwarning('', f'{song_name}没有难度{difficulty}')
                return

            attribution_value = attribution_entry.get()
            attribution_value = self.valid_test(attribution_type, attribution_value)
            if (attribution_value in ('无', 'error')):
                return
            if (attribution_type in self.diff_attri):  # 更改难度相关属性
                messagebox.showinfo("更改", f"{song_name}({difficulty}){attribution_type}:{diff_elm.find(attribution_type).text}->{attribution_value}")
                diff_elm.find(attribution_type).text = attribution_value
            else:  # 更改通用属性
                if (attribution_type in ('名称', '曲师')):  # 维护相应列表
                    bracket_idx = song_name.rindex('(')
                    name = song_name[:bracket_idx:] if attribution_type == '曲师' else attribution_value
                    composer = song_name[bracket_idx + 1: -1:] if attribution_type == '名称' else attribution_value
                    select_song_choose.option_menu.configure(variable=ctk.StringVar(value=f'{name}({composer})'))  # 在更改名称或曲师后 自动将歌曲选择框的内容更改掉 以便继续更改其他属性

                    self.song_list.remove(song_name)
                    self.tip_song = f'{name}({composer})'
                    self.song_list.append(self.tip_song)
                    select_song_choose.option_menu.configure(values=[self.tip_song])

                elif (attribution_type == '俗称'):
                    nickname = song.find(attribution_type).text
                    if (nickname != '无'):
                        self.nickname_list.remove(nickname)
                        del self.nickname_dic[nickname]
                    if (attribution_value != '无'):
                        self.nickname_list.append(attribution_value)
                        self.nickname_dic[attribution_value] = song_name

                messagebox.showinfo("更改", f"{song_name}({difficulty}){attribution_type}:{song.find(attribution_type).text}->{attribution_value}")
                song.find(attribution_type).text = attribution_value

            if (attribution_type in ['acc', '定数']):
                if (float(diff_elm.find('acc').text) >= 70):
                    singal_rks = str(round(float(diff_elm.find('定数').text) * pow((float(diff_elm.find('acc').text) - 55) / 45, 2), 4))
                else:
                    singal_rks = '0'
                diff_elm.find('单曲rks').text = singal_rks

            tree.write(xmlpath, encoding='utf-8', xml_declaration=True)
            self.change_current_info()
            if (attribution_type in ['acc', '定数']):
                song_info = self.get_song_data('index', song_idx)
                singal_rks = float(singal_rks)
                if (self.b27_list[-1][0] <= singal_rks):
                    new_complex_name = f'{['名称']}({song_info['曲师']})'
                    exist = False
                    for b27i in self.b27_list:
                        if (f'{b27i[1]['名称']}({b27i[1]['曲师']})' == new_complex_name or f'{b27i[1]['名称']}({b27i[1]['曲师']})' == song_name):  # 有可能改了名称或曲师 所以改前改后都要看看
                            if (attribution_type in self.diff_attri and b27i[-1] == difficulty):  # 与难度相关的属性需要匹配难度
                                # print(b27i)
                                b27i[1] = song_info
                                b27i[0] = singal_rks
                                exist = True
                            elif (attribution_type in self.commen_attri):
                                b27i[1] = song_info
                                exist = True
                    if (exist is False):
                        self.b27_list = self.b27_list[:len(self.b27_list) - 1:]
                        self.b27_list.append((singal_rks, song_info, difficulty))
                    self.b27_list.sort(reverse=True, key=lambda x: x[0])  # 即使歌曲已经存在 只要改了acc/定数 也会改变位置 所以都要sort
                    self.generate_rks_conpound(self.contain_item['查']['滚动页面'])

                if (int(eval(diff_elm.find('acc').text)) == 100 and self.phi3_list[-1][0] <= singal_rks):
                    new_complex_name = f'{['名称']}({song_info['曲师']})'
                    exist = False
                    for phi3i in self.phi3_list:
                        if (f'{phi3i[1]['名称']}({phi3i[1]['曲师']})' == new_complex_name or f'{phi3i[1]['名称']}({phi3i[1]['曲师']})' == song_name):
                            if (attribution_type in self.diff_attri and phi3i[-1] == difficulty):  # 与难度相关的属性需要匹配难度
                                phi3i[1] = song_info
                                phi3i[0] = singal_rks
                                exist = True
                            elif (attribution_type in self.commen_attri):
                                phi3i[1] = song_info
                                exist = True
                    if (not exist):
                        self.phi3_list = self.phi3_list[:len(self.phi3_list) - 1:]
                        self.phi3_list.append((singal_rks, song_info, difficulty))
                    self.phi3_list.sort(reverse=True, key=lambda x: x[0])
                    self.generate_rks_conpound(self.contain_item['查']['滚动页面'])

        confirm_button = ctk.CTkButton(change_content_frame, text='更改选中歌曲信息', command=change_confirm)
        confirm_button.grid(row=rowi, column=0, pady=5, padx=10)
        self.contain_item['改']['确认'] = confirm_button
        rowi += 1

        image_frame = ctk.CTkFrame(change_content_frame)
        image_frame.configure(fg_color='transparent')
        image_frame.grid(row=rowi, column=0, sticky="nsew", padx=50, pady=0)
        self.grid_item['改']['曲绘窗口'] = image_frame
        rowi += 1

        change_content_frame.grid(row=0, column=0, sticky="nsew", padx=0, pady=0)
        self.view_page('改')
        self.nav_buttons['改'].grid()

    def change_current_info(self):
        tree = ET.parse(xmlpath)
        xmlroot = tree.getroot()
        show_text = ''
        if (not (self.tip_attri and self.tip_diff)):
            return
        # print(self.tip_attri)
        song_idx = self.song_list.index(self.tip_song)
        songi = xmlroot[song_idx]
        self.contain_item['改']['值'].ctktext.delete("0.0", "end")
        if (self.tip_attri in ['定数', 'acc', '简评', '物量', '谱师']):  # 后面要+rks的
            diff = songi.find(self.tip_diff)
            singal_rks = diff.find('单曲rks').text  # .find('')
            show_text = diff.find(self.tip_attri).text
            self.contain_item['改']['值'].ctktext.insert("0.0", show_text if show_text else '无')
            show_text += f'\n单曲rks:{singal_rks}'
        else:
            show_text = songi.find(self.tip_attri).text
            self.contain_item['改']['值'].ctktext.insert("0.0", show_text if show_text else '无')
        show_text_form = ''
        for i in range(0, len(show_text), 40):
            show_text_form += show_text[i:i+40:] + '\n'
        self.contain_item['改']['提示'].configure(text=f"{self.tip_attri}:{show_text_form}")
        self.update()

    def change_find_window(self, attri):  # 根据查找属性更改查找页面的布局
        if (attri not in ['名称', '曲师', '章节', '单曲rks', '定数', 'acc', '简评']):
            messagebox.showerror('', '你这换页查找的属性输入不对啊')
            return
        for page_namei in ('名称', '曲师', '章节', '单曲rks', '定数', 'acc', '简评'):
            if (attri != page_namei):
                # print(f'移除{page_namei}')
                self.grid_item['查'][page_namei].grid_remove()
        self.grid_item['查'][attri].grid()
        # print(f'布局{attri}')
        self.find_now_page = attri
        for content_pagei in self.page_administrator:  # 把滚动框内容全清除
            content_pagei.destroy()
        self.page_administrator = []

    def init_find_attri_setting_window(self):
        find_attri_setting = ctktoplevel_frame(self.sidebar_frame, '查找结果可见属性设置')
        find_attri_setting.set_size(300, 1100, 100, 100)

        def ban_exit_window():
            # print('用户尝试关闭')
            find_attri_setting.withdraw()  # 隐藏
        find_attri_setting.protocol("WM_DELETE_WINDOW", ban_exit_window)
        find_attri_setting.withdraw()  # 隐藏
        self.contain_item['查']['设置窗口'] = find_attri_setting
        rowi = 0

        commen_label = ctk.CTkLabel(find_attri_setting, text='通用属性:', fg_color="#F0FFFF", corner_radius=6, font=(ctitle_font, 27))
        commen_label.grid(row=rowi, column=0, pady=10, padx=10, sticky='nsew')
        rowi += 1

        self.attri_var_dic = {}
        for attri in self.commen_attri + ['曲绘']:
            attri_var = tk.BooleanVar(value=True if attri in ('名称', '曲师', '俗称', '曲绘') else False)
            self.attri_var_dic[attri] = attri_var
            attri_checkbox = ctk.CTkCheckBox(master=find_attri_setting, text=attri, variable=attri_var, font=(ctitle_font, 25))
            attri_checkbox.grid(row=rowi, column=0, pady=10, padx=10, sticky='nsew')
            rowi += 1

        diff_label = ctk.CTkLabel(find_attri_setting, text='难度差分属性:', fg_color="#F0FFFF", corner_radius=6, font=(ctitle_font, 27))
        diff_label.grid(row=rowi, column=0, pady=10, padx=10, sticky='nsew')
        rowi += 1

        for attri in self.diff_attri:
            attri_var = tk.BooleanVar(value=True if attri in ('定数', 'acc', '单曲rks', '简评') else False)
            self.attri_var_dic[attri] = attri_var
            attri_checkbox = ctk.CTkCheckBox(master=find_attri_setting, text=attri, variable=attri_var, font=(ctitle_font, 25))
            attri_checkbox.grid(row=rowi, column=0, pady=10, padx=10, sticky='nsew')
            rowi += 1

        def confirm():
            self.ban_hid_attri = []  # 覆盖上次的选择
            for attri, vari in self.attri_var_dic.items():
                if (vari.get() is False):  # 不布局此属性
                    self.ban_hid_attri.append(attri)
            # print(self.ban_hid_attri)

        button = ctk.CTkButton(find_attri_setting, text='更改可见性', command=confirm)
        button.grid(row=rowi, column=0, pady=10, padx=10)
        rowi += 1

    def init_find_window(self):
        global find_info_page, seek_type_choose
        tab_window = ctk.CTkTabview(self.content_frame, width=500, height=550, corner_radius=10, fg_color="lightblue")
        self.grid_item['查']['总框'] = tab_window

        def change_setting_viewable():
            self.contain_item['查']['设置窗口'].deiconify()

        find_attri_setting_button = ctk.CTkButton(self.sidebar_frame, text='更改可见性', command=change_setting_viewable)
        self.contain_item['查']['设置按钮'] = find_attri_setting_button
        find_attri_setting_button.place(
            relx=0.25,
            rely=0.95,
            anchor="s",
            relwidth=0.7  # 相对宽度
        )
        find_attri_setting_button.place_forget()

        find_rks_page = tab_window.add('rks组成')
        find_info_page = tab_window.add('歌曲信息查找')

        '''处理rks组成'''
        tree = ET.parse(xmlpath)
        xmlroot = tree.getroot()
        self.b27_list = []
        self.phi3_list = []
        index_counter = 0  # 递增

        for index in range(len(xmlroot)):
            song_info = self.get_song_data('index', index)
            for diffi in self.diff_list:
                if (diffi in song_info.keys()):
                    acc = float(song_info[diffi]['acc'])
                    singal_rks = float(song_info[diffi]['单曲rks'])
                    index_counter += 1
                    item = [singal_rks, index_counter, song_info, diffi]

                    if len(self.b27_list) < 27:
                        heapq.heappush(self.b27_list, item)
                    else:
                        heapq.heappushpop(self.b27_list, item)

                    if (int(acc) == 100):
                        # print(name)
                        if len(self.phi3_list) < 3:
                            heapq.heappush(self.phi3_list, item)
                        else:
                            heapq.heappushpop(self.phi3_list, item)

        self.b27_list = [[item[0], item[2], item[3]] for item in self.b27_list]
        self.b27_list.sort(reverse=True, key=lambda x: x[0])  # 降序排列

        self.phi3_list = [[item[0], item[2], item[3]] for item in self.phi3_list]
        self.phi3_list.sort(reverse=True, key=lambda x: x[0])  # 降序排列
        # print(f'phi3={self.phi3_list}')

        scroll_frame = ctk.CTkScrollableFrame(find_rks_page, width=540, height=540)
        scroll_frame.configure(fg_color='transparent')
        self.contain_item['查']['滚动页面'] = scroll_frame
        scroll_frame.pack(fill="both", expand=True, padx=0, pady=0)
        self.generate_rks_conpound(self.contain_item['查']['滚动页面'])

        '''按照属性查找'''
        self.find_now_page = '名称'  # find_now_page==查找页面当前的窗口
        seek_type_choose = optionmenu_frame(find_info_page, '选择查找属性', '查找属性', ['名称', '曲师', '章节', '单曲rks', '定数', 'acc', '简评'], self.find_now_page)
        seek_type_choose.configure(fg_color='transparent')
        seek_type_choose.grid(row=0, column=0, pady=10, padx=10, sticky='nsew')
        self.contain_item['查']['属性'] = seek_type_choose

        self.init_find_composor_page()
        self.init_find_chapter_page()
        self.init_find_name_page()
        self.init_find_comment_page()
        self.init_find_acc_page()
        self.init_find_rks_page()
        self.init_find_level_page()
        self.init_find_attri_setting_window()

        self.now_find_page = 0  # now_find_page==当前查找的页数
        self.find_rst_list = []
        self.total_find_page = 0
        self.show_num_perpage = 20
        self.find_rst_page = ''
        self.page_administrator = []  # 不预先定义 初始化切换查找页面无法通过

        def confirm():
            self.show_num_perpage = self.contain_item['查']['展示数'].get()
            # print(self.show_num_perpage)
            if (self.show_num_perpage.isdigit() is False):
                messagebox.showerror('', '页数输入非全数字')
                return
            else:
                self.show_num_perpage = int(self.show_num_perpage)
            for content_pagei in self.page_administrator:  # 清除滚动展示框中上一次的内容
                content_pagei.destroy()
            self.page_administrator = []
            self.find_rst_list = []
            if (seek_type_choose.get() in ['名称', '曲师', '章节', '简评']):  # 内容选择框+难度框
                page = seek_type_choose.get()
                find_goal = self.valid_test(page, self.contain_item['查'][f'{page}-名称'].get())
                if (find_goal == '无'):
                    messagebox.showerror('', f'你这{page}输入有问题啊')
                    return
                # print(f'查找目标{find_goal}')
                if (page != '简评'):
                    difficulty = self.contain_item['查'][f'{page}-难度'].get()

                tree = ET.parse(xmlpath)
                xmlroot = tree.getroot()
                for song_idx in range(len(xmlroot)):
                    song_elm = xmlroot[song_idx]
                    if (page == '名称'):
                        if (find_goal in self.song_list):  # 准确搜索
                            song_info = self.get_song_data('name', find_goal)
                            if (song_info and difficulty in song_info.keys()):
                                self.find_rst_list.append((song_info, difficulty))
                                break
                        elif (find_goal.lower() in song_elm.find('名称').text.lower()):  # 模糊搜索
                            song_info = self.get_song_data('index', song_idx)
                            if (difficulty in song_info.keys()):
                                self.find_rst_list.append((song_info, difficulty))

                    elif (page == '曲师' and find_goal.lower() in song_elm.find('曲师').text.lower()):
                        song_info = self.get_song_data('index', song_idx)
                        if (difficulty in song_info.keys()):
                            self.find_rst_list.append((song_info, difficulty))

                    elif (page == '章节' and find_goal.lower() in song_elm.find('章节').text.lower()):
                        song_info = self.get_song_data('index', song_idx)
                        if (difficulty in song_info.keys()):
                            self.find_rst_list.append((song_info, difficulty))

                    elif (page == '简评'):
                        song_info = self.get_song_data('index', song_idx)
                        for diffi in self.diff_list:
                            if (diffi in song_info.keys()):
                                commenti = song_info[diffi]['简评'].lower()
                                if (commenti == '无'):
                                    break
                                if (find_goal.lower() in commenti):
                                    self.find_rst_list.append((song_info, diffi))

            elif (seek_type_choose.get() in ['单曲rks', '定数', 'acc']):  # 范围输入框
                page = seek_type_choose.get()
                min_num = self.contain_item['查'][f'{page}-最小值'].get()
                if (min_num == ''):
                    min_num = '0'
                else:
                    min_num = self.valid_test(page, min_num)

                max_num = self.contain_item['查'][f'{page}-最大值'].get()
                if (max_num == ''):
                    if (page == 'acc'):
                        max_num = '100'
                    elif (page in ('单曲rks', '定数')):
                        max_num = self.MAX_LEVEL
                else:
                    max_num = self.valid_test(page, max_num)
                if ('error' in (min_num, max_num)):
                    messagebox.showerror('', f'你这{page}输入有问题啊')
                    return

                # print(f'min={min_num}max={max_num}')
                tree = ET.parse(xmlpath)
                xmlroot = tree.getroot()
                for song_idx in range(len(xmlroot)):
                    song_info = self.get_song_data('index', song_idx)
                    for diffi in self.diff_list:
                        if (diffi in song_info.keys()):
                            if (song_info[diffi][page] != '无'):
                                song_num = float(song_info[diffi][page])
                                if (float(min_num) <= song_num <= float(max_num)):
                                    self.find_rst_list.append((song_info, diffi))

            self.find_rst_page = page
            self.grid_find_rst()

        button = ctk.CTkButton(find_info_page, text='查找选中歌曲', command=confirm)
        button.grid(row=2, column=0, pady=10, padx=10)

        num_perpage_choose = combobox_frame(find_info_page, '每页展示结果数量:', '展示数量', ['10', '20', '30'], '20')
        num_perpage_choose.grid(row=3, column=0, pady=0, padx=0, sticky='nsew')
        self.contain_item['查']['展示数'] = num_perpage_choose

        last_page_button = ctk.CTkButton(find_info_page, text='上一页', command=lambda x=None: self.switch_find_page('上一页'), state="disabled" if (self.now_find_page < 1) else 'normal')
        last_page_button.place(relx=0.25, rely=1.0, anchor="se", relwidth=0.25)
        self.contain_item['查']['上一页'] = last_page_button
        tooltip = CTkToolTip(last_page_button, message='没有上一页了哦' if (self.now_find_page < 1) else f'前往{self.now_find_page - 1}页', bg_color="gray90", font=(ctext_font, 18))
        self.contain_item['查']['上一页提示'] = tooltip

        page_label = ctk.CTkLabel(find_info_page, text='当前页数:1/?', fg_color="#F0FFFF", corner_radius=6)
        self.contain_item['查']['当前页/总页'] = page_label
        page_label.place(relx=0.5, rely=1.0, anchor="s")

        next_page_button = ctk.CTkButton(find_info_page, text='下一页', command=lambda x=None: self.switch_find_page('下一页'), state="disabled")
        next_page_button.place(relx=0.75, rely=1.0, anchor="sw", relwidth=0.25)
        self.contain_item['查']['下一页'] = next_page_button
        tooltip = CTkToolTip(next_page_button, message='正在布局中...', font=(ctext_font, 18))
        self.contain_item['查']['下一页提示'] = tooltip

        tab_window.grid(row=0, column=0, sticky="nsew", padx=0, pady=0)
        self.view_page('查')
        self.nav_buttons['查'].grid()
        self.change_hide_statue_btn.grid()

    def grid_find_rst(self):  # 布局搜索结果
        find_start_time = time.time()

        # 在滚动框架下布局 folder
        self.total_find_page = (len(self.find_rst_list) + self.show_num_perpage - 1) // self.show_num_perpage
        print(self.total_find_page)
        try:
            self.contain_item['查']['属性-内容滚动框'].destroy()
        except:
            pass
        scroll_frame = ctk.CTkScrollableFrame(find_info_page, width=460, height=320)
        scroll_frame.configure(fg_color='transparent')
        scroll_frame.place(
            relx=0.01,    # X起始位置占窗口宽度的10%
            rely=0.40,    # Y起始位置占窗口高度的20%
            relwidth=0.95,  # 控件宽度随窗口宽度变化（始终维持80%）
            relheight=0.45,  # 控件高度随窗口高度变化（始终维持60%）
            anchor="nw"    # 锚点控制延展方向（nw=左上角开始扩展）
        )
        self.contain_item['查']['属性-内容滚动框'] = scroll_frame
        self.page_administrator = []

        for i in range(self.total_find_page):
            page_content_frame = ctk.CTkFrame(scroll_frame)
            page_content_frame.configure(fg_color='transparent')
            self.page_administrator.append(page_content_frame)
            self.page_administrator[i].grid(row=0, column=0, padx=0, pady=0, sticky="nsew")
            self.page_administrator[i].grid_remove()
        self.page_administrator[0].grid()
        for index, songi in enumerate(self.find_rst_list):  # 遍历布局歌曲
            master = self.page_administrator[index//self.show_num_perpage]
            # print(songi)
            song_info = songi[0]
            difficulty = songi[1]
            if (self.find_rst_page in ('曲师', '章节')):
                title_info = song_info[self.find_rst_page]
            elif (self.find_rst_page in ('单曲rks', '定数', 'acc', '简评')):
                title_info = song_info[difficulty][self.find_rst_page]
            elif (self.find_rst_page == '名称'):
                title_info = song_info[difficulty]['单曲rks']
            songi_frame = expand_frame(master, f'{index + 1}.{song_info['名称']}:{title_info[:min(len(title_info), 20):]}', text_color=self.diff_color[difficulty])
            songi_frame.grid(row=index % self.show_num_perpage, column=0, padx=10, pady=5, sticky="w")
            # 布局歌曲隐藏属性
            # print(song_info)
            rowi = 0
            if ('曲绘' not in self.ban_hid_attri):
                try:
                    song_image = ctk.CTkImage(light_image=Image.open(image_path_prefix + f'{song_info['歌曲id']}.png'), size=(454, 240))
                    image_label = ctk.CTkLabel(songi_frame.content_frame, text='', image=song_image)
                    image_label.grid(row=rowi, column=0, pady=5, padx=10, sticky='w')
                    rowi += 1
                except:
                    print(f'{index + 1}.{song_info['名称']}未找到图片')

            for titlei, attri in list(song_info.items()):
                if (titlei in self.diff_list and titlei != songi[1]):  # 仅布局指定难度
                    continue
                if (titlei in self.ban_hid_attri):  # 禁止通用属性
                    # print('禁止布局')
                    continue
                if (type(attri) is not type({1: 1})):
                    # print(f'{titlei}:{attri}')
                    info_label = ctk.CTkLabel(songi_frame.content_frame, text=f'{titlei}:{attri}', fg_color="#F0FFFF", corner_radius=6, width=300, anchor='w')
                    info_label.grid(row=rowi, column=0, padx=10, pady=5, sticky="w")
                    rowi += 1
                else:
                    for dic_titlei, dic_attri in song_info[difficulty].items():
                        if (dic_titlei in self.ban_hid_attri):  # 禁止分级属性
                            continue
                        # print(f'{dic_titlei}:{dic_attri}')
                        info_label = ctk.CTkLabel(songi_frame.content_frame, text=f'{dic_titlei}:{dic_attri}', fg_color="#F0FFFF", corner_radius=6, width=300, anchor='w')
                        info_label.grid(row=rowi, column=0, padx=10, pady=5, sticky="w")
                        rowi += 1

            self.update()
            self.contain_item['查']['下一页'].configure(state="normal" if (self.now_find_page < self.total_find_page-1) else 'disabled')

        # self.contain_item['查']['下一页'].configure(state="normal" if (self.now_find_page < self.total_find_page-1) else 'disabled')
        self.contain_item['查']['当前页/总页'].configure(text=f'当前页数:{self.now_find_page + 1}/{self.total_find_page}')

        print(f'搜索完毕 共找到{len(self.find_rst_list)}个项目 用时{time.time() - find_start_time}s')

    def generate_rks_conpound(self, scroll_frame):  # 布局rks组成结果
        print('rks组成正在生成中...')
        start_time = time.time()
        self.rks = 0
        rowi = 1
        for widget in scroll_frame.winfo_children():
            widget.destroy()
        b27_frame = expand_frame(scroll_frame, 'b27组成:', True)
        b27_frame.set_color('#FFFFF0')
        b27_frame.grid(row=rowi, column=0, pady=5, padx=2, sticky='nsew')
        self.contain_item['查']['b27文件夹'] = b27_frame
        rowi += 1
        for i in range(min(len(self.b27_list), 27)):
            self.rks += self.b27_list[i][0]
            song_info = self.b27_list[i][1]  # (singal_rks, song_info, diffi)
            diffi = self.b27_list[i][2]

            b27_song_label = expand_frame(b27_frame.content_frame, f'{i + 1}.{song_info['名称'][:min(len(song_info['名称']), 20):]}: {self.b27_list[i][0]}', text_color=self.diff_color[diffi])
            b27_song_label.set_color('#FFFFF0')
            b27_song_label.grid(row=i, column=0, pady=5, padx=10, sticky='w')

            show_name = song_info['俗称'] if song_info['俗称'] and song_info['俗称'] != '无' else song_info['名称']
            b27_hid_info = [f'名称:{show_name}', f'难度:{diffi}', f'rks:{self.b27_list[i][0]}', f'acc:{song_info[diffi]['acc']}', f'定数:{song_info[diffi]['定数']}']
            try:
                song_image = ctk.CTkImage(
                    light_image=Image.open(image_path_prefix + f'{song_info['歌曲id']}.png'), size=(454, 240)
                )
                b27_hid_img_label = ctk.CTkLabel(b27_song_label.content_frame, text='', image=song_image)
                b27_hid_img_label.grid(row=0, column=0, pady=5, padx=10, sticky='w')
            except:
                print(f'名称:{show_name}({diffi})图像生成错误')

            for rowj in range(1, len(b27_hid_info)+1):  # 展示属性个数
                b27_hid_info_label = ctk.CTkLabel(b27_song_label.content_frame, text=b27_hid_info[rowj-1], font=(ctext_font, 30), fg_color="#F0FFFF", width=400, anchor='w')
                b27_hid_info_label.grid(row=rowj, column=0, pady=5, padx=10, sticky='w')

        phi3_frame = expand_frame(scroll_frame, 'phi3组成:', True)
        phi3_frame.set_color('#FFFFF0')
        phi3_frame.grid(row=rowi, column=0, pady=5, padx=2, sticky='nsew')
        self.contain_item['查']['phi3文件夹'] = phi3_frame
        rowi += 1

        for i in range(min(len(self.phi3_list), 3)):
            self.rks += self.phi3_list[i][0]
            song_info = self.phi3_list[i][1]  # (singal_rks, song_info, diffi)
            diffi = self.phi3_list[i][2]
            phi3_song_label = expand_frame(phi3_frame.content_frame, f'{i + 1}.{song_info['名称'][:min(len(song_info['名称']), 20):]}: {self.phi3_list[i][0]}', text_color=self.diff_color[diffi])
            phi3_song_label.set_color('#FFFFF0')
            phi3_song_label.grid(row=i, column=0, pady=5, padx=10, sticky='w')

            show_name = song_info['俗称'] if song_info['俗称'] and song_info['俗称'] != '无' else song_info['名称']
            phi3_hid_info = [f'名称:{show_name}', f'难度:{diffi}', f'rks:{self.phi3_list[i][0]}', f'acc:{song_info[diffi]['acc']}', f'定数:{song_info[diffi]['定数']}']
            try:
                song_image = ctk.CTkImage(
                    light_image=Image.open(image_path_prefix + f'{song_info['歌曲id']}.png'), size=(454, 240)
                )
                phi3_hid_info_label = ctk.CTkLabel(phi3_song_label.content_frame, text='', image=song_image)
                phi3_hid_info_label.grid(row=0, column=0, pady=5, padx=10, sticky='w')
            except:
                print(f'名称:{show_name}({diffi})图像生成错误')
            for rowj in range(1, len(phi3_hid_info) + 1):  # 展示属性个数
                phi3_hid_info_label = ctk.CTkLabel(phi3_song_label.content_frame, text=phi3_hid_info[rowj - 1], font=(ctext_font, 30), fg_color="#F0FFFF", width=400, anchor='w')
                phi3_hid_info_label.grid(row=rowj, column=0, pady=5, padx=10, sticky='w')

        rks_label = ctk.CTkLabel(scroll_frame, text=f'rks={round(self.rks/30, 4)}', font=(ctext_font, 35), fg_color="#F0FFFF", width=400, anchor='center')
        rks_label.grid(row=0, column=0, pady=5, padx=5, sticky='w')
        self.contain_item['查']['rks文字'] = rks_label

        print(f'rks组成生成完毕,用时{round(time.time() - start_time, 2)}s')

    def switch_find_page(self, operation):
        self.page_administrator[self.now_find_page].grid_remove()
        self.contain_item['查']['属性-内容滚动框']._parent_canvas.yview_moveto(0)  # 重置换页后滚动条的位置
        self.contain_item['查']['属性-内容滚动框'].update_idletasks()
        if (operation == '上一页'):
            self.now_find_page -= 1
        elif (operation == '下一页'):
            self.now_find_page += 1
        self.page_administrator[self.now_find_page].grid()
        self.contain_item['查']['下一页'].configure(state="normal" if (self.now_find_page < self.total_find_page-1) else 'disabled')
        self.contain_item['查']['下一页提示'].configure(message=f'前往{self.now_find_page + 2}页' if (self.now_find_page < self.total_find_page - 1) else '没有下一页了哦')

        self.contain_item['查']['上一页'].configure(state="disabled" if (self.now_find_page < 1) else 'normal')
        self.contain_item['查']['上一页提示'].configure(message='没有上一页了哦' if (self.now_find_page < 1) else f'前往{self.now_find_page}页')
        self.contain_item['查']['当前页/总页'].configure(text=f'当前页数:{self.now_find_page + 1}/{self.total_find_page}')

    def init_find_name_page(self):  # 记录根据名称寻找的歌曲的限制条件
        find_name_content_frame = ctk.CTkFrame(find_info_page)
        find_name_content_frame.configure(fg_color='transparent')
        self.grid_item['查']['名称'] = find_name_content_frame

        rowi = 0
        seek_list = self.song_list + self.nickname_list
        select_song = combobox_frame(find_name_content_frame, '选择要查找的歌名称/俗称', '查找歌曲', seek_list)
        select_song.configure(fg_color='transparent')
        select_song.set_size(230)
        select_song.grid(row=rowi, column=0, pady=10, padx=10, sticky='nsew')
        self.contain_item['查']['名称-名称'] = select_song
        rowi += 1

        def filter_values(event):
            input_text = select_song.get().strip().lower().replace(' ', '')
            if not input_text:
                select_song.option_menu.configure(values=seek_list)
                return
            filtered = [item for item in seek_list if input_text in item.lower()]
            select_song.option_menu.configure(values=filtered)
        select_song.option_menu.bind("<KeyRelease>", filter_values)

        difficulty_choose = optionmenu_frame(find_name_content_frame, '选择查找难度', '查找难度', self.diff_list, 'IN')
        difficulty_choose.configure(fg_color='transparent')
        difficulty_choose.grid(row=rowi, column=0, pady=10, padx=10, sticky='nsew')
        self.contain_item['查']['名称-难度'] = difficulty_choose  # 查找页面的名称页面下的难度控件
        rowi += 1

        find_name_content_frame.grid(row=1, column=0, sticky="nsew", padx=0, pady=0)

    def init_find_composor_page(self):
        find_composor_content_frame = ctk.CTkFrame(find_info_page)
        find_composor_content_frame.configure(fg_color='transparent')
        self.grid_item['查']['曲师'] = find_composor_content_frame
        find_composor_content_frame.grid(row=1, column=0, sticky="nsew", padx=0, pady=0)

        rowi = 0
        seek_list = self.composer_list
        select_song = combobox_frame(find_composor_content_frame, '选择要查找的曲师名称', '查找曲师', seek_list)
        select_song.configure(fg_color='transparent')
        select_song.set_size(230)
        select_song.grid(row=rowi, column=0, pady=10, padx=10, sticky='nsew')
        self.contain_item['查']['曲师-名称'] = select_song
        rowi += 1

        def filter_values(event):
            input_text = select_song.get().strip().lower()
            if not input_text:
                select_song.option_menu.configure(values=seek_list)
                return
            filtered = [item for item in seek_list if input_text in item.lower()]
            select_song.option_menu.configure(values=filtered)
        select_song.option_menu.bind("<KeyRelease>", filter_values)

        difficulty_choose = optionmenu_frame(find_composor_content_frame, '选择查找难度', '查找难度', self.diff_list, 'IN')
        difficulty_choose.configure(fg_color='transparent')
        difficulty_choose.grid(row=rowi, column=0, pady=10, padx=10, sticky='nsew')
        self.contain_item['查']['曲师-难度'] = difficulty_choose
        rowi += 1

    def init_find_chapter_page(self):
        find_chapter_content_frame = ctk.CTkFrame(find_info_page)
        find_chapter_content_frame.configure(fg_color='transparent')
        self.grid_item['查']['章节'] = find_chapter_content_frame

        rowi = 0
        seek_list = self.chapter_list
        select_song = combobox_frame(find_chapter_content_frame, '选择要查找的章节', '查找章节', seek_list)
        select_song.configure(fg_color='transparent')
        select_song.set_size(230)
        select_song.grid(row=rowi, column=0, pady=10, padx=10, sticky='nsew')
        self.contain_item['查']['章节-名称'] = select_song
        rowi += 1

        def filter_values(event):
            input_text = select_song.get().strip().lower()
            if not input_text:
                select_song.option_menu.configure(values=seek_list)
                return
            filtered = [item for item in seek_list if input_text in item.lower()]
            select_song.option_menu.configure(values=filtered)
        select_song.option_menu.bind("<KeyRelease>", filter_values)

        difficulty_choose = optionmenu_frame(find_chapter_content_frame, '选择查找难度', '查找难度', self.diff_list, 'IN')
        difficulty_choose.configure(fg_color='transparent')
        difficulty_choose.grid(row=rowi, column=0, pady=10, padx=10, sticky='nsew')
        self.contain_item['查']['章节-难度'] = difficulty_choose
        rowi += 1

        find_chapter_content_frame.grid(row=1, column=0, sticky="nsew", padx=0, pady=0)

    def init_find_comment_page(self):
        find_comment_content_frame = ctk.CTkFrame(find_info_page)
        find_comment_content_frame.configure(fg_color='transparent')
        self.grid_item['查']['简评'] = find_comment_content_frame

        rowi = 0

        comment_entry = entry_frame(find_comment_content_frame, '输入简评内容')
        comment_entry.configure(fg_color='transparent')
        comment_entry.set_size(230)
        comment_entry.grid(row=rowi, column=0, pady=10, padx=10, sticky='nsew')
        self.contain_item['查']['简评-名称'] = comment_entry
        rowi += 1

        find_comment_content_frame.grid(row=1, column=0, sticky="nsew", padx=0, pady=0)

    def init_find_acc_page(self):
        find_acc_content_frame = ctk.CTkFrame(find_info_page)
        find_acc_content_frame.configure(fg_color='transparent')
        self.grid_item['查']['acc'] = find_acc_content_frame
        rowi = 0

        min_entry = entry_frame(find_acc_content_frame, '最小acc(不写默认0)')
        min_entry.configure(fg_color='transparent')
        min_entry.set_size(230)
        min_entry.grid(row=rowi, column=0, pady=10, padx=10, sticky='nsew')
        self.contain_item['查']['acc-最小值'] = min_entry
        rowi += 1

        max_entry = entry_frame(find_acc_content_frame, '最大acc(不写默认100)')
        max_entry.configure(fg_color='transparent')
        max_entry.set_size(230)
        max_entry.grid(row=rowi, column=0, pady=10, padx=10, sticky='nsew')
        self.contain_item['查']['acc-最大值'] = max_entry
        rowi += 1

        find_acc_content_frame.grid(row=1, column=0, sticky="nsew", padx=0, pady=0)

    def init_find_rks_page(self):
        find_rks_content_frame = ctk.CTkFrame(find_info_page)
        find_rks_content_frame.configure(fg_color='transparent')
        self.grid_item['查']['单曲rks'] = find_rks_content_frame
        rowi = 0

        min_entry = entry_frame(find_rks_content_frame, '最小单曲rks(不写默认0)')
        min_entry.configure(fg_color='transparent')
        min_entry.set_size(230)
        min_entry.grid(row=rowi, column=0, pady=10, padx=10, sticky='nsew')
        self.contain_item['查']['单曲rks-最小值'] = min_entry
        rowi += 1

        max_entry = entry_frame(find_rks_content_frame, f'最大单曲rks(不写默认{self.MAX_LEVEL})')
        max_entry.configure(fg_color='transparent')
        max_entry.set_size(230)
        max_entry.grid(row=rowi, column=0, pady=10, padx=10, sticky='nsew')
        self.contain_item['查']['单曲rks-最大值'] = max_entry
        rowi += 1

        find_rks_content_frame.grid(row=1, column=0, sticky="nsew", padx=0, pady=0)

    def init_find_level_page(self):
        find_level_content_frame = ctk.CTkFrame(find_info_page)
        find_level_content_frame.configure(fg_color='transparent')
        self.grid_item['查']['定数'] = find_level_content_frame
        rowi = 0

        min_entry = entry_frame(find_level_content_frame, '最小定数(不写默认0)')
        min_entry.configure(fg_color='transparent')
        min_entry.set_size(230)
        min_entry.grid(row=rowi, column=0, pady=10, padx=10, sticky='nsew')
        self.contain_item['查']['定数-最小值'] = min_entry
        rowi += 1

        max_entry = entry_frame(find_level_content_frame, f'最大定数(不写默认{self.MAX_LEVEL})')
        max_entry.configure(fg_color='transparent')
        max_entry.set_size(230)
        max_entry.grid(row=rowi, column=0, pady=10, padx=10, sticky='nsew')
        self.contain_item['查']['定数-最大值'] = max_entry
        rowi += 1

        find_level_content_frame.grid(row=1, column=0, sticky="nsew", padx=0, pady=0)

    def grab_info(self):  # 能跑就行
        # os.environ["CFT_CDN_URL"] = "https://mirrors.cloud.tencent.com/chrome-for-testing"# 强制指定国内镜像源
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
        options = webdriver.ChromeOptions()
        options.add_argument("--headless=new")
        options.add_argument("--disable-images")
        options.page_load_strategy = "eager"
        driver = webdriver.Chrome(options=options)  # 忽略证书错误（仅测试环境使用）
        driver.get("https://mzh.moegirl.org.cn/Phigros/%E8%B0%B1%E9%9D%A2%E4%BF%A1%E6%81%AF")  # 打开萌娘百科-phi-曲目信息
        wait = WebDriverWait(driver, 2)
        _ = wait.until(EC.presence_of_all_elements_located(
            (By.CSS_SELECTOR, "table.wikitable")
        ))
        tree = ET.parse(xmlpath)
        xmlroot = tree.getroot()
        self.get_song_list()
        add_idx = len(xmlroot) + 1

        alltable = driver.find_elements(By.CSS_SELECTOR, 'table.wikitable')

        '''
        tr
        0名称
        1图片 img.
        2章节 td 1.text
        3td 1:BPM 3:曲师
        4td 1:时长 3:画师
        5各种标题 省略
        6EZ等级 定数 物量 谱师
        7HD
        8IN
        (9AT)
        ...len(tr)
        '''
        cnt = 0
        for tablei in alltable:
            alltr = tablei.find_elements(By.TAG_NAME, 'tr')
            cnt_tr = len(alltr)
            diff_dic = {6: 'EZ', 7: 'HD', 8: 'IN', 9: 'AT'}
            for tr_idx in range(cnt_tr):
                now_tr = alltr[tr_idx]
                if (tr_idx == 0):
                    song_name = now_tr.text.replace(' ', '').replace('（', '(').replace('）', ')')
                    song_name = re.sub(r'\[\d+\]', '', song_name)
                    song_name = self.valid_test('名称', song_name)
                    print(f'{cnt}.{song_name}')
                    # print(f'')

                elif (tr_idx == 2):
                    alltd = now_tr.find_elements(By.TAG_NAME, 'td')
                    chapter = self.valid_test('chapter', alltd[1].text)
                    # print(f'章节{chapter}')

                elif (tr_idx == 3):  # 3td 1:BPM 3:曲师
                    alltd = now_tr.find_elements(By.TAG_NAME, 'td')
                    bpm = alltd[1].text
                    if (self.valid_test('bpm', bpm) == 'error'):
                        bpm = '0'
                    # print(f'bpm{bpm}')
                    composer = alltd[3].text
                    composer = re.sub(r'\[\d+\]', '', composer)
                    composer = self.valid_test('曲师', composer)
                    # print(f'曲师{composer}')
                    complex_name = f"{song_name}({composer})"
                    if (complex_name in self.song_list):
                        # print(f'{complex_name}在列表中')
                        song_idx = self.song_list.index(complex_name)
                        song = xmlroot[song_idx]

                        song.find('曲师').text = composer  # 曲师都是查找的依据的一部分了 怎么可能不存在

                    else:
                        print(f'{complex_name}不在列表中')
                        song = ET.SubElement(xmlroot, 'song')
                        ET.SubElement(song, '曲师').text = composer
                        song.attrib['id'] = f'{add_idx}'
                        add_idx += 1

                    song_id = song.attrib['id']
                    if (song.find('名称') is not None):
                        song.find('名称').text = song_name
                    else:
                        ET.SubElement(song, '名称').text = song_name

                    if (song.find('俗称') is not None):
                        pass
                    else:
                        ET.SubElement(song, '俗称').text = '无'

                    if (song.find('章节') is not None):
                        song.find('章节').text = chapter
                    else:
                        ET.SubElement(song, '章节').text = chapter

                    if (song.find('bpm') is not None):
                        song.find('bpm').text = bpm
                    else:
                        ET.SubElement(song, 'bpm').text = bpm

                elif (tr_idx == 4):  # 4td 1:时长 3:画师
                    alltd = now_tr.find_elements(By.TAG_NAME, 'td')

                    time_span = self.valid_test('时长', alltd[1].text)
                    if (time_span == 'error'):
                        time_span = '0.0'
                    # print(f'时长{time_span}')
                    if (song.find('时长') is not None):
                        song.find('时长').text = time_span
                    else:
                        ET.SubElement(song, '时长').text = time_span

                    drawer = self.valid_test('画师', alltd[3].text)
                    # print(f'画师{drawer}')
                    if (song.find('画师') is not None):
                        song.find('画师').text = drawer
                    else:
                        ET.SubElement(song, '画师').text = drawer

                elif (tr_idx > 5):  # 6 EZ 等级 定数 物量 谱师 7HD 8IN 9AT
                    alltd = now_tr.find_elements(By.TAG_NAME, 'td')
                    level = self.valid_test('定数', alltd[2].text)
                    if (level == 'error'):
                        level = '0'
                    note_cnt = self.valid_test('物量', alltd[3].text)
                    if (note_cnt == 'error'):
                        note_cnt = '0'
                    noter = self.valid_test('谱师', alltd[4].text)
                    noter = re.sub(r'\[\d+\]', '', noter)
                    now_diff = diff_dic[tr_idx]

                    if (song.find(now_diff) is not None):
                        diff = song.find(now_diff)
                    else:
                        diff = ET.SubElement(song, now_diff)

                    if (diff.find('物量') is not None):
                        diff.find('物量').text = note_cnt
                    else:
                        ET.SubElement(diff, '物量').text = note_cnt

                    if (diff.find('谱师') is not None):
                        diff.find('谱师').text = noter
                    else:
                        ET.SubElement(diff, '谱师').text = noter

                    if (diff.find('定数') is not None):
                        diff.find('定数').text = level
                    else:
                        ET.SubElement(diff, '定数').text = level

                    if (diff.find('acc') is None):
                        ET.SubElement(diff, 'acc').text = '0'

                    if (float(diff.find('acc').text) >= 70):
                        singal_rks = str(round(float(diff.find('定数').text) * pow((float(diff.find('acc').text) - 55) / 45, 2), 4))
                    else:
                        singal_rks = '0'

                    if (diff.find('单曲rks') is None):
                        ET.SubElement(diff, '单曲rks').text = singal_rks
                    else:
                        diff.find('单曲rks').text = singal_rks
                    if (diff.find('简评') is None):
                        ET.SubElement(diff, '简评').text = '无'

            img_path = tablei.find_element(By.CSS_SELECTOR, 'img.lazyload').get_attribute("data-lazy-src")
            # print(f'img_path = {img_path}')
            response = requests.get(img_path, headers=headers)
            response.raise_for_status()
            if not os.path.exists(image_path_prefix):
                os.makedirs(image_path_prefix)
            full_path = os.path.join(image_path_prefix, f"{song_id}.png")
            with open(full_path, 'wb') as f:
                f.write(response.content)
            response = requests.get(img_path, headers=headers)
            response.raise_for_status()

            cnt += 1
            if (cnt and cnt % 2 == 0):
                driver.execute_script("""
                    arguments[0].scrollIntoView({
                        behavior: 'auto',
                        block: 'end',
                        inline: 'nearest'
                    });
                """, tablei)

        tree.write(xmlpath, encoding='utf-8', xml_declaration=True)  # 更新完一段就写入 防止error
        self.get_song_list()
        driver.quit()

    def test(self):  # 测试模块
        print('test st')
        print('test ed')


phigros_root = phigros_data()
phigros_root.set_size(1000, 750, 720, 300)
phigros_root.mainloop()
