import sys
import time
import xml.etree.ElementTree as ET
from tkinter import messagebox
import customtkinter
import subprocess
import pyautogui
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options
code_path = 'design of class/rhythmgame_database/database.py'
xmlpath = 'design of class/rhythmgame_database/phigros_data.xml'
ctext_font = '华文楷体'; ctitle_font = '仿宋'

def extract_float(s):
    try:
        rst = eval(s)
    except:
        rst = -1
    return rst

class ctktoplevel_frame(customtkinter.CTkToplevel):
    def __init__(self, master, title):
        super().__init__(master)
        self.title(title)
        def destroy_window(event):
            self.destroy()
        self.bind("<Escape>", destroy_window)
    
    def set_size(self, x, y, dx, dy):
        self.width = x
        self.high = y
        self.geometry("{}x{}+{}+{}".format(x, y, dx, dy))

class combobox_frame(customtkinter.CTkFrame):#下拉框
    def __init__(self, master, title, button_name, values, default_value = ''):
        super().__init__(master)
        self.grid_columnconfigure(0, weight=1)
        self.values = values
        self.default_value = default_value
        self.title = title
        self.aa = title
        self.radiobuttons = []
        self.variable = customtkinter.StringVar(value = default_value)

        self.title = customtkinter.CTkLabel(self, text=self.title, fg_color="gray70", corner_radius=6, font = (ctitle_font, 20))
        self.title.grid(row=0, column=0, padx=10, pady=5, sticky="w")

        self.option_menu = customtkinter.CTkComboBox(self, values = self.values, variable = self.variable, command=lambda x: self.click(button_name), font = (ctext_font, 20))
        self.option_menu.grid(row = 0, column = 1, padx=10, pady=5)
    
    def get(self):
        return self.option_menu.get()
    
    def set_size(self, width = 140, height = 28):
        self.option_menu.configure(width = width, height = height)
    
    def click(self, button_name):
        if(button_name == '更改歌曲'):
            song_name = self.get()
            if(song_name in phigros_root.nickname_list):
                song_name = phigros_root.nickname_dic[song_name]
            phigros_root.tip_song = song_name
            rowi = 1
            avaliable_diff_list = []

            tree = ET.parse(xmlpath)
            xmlroot = tree.getroot()
            song_idx = phigros_root.song_list.index(song_name)
            song = xmlroot[song_idx]
            for avaliable_diff_listi in range(2, len(song)):
                avaliable_diff_list.append(song[avaliable_diff_listi].tag)
            change_difflculty_choose = optionmenu_frame(phigros_root.change_attribution_window, '选择更改的难度:','更改难度', avaliable_diff_list, avaliable_diff_list[0])
            change_difflculty_choose.grid(row = rowi, column = 0, pady = 10, padx = 10, sticky = 'nsew')
            rowi += 1
            phigros_root.tip_diffy = avaliable_diff_list[0]
            # print(change_difflculty_choose.get())

            phigros_root.tip_attri = 'acc'
            attribution_choose = optionmenu_frame(phigros_root.change_attribution_window, '选择更改的属性:','更改属性', ('名称', '俗称', '定数', 'acc', '简评'), phigros_root.tip_attri)
            
            attribution_choose.grid(row = rowi, column = 0, pady = 10, padx = 10, sticky = 'nsew')
            rowi += 1
            phigros_root.change_current_info()
            
            attribution_entry = entry_frame(phigros_root.change_attribution_window, '输入更改值:')
            attribution_entry.grid(row = rowi, column = 0, pady = 10, padx = 10, sticky = 'nsew')
            attribution_entry.set_size(width=300)
            rowi += 1

            def song_click():
                change_song = phigros_root.select_song_choose.get()
                attribution_type = attribution_choose.get()
                difflculty = change_difflculty_choose.get()
                attribution_value = attribution_entry.get()
                if(attribution_type ==  '名称'):
                    if(not attribution_type):
                        messagebox.showwarning("名称错误","不能输入空白名称")
                        return
                    messagebox.showinfo('更改',f'名称更改成功\n名称:{song[0].text}->{attribution_value}')
                    song[0].text = attribution_value
                    
                if(attribution_type ==  '俗称'):
                    messagebox.showinfo('更改',f'俗称更改成功\n俗称:{song[1].text}->{attribution_value}')
                    song[1].text = attribution_value
                
                difficulty_find = song.find(difflculty)
                if(difficulty_find ==  None):
                    messagebox.showwarning("难度不存在",f'{change_song}没有{difflculty}难度')
                    return
                if(attribution_type ==  '定数'):
                    messagebox.showinfo("更改",f"{change_song}({difflculty})定数:{difficulty_find[0].text}->{attribution_value}")
                    # fi = open('change.txt', 'a+', encoding='utf-8')
                    # fi.write(f"{change_song}({difflculty}):{difficulty_find[0].text}->{attribution_value}\n")#定数变化写入文件
                    difficulty_find[0].text = attribution_value
                if(attribution_type ==  'acc'):
                    if(not attribution_value.isdigit()):
                        attribution_value = extract_float(attribution_value)
                        if(attribution_value != -1):
                            messagebox.showinfo("更改",f"{change_song}({difflculty})acc:{difficulty_find[1].text}->{attribution_value}")
                            difficulty_find[1].text = attribution_value
                        else:
                            messagebox.showwarning('输入错误','请输入正确浮点数')
                if(attribution_type ==  'acc' or attribution_type ==  '定数'):
                    if(float(difficulty_find[1].text) >= 70):
                        singal_rks = str(round(float(difficulty_find[0].text) * pow((float(difficulty_find[1].text) - 55) / 45, 2), 4))
                    else:
                        singal_rks = '0'
                    difficulty_find[2].text = singal_rks
                if(attribution_type ==  '简评'):
                    difficulty_find[3].text = attribution_value
                    messagebox.showinfo("更改",f"{change_song}({difflculty})简评更改成功")
                    # print(f"{change_song}简评更改成功")
                tree.write(xmlpath, encoding = 'utf-8', xml_declaration = True)
                phigros_root.get_song_list()
                phigros_root.change_current_info()

            confirm_button = customtkinter.CTkButton(phigros_root.change_attribution_window, text = '更改选中歌曲信息', command = song_click)
            confirm_button.grid(row = 6, column = 0, pady = 10, padx = 10)

        if(button_name == '删除歌曲'):
            rowi = 1
            tree = ET.parse(xmlpath)
            xmlroot = tree.getroot()
            diffy = []
            delete_song = self.get()
            if(delete_song in phigros_root.nickname_list):
                delete_song = phigros_root.nickname_dic[delete_song]
            if(delete_song not in phigros_root.song_list):
                messagebox.showwarning('曲名错误', '无法找到该歌曲')
            else:
                song_idx = phigros_root.song_list.index(delete_song)
            song = xmlroot[song_idx]
            for diffyi in range(2, len(song)):
                diffy.append(song[diffyi].tag)
            difficulty_choose = optionmenu_frame(phigros_root.delete_attribution_window, '选择难度(留空则删掉整首歌)','删除难度', tuple(diffy))
            difficulty_choose.grid(row = rowi, column = 0, pady = 10, padx = 10, sticky = 'nsew')
            rowi += 1

            attributions = optionmenu_frame(phigros_root.delete_attribution_window, '选择属性','删除属性', ['简评'])
            attributions.grid(row = rowi, column = 0, pady = 10, padx = 10, sticky = 'nsew')
            rowi += 1
            def delete_song_click():
                if(difficulty_choose.get() == ''):#没有指定难度 直接删掉整首歌
                    messagebox.showinfo('删除歌曲',f"删除歌曲{delete_song}")
                    delete_index = phigros_root.song_list.index(delete_song) - 1
                    xmlroot.remove(song)
                    for index in range(delete_index, len(xmlroot)):
                        xmlroot[index].tag = f'song{index + 1}' 
                    tree.write(xmlpath, encoding = 'utf-8', xml_declaration = True)
                    return
                else:
                    diffi = song.find(difficulty_choose.get())#指定删除的难度
                    if(diffi ==  None):
                        messagebox.showwarning("难度不存在",f'{delete_song}没有{difficulty_choose.get()}难度')
                        return
                if(attributions.get() == ''):#未指定属性 删除整个难度
                    messagebox.showinfo('删除难度',f'删除难度{difficulty_choose.get()}')
                    song.remove(diffi)
                else:
                    messagebox.showinfo('删除属性',f'删除属性{attributions.get()}')
                    diffi.remove(diffi.find(attributions.get()))#删除属性
                tree.write(xmlpath, encoding = 'utf-8', xml_declaration = True)
                phigros_root.get_song_list()
            
            confirm_button = customtkinter.CTkButton(phigros_root.delete_attribution_window, text = '删除选中歌曲的所选属性', command = delete_song_click)
            confirm_button.grid(row = 3, column = 0, pady = 10, padx = 10)

        if(button_name == '查找歌曲'):
            rowi = 2
            tree = ET.parse(xmlpath)
            xmlroot = tree.getroot()
            diffy = []
            for song in xmlroot:
                if(self.get() in [song[0].text, song[1].text]):
                    for diffyi in range(2, len(song)):
                        diffy.append(song[diffyi].tag)
                    break

            difficulty_choose = optionmenu_frame(find_info_page, '选择查找难度(留空查找所有难度)','查找难度', tuple(diffy))
            difficulty_choose.configure(fg_color = 'transparent')
            difficulty_choose.grid(row = rowi, column = 0, pady = 10, padx = 10, sticky = 'nsew')
            rowi += 1
            
            def confirm():
                scroll_frame = customtkinter.CTkScrollableFrame(find_info_page, width=400, height=280)
                scroll_frame.configure(fg_color = 'transparent')
                scroll_frame.grid(row = 6, column = 0, pady = 10, padx = 10, sticky = 'nsew')
                tree = ET.parse(xmlpath)
                xmlroot = tree.getroot()
                find_song = self.get()
                difficulty = difficulty_choose.get()
                for song in xmlroot:
                    if(song[0].text == find_song or song[1].text == find_song):
                        relyi = 0.65; dy = 0.05; relxi = 0.22
                        try:
                            root.name_show.destroy()
                            root.nickname_show.destroy()
                            root.difflculty_show.destroy()
                            root.attribution_show.destroy()
                        except:
                            pass
                        rowi = 0
                        root.name_show = customtkinter.CTkLabel(scroll_frame, text = '{}:{}'.format(song[0].tag, song[0].text), font = (ctext_font, 20))
                        root.name_show.grid(row=rowi, column=0, padx=10, pady=5, sticky="w")
                        rowi += 1

                        root.nickname_show = customtkinter.CTkLabel(scroll_frame, text = '{}:{}'.format(song[1].tag, song[1].text), font = (ctext_font, 20))
                        root.nickname_show.grid(row=rowi, column=0, padx=10, pady=5, sticky="w")
                        rowi += 1

                        if(difficulty == ''):#不指定难度 全都要
                            for index in range(2, len(song)):
                                diffy = song[index]
                                root.difflculty_show = customtkinter.CTkLabel(scroll_frame, text = '{}:'.format(diffy.tag), font = (ctext_font, 20))
                                root.difflculty_show.grid(row=rowi, column=0, padx=10, pady=5, sticky="w")
                                rowi += 1

                                for attri in range(len(diffy)):
                                    root.attribution_show = customtkinter.CTkLabel(scroll_frame, text = '{}:{}'.format(diffy[attri].tag, diffy[attri].text), font = (ctext_font, 20))
                                    root.attribution_show.grid(row=rowi, column=0, padx=10, pady=5, sticky="w")
                                    rowi += 1
                        else:
                            diffy = song.find(difficulty)
                            root.difflculty_show = customtkinter.CTkLabel(scroll_frame, text = '{}:'.format(diffy.tag), font = (ctext_font, 20))
                            root.difflculty_show.grid(row=rowi, column=0, padx=10, pady=5, sticky="w")
                            rowi += 1

                            for attri in range(len(diffy)):
                                root.attribution_show = customtkinter.CTkLabel(scroll_frame, text = '{}:{}'.format(diffy[attri].tag, diffy[attri].text), font = (ctext_font, 20))
                                root.attribution_show.grid(row=rowi, column=0, padx=10, pady=5, sticky="w")
                                rowi += 1
                        return
                messagebox.showwarning('查找失败''查找失败',)
                
            button = customtkinter.CTkButton(find_info_page, text = '查找选中歌曲', command = confirm)
            button.grid(row = rowi, column = 0, pady = 10, padx = 10)
            rowi += 1
               
