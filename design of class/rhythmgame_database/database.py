'''
加入曲绘图
将EZ IN分颜色输出
布局改成展示全部控件 等选择后更改值的形式
'''
import re
import heapq
import time
import xml.etree.ElementTree as ET
from tkinter import messagebox
import customtkinter as ctk
from PIL import Image
import subprocess
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
py_path = 'rhythmgame_database/database.py'
xmlpath = 'rhythmgame_database/phigros_data.xml'

ctext_font = '华文楷体'; ctitle_font = '仿宋'

class ctktoplevel_frame(ctk.CTkToplevel):
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

class combobox_frame(ctk.CTkFrame):#下拉框+输入
    def __init__(self, master, title, button_name, values, default_value = ''):
        super().__init__(master)
        self.grid_columnconfigure(0, weight=1)
        self.values = values
        self.default_value = default_value
        self.title = title
        self.variable = ctk.StringVar(value = default_value)

        self.title = ctk.CTkLabel(self, text=self.title, fg_color="#F0FFFF", corner_radius=6, font = (ctitle_font, 20))
        self.title.grid(row=0, column=0, padx=10, pady=5, sticky="w")

        self.option_menu = ctk.CTkComboBox(self, values = self.values, variable = self.variable, command=lambda x: self.click(button_name), font = (ctext_font, 20))
        self.option_menu.grid(row = 0, column = 1, padx=10, pady=5)
        self.option_menu.configure(width = 300)
    
    def get(self):
        return self.option_menu.get()
    
    def set_size(self, width = 300, height = 28):
        self.option_menu.configure(width = width, height = height)
    
    def click(self, button_name):
        if(button_name == '添加歌曲'):
            complex_name = self.get()
            bracket_idx = complex_name.rindex('(')
            name = complex_name[:bracket_idx:]
            composer = complex_name[bracket_idx + 1: -1:]
            print(name)
            print(composer)
            song_info = phigros_root.get_song_data('name',(name, composer))
            avaliable_diff_list = []
            for diffi in phigros_root.diff_list:#按照频率排序 加进去的时候就是同样的顺序
                if diffi not in song_info.keys():
                    avaliable_diff_list.append(diffi)
            if(not len(avaliable_diff_list)):
                messagebox.showerror('无', '无可增加难度 请重新选歌')
                phigros_root.song_name_choose.option_menu.configure(variable = ctk.StringVar(value = ''))
                return
            var = ctk.StringVar(value = avaliable_diff_list[0])
            phigros_root.difficulty_choose.option_menu.configure(values = avaliable_diff_list, variable = var)

        if(button_name == '更改歌曲'):
            song_name = phigros_root.valid_test('曲名',self.get())
            phigros_root.tip_song = song_name
            rowi = 1
            avaliable_diff_list = []

            tree = ET.parse(xmlpath)
            xmlroot = tree.getroot()
            song_idx = phigros_root.song_list.index(song_name)
            song = xmlroot[song_idx]
            for diffi in phigros_root.diff_list:#按照频率排序 加进去的时候就是同样的顺序
                if song.find(diffi) is not None:
                    avaliable_diff_list.append(diffi)
            change_difflculty_choose = optionmenu_frame(phigros_root.content_frame, '选择更改的难度:','更改难度', avaliable_diff_list, avaliable_diff_list[0])
            change_difflculty_choose.grid(row = rowi, column = 0, pady = 10, padx = 10, sticky = 'nsew')
            rowi += 1
            phigros_root.tip_diff = avaliable_diff_list[0]
            # print(change_difflculty_choose.get())

            phigros_root.tip_attri = 'acc'
            attribution_choose = optionmenu_frame(phigros_root.content_frame, '选择更改的属性:','更改属性', ('名称', '俗称', '曲师', '章节', '定数', 'acc', '简评'), phigros_root.tip_attri)
            attribution_choose.grid(row = rowi, column = 0, pady = 10, padx = 10, sticky = 'nsew')
            rowi += 1
            phigros_root.change_current_info()
            
            global attribution_entry
            attribution_entry = muti_entry_frame(phigros_root.content_frame, '输入更改值:')
            attribution_entry.grid(row = rowi, column = 0, pady = 10, padx = 10, sticky = 'nsew')
            rowi += 1

            def song_click():
                song_name = phigros_root.valid_test('曲名', self.get())
                if(song_name == '无' or song_name not in phigros_root.song_list):
                    messagebox.showerror('无效曲名', f'{song_name}不存在')
                    return
                attribution_type = attribution_choose.get()
                difflculty = change_difflculty_choose.get()
                attribution_value = attribution_entry.get()
                diff_elm = song.find(difflculty)

                if(attribution_type ==  '名称'):
                    if(not attribution_value):
                        messagebox.showwarning("名称错误","不能输入空白名称")
                        return
                    last_name = song.find(attribution_type).text
                    messagebox.showinfo('更改',f'名称更改成功\n名称:{last_name}->{attribution_value}')
                    song.find(attribution_type).text = attribution_value
                    phigros_root.tip_song = f'{attribution_value}({song.find('曲师').text})'
                    
                elif(attribution_type ==  '俗称'):
                    last_attri = song.find(attribution_type).text
                    messagebox.showinfo('更改',f'俗称更改成功\n俗称:{last_attri}->{attribution_value}')
                    song.find(attribution_type).text = attribution_value
                
                elif(attribution_type ==  '定数'):
                    attribution_value = phigros_root.valid_test('定数', attribution_value)
                    if(attribution_value == '无'): return
                    messagebox.showinfo("更改",f"{song_name}({difflculty})定数:{diff_elm.find(attribution_type).text}->{attribution_value}")
                    # fi = open('change.txt', 'a+', encoding='utf-8')
                    # fi.write(f"{song_name}({difflculty}):{diff_elm[0].text}->{attribution_value}\n")#定数变化写入文件
                    diff_elm.find(attribution_type).text = attribution_value
                
                elif(attribution_type ==  '曲师'):
                    last_attri = song.find(attribution_type).text
                    messagebox.showinfo('更改',f'曲师更改成功\n曲师:{last_attri}->{attribution_value}')
                    song.find(attribution_type).text = attribution_value
                    phigros_root.tip_song = f'{song.find('名称').text}({attribution_value})'

                elif(attribution_type ==  '章节'):
                    last_attri = song.find(attribution_type).text
                    messagebox.showinfo('更改',f'章节更改成功\n章节:{last_attri}->{attribution_value}')
                    song.find(attribution_type).text = attribution_value

                elif(attribution_type ==  'acc'):
                    attribution_value = phigros_root.valid_test('acc', attribution_value)
                    if(attribution_value == '无'): return
                    messagebox.showinfo("更改",f"{song_name}({difflculty})acc:{diff_elm.find(attribution_type).text}->{attribution_value}")
                    diff_elm.find(attribution_type).text = attribution_value

                elif(attribution_type ==  '简评'):
                    diff_elm.find(attribution_type).text = attribution_value
                    messagebox.showinfo("更改",f"{song_name}({difflculty})简评更改成功")

                if(attribution_type in ['acc', '定数']):
                    if(float(diff_elm.find('acc').text) >= 70):
                        singal_rks = str(round(float(diff_elm.find('定数').text) * pow((float(diff_elm.find('acc').text) - 55) / 45, 2), 4))
                    else:
                        singal_rks = '0'
                    diff_elm.find('单曲rks').text = singal_rks

                tree.write(xmlpath, encoding = 'utf-8', xml_declaration = True)
                phigros_root.get_song_list()
                phigros_root.change_current_info()

            confirm_button = ctk.CTkButton(phigros_root.content_frame, text = '更改选中歌曲信息', command = song_click)
            confirm_button.grid(row = 6, column = 0, pady = 10, padx = 10)

        if(button_name == '删除歌曲'):
            rowi = 1
            tree = ET.parse(xmlpath)
            xmlroot = tree.getroot()
            diff = []
            delete_song = self.get()
            if(delete_song in phigros_root.nickname_list):
                delete_song = phigros_root.nickname_dic[delete_song]
            if(delete_song not in phigros_root.song_list):
                messagebox.showwarning('曲名错误', '无法找到该歌曲')
                return
            else:
                song_idx = phigros_root.song_list.index(delete_song)
            song = xmlroot[song_idx]
            for diffi in range(2, len(song)):
                diff.append(song[diffi].tag)
            difficulty_choose = optionmenu_frame(phigros_root.content_frame, '选择难度(留空则删掉整首歌)','删除难度', tuple(diff))
            difficulty_choose.grid(row = rowi, column = 0, pady = 10, padx = 10, sticky = 'nsew')
            rowi += 1

            def delete_song_click():
                delete_song = self.get()
                if(delete_song in phigros_root.nickname_list):
                    delete_song = phigros_root.nickname_dic[delete_song]
                if(delete_song not in phigros_root.song_list):
                    messagebox.showwarning('曲名错误', '无法找到该歌曲')
                    return
                else:
                    song_idx = phigros_root.song_list.index(delete_song)
                song = xmlroot[song_idx]

                if(difficulty_choose.get() == ''):#没有指定难度 直接删掉整首歌
                    messagebox.showinfo('删除歌曲',f"删除歌曲{delete_song}")
                    delete_index = phigros_root.song_list.index(delete_song)
                    print(f'删除{song.find('名称').text}')
                    xmlroot.remove(song)
                    for index in range(delete_index, len(xmlroot)):#更新索引
                        xmlroot[index].attrib['id'] = f'{index}'
                else:
                    diffi = song.find(difficulty_choose.get())#指定删除的难度
                    if(diffi ==  None):
                        messagebox.showwarning("难度不存在",f'{delete_song}没有{difficulty_choose.get()}难度')
                        return
                    else:
                        messagebox.showinfo('删除难度',f'删除难度{difficulty_choose.get()}')
                        song.remove(diffi)
                tree.write(xmlpath, encoding = 'utf-8', xml_declaration = True)
                phigros_root.get_song_list()
            
            confirm_button = ctk.CTkButton(phigros_root.content_frame, text = '删除选中歌曲的所选属性', command = delete_song_click)
            confirm_button.grid(row = 3, column = 0, pady = 10, padx = 10)

        if(button_name == '查找歌曲'):
            rowi = 2
            tree = ET.parse(xmlpath)
            xmlroot = tree.getroot()
            diff = []
            complex_song = self.get()
            if(complex_song in phigros_root.nickname_list):
                complex_song = phigros_root.nickname_dic[complex_song]
            bracket_idx = complex_song.rindex('(')
            name = complex_song[:bracket_idx:]
            composer = complex_song[bracket_idx + 1: -1:]
            song_info = phigros_root.get_song_data('name', (name, composer))
            # print(song_info)
            for diffi in phigros_root.diff_list:
                if(diffi in song_info.keys()):
                    diff.append(diffi)
            # print(diff)

            difficulty_choose = optionmenu_frame(find_info_page, '选择查找难度(留空查找所有难度)','查找难度', tuple(diff))
            difficulty_choose.configure(fg_color = 'transparent')
            difficulty_choose.grid(row = rowi, column = 0, pady = 10, padx = 10, sticky = 'nsew')
            rowi += 1
            
            def confirm():
                scroll_frame = ctk.CTkScrollableFrame(find_info_page, width=400, height=280)
                scroll_frame.configure(fg_color = 'transparent')
                scroll_frame.grid(row = 6, column = 0, pady = 10, padx = 10, sticky = 'nsew')

                complex_song = self.get()
                goal_diff = difficulty_choose.get()
                if(complex_song in phigros_root.nickname_list):
                    complex_song = phigros_root.nickname_dic[complex_song]
                bracket_idx = complex_song.rindex('(')
                name = complex_song[:bracket_idx:]
                composer = complex_song[bracket_idx + 1: -1:]
                song_info = phigros_root.get_song_data('name', (name, composer))
                nickname = song_info['俗称']
                chapter = song_info['章节']
                try:
                    phigros_root.name_show.destroy()
                    phigros_root.nickname_show.destroy()
                    phigros_root.difflculty_show.destroy()
                    phigros_root.attribution_show.destroy()
                    phigros_root.composer_show.destroy()
                    phigros_root.capter_show.destroy()
                except:
                    pass
                rowi = 0; text_fgcolor = "#F0FFFF"
                phigros_root.name_show = ctk.CTkLabel(scroll_frame, text = f'名称:{name}', font = (ctext_font, 20), fg_color=text_fgcolor)
                phigros_root.name_show.grid(row=rowi, column=0, padx=10, pady=5, sticky="w")
                rowi += 1

                phigros_root.nickname_show = ctk.CTkLabel(scroll_frame, text = f'俗称:{nickname}', font = (ctext_font, 20), fg_color=text_fgcolor)
                phigros_root.nickname_show.grid(row=rowi, column=0, padx=10, pady=5, sticky="w")
                rowi += 1

                phigros_root.composer_show = ctk.CTkLabel(scroll_frame, text = f'曲师:{composer}', font = (ctext_font, 20), fg_color=text_fgcolor)
                phigros_root.composer_show.grid(row=rowi, column=0, padx=10, pady=5, sticky="w")
                rowi += 1

                phigros_root.chapter_show = ctk.CTkLabel(scroll_frame, text = f'章节:{chapter}', font = (ctext_font, 20), fg_color=text_fgcolor)
                phigros_root.chapter_show.grid(row=rowi, column=0, padx=10, pady=5, sticky="w")
                rowi += 1

                if(goal_diff == ''):#不指定难度 全都要
                    for diff in phigros_root.diff_list:
                        if(diff in song_info.keys()):
                            phigros_root.difflculty_show = ctk.CTkLabel(scroll_frame, text = f'{diff}:', font = (ctext_font, 20), fg_color=text_fgcolor)
                            phigros_root.difflculty_show.grid(row=rowi, column=0, padx=10, pady=5, sticky="w")
                            rowi += 1
                            for keyi, vali in song_info[diff].items():
                                phigros_root.attribution_show = ctk.CTkLabel(scroll_frame, text = f'{keyi}:{vali}', font = (ctext_font, 20), fg_color=text_fgcolor)
                                phigros_root.attribution_show.grid(row=rowi, column=0, padx=10, pady=5, sticky="w")
                                rowi += 1
                else:
                    phigros_root.difflculty_show = ctk.CTkLabel(scroll_frame, text = f'{goal_diff}:', font = (ctext_font, 20), fg_color=text_fgcolor)
                    phigros_root.difflculty_show.grid(row=rowi, column=0, padx=10, pady=5, sticky="w")
                    rowi += 1

                    for keyi, vali in song_info[goal_diff].items():
                        phigros_root.attribution_show = ctk.CTkLabel(scroll_frame, text = f'{keyi}:{vali}', font = (ctext_font, 20), fg_color=text_fgcolor)
                        phigros_root.attribution_show.grid(row=rowi, column=0, padx=10, pady=5, sticky="w")
                        rowi += 1
                
            button = ctk.CTkButton(find_info_page, text = '查找选中歌曲', command = confirm)
            button.grid(row = rowi, column = 0, pady = 10, padx = 10)
            rowi += 1
               