class optionmenu_frame(customtkinter.CTkFrame):#下拉框
    def __init__(self, master, title, button_name, values, default_value = ''):
        super().__init__(master)
        self.grid_columnconfigure(0, weight=1)
        self.values = values
        self.default_value = default_value
        self.title = title
        self.radiobuttons = []
        self.variable = customtkinter.StringVar(value = default_value)

        self.title = customtkinter.CTkLabel(self, text=self.title, fg_color="gray70", corner_radius=6, font = (ctitle_font, 20))
        self.title.grid(row=0, column=0, padx=10, pady=5, sticky="w")

        self.option_menu = customtkinter.CTkOptionMenu(self, values = self.values, variable = self.variable, command=lambda x: self.click(button_name), font = (ctext_font, 20))
        self.option_menu.grid(row = 0, column = 1, padx=10, pady=5)

    def get(self):
        return self.option_menu.get()

    def set_size(self, width = 140, height = 28):
        self.option_menu.configure(width = width, height = height)

    def click(self, button_name):
        if(button_name == '查找方式'):
            def destroy_all(keep_wid):
                for widget in find_info_page.winfo_children():
                    if(widget != keep_wid):
                        widget.destroy()

            seek_type = self.get()
            print(f"查找方式:指定{seek_type}")
            rowi = 1

            if(seek_type in ['名称', '俗称']):
                destroy_all(seek_type_choose)
                phigros_root.get_song_list()
                if(seek_type == '名称'):
                    seek_list = phigros_root.song_list
                if(seek_type == '俗称'):
                    seek_list = phigros_root.nickname_list

                select_song = combobox_frame(find_info_page, '选择要查找的歌曲', '查找歌曲', seek_list)
                select_song.configure(fg_color = 'transparent')
                select_song.set_size(230)
                select_song.grid(row = rowi, column = 0, pady = 10, padx = 10, sticky = 'nsew')
                rowi += 1
                def filter_values(event):
                    input_text = select_song.get().strip().lower()
                    if not input_text:
                        select_song.option_menu.configure(values=seek_list)
                        return
                    filtered = [item for item in seek_list if input_text in item.lower()]
                    select_song.option_menu.configure(values=filtered)
                select_song.option_menu.bind("<KeyRelease>", filter_values)
            
            if(seek_type in ['单曲rks', '定数', 'acc', '简评']):
                destroy_all(seek_type_choose)
                scroll_frame = customtkinter.CTkScrollableFrame(find_info_page, width=400, height=280)
                scroll_frame.configure(fg_color = 'transparent')
                scroll_frame.grid(row = 6, column = 0, pady = 10, padx = 10, sticky = 'nsew')
                if(seek_type != '简评'):
                    min_entry = entry_frame(find_info_page, '输入最小值:', default_value = '0')
                    min_entry.configure(fg_color = 'transparent')
                    min_entry.grid(row = rowi, column = 0, pady = 10, padx = 10, sticky = 'nsew')
                    rowi +=  1

                    max_entry = entry_frame(find_info_page, '输入最大值:')
                    max_entry.configure(fg_color = 'transparent')
                    max_entry.grid(row = rowi, column = 0, pady = 10, padx = 10, sticky = 'nsew')
                    rowi +=  1
                else:
                    comment_entry = entry_frame(find_info_page, '输入简评:')
                    comment_entry.configure(fg_color = 'transparent')
                    comment_entry.set_size(260)
                    comment_entry.grid(row = rowi, column = 0, pady = 10, padx = 10, sticky = 'nsew')
                    rowi +=  1
                def confirm():
                    try:
                        for widget in scroll_frame.winfo_children():
                            widget.destroy()
                    except:
                        print("控件销毁失败")
                    tree = ET.parse(xmlpath)
                    xmlroot = tree.getroot()
                    rst_list = {}
                    if(seek_type != '简评'):
                        minimum = float(min_entry.get())
                        maxmum = max_entry.get()
                    else:
                        comment = comment_entry.get().strip().lower()
                    if(seek_type == '定数'):
                        index = 0
                        maxmum = float(maxmum) if maxmum != '' else 16.9
                    if(seek_type == 'acc'):
                        index = 1
                        maxmum = float(maxmum) if maxmum != '' else 100
                    if(seek_type == '单曲rks'):
                        index = 2
                        maxmum = float(maxmum) if maxmum != '' else 16.9
                    if(seek_type == '简评'):
                        index = 3
                    for song in xmlroot:
                        for difficulty in range(2, len(song)):
                            if(seek_type != '简评' and minimum <= float(song[difficulty][index].text) <= maxmum):
                                try:
                                    rst_list[(song[1].text if (song[1].text != '无' and song[1].text != None)  else song[0].text) + '-'+ song[difficulty].tag] = float(song[difficulty][index].text)
                                except:
                                    print(f"error{song[1].text} {song[0].text}")
                            elif(seek_type == '简评' and song[difficulty][index].text is not None and comment in song[difficulty][index].text):
                                try:
                                    rst_list[(song[1].text if (song[1].text != '无' and song[1].text != None)  else song[0].text) + '-'+ song[difficulty].tag] = song[difficulty][index].text
                                except:
                                    print(f"error{song[1].text} {song[0].text}")

                    rst_list = sorted(rst_list.items(), key=lambda x: x[1], reverse= True) if len(rst_list) else [('未找到','匹配结果')]
                    # print(rst_list)
                    rowi = 0
                    for key, value in rst_list:
                        label = customtkinter.CTkLabel(scroll_frame, text=f'{str(rowi + 1)}.{key}:{str(value)}', fg_color="gray70", corner_radius=6)
                        label.grid(row=rowi, column=0, padx=10, pady=5, sticky="w")
                        rowi += 1

                button = customtkinter.CTkButton(find_info_page, text = '查找选中歌曲', command = confirm)
                button.grid(row = rowi, column = 0, pady = 10, padx = 10)
                rowi += 1

        if(button_name == '更改属性'):
            phigros_root.tip_attri = self.get()
            phigros_root.change_current_info()

        if(button_name == '更改难度'):
            phigros_root.tip_diffy = self.get()
            phigros_root.change_current_info()