class optionmenu_frame(ctk.CTkFrame):#下拉框
    def __init__(self, master, title, button_name, values, default_value = ''):
        super().__init__(master)
        self.grid_columnconfigure(0, weight=1)
        self.values = values
        self.default_value = default_value
        self.title = title
        self.radiobuttons = []
        self.variable = ctk.StringVar(value = default_value)

        self.title = ctk.CTkLabel(self, text=self.title, fg_color="#F0FFFF", corner_radius=6, font = (ctitle_font, 20))
        self.title.grid(row=0, column=0, padx=10, pady=5, sticky="w")

        self.option_menu = ctk.CTkOptionMenu(self, values = self.values, variable = self.variable, command=lambda x: self.click(button_name), font = (ctext_font, 20))
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
                if(seek_type == '名称'):
                    seek_list = phigros_root.song_list
                if(seek_type == '俗称'):
                    seek_list = phigros_root.nickname_list

                select_song = combobox_frame(find_info_page, f'选择要查找的歌曲{seek_type}', '查找歌曲', seek_list)
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
            
            if(seek_type in ['单曲rks', '定数', 'acc', '简评', '曲师', '章节']):
                destroy_all(seek_type_choose)
                global scroll_frame
                scroll_frame = ctk.CTkScrollableFrame(find_info_page, width=460, height=320)
                scroll_frame.configure(fg_color = 'transparent')
                scroll_frame.grid(row = 4, column = 0, pady = 10, padx = 10, sticky = 'nsew')
                if(seek_type in ['单曲rks', '定数', 'acc']):
                    min_entry = entry_frame(find_info_page, '输入最小值:', default_value = '0')
                    min_entry.configure(fg_color = 'transparent')
                    min_entry.grid(row = rowi, column = 0, pady = 10, padx = 10, sticky = 'nsew')
                    rowi +=  1

                    max_entry = entry_frame(find_info_page, '输入最大值:')
                    max_entry.configure(fg_color = 'transparent')
                    max_entry.grid(row = rowi, column = 0, pady = 10, padx = 10, sticky = 'nsew')
                    rowi +=  1
                elif(seek_type == '简评'):
                    text_entry = entry_frame(find_info_page, '输入简评:')
                    text_entry.configure(fg_color = 'transparent')
                    text_entry.set_size(260)
                    text_entry.grid(row = rowi, column = 0, pady = 10, padx = 10, sticky = 'nsew')
                    rowi +=  1
                else:
                    seek_list = phigros_root.composer_list
                    text_entry = combobox_frame(find_info_page, f'选择要查找的{seek_type}', '查找曲师章节', seek_list)
                    text_entry.configure(fg_color = 'transparent')
                    text_entry.set_size(230)
                    text_entry.grid(row = rowi, column = 0, pady = 10, padx = 10, sticky = 'nsew')
                    rowi += 1
                    def filter_values(event):
                        input_text = text_entry.get().strip().lower()
                        if not input_text:
                            text_entry.option_menu.configure(values=seek_list)
                            return
                        filtered = [item for item in seek_list if input_text in item.lower()]
                        text_entry.option_menu.configure(values=filtered)
                    text_entry.option_menu.bind("<KeyRelease>", filter_values)

                def confirm():
                    try:
                        for widget in scroll_frame.winfo_children():
                            widget.destroy()
                    except:
                        print("控件销毁失败")
                    last_page_button = ctk.CTkButton(find_info_page, text = '上一页', command=lambda x=0 : show_page(phigros_root.now_page - 1, find_rst_list, page_label), state="disabled")
                    last_page_button.place(relx=0.25, rely=1.0, anchor="se", relwidth=0.25) 

                    next_page_button = ctk.CTkButton(find_info_page, text = '下一页', command=lambda x=0 : show_page(phigros_root.now_page + 1, find_rst_list, page_label), state="normal")
                    next_page_button.place(relx=0.75, rely=1.0, anchor="sw", relwidth=0.25) 
                    tree = ET.parse(xmlpath)
                    xmlroot = tree.getroot()
                    if(seek_type in ['单曲rks', '定数', 'acc']):
                        minimum = float(min_entry.get())
                        maxmum = max_entry.get()
                    else:
                        text = text_entry.get().strip().lower()

                    if(seek_type == '定数'):
                        maxmum = float(maxmum) if maxmum != '' else 16.9
                    if(seek_type == 'acc'):
                        maxmum = float(maxmum) if maxmum != '' else 100
                    if(seek_type == '单曲rks'):
                        maxmum = float(maxmum) if maxmum != '' else 16.9

                    find_rst_list = []
                    for idx in range(len(xmlroot)):
                        song_info = phigros_root.get_song_data('index', idx)
                        for diffi in phigros_root.diff_list:
                            if(diffi in song_info):
                                acc = song_info[diffi]['acc']
                                if(seek_type in ['单曲rks', '定数', 'acc'] and minimum <= float(song_info[diffi][seek_type]) <= maxmum):
                                    find_rst_list.append(((song_info['俗称'] 
    if (song_info['俗称'] != '无' and song_info['俗称'] is not None) 
    else (f'{song_info['名称']}({song_info['曲师']})'))
      + '-' + diffi + f'({acc})', float(song_info[diffi][seek_type]) ))
                                    
                                elif(seek_type == '简评' and song_info[diffi][seek_type] is not None and song_info[diffi][seek_type] != '无' and text in song_info[diffi][seek_type].lower()):
                                    find_rst_list.append((
    (song_info['俗称'] if (song_info['俗称'] != '无' and song_info['俗称'] is not None) 
    else f'{song_info['名称']}({song_info['曲师']})') 
    + '-' + diffi, song_info[diffi][seek_type] ))
                        # print(f'输入{text}, 存储{song_info[seek_type]}')
                        if(seek_type in ['曲师', '章节'] and song_info[seek_type] is not None and song_info[seek_type] != '无' and text in song_info[seek_type].lower()):
                            find_rst_list.append((song_info[seek_type], song_info['名称']))

                    find_rst_list = sorted(find_rst_list, key=lambda x: x[1], reverse= True) if len(find_rst_list) else [('未找到','匹配结果')]
                    # print(find_rst_list)
                    rowi = 0
                    rowi += 1
                    total_page = (len(find_rst_list)//20 if len(find_rst_list)%20 == 0 else len(find_rst_list)//20 + 1)
                    def show_page(page, find_rst_list, page_label):
                        total_page = (len(find_rst_list)//20 if len(find_rst_list)%20 == 0 else len(find_rst_list)//20 + 1)
                        if(page == 0 or page > total_page): return
                        for widget in scroll_frame.winfo_children():
                            widget.destroy()
                        scroll_frame._parent_canvas.yview_moveto(0)
                        scroll_frame.update_idletasks()
                        rowi = 0; phigros_root.now_page = page
                        for key, value in find_rst_list[(page - 1) * 20:min(len(find_rst_list), page * 20):]:
                            label = ctk.CTkLabel(scroll_frame, text=f'{20 * (page-1)+rowi+1}.{key}:{value}', fg_color="#F0FFFF", corner_radius=6, width=300, anchor='w')
                            label.grid(row=rowi, column=0, padx=10, pady=5, sticky="w")
                            rowi += 1
                        page_label.configure(text = f'当前页数:{phigros_root.now_page}/{total_page}')
                        last_page_button.configure(state="normal" if phigros_root.now_page > 1 else "disabled")
                        next_page_button.configure(state="normal" if phigros_root.now_page < total_page else "disabled")
                        
                    page_label = ctk.CTkLabel(find_info_page, text=f'当前页数:{phigros_root.now_page}/{total_page}', fg_color="#F0FFFF", corner_radius=6)
                    page_label.place(relx=0.5, rely=1.0, anchor="s") 
                    show_page(1, find_rst_list, page_label)
                    
                button = ctk.CTkButton(find_info_page, text = '查找选中歌曲', command = confirm)
                button.grid(row = rowi, column = 0, pady = 10, padx = 10)
                rowi += 1

        if(button_name == '更改属性'):
            phigros_root.tip_attri = self.get()
            phigros_root.change_current_info()

        if(button_name == '更改难度'):
            phigros_root.tip_diff = self.get()
            phigros_root.change_current_info()

class entry_frame(ctk.CTkFrame):#单选框
    def __init__(self, master, title, placeholder_text = '', default_value = ''):
        super().__init__(master)
        self.grid_columnconfigure(0, weight=1)
        self.title = title

        self.title = ctk.CTkLabel(self, text=self.title, fg_color="#F0FFFF", font = (ctitle_font, 20),corner_radius=6)
        self.title.grid(row=0, column=0, padx=10, pady=5, sticky="w")

        self.ctkentry = ctk.CTkEntry(self, placeholder_text = placeholder_text, font = (ctext_font, 20))
        if default_value != '': self.ctkentry.insert(0, default_value)
        self.ctkentry.configure(width = 150, height = 32)
        self.ctkentry.grid(row = 0, column = 1, padx=10, pady=5, sticky="nsew")
        self.ctkentry.configure(width = 300)

    def get(self):
        return self.ctkentry.get()
    
    def set_size(self, width = 300, height = 32):
        self.ctkentry.configure(width = width, height = height)

class muti_entry_frame(ctk.CTkFrame):
    def __init__(self, master, title, placeholder_text=''):
        super().__init__(master)
        self.grid_columnconfigure(0, weight=1)

        # 标题标签（增加行距设置）
        self.title = title
        self.placeholder = placeholder_text
        self.title_label = ctk.CTkLabel(
            self, 
            text=self.title, fg_color="#F0FFFF",
            font=(ctitle_font, 20),
            corner_radius=6
        )
        self.title_label.grid(row=0, column=0, padx=10, pady=5, sticky="w")
        
        # 多行文本输入框（2025年新增wrap选项）
        self.ctktext = ctk.CTkTextbox(
            self,
            wrap="word",  # 自动换行模式：word/char/none
            font=(ctext_font, 20),
            height=70,   # 初始高度
            width=300,
            activate_scrollbars=True,  # 自动显示滚动条
            border_width=2,
            corner_radius=8
        )
        
        # 输入提示文字（支持多行）
        if placeholder_text:
            self.ctktext.insert("0.0", placeholder_text)
            self.ctktext.bind("<FocusIn>", self._clear_placeholder)
        
        # 布局配置（自动扩展）
        self.ctktext.bind("<FocusOut>", self.restore_placeholder)
        self.ctktext.grid(row=0, column=1, padx=10, pady=5, sticky="nsew")
        self.grid_rowconfigure(0, weight=1)
    
    def get(self):
        """获取文本（自动去除首尾空行）"""
        content = self.ctktext.get("0.0", "end-1c")
        return content.strip()
    
    def set_size(self, width=150, height=32):
        """动态设置尺寸（支持百分比）"""
        self.ctktext.configure(
            width=width if isinstance(width, int) else f"{width}%",
            height=height if isinstance(height, int) else f"{height}%"
        )
    
    def _clear_placeholder(self, event):
        """清除提示文字"""
        if(self.get() == self.placeholder):
            self.ctktext.delete("1.0", "end")
    
    def _auto_resize_height(self, event=None):
        """根据内容自动调整高度（最大500px）"""
        lines = int(self.ctktext.index('end-1c').split('.')[0])
        new_height = min(max(lines * 20 + 10, 32), 500)
        self.ctktext.configure(height=new_height)

    def restore_placeholder(self, event):
        if(not self.get()):
            self.ctktext.insert("0.0", self.placeholder)


    def set_size(self, x, y, dx, dy):
        self.width = x
        self.high = y
        self.geometry("{}x{}+{}+{}".format(x, y, dx, dy))

class expand_frame(ctk.CTkFrame):
    def __init__(self, master, title, is_expanded = False):
        super().__init__(master)
        
        # 控制展开状态的变量
        self.is_expanded = is_expanded
        self.title = title
        self.configure(border_width = 2, border_color = '#FFF5EE')
        
        # 创建标题按钮
        self.grid_columnconfigure(0, weight=1)  # 主窗口第0列可扩展
        self.header_button = ctk.CTkButton(
            self,
            text=f"▶ {self.title}",
            command=self.toggle,
            anchor="w",
            fg_color="transparent",
            text_color='black',
            font=(ctitle_font, 35),
            hover=False
        )
        self.header_button.grid(row=0, column=0, sticky="ew",padx=2, pady=2)
        
        # 创建内容区域
        self.content_frame = ctk.CTkFrame(self, fg_color='#E0FFFF', corner_radius = 0, width=self.winfo_width()-4)#
        
        # 初始隐藏内容
        self.content_frame.grid(row=1, column=0, sticky="ew",padx=2, pady=2)
        if(not is_expanded):
            self.content_frame.grid_remove()

    def toggle(self):
        self.is_expanded = not self.is_expanded
        if self.is_expanded:
            self.header_button.configure(text=f"▼ {self.title}")
            self.content_frame.grid()
        else:
            self.header_button.configure(text=f"▶ {self.title}")
            self.content_frame.grid_remove()

    def set_color(self, fg_color):
        self.configure(fg_color= fg_color)

class phigros_data(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.sidebar_expanded = True
        self.current_page = ""
        self.title("phigros数据库")
                    
        def refresh_root(event):
            self.destroy()
            subprocess.run(['python', py_path])
        self.bind('<F5>', refresh_root)

        def phigros_destroy(event):
            self.destroy()
        self.bind("<Escape>", phigros_destroy)
        
        self.create_sidebar()
        self.content_frame = ctk.CTkFrame(self)
        self.content_frame.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)
        self.pages = {
            "增": self.add_attribution,
            "删": self.delete_attribution,
            "改": self.change_attribution,
            '查': self.find_attribution,
            '更': self.grab_info,
            '测' : self.test
        }

        self.tip_song = ''; self.tip_attri = ''; self.tip_diff = ''
        self.diff_list = ['AT', 'IN', 'HD','EZ']
        self.addable_song = {}
        
        tree = ET.parse(xmlpath)
        xmlroot = tree.getroot()
        for idx in range(len(xmlroot)):
            avali_diff_list = []
            song_info = self.get_song_data('index', idx)
            if(song_info):
                for diffi in self.diff_list:
                    if(diffi not in song_info.keys()):
                        avali_diff_list.append(diffi)
            else:
                messagebox.showerror('', '无法获取歌曲信息')
                continue
            if(avali_diff_list):
                self.addable_song[f'{song_info['名称']}({song_info['曲师']})'] = avali_diff_list
                if(song_info['俗称'] != '无'):
                    self.addable_song[f'{song_info['俗称']}'] = avali_diff_list
        # print(f'可添加难度歌曲:{self.addable_song}')

    def set_size(self, x, y, dx, dy):
        self.geometry("{}x{}+{}+{}".format(x, y, dx, dy))


    def get_song_data(self, get_type, data):
        '''{
            '名称': 'Glaciaxion', 
            '曲师': 'SunsetRay', 
            '俗称': '无', 
            '章节': '无', 
            'IN': {'定数': '12.6', 'acc': '0', '单曲rks': '0', '简评': '无'}, 
            'HD': {'定数': '6.5', 'acc': '0', '单曲rks': '0', '简评': '无'}, 
            'EZ': {'定数': '1.0', 'acc': '0', '单曲rks': '0', '简评': '无'}
        }'''
        tree = ET.parse(xmlpath)
        xmlroot = tree.getroot()
        song_info = {}
        if(get_type == 'name'):
            name, composer = data
            # print(name, '\n',composer)
            for songi in xmlroot:
                name_elm = songi.find('名称')
                composer_elm = songi.find('曲师')
                if(name_elm.text == name and composer_elm.text == composer):
                    song_info['名称'] = name
                    song_info['曲师'] = composer
                    nickname = songi.find('俗称').text
                    song_info['俗称'] = nickname
                    chapter = songi.find('章节').text
                    song_info['章节'] = chapter
                    for diffi in self.diff_list:
                        avaliable_diff_elm = songi.find(diffi)
                        if(avaliable_diff_elm is not None):
                            diff_attri = {}
                            level = avaliable_diff_elm.find('定数').text
                            diff_attri['定数'] = level
                            acc = avaliable_diff_elm.find('acc').text
                            diff_attri['acc'] = acc
                            singal_rks = avaliable_diff_elm.find('单曲rks').text
                            diff_attri['单曲rks'] = singal_rks
                            comment = avaliable_diff_elm.find('简评').text
                            diff_attri['简评'] = comment
                            song_info[diffi] = diff_attri
        
        elif(get_type == 'index'):
            idx = data
            songi = xmlroot[idx]
            name = songi.find('名称').text
            song_info['名称'] = name
            composer = songi.find('曲师').text
            song_info['曲师'] = composer
            nickname = songi.find('俗称').text
            song_info['俗称'] = nickname
            chapter = songi.find('章节').text
            song_info['章节'] = chapter
            for diffi in self.diff_list:
                avaliable_diff_elm = songi.find(diffi)
                if(avaliable_diff_elm is not None):
                    diff_attri = {}
                    level = avaliable_diff_elm.find('定数').text
                    diff_attri['定数'] = level
                    acc = avaliable_diff_elm.find('acc').text
                    diff_attri['acc'] = acc
                    singal_rks = avaliable_diff_elm.find('单曲rks').text
                    diff_attri['单曲rks'] = singal_rks
                    comment = avaliable_diff_elm.find('简评').text
                    diff_attri['简评'] = comment
                    song_info[diffi] = diff_attri
        else:
            return 0
        return song_info

    def get_song_list(self):
        tree = ET.parse(xmlpath)
        xmlroot = tree.getroot()
        self.song_list = []
        self.nickname_list = []
        self.nickname_dic = {} #俗称:名称
        self.composer_list = []
        self.chapter_list = []
        for songi in xmlroot:
            composer = songi.find('曲师')
            if(composer.text and composer.text != '无'):
                self.composer_list.append(composer.text)
            name = songi.find('名称')
            self.song_list.append(f'{name.text}({composer.text})')
            nickname = songi.find('俗称')
            if(nickname.text and nickname.text != '无'):
                self.nickname_list.append(nickname.text)
                self.nickname_dic[nickname.text] = f'{name.text}({composer.text})'

            chapter = songi.find('章节')
            if(chapter.text and chapter.text != '无'):
                self.chapter_list.append(chapter.text)
        # print(self.nickname_dic)
        self.composer_list = list(set(self.composer_list))
        self.chapter_list = list(set(self.chapter_list))

    def valid_test(self, s_type, val):
        val = val.strip()
        if(not val):
            return '无'
        
        def valid_float(val, minn, maxx):
            try:
                rst = eval(val)
                if(minn<=rst<=maxx):
                    return str(rst)
                else:
                    messagebox.showerror('非法范围', f'哪有数值为{rst}的歌啊?')
                    return '无'
            except:
                valid_char = [str(i) for i in range(10)] + ['.']
                print(f'vlaid_char = {valid_char}')
                error_char = ''
                for i in val:
                    if(i not in valid_char):
                        error_char += i
                messagebox.showerror('非法输入', f'输入中包含 {set(error_char)} 等非法字符')
                return '无'
            
        if(s_type == '曲名'):
            if(val in phigros_root.nickname_list):
                val = phigros_root.nickname_dic[val]
                print(f'俗称转曲名:{val}')
        
        elif(s_type == '定数'):
            return valid_float(val, 0, 17.6)
        
        elif(s_type == 'acc'):
            return valid_float(val, 0, 100)

        return val


    def create_sidebar(self):
        """创建基本侧边栏框架"""
        self.sidebar_frame = ctk.CTkFrame(self)
        self.sidebar_frame.grid(row=0, column=0, sticky="nsew")
        
        # 折叠按钮
        rowi =0
        self.toggle_btn = ctk.CTkButton(
            self.sidebar_frame,
            text="☰",
            command=self.toggle_sidebar
        )
        self.toggle_btn.grid(row = rowi, column = 0, pady = 10, padx = 10, sticky = 'nsew')
        rowi += 1
        
        # 导航按钮
        self.nav_buttons = {}
        pages = {
            "增": " 新增项目",
            "删": " 删除项目",
            "改": " 修改项目",
            '查': ' 查询项目',
            '更': ' 更新数据',
            '测' : '测试模块'
        }

        icon_prefix = 'rhythmgame_database/icons/'
        icon_path = ['add song.png', 'change song.png', 'delete song.png','find song.png','grab.png','test.png']
        idx = 0
        for page_id, text in pages.items():
            icon_image = ctk.CTkImage(
                light_image=Image.open(icon_prefix + icon_path[idx]),
                size=(20, 20)  # 调整图标尺寸以适应按钮
            )
            idx += 1
            btn = ctk.CTkButton(
                self.sidebar_frame,
                text=text,
                command=lambda pid=page_id: self.switch_page(pid),
                anchor="w",
                image=icon_image,
                compound="left"  # 图片在文字左侧
            )
            btn.grid(row = rowi, column = 0, pady = 10, padx = 10, sticky = 'nsew')
            rowi += 1
            self.nav_buttons[page_id] = btn

    def toggle_sidebar(self):
        """切换侧边栏状态"""
        if self.sidebar_expanded:
            self.sidebar_frame.configure(width=20)
            self.toggle_btn.configure(width = 20)
            for i in self.nav_buttons.values():
                i.grid_remove()
        else:
            self.sidebar_frame.configure(width=250)
            self.toggle_btn.configure(width = 140)
            for i in self.nav_buttons.values():
                i.grid()
        
        self.sidebar_expanded = not self.sidebar_expanded
 
    def switch_page(self, page_id):
        for widget in self.content_frame.winfo_children():
            widget.destroy()
        self.pages[page_id]()


    def add_attribution(self):
        rowi = 0
        song_values = list(self.addable_song.keys())
        # print(song_values)
        self.get_song_list()
        self.song_name_choose = combobox_frame(self.content_frame, '歌曲名称/俗称', '添加歌曲', song_values)
        self.song_name_choose.grid(row = rowi, column = 0, pady = 10, padx = 10, sticky = 'nsew')
        rowi += 1
        def filter_values(event):#模糊搜索 过滤结果
            input_text = self.song_name_choose.get().strip().lower()
            if not input_text:
                self.song_name_choose.option_menu.configure(values=song_values)
                return
            filtered = [item for item in song_values if input_text in item.lower()]
            self.song_name_choose.option_menu.configure(values=filtered)
        self.song_name_choose.option_menu.bind("<KeyRelease>", filter_values)
        
        nickname_entry = entry_frame(self.content_frame, '歌曲俗称:', '儿童鞋垫')
        nickname_entry.grid(row = rowi, column = 0, pady = 10, padx = 10, sticky = 'nsew')
        rowi +=  1

        self.composer_choose = combobox_frame(self.content_frame, '曲师','增加曲师', self.composer_list)
        self.composer_choose.grid(row = rowi, column = 0, pady = 10, padx = 10, sticky = 'nsew')
        rowi +=  1

        self.chapter_choose = optionmenu_frame(self.content_frame, '章节名称','增加章节', self.chapter_list)
        self.chapter_choose.grid(row = rowi, column = 0, pady = 10, padx = 10, sticky = 'nsew')
        rowi +=  1

        self.difficulty_choose = optionmenu_frame(self.content_frame, '歌曲难度','增加难度', ('AT', 'IN', 'HD', 'EZ'), 'IN')
        self.difficulty_choose.grid(row = rowi, column = 0, pady = 10, padx = 10, sticky = 'nsew')
        rowi +=  1

        level_entry = entry_frame(self.content_frame, '歌曲定数:', '11.3')
        level_entry.grid(row = rowi, column = 0, pady = 10, padx = 10, sticky = 'nsew')
        rowi +=  1

        accuracy_entry = entry_frame(self.content_frame, 'acc:', '98.6')
        accuracy_entry.grid(row = rowi, column = 0, pady = 10, padx = 10, sticky = 'nsew')
        rowi +=  1

        song_text_entry = muti_entry_frame(self.content_frame, '简评一下:', '先生 买朵花吗~?')
        song_text_entry.grid(row = rowi, column = 0, pady = 10, padx = 10, sticky = 'nsew')
        rowi +=  1

        def get_data():
            tree = ET.parse(xmlpath)
            xmlroot = tree.getroot()
            
            song_name = self.valid_test('曲名', self.song_name_choose.get())
            level = self.valid_test('定数', level_entry.get())
            accuracy = self.valid_test('acc', accuracy_entry.get())
            if((song_name or level or accuracy) == '无'):
                return
            
            difficulty = self.difficulty_choose.get()
            nickname = self.valid_test('俗名', nickname_entry.get())#self.valid_test('', )
            song_text = self.valid_test('简评', song_text_entry.get())
            composer = self.valid_test('曲师', self.composer_choose.get())
            chapter = self.valid_test('章节', self.chapter_choose.get())

            if(song_name in phigros_root.song_list):#已有歌曲新差分
                print(f'{song_name}已经在列表中,差分')
                index = phigros_root.song_list.index(song_name)
                #print('index = ', index)
                add_song = xmlroot[index]
                if(add_song.find(difficulty) is not None):
                    print(f'{difficulty}难度已经存在')
                    return
            else:
                print(f'新建歌曲{song_name}')
                add_song = ET.SubElement(xmlroot, 'song')
                add_song.attrib['id'] = f'{len(xmlroot)}'
                ET.SubElement(add_song, '名称').text = song_name
                ET.SubElement(add_song, '俗称').text = nickname
                ET.SubElement(add_song, '曲师').text = composer
                ET.SubElement(add_song, '章节').text = chapter

            chafen = ET.SubElement(add_song, f'{difficulty}')
            ET.SubElement(chafen, '定数').text = level
            ET.SubElement(chafen, 'acc').text = accuracy
            if(float(accuracy) < 70):
                ET.SubElement(chafen, '单曲rks').text = '0'
            else:
                ET.SubElement(chafen, '单曲rks').text = str(round(float(level) * pow((float(accuracy) - 55) / 45, 2), 4))
            ET.SubElement(chafen, '简评').text = song_text
            # 写回文件，覆盖原文件
            messagebox.showinfo("",f'{song_name}成功加入数据库')
            tree.write(xmlpath, encoding = 'utf-8', xml_declaration = True)

        confirm_button = ctk.CTkButton(self.content_frame, text = '写入数据库', command = get_data)
        confirm_button.grid(row = rowi + 1, column = 0, pady = 10, padx = 10)
        rowi += 1


    def delete_attribution(self):
        rowi = 0
        phigros_root.get_song_list()
        select_song = combobox_frame(self.content_frame, '选择要删除的歌曲','删除歌曲', phigros_root.song_list)
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
        if(not (self.tip_attri and self.tip_diff)):
            return
        # print(self.tip_attri)
        song_idx = self.song_list.index(self.tip_song)
        songi = xmlroot[song_idx]
        if(self.tip_attri in ['定数', 'acc', '简评']):
            diff = songi.find(self.tip_diff)
            singal_rks = diff.find('单曲rks').text#.find('')
            if(self.tip_attri == '定数'):
                show_text = diff.find('定数').text
            if(self.tip_attri == 'acc'):
                show_text = diff.find('acc').text
            if(self.tip_attri == '简评'):
                attribution_entry.ctktext.delete("0.0", "end")
                show_text = diff.find('简评').text
                attribution_entry.ctktext.insert("0.0", show_text if show_text else '无')
            show_text += f'\n单曲rks:{singal_rks}'
        else:
            if(self.tip_attri == '名称'):
                show_text = songi.find('名称').text
            if(self.tip_attri == '俗称'):
                show_text = songi.find('俗称').text
            if(self.tip_attri == '曲师'):
                show_text = songi.find('曲师').text
            if(self.tip_attri == '章节'):
                show_text = songi.find('章节').text

        show_text_form = ''
        for i in range(0,len(show_text),40):
            show_text_form += show_text[i:i+40:] + '\n'
        self.change_attribution_window_tips.configure(text = f"{self.tip_attri}:{show_text_form}")
        phigros_root.update()

    def change_attribution(self):
        rowi = 0
        phigros_root.get_song_list()
        self.select_song_choose = combobox_frame(self.content_frame, '选择更改的歌曲:','更改歌曲', phigros_root.song_list)
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
        
        self.change_attribution_window_tips = ctk.CTkLabel(self.content_frame, text = '', fg_color="transparent")
        self.change_attribution_window_tips.grid(row = 5, column = 0, pady = 10, padx = 10)
        rowi += 1


    def show_rks_compose(self, master):
        tree = ET.parse(xmlpath)
        xmlroot = tree.getroot()
        rks = 0
        b27_list = []; phi3_list = []; index_counter = 0#递增
        
        for index in range(len(xmlroot)):
            song_info = self.get_song_data('index', index)
            for diffi in self.diff_list:
                if(diffi in song_info.keys()):
                    acc = float(song_info[diffi]['acc'])
                    singal_rks = float(song_info[diffi]['单曲rks'])
                    index_counter += 1
                    item = (singal_rks, index_counter, song_info, diffi)  # 注意负号
                    
                    if len(b27_list) < 27:
                        heapq.heappush(b27_list, item)
                    else:
                        heapq.heappushpop(b27_list, item)

                    if(int(acc) == 100):
                        # print(name)
                        if len(phi3_list) < 3:
                            heapq.heappush(phi3_list, item)
                        else:
                            heapq.heappushpop(phi3_list, item)

        # b27_list = sorted(b27_list, reverse = True)#根据rks排序
        b27_list = [(item[0], item[2], item[3]) for item in b27_list]
        b27_list.sort(reverse=True, key=lambda x: x[0])  # 降序排列
        
        phi3_list = [(item[0], item[2], item[3]) for item in phi3_list]
        phi3_list.sort(reverse=True, key=lambda x: x[0])  # 降序排列
        # print(f'phi3={phi3_list}')
        scroll_frame = ctk.CTkScrollableFrame(master, width=540, height=540)
        scroll_frame.configure(fg_color = 'transparent')
        # scroll_frame.grid(row = 0, column = 0, pady = 0, padx = 0, sticky = 'ew')
        scroll_frame.pack(fill="both", expand=True, padx=0, pady=0)
        rowi = 1

        b27_frame = expand_frame(scroll_frame, 'b27组成:', True)
        b27_frame.set_color('#FFFFF0')
        b27_frame.grid(row = rowi, column = 0, pady = 5, padx = 2, sticky = 'nsew')
        rowi += 1

        for i in range(min(len(b27_list), 27)):
            rks += b27_list[i][0]
            song_info = b27_list[i][1]#(singal_rks, song_info, diffi)
            diffi = b27_list[i][2]
            b27_song_label = expand_frame(b27_frame.content_frame, f'{i + 1}.{song_info['名称']}: {b27_list[i][0]}')
            b27_song_label.set_color('#FFFFF0')
            b27_song_label.grid(row = i, column = 0, pady = 5, padx = 10, sticky = 'w')

            show_name = song_info['俗称'] if song_info['俗称'] and song_info['俗称'] != '无' else song_info['名称']
            b27_hid_info = [f'名称:{show_name}', f'rks:{b27_list[i][0]}', f'acc:{song_info[diffi]['acc']}', f'定数:{song_info[diffi]['定数']}']
            for rowj in range(4):#展示属性个数
                b27_hid_info_label = ctk.CTkLabel(b27_song_label.content_frame, text = b27_hid_info[rowj], font = (ctext_font, 30), fg_color="#F0FFFF",width=400,anchor = 'w')
                b27_hid_info_label.grid(row = rowj, column = 0, pady = 5, padx = 10, sticky = 'w')

        phi3_frame = expand_frame(scroll_frame, 'phi3组成:', True)
        phi3_frame.set_color('#FFFFF0')
        phi3_frame.grid(row = rowi, column = 0, pady = 2, padx = 2, sticky = 'nsew')
        rowi += 1

        for i in range(min(len(phi3_list), 3)):
            rks += phi3_list[i][0]
            song_info = phi3_list[i][1]#(singal_rks, song_info, diffi)
            diffi = phi3_list[i][2]
            phi3_song_label = expand_frame(phi3_frame.content_frame, f'{i + 1}.{song_info['名称']}: {phi3_list[i][0]}')
            phi3_song_label.set_color('#FFFFF0')
            phi3_song_label.grid(row = i, column = 0, pady = 2, padx = 2, sticky = 'w')
            
            show_name = song_info['俗称'] if song_info['俗称'] and song_info['俗称'] != '无' else song_info['名称']
            phi3_hid_info = [f'名称:{show_name}', f'rks:{phi3_list[i][0]}', f'acc:{song_info[diffi]['acc']}', f'定数:{song_info[diffi]['定数']}']
            for rowj in range(4):#展示属性个数
                phi3_hid_info_label = ctk.CTkLabel(phi3_song_label.content_frame, text = phi3_hid_info[rowj], font = (ctext_font, 30), fg_color="#F0FFFF",width=400, anchor = 'w')
                phi3_hid_info_label.grid(row = rowj, column = 0, pady = 5, padx = 5, sticky = 'w')
            
        rks_label = ctk.CTkLabel(scroll_frame, text = f'rks={round(rks/30, 4)}', font = (ctext_font, 35), fg_color="#F0FFFF", width=400, anchor = 'center')
        rks_label.grid(row = 0, column = 0, pady = 5, padx = 5, sticky = 'w')

    def find_attribution(self):
        global find_info_page, seek_type_choose
        phigros_root.set_size(1000, 750, 720, 300)
        tab_window = ctk.CTkTabview(self.content_frame, width=500, height=550, corner_radius=10, fg_color="lightblue")
        tab_window.pack(fill="both", expand=True, padx=0, pady=0)

        find_rks_page = tab_window.add('rks组成')
        # tab_window.grid_columnconfigure(0, weight=1)
        find_info_page = tab_window.add('歌曲信息查找')

        rowi = 0
        phigros_root.get_song_list()
        self.show_rks_compose(find_rks_page)
        seek_type_choose = optionmenu_frame(find_info_page, '选择查找方式', '查找方式', ['名称','俗称', '曲师', '章节', '单曲rks', '定数', 'acc', '简评'])
        seek_type_choose.configure(fg_color = 'transparent')
        seek_type_choose.grid(row = rowi, column = 0, pady = 10, padx = 10, sticky = 'nsew')
        rowi += 1
        self.now_page = 1; self.find_rst_list = {}


    def grab_info(self):
        chrome_options = Options()
        chrome_options.add_argument("--blink-settings=imagesEnabled=false")
        
        driver = webdriver.Chrome(options=chrome_options)
        driver.get("https://mzh.moegirl.org.cn/Phigros/%E6%9B%B2%E7%9B%AE%E5%88%97%E8%A1%A8")#打开萌娘百科-phi-曲目列表
        wait = WebDriverWait(driver, 2)
        _ = wait.until(EC.presence_of_all_elements_located(
            (By.CSS_SELECTOR, "div.mw-parser-output")
        ))
        actions = ActionChains(driver)
        tree = ET.parse(xmlpath)
        xmlroot = tree.getroot()
        self.get_song_list()
        add_idx = len(xmlroot) + 1

        ask_replace = False
        replace_ask = messagebox.askokcancel("", "当爬取数据与记录数据不同时是否询问?\n默认直接覆盖")
        if replace_ask:
            ask_replace = True

        phi_allsong_div = driver.find_element(By.CSS_SELECTOR, "div.mw-parser-output")
        alltable = phi_allsong_div.find_elements(By.CSS_SELECTOR, 'table.wikitable')
        
        def get_level_num(s):
            s = s.split('(')
            return s[1].replace(')', '')
        current_title = None
        for tableidx in range(5):#0主线章节 4单曲 5AT
            alltr = alltable[tableidx].find_elements(By.TAG_NAME, 'tr')
            high = alltable[tableidx].size["height"]
            for tridx in range(len(alltr)):
                title_cell = alltr[tridx].find_elements(By.CSS_SELECTOR, "span.mw-headline")
                if title_cell:
                    # 更新当前标题
                    current_title = title_cell[0].text
                    # print(f'当前标题为:{current_title}')

                alltd = alltr[tridx].find_elements(By.TAG_NAME, 'td')
                lentd = len(alltd)#用td标签个数区分表头和要爬取的内容
                # print(f'lentd={lentd}')
                '''记录爬取数据'''
                # if(lentd == 1 and .find_elements(By.CSS_SELECTOR, "span.mw-headline"))
                if(tableidx < 4 and lentd == 7):#主线章节 支线章节 额外章节 外传章节的表格只有7个(标题 作者 BPM 难度 备注)
                    name = re.sub(r'\[\d+\]', '', alltd[0].text)
                    composer = re.sub(r'\[\d+\]', '', alltd[1].text)
                    diff_ez = get_level_num(alltd[3].text)
                    diff_hd = get_level_num(alltd[4].text)
                    diff_in = get_level_num(alltd[5].text)

                elif(tableidx == 4 and lentd == 8):#单曲 (更新日期 标题 作者 BPM 难度 备注) 多了一列更新时间
                    name_table = alltd[1]
                    # text = name_table.text.strip()
                    classes = name_table.get_attribute("class").split()#曲师 曲名可能有链接 分类讨论
                    if "a" in classes:
                        name = name_table.find_element(By.TAG_NAME, 'a').text
                    else:
                        name = name_table.text
                    name = re.sub(r'\[\d+\]', '', name)
                    
                    composer_table = alltd[2]
                    classes = composer_table.get_attribute("class").split()
                    if "a" in classes:
                        composer = composer_table.find_element(By.TAG_NAME, 'a').text
                    else:
                        composer = composer_table.text
                    composer = re.sub(r'\[\d+\]', '', composer)
                    diff_ez = get_level_num(alltd[4].text)
                    diff_hd = get_level_num(alltd[5].text)
                    diff_in = get_level_num(alltd[6].text)
                
                else:#不写else就会在标题行移动到下方写入模块
                    continue
                
                '''写入数据'''
                song_exist = False#处理重名歌曲
                song_idx = -1
                complex_name = f'{name}({composer})'
                if(complex_name in self.song_list):
                    find_idx = [find_idxi for find_idxi, x in enumerate(self.song_list) if x == complex_name]
                    for idxi in find_idx:
                        composer_elm = xmlroot[idxi].find('曲师')
                        if(composer_elm is not None and composer_elm.text == composer):
                            song_exist = True
                            song_idx = idxi
                if(song_exist):
                    # print(f"歌曲{name}已存在")
                    song = xmlroot[song_idx]
                    composer_elm = song.find('曲师')
                    composer_elm.text = composer#曲师直接覆盖
                    song.find('章节').text = current_title

                    if(song.find('EZ') == None):
                        add_diff = ET.SubElement(song, 'EZ')
                        ET.SubElement(add_diff, '定数').text = diff_ez
                        ET.SubElement(add_diff, 'acc').text = '0'
                        ET.SubElement(add_diff, '单曲rks').text = '0'
                        ET.SubElement(add_diff, '简评').text = '无'
                    else:
                        diff_attri = song.find('EZ')
                        level_elm = diff_attri.find('定数')
                        acc_elm = diff_attri.find('acc')
                        singal_rks_elm = diff_attri.find('单曲rks')
                        if(level_elm.text != diff_ez):
                            if(ask_replace):
                                replace_flag = False
                                replace_ez = messagebox.askokcancel("选择", f"歌曲:{name}(EZ)\n是否用抓取数据({diff_ez})\n替换原先数据({level_elm.text})")
                                if replace_ez:
                                    replace_flag = True
                            else:#不问 默认换成爬取的数据
                                replace_flag = True

                            if(replace_flag):
                                level_elm.text = diff_ez
                                if(float(acc_elm.text) >= 70):
                                    singal_rks = str(round(float(level_elm.text) * pow((float(acc_elm.text) - 55) / 45, 2), 4))
                                else:
                                    singal_rks = '0'
                                singal_rks_elm.text = singal_rks

                    if(song.find('HD') == None):
                        add_diff = ET.SubElement(song, 'HD')
                        ET.SubElement(add_diff, '定数').text = diff_hd
                        ET.SubElement(add_diff, 'acc').text = '0'
                        ET.SubElement(add_diff, '单曲rks').text = '0'
                        ET.SubElement(add_diff, '简评').text = '无'
                    else:
                        diff_attri = song.find('HD')
                        level_elm = diff_attri.find('定数')
                        acc_elm = diff_attri.find('acc')
                        singal_rks_elm = diff_attri.find('单曲rks')
                        if(diff_attri[0].text != diff_hd):
                            if(ask_replace):
                                replace_flag = False
                                replace_hd = messagebox.askokcancel("选择", f"歌曲:{name}(HD)\n是否用抓取数据({diff_hd})\n替换原先数据({level_elm.text})")
                                if replace_hd:
                                    replace_flag = True
                            else:
                                replace_flag = True

                            if(replace_flag):
                                level_elm.text = diff_hd
                                if(float(acc_elm.text) >= 70):
                                    singal_rks = str(round(float(level_elm.text) * pow((float(acc_elm.text) - 55) / 45, 2), 4))
                                else:
                                    singal_rks = '0'
                                singal_rks_elm.text = singal_rks

                    if(song.find('IN') == None):
                        add_diff = ET.SubElement(song, 'IN') 
                        ET.SubElement(add_diff, '定数').text = diff_in
                        ET.SubElement(add_diff, 'acc').text = '0'
                        ET.SubElement(add_diff, '单曲rks').text = '0'
                        ET.SubElement(add_diff, '简评').text = '无'
                    else:
                        diff_attri = song.find('IN')
                        level_elm = diff_attri.find('定数')
                        acc_elm = diff_attri.find('acc')
                        singal_rks_elm = diff_attri.find('单曲rks')
                        if(level_elm.text != diff_in):
                            if(ask_replace):
                                replace_flag = False
                                replace_in = messagebox.askokcancel("选择", f"歌曲:{name}(IN)\n是否用抓取数据({diff_in})\n替换原先数据({level_elm.text})")
                                if replace_in:
                                    replace_flag = True
                            else:
                                replace_flag = True

                            if(replace_flag):
                                level_elm.text = diff_in
                                if(float(acc_elm.text) >= 70):
                                    singal_rks = str(round(float(level_elm.text) * pow((float(acc_elm.text) - 55) / 45, 2), 4))
                                else:
                                    singal_rks = '0'
                                singal_rks_elm.text = singal_rks
                
                else:
                    # print(f"歌曲{name}不存在")
                    song = ET.SubElement(xmlroot, 'song')
                    song.attrib['id'] = f'{add_idx}'
                    add_idx += 1
                    ET.SubElement(song, '名称').text = name
                    ET.SubElement(song, '俗称').text = '无'
                    ET.SubElement(song, '曲师').text = composer
                    ET.SubElement(song, '章节').text = current_title

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
            
            actions.scroll_by_amount(0, high).perform() #移动1 对齐顶部 向下滑动 参数为 (x, y) 偏移量 
            time.sleep(0.5)
            tree.write(xmlpath, encoding = 'utf-8', xml_declaration = True)#更新完一段就写入 防止error
        self.get_song_list()

        '''爬AT难度的信息'''
        alltr = alltable[5].find_elements(By.TAG_NAME, 'tr')
        high = alltable[5].size["height"]
        pure_name_list = []
        tree = ET.parse(xmlpath)
        xmlroot = tree.getroot()#如果前面加入了歌曲 沿用上方的xmlroot就会找不到新歌
        for songi in xmlroot:
            name = songi.find('名称').text
            pure_name_list.append(name)
        for tridx in range(len(alltr)):
            alltd = alltr[tridx].find_elements(By.TAG_NAME, 'td')
            lentd = len(alltd)
            if(lentd == 6):#标题 所在章节 难度(EZ HD IN AT)
                name = alltd[0].text
                diff_at = alltd[5].text
                diff_at = get_level_num(diff_at)
            else:
                continue
            if(name in pure_name_list):#不去重名:如果有重名存在 表格必然会给到曲师以区分
                # print(f"歌曲{name}已存在")
                song_idx = pure_name_list.index(name)
                song = xmlroot[song_idx]
                if(song.find('AT') == None):
                    add_diff = ET.SubElement(song, 'AT')
                    ET.SubElement(add_diff, '定数').text = diff_at
                    ET.SubElement(add_diff, 'acc').text = '0'
                    ET.SubElement(add_diff, '单曲rks').text = '0'
                    ET.SubElement(add_diff, '简评').text = '无'
                else:
                    diff_attri = song.find('AT')
                    level_elm = diff_attri.find('定数')
                    acc_elm = diff_attri.find('acc')
                    singal_rks_elm = diff_attri.find('单曲rks')
                    if(level_elm.text != diff_at):
                        if(ask_replace):
                            replace_flag = False
                            replace_at = messagebox.askokcancel("选择", f"歌曲:{name}(AT)\n是否用抓取数据({diff_at})\n替换原先数据({level_elm.text})")
                            if replace_at:
                                replace_flag = True
                        else:
                            replace_flag = True
                        if(replace_flag):
                            level_elm.text = diff_at
                            if(float(acc_elm.text) >= 70):
                                singal_rks = str(round(float(level_elm.text) * pow((float(acc_elm.text) - 55) / 45, 2), 4))
                            else:
                                singal_rks = '0'
                            singal_rks_elm.text = singal_rks
            else:
                print(f"歌曲{complex_name}不存在?怎么可能...")
        # print(self.song_list)
                
        actions.scroll_by_amount(0, high).perform()  #移动1 对齐顶部 向下滑动 参数为 (x, y) 偏移量 
        time.sleep(0.5)
        tree.write(xmlpath, encoding = 'utf-8', xml_declaration = True)

        driver.quit()

    #测试模块
    def test(self):
        print('test st')
        print(self.get_song_data('name',('Glaciaxion', 'SunsetRay')))
        print(self.get_song_data('index', 0))
        print('test ed')

phigros_root = phigros_data()
phigros_root.set_size(800, 750, 860, 300)
phigros_root.mainloop()
'''
爬取的网页中出现17(17.3)有效数字是17.3 但是存在只打左括号的情况
用多行注释标识下面模块的作用
rks组成用heap维护 防MLE 虽然只有1000的数据量(((
正则表达式模式处理曲师及曲名后的[5]
'''