class entry_frame(customtkinter.CTkFrame):#单选框
    def __init__(self, master, title, placeholder_text = '', default_value = ''):
        super().__init__(master)
        self.grid_columnconfigure(0, weight=1)
        self.title = title

        self.title = customtkinter.CTkLabel(self, text=self.title, fg_color="gray70", font = (ctitle_font, 20),corner_radius=6)
        self.title.grid(row=0, column=0, padx=10, pady=5, sticky="w")

        self.ctkentry = customtkinter.CTkEntry(self, placeholder_text = placeholder_text, font = (ctext_font, 20))
        if default_value != '': self.ctkentry.insert(0, default_value)
        self.ctkentry.configure(width = 150, height = 32)
        self.ctkentry.grid(row = 0, column = 1, padx=10, pady=5, sticky="nsew")

    def get(self):
        return self.ctkentry.get()
    
    def set_size(self, width = 150, height = 32):
        self.ctkentry.configure(width = width, height = height)

class App(customtkinter.CTk):#主窗口
    def __init__(self):
        super().__init__()
        self.title("数据库选择")
        def root_destroy(event):
            sys.exit()
                    
        def refresh_root(event):
            try:
                root.destroy()
                phigros_root.destroy()
                subprocess.run(['python', py_path])
            except:
                pass

        self.bind("<Escape>", root_destroy)
        self.bind('<F5>', refresh_root)
        
        relyi = 0.15; dy = 0.18
        def create_phigros_root():
            global phigros_root
            phigros_root = phigros_data()
            phigros_root.set_size(250, 250, 1160, 368)
            phigros_root.mainloop()
        add_song = customtkinter.CTkButton(self, text = 'phigros', command = create_phigros_root , font = (ctitle_font, 25))
        add_song.place(relx=0.5, rely=relyi, anchor="center")
        relyi += dy

    def set_size(self, x, y, dx, dy):
        self.width = x
        self.high = y
        self.geometry("{}x{}+{}+{}".format(x, y, dx, dy))

class phigros_data(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        self.title("phigros数据库")
        def phigros_destroy(event):
            self.destroy()
        self.bind("<Escape>", phigros_destroy)

        self.tip_song = ''; self.tip_attri = ''; self.tip_diffy = ''

        relyi = 0.15; dy = 0.18
        add_song_button = customtkinter.CTkButton(self, text = '新增项目', command = self.add_attribution , font = (ctitle_font, 25))
        add_song_button.place(relx=0.5, rely=relyi, anchor="center")
        relyi += dy

        delete_song_button = customtkinter.CTkButton(self, text = '删除项目', command = self.delete_attribution , font = (ctitle_font, 25))
        delete_song_button.place(relx=0.5, rely=relyi, anchor="center")
        relyi += dy

        change_song_button = customtkinter.CTkButton(self, text = '修改项目', command = self.change_attribution , font = (ctitle_font, 25))
        change_song_button.place(relx=0.5, rely=relyi, anchor="center")
        relyi += dy

        find_song_button = customtkinter.CTkButton(self, text = '查询项目', command = self.find_attribution , font = (ctitle_font, 25))
        find_song_button.place(relx=0.5, rely=relyi, anchor="center")
        relyi += dy

        text_button = customtkinter.CTkButton(self, text = '更新数据', command = self.grab_info , font = (ctitle_font, 25))
        text_button.place(relx=0.5, rely=relyi, anchor="center")
        relyi += dy

    def grab_info(self):
        # 配置 Chrome 选项
        chrome_options = Options()
        chrome_options.add_argument('--ignore-certificate-errors')  # 忽略证书错误
        chrome_options.add_argument('--allow-running-insecure-content')  # 允许不安全内容

        driver = webdriver.Chrome(options=chrome_options)
        driver.get("https://mzh.moegirl.org.cn/Phigros/%E6%9B%B2%E7%9B%AE%E5%88%97%E8%A1%A8")#打开对应地址的网页
        self.get_song_list()
        process_tip_list = ['主线章节', '支线章节', '额外章节', '外传章节', '单曲', 'AT难度']
        time.sleep(2)#等待网页加载
        ask_replace = False
        replace_ask = messagebox.askokcancel("", "当爬取数据与记录数据不同时是否询问?\n默认直接覆盖")
        if replace_ask:
            ask_replace = True
        phi_allsong_div = driver.find_element(By.CSS_SELECTOR, "div.mw-parser-output")
        alltable = phi_allsong_div.find_elements(By.CSS_SELECTOR, 'table.wikitable')
        actions = ActionChains(driver)
        
        tree = ET.parse(xmlpath)
        xmlroot = tree.getroot()
        add_idx = len(xmlroot) + 1
        def get_level_num(s):
            s = s.split('(')
            return s[1].replace(')', '')
        for tableidx in range(5):#0主线章节 4单曲 5AT
            alltr = alltable[tableidx].find_elements(By.TAG_NAME, 'tr')
            high = alltable[tableidx].size["height"]
            for tridx in range(len(alltr)):
                alltd = alltr[tridx].find_elements(By.TAG_NAME, 'td')
                lentd = len(alltd)
                # print(f'lentd={lentd}')
                if(tableidx < 4 and lentd == 7):#0 3 4 5
                    name = alltd[0].text
                    diff_ez = alltd[3].text
                    diff_ez = get_level_num(diff_ez)
                    diff_hd = alltd[4].text
                    diff_hd = get_level_num(diff_hd)
                    diff_in = alltd[5].text
                    diff_in = get_level_num(diff_in)

                elif(tableidx == 4 and lentd == 8):
                    name_table = alltd[1]
                    # text = name_table.text.strip()
                    classes = name_table.get_attribute("class").split()  # 获取类列表
                    if "a" in classes:
                        name = name_table.find_element(By.TAG_NAME, 'a').text
                    else:
                        name = name_table.text
                        
                    # print(f'name={name}')
                    diff_ez = alltd[4].text
                    diff_ez = get_level_num(diff_ez)
                    diff_hd = alltd[5].text
                    diff_hd = get_level_num(diff_hd)
                    diff_in = alltd[6].text
                    diff_in = get_level_num(diff_in)
                
                else:
                    continue

                if(name in self.song_list):
                    # print(f"歌曲{name}已存在")
                    song_idx = self.song_list.index(name)
                    song = xmlroot[song_idx]
                    if(song.find('EZ') == None):
                        add_diff = ET.SubElement(song, 'EZ')
                        ET.SubElement(add_diff, '定数').text = diff_ez
                        ET.SubElement(add_diff, 'acc').text = '0'
                        ET.SubElement(add_diff, '单曲rks').text = '0'
                        ET.SubElement(add_diff, '简评').text = '无'
                    else:
                        diff_attri = song.find('EZ')
                        if(diff_attri is not None and diff_attri[0].text != diff_ez):
                            if(ask_replace):
                                replace_flag = False
                                replace_ez = messagebox.askokcancel("选择", f"歌曲:{name}(EZ)\n是否用抓取数据({diff_ez})\n替换原先数据({diff_attri[0].text})")
                                if replace_ez:
                                    replace_flag = True
                            else:
                                replace_flag = True
                            if(replace_flag):
                                text_ez = diff_attri.find('定数')
                                text_ez.text = diff_ez
                                if(float(diff_attri[1].text) >= 70):
                                    singal_rks = str(round(float(diff_attri[0].text) * pow((float(diff_attri[1].text) - 55) / 45, 2), 4))
                                else:
                                    singal_rks = '0'
                                diff_attri[2].text = singal_rks

                    
                    if(song.find('HD') == None):
                        add_diff = ET.SubElement(song, 'HD')
                        ET.SubElement(add_diff, '定数').text = diff_hd
                        ET.SubElement(add_diff, 'acc').text = '0'
                        ET.SubElement(add_diff, '单曲rks').text = '0'
                        ET.SubElement(add_diff, '简评').text = '无'
                    else:
                        diff_attri = song.find('HD')
                        if(diff_attri  is not None and diff_attri[0].text != diff_hd):
                            if(ask_replace):
                                replace_flag = False
                                replace_hd = messagebox.askokcancel("选择", f"歌曲:{name}(HD)\n是否用抓取数据({diff_hd})\n替换原先数据({diff_attri[0].text})")
                                if replace_hd:
                                    replace_flag = True
                            else:
                                replace_flag = True
                            if(replace_flag):
                                text_hd = diff_attri.find('定数')
                                text_hd.text = diff_hd
                                if(float(diff_attri[1].text) >= 70):
                                    singal_rks = str(round(float(diff_attri[0].text) * pow((float(diff_attri[1].text) - 55) / 45, 2), 4))
                                else:
                                    singal_rks = '0'
                                diff_attri[2].text = singal_rks

                    if(song.find('IN') == None):
                        add_diff = ET.SubElement(song, 'IN') 
                        ET.SubElement(add_diff, '定数').text = diff_in
                        ET.SubElement(add_diff, 'acc').text = '0'
                        ET.SubElement(add_diff, '单曲rks').text = '0'
                        ET.SubElement(add_diff, '简评').text = '无'
                    else:
                        diff_attri = song.find('IN')
                        if(diff_attri is not None and diff_attri[0].text != diff_in):
                            if(ask_replace):
                                replace_flag = False
                                replace_in = messagebox.askokcancel("选择", f"歌曲:{name}(IN)\n是否用抓取数据({diff_in})\n替换原先数据({diff_attri[0].text})")
                                if replace_in:
                                    replace_flag = True
                            else:
                                replace_flag = True
                            if(replace_flag):
                                text_in = diff_attri.find('定数')
                                text_in.text = diff_in
                                if(float(diff_attri[1].text) >= 70):
                                    singal_rks = str(round(float(diff_attri[0].text) * pow((float(diff_attri[1].text) - 55) / 45, 2), 4))
                                else:
                                    singal_rks = '0'
                                diff_attri[2].text = singal_rks
                else:
                    # print(f"歌曲{name}不存在")
                    song = ET.SubElement(xmlroot, f'song{add_idx}') 
                    ET.SubElement(song, '名称').text = name
                    ET.SubElement(song, '俗称').text = '无'
                    add_idx += 1
                    add_diff = ET.SubElement(song, 'EZ') 
                    ET.SubElement(add_diff, '定数').text = diff_ez
                    ET.SubElement(add_diff, 'acc').text = '0'
                    ET.SubElement(add_diff, '单曲rks').text = '0'
                    ET.SubElement(add_diff, '简评').text = '无'

                    add_diff = ET.SubElement(song, 'HD')
                    ET.SubElement(add_diff, '定数').text = diff_hd
                    ET.SubElement(add_diff, 'acc').text = '0'
                    ET.SubElement(add_diff, '单曲rks').text = '0'
                    ET.SubElement(add_diff, '简评').text = '无'

                    add_diff = ET.SubElement(song, 'IN') 
                    ET.SubElement(add_diff, '定数').text = diff_in
                    ET.SubElement(add_diff, 'acc').text = '0'
                    ET.SubElement(add_diff, '单曲rks').text = '0'
                    ET.SubElement(add_diff, '简评').text = '无'
            #0名称 5AT
            actions.scroll_by_amount(0, high).perform()  #移动1对齐顶部 向下滑动 参数为 (x, y) 偏移量 
            time.sleep(0.5)  # 等待1秒
            print(f'{process_tip_list[tableidx]}更新完成')
        tree.write(xmlpath, encoding = 'utf-8', xml_declaration = True)
        self.get_song_list()
        
        alltr = alltable[5].find_elements(By.TAG_NAME, 'tr')
        high = alltable[5].size["height"]
        for tridx in range(len(alltr)):
            alltd = alltr[tridx].find_elements(By.TAG_NAME, 'td')
            lentd = len(alltd)
            if(lentd == 6):
                name = alltd[0].text
                # print(f'name={name}')
                diff_at = alltd[5].text
                diff_at = get_level_num(diff_at)
            else:
                continue
            if(name in self.song_list):
                # print(f"歌曲{name}已存在")
                song_idx = self.song_list.index(name)
                song = xmlroot[song_idx]
                if(song.find('AT') == None):
                    add_diff = ET.SubElement(song, 'AT')
                    ET.SubElement(add_diff, '定数').text = diff_at
                    ET.SubElement(add_diff, 'acc').text = '0'
                    ET.SubElement(add_diff, '单曲rks').text = '0'
                    ET.SubElement(add_diff, '简评').text = '无'
                else:
                    diff_attri = song.find('AT')
                    if(diff_attri  is not None and diff_attri[0].text != diff_at):
                        if(ask_replace):
                            replace_flag = False
                            replace_at = messagebox.askokcancel("选择", f"歌曲:{name}(AT)\n是否用抓取数据({diff_at})\n替换原先数据({diff_attri[0].text})")
                            if replace_at:
                                replace_flag = True
                        else:
                            replace_flag = True
                        if(replace_flag):
                            text_at = diff_attri.find('定数')
                            text_at.text = diff_at
                            if(float(diff_attri[1].text) >= 70):
                                singal_rks = str(round(float(diff_attri[0].text) * pow((float(diff_attri[1].text) - 55) / 45, 2), 4))
                            else:
                                singal_rks = '0'
                            diff_attri[2].text = singal_rks
            else:
                print(f"歌曲{name}不存在?怎么可能...")
                
        actions.scroll_by_amount(0, high).perform()  #移动1对齐顶部 向下滑动 参数为 (x, y) 偏移量 
        time.sleep(0.5)  # 等待1秒
        print(f'{process_tip_list[5]}更新完成')
        tree.write(xmlpath, encoding = 'utf-8', xml_declaration = True)
        # table.wikitable
        driver.quit()

    def set_size(self, x, y, dx, dy):
        self.width = x
        self.high = y
        self.geometry("{}x{}+{}+{}".format(x, y, dx, dy))

    def get_song_list(self):
        tree = ET.parse(xmlpath)
        xmlroot = tree.getroot()
        self.song_list = []
        self.nickname_list = []
        self.nickname_dic = {}
        for i in xmlroot:
            self.song_list.append(i[0].text)
            if(i[1].text and i[1].text != '无'):
                self.nickname_list.append(i[1].text)
                self.nickname_dic[i[1].text] = i[0].text

    def show_rks_compose(self, master):
        tree = ET.parse(xmlpath)
        xmlroot = tree.getroot()
        rks = 0
        b27_list = []; phi3_dic = {}
        
        for song in xmlroot:
            for diffyi in range(2, len(song)):
                try:
                    b27_list.append((float(song[diffyi][2].text), (song[1].text if song[1].text != '无'  else song[0].text) + '(' + song[diffyi].tag + ')'))#(rks,曲名(难度))
                    
                    if(int(song[diffyi][1].text) ==  100):#acc = 100
                        phi_name = song[0].text + '(' + song[diffyi].tag + ')'
                        phi_level = float(song[diffyi][0].text)
                        phi3_dic[phi_level] = phi_name
                        # print(f'phi_name_level={phi_name_level}')
                except:
                    pass
        b27_dic = sorted(b27_list, key = lambda x : x[0], reverse = True)#根据rks排序
        phi3_list = sorted(phi3_dic.items(), reverse = True)[:3:]
        # print(f'phi3={phi3_list}')
        scroll_frame = customtkinter.CTkScrollableFrame(master, width=500, height=520)
        scroll_frame.configure(fg_color = 'transparent')
        scroll_frame.grid(row = 0, column = 0, pady = 10, padx = 10, sticky = 'w')

        b27_label = customtkinter.CTkLabel(scroll_frame, text = 'b27组成:', font = (ctitle_font, 28))
        b27_label.grid(row = 1, column = 0, pady = 10, padx = 10, sticky = 'w')
        for i in range(min(len(b27_dic), 27)):
            rks += b27_dic[i][0]
            b27_song_label = customtkinter.CTkLabel(scroll_frame, text = '{}.{}:{}'.format(i + 1, b27_dic[i][1], b27_dic[i][0]), font = (ctext_font, 24))
            b27_song_label.grid(row = i + 2, column = 0, pady = 10, padx = 10, sticky = 'w')
        phi3_label = customtkinter.CTkLabel(scroll_frame, text = 'phi3组成:', font = (ctitle_font, 28))
        phi3_label.grid(row = 29, column = 0, pady = 10, padx = 10, sticky = 'w')
        for i in range(min(3, len(phi3_list))):
            rks += phi3_list[i][0]
            phi3_song_label = customtkinter.CTkLabel(scroll_frame, text = '{}.{}:{}'.format(i + 1, phi3_list[i][1], phi3_list[i][0]), font = (ctext_font, 24))
            phi3_song_label.grid(row = i + 30, column = 0, pady = 10, padx = 10, sticky = 'w')
            
        rks_label = customtkinter.CTkLabel(scroll_frame, text = f'rks={rks/30}', font = (ctext_font, 28))
        rks_label.grid(row = 0, column = 0, pady = 10, padx = 10, sticky = 'w')

    def add_attribution(self):
        try:
            self.add_attribution_window.destroy()
        except:
            pass
        self.add_attribution_window = ctktoplevel_frame(self, '添加歌曲界面')
        self.add_attribution_window.set_size(470,450,1679,100)
        
        def refresh_self(event):
            self.add_attribution_window.destroy()
            self.add_attribution()
        self.add_attribution_window.bind('<F5>', refresh_self)
        rowi = 0

        phigros_root.get_song_list()
        song_name_choose = combobox_frame(self.add_attribution_window, '歌曲名称/俗称', '添加歌曲', phigros_root.song_list)
        song_name_choose.grid(row = rowi, column = 0, pady = 10, padx = 10, sticky = 'nsew')
        rowi += 1
        def filter_values(event):
            input_text = song_name_choose.get().strip().lower()
            if not input_text:
                song_name_choose.option_menu.configure(values=phigros_root.song_list)
                return
            filtered = [item for item in (phigros_root.song_list + phigros_root.nickname_list) if input_text in item.lower()]
            song_name_choose.option_menu.configure(values=filtered)
        song_name_choose.option_menu.bind("<KeyRelease>", filter_values)

        difficulty_choose = optionmenu_frame(self.add_attribution_window, '歌曲难度','增加难度', ('AT', 'IN', 'HD', 'EZ'), 'IN')
        difficulty_choose.grid(row = rowi, column = 0, pady = 10, padx = 10, sticky = 'nsew')
        rowi +=  1

        nickname_entry = entry_frame(self.add_attribution_window, '歌曲俗称:', '儿童鞋垫')
        nickname_entry.grid(row = rowi, column = 0, pady = 10, padx = 10, sticky = 'nsew')
        rowi +=  1

        level_entry = entry_frame(self.add_attribution_window, '歌曲定数:', '11.3')
        level_entry.grid(row = rowi, column = 0, pady = 10, padx = 10, sticky = 'nsew')
        rowi +=  1

        accuracy_entry = entry_frame(self.add_attribution_window, 'acc:', '98.6')
        accuracy_entry.grid(row = rowi, column = 0, pady = 10, padx = 10, sticky = 'nsew')
        rowi +=  1

        song_text_entry = entry_frame(self.add_attribution_window, '简评一下:', '噔 噔 咚!')
        song_text_entry.set_size(width=300)
        song_text_entry.grid(row = rowi, column = 0, pady = 10, padx = 10, sticky = 'nsew')
        rowi +=  1

        def get_data():
            tree = ET.parse(xmlpath)
            xmlroot = tree.getroot()
            phigros_root.get_song_list()
            song_name = song_name_choose.get()
            if(song_name in phigros_root.nickname_list):
                song_name = phigros_root.nickname_dic[song_name]
                print(f'俗称转songname{song_name}')
            difficulty = difficulty_choose.get()
            nickname = nickname_entry.get()
            nickname = nickname if nickname else '无'
            level = level_entry.get()
            accuracy = accuracy_entry.get()
            song_text = song_text_entry.get()
            song_text = song_text if song_text else '无'

            if(song_name in phigros_root.song_list):#已有歌曲新差分
                print(f'{song_name}已经在列表中,差分')
                index = phigros_root.song_list.index(song_name)
                #print('index = ', index)
                add_song = xmlroot[index]
                if(add_song.find(difficulty) !=  None):
                    print(f'{difficulty}难度已经存在')
                    return
            else:
                print(f'新建歌曲{song_name}')
                add_song = ET.SubElement(xmlroot, f'song{len(xmlroot) + 1}') 
                ET.SubElement(add_song, '名称').text = song_name
                ET.SubElement(add_song, '俗称').text = nickname
                #只有在新建歌曲才提供通用属性的定义 否则是否判空舍弃都会出问题(新建歌曲 判空跳过会导致没有 添加难度 判空不跳过会覆盖原有属性)

            chafen = ET.SubElement(add_song, f'{difficulty}')
            ET.SubElement(chafen, '定数').text = level#float
            ET.SubElement(chafen, 'acc').text = accuracy
            if(float(accuracy) < 70):
                ET.SubElement(chafen, '单曲rks').text = '0'
            else:
                ET.SubElement(chafen, '单曲rks').text = str(round(float(level) * pow((float(accuracy) - 55) / 45, 2), 4))
            ET.SubElement(chafen, '简评').text = song_text
            # 写回文件，覆盖原文件
            print(f'{song_name}成功加入数据库')
            messagebox.showinfo("",f'{song_name}成功加入数据库')
            tree.write(xmlpath, encoding = 'utf-8', xml_declaration = True)

        confirm_button = customtkinter.CTkButton(self.add_attribution_window, text = '写入数据库', command = get_data)
        confirm_button.grid(row = rowi + 1, column = 0, pady = 10, padx = 10)
        rowi += 1

    def delete_attribution(self):
        try:
            self.delete_attribution_window.destroy()
        except:
            pass
        self.delete_attribution_window = ctktoplevel_frame(self, '删除项目')
        self.delete_attribution_window.set_size(470,250,200,1074)
        def refresh_self(event):
            self.delete_attribution_window.destroy()
            self.delete_attribution()
        self.delete_attribution_window.bind('<F5>', refresh_self)

        rowi = 0
        phigros_root.get_song_list()
        select_song = combobox_frame(self.delete_attribution_window, '选择要删除的歌曲','删除歌曲', phigros_root.song_list)
        def filter_values(event):
            input_text = select_song.get().strip().lower()
            if not input_text:
                select_song.option_menu.configure(values=phigros_root.song_list)
                return
            filtered = [item for item in (phigros_root.song_list + phigros_root.nickname_list) if input_text in item.lower()]
            select_song.option_menu.configure(values=filtered)
        select_song.option_menu.bind("<KeyRelease>", filter_values)
        select_song.grid(row = rowi, column = 0, pady = 10, padx = 10, sticky = 'nsew')
        rowi += 1
        
    def change_current_info(self):
        tree = ET.parse(xmlpath)
        xmlroot = tree.getroot()
        show_text = ''
        if(not (self.tip_attri and self.tip_diffy)):
            return
        # print(self.tip_attri)
        song_idx = self.song_list.index(self.tip_song)
        songi = xmlroot[song_idx]
        if(self.tip_attri in ['定数', 'acc', '简评']):
            diff = songi.find(self.tip_diffy)
            singal_rks = diff[2].text
            if(self.tip_attri == '定数'):
                show_text = diff[0].text
            if(self.tip_attri == 'acc'):
                show_text = diff[1].text
            if(self.tip_attri == '简评'):
                show_text = diff[3].text
            show_text += f'\n单曲rks:{singal_rks}'
        else:
            if(self.tip_attri == '名称'):
                show_text = songi[0].text
            if(self.tip_attri == '俗称'):
                show_text = songi[1].text
        self.change_attribution_window_tips.configure(text = f"{self.tip_attri}:{show_text}")
        phigros_root.update()

    def change_attribution(self):
        try:
            self.change_attribution_window.destroy()
        except:
            pass
        self.change_attribution_window = ctktoplevel_frame(self, '修改项目')
        self.change_attribution_window.set_size(500,350,1700,935)
        rowi = 0
        def refresh_self(event):
            self.change_attribution_window.destroy()
            self.change_attribution()
        self.change_attribution_window.bind('<F5>', refresh_self)

        phigros_root.get_song_list()
        self.select_song_choose = combobox_frame(self.change_attribution_window, '选择更改的歌曲:','更改歌曲', phigros_root.song_list)
        self.select_song_choose.set_size(230)
        self.select_song_choose.grid(row = rowi, column = 0, pady = 10, padx = 10, sticky = 'nsew')
        rowi += 1
        def filter_values(event = None):
            input_text = self.select_song_choose.get().strip().lower()
            if not input_text:
                self.select_song_choose.option_menu.configure(values=phigros_root.song_list)
                return
            filtered = [item for item in (phigros_root.song_list + phigros_root.nickname_list) if input_text in item.lower()]
            self.select_song_choose.option_menu.configure(values=filtered)
        self.select_song_choose.option_menu.bind("<KeyRelease>", filter_values)
        
        self.change_attribution_window_tips = customtkinter.CTkLabel(self.change_attribution_window, text = '')
        self.change_attribution_window_tips.grid(row = 5, column = 0, pady = 10, padx = 10)
        rowi += 1

    def find_attribution(self):
        global seek_type_choose, find_info_page
        find_attribution_window = ctktoplevel_frame(self, '查找项目')
        find_attribution_window.set_size(600,650,72,8)

        tab_window = customtkinter.CTkTabview(find_attribution_window, width=500, height=550, corner_radius=10, fg_color="lightblue")
        tab_window.pack(fill="both", expand=True, padx=20, pady=20)

        find_rks_page = tab_window.add('rks组成')
        find_info_page = tab_window.add('歌曲信息查找')

        rowi = 0
        self.show_rks_compose(find_rks_page)
        def refresh_self(event):
            find_attribution_window.destroy()
            self.find_attribution()
        find_attribution_window.bind('<F5>', refresh_self)
        seek_type_choose = optionmenu_frame(find_info_page, '选择查找方式', '查找方式', ['名称','俗称', '单曲rks', '定数', 'acc', '简评'])
        seek_type_choose.configure(fg_color = 'transparent')
        seek_type_choose.grid(row = rowi, column = 0, pady = 10, padx = 10, sticky = 'nsew')
        rowi += 1

root = App()
root.set_size(250, 250, 1068, 885)
pyautogui.moveTo(1248, 986)
root.mainloop()
