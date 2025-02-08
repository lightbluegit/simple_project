import sys
import xml.etree.ElementTree as ET
import customtkinter
import subprocess
code_path = 'design of class/rhythmgame_database/database.py'
xmlpath = 'design of class/rhythmgame_database/phigros_data.xml'
ctext_font = '华文楷体'; ctitle_font = '仿宋'

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
            phigros_root.tip_song = self.get()
            phigros_root.change_current_info()
            rowi = 1
            tree = ET.parse(xmlpath)
            xmlroot = tree.getroot()
            avaliable_diff_list = []
            for song in xmlroot:
                if(song[0].text == self.get()):
                    for avaliable_diff_listi in range(2, len(song)):
                        avaliable_diff_list.append(song[avaliable_diff_listi].tag)
                    break
            change_difflculty_choose = optionmenu_frame(phigros_root.change_attribution_window, '选择更改的难度:','更改难度', avaliable_diff_list)
            change_difflculty_choose.grid(row = rowi, column = 0, pady = 10, padx = 10, sticky = 'nsew')
            rowi += 1

            attribution_choose = optionmenu_frame(phigros_root.change_attribution_window, '选择更改的属性:','更改属性', ('名称', '俗称', '定数', 'acc', '简评'), 'acc')
            attribution_choose.grid(row = rowi, column = 0, pady = 10, padx = 10, sticky = 'nsew')
            rowi += 1
            
            attribution_entry = entry_frame(phigros_root.change_attribution_window, '输入更改值:')
            attribution_entry.grid(row = rowi, column = 0, pady = 10, padx = 10, sticky = 'nsew')
            attribution_entry.set_size(width=300)
            rowi += 1

            def song_click():
                change_song = phigros_root.select_song_choose.get()
                attribution_type = attribution_choose.get()
                difflculty = change_difflculty_choose.get()
                attribution_value = attribution_entry.get()
                for song in xmlroot:
                    if(song[0].text ==  change_song):
                        if(attribution_type ==  '名称'):
                            if(not attribution_type):
                                print("无效名称")
                                return
                            song[0].text = attribution_value
                            print("名称更改成功")
                        if(attribution_type ==  '俗称'):
                            if(not attribution_value):
                                print("无效俗称")
                                return
                            song[1].text = attribution_value
                            print("俗称更改成功")
                        
                        difficulty_find = song.find(difflculty)
                        if(difficulty_find ==  None):
                            print(f'{change_song}没有{difflculty}难度')
                            return
                        if(attribution_type ==  '定数'):
                            difficulty_find[0].text = attribution_value
                            print(f"{change_song}定数更改成功")
                        if(attribution_type ==  'acc'):
                            difficulty_find[1].text = attribution_value
                            print(f"{change_song}acc更改成功")
                        if(attribution_type ==  'acc' or attribution_type ==  '定数'):
                            singal_rks = str(round(float(difficulty_find[0].text) * pow((float(difficulty_find[1].text) - 55) / 45, 2), 4))
                            difficulty_find[2].text = singal_rks
                        if(attribution_type ==  '简评'):
                            difficulty_find[3].text = attribution_value
                            print(f"{change_song}简评更改成功")
                        tree.write(xmlpath, encoding = 'utf-8', xml_declaration = True)
                        return
                print('更改失败')

            confirm_button = customtkinter.CTkButton(phigros_root.change_attribution_window, text = '更改选中歌曲信息', command = song_click)
            confirm_button.grid(row = 6, column = 0, pady = 10, padx = 10)

        if(button_name == '删除歌曲'):
            rowi = 1
            tree = ET.parse(xmlpath)
            xmlroot = tree.getroot()
            diffy = []
            for song in xmlroot:
                if(song[0].text == self.get()):
                    for diffyi in range(2, len(song)):
                        diffy.append(song[diffyi].tag)
                    break
            difficulty_choose = optionmenu_frame(phigros_root.delete_attribution_window, '选择难度(留空则删掉整首歌)','删除难度', tuple(diffy))
            difficulty_choose.grid(row = rowi, column = 0, pady = 10, padx = 10, sticky = 'nsew')
            rowi += 1

            attributions = optionmenu_frame(phigros_root.delete_attribution_window, '选择属性','删除属性', ['简评'])
            attributions.grid(row = rowi, column = 0, pady = 10, padx = 10, sticky = 'nsew')
            rowi += 1
            def delete_song_click():
                delete_song = self.get()
                for song in xmlroot:
                    if(song[0].text == delete_song):
                        if(difficulty_choose.get() == ''):#没有指定难度 直接删掉整首歌
                            print(f"删除歌曲{delete_song}")
                            delete_index = phigros_root.song_list.index(delete_song) - 1
                            xmlroot.remove(song)
                            for index in range(delete_index, len(xmlroot)):
                                xmlroot[index].tag = f'song{index + 1}' 
                            tree.write(xmlpath, encoding = 'utf-8', xml_declaration = True)
                            #delete_attribution()
                            return
                        else:
                            diffi = song.find(difficulty_choose.get())#指定删除的难度
                            if(diffi ==  None):
                                print(f'当前歌曲无{difficulty_choose.get()}难度')
                                return
                        if(attributions.get() == ''):#未指定属性 删除整个难度
                            print(f'删除难度{difficulty_choose.get()}')
                            song.remove(diffi)
                        else:
                            print(f'删除属性{attributions.get()}')
                            diffi.remove(diffi.find(attributions.get()))#删除属性
                        print('删除成功')
                        tree.write(xmlpath, encoding = 'utf-8', xml_declaration = True)
                        return
                print('删除失败')
                
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
                            print("未指定难度")
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

                        print('查找成功')
                        return
                print('查找失败')
                
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
                select_song.grid(row = rowi, column = 0, pady = 10, padx = 10, sticky = 'w')
                rowi += 1
                def filter_values(event):
                    input_text = select_song.get().strip().lower()
                    if not input_text:
                        select_song.option_menu.configure(values=seek_list)
                        return
                    filtered = [item for item in seek_list if input_text in item.lower()]
                    select_song.option_menu.configure(values=filtered)
                select_song.option_menu.bind("<KeyRelease>", filter_values)
            
            if(seek_type in ['单曲rks', '定数', 'acc']):
                destroy_all(seek_type_choose)
                scroll_frame = customtkinter.CTkScrollableFrame(find_info_page, width=400, height=280)
                scroll_frame.configure(fg_color = 'transparent')
                scroll_frame.grid(row = 6, column = 0, pady = 10, padx = 10, sticky = 'nsew')

                min_entry = entry_frame(find_info_page, '输入最小值:', default_value = '0')
                min_entry.configure(fg_color = 'transparent')
                min_entry.grid(row = rowi, column = 0, pady = 10, padx = 10, sticky = 'nsew')
                rowi +=  1

                max_entry = entry_frame(find_info_page, '输入最大值:')
                max_entry.configure(fg_color = 'transparent')
                max_entry.grid(row = rowi, column = 0, pady = 10, padx = 10, sticky = 'nsew')
                rowi +=  1
                def confirm():
                    minimum = float(min_entry.get())
                    maxmum = max_entry.get()
                    tree = ET.parse(xmlpath)
                    xmlroot = tree.getroot()
                    rst_list = {}
                    if(seek_type == '定数'):
                        index = 0
                        maxmum = float(maxmum) if maxmum != '' else 16.9
                    if(seek_type == 'acc'):
                        index = 1
                        maxmum = float(maxmum) if maxmum != '' else 100
                    if(seek_type == '单曲rks'):
                        index = 2
                        maxmum = float(maxmum) if maxmum != '' else 16.9
                    for song in xmlroot:
                        for difficulty in range(2, len(song)):
                            if(minimum <= float(song[difficulty][index].text) <= maxmum):
                                try:
                                    rst_list[(song[1].text if (song[1].text != '无' and song[1].text != None)  else song[0].text) + '-'+ song[difficulty].tag] = float(song[difficulty][index].text)
                                except:
                                    print(f"error{song[1].text} {song[0].text}")
                    rst_list = sorted(rst_list.items(), key=lambda x: x[1], reverse= True)
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
        self.ctkentry.grid(row = 0, column = 1, padx=10, pady=5, sticky="nsew")

    def get(self):
        return self.ctkentry.get()
    
    def set_size(self, width = 140, height = 28):
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
                subprocess.run(['python', code_path])
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

        self.tip_song = ''; self.tip_attri = 'acc'; self.tip_diffy = ''

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

    def set_size(self, x, y, dx, dy):
        self.width = x
        self.high = y
        self.geometry("{}x{}+{}+{}".format(x, y, dx, dy))

    def get_song_list(self):
        tree = ET.parse(xmlpath)
        xmlroot = tree.getroot()
        self.song_list = []
        self.nickname_list = []
        for i in xmlroot:
            self.song_list.append(i[0].text)
            if(i[1].text and i[1].text != '无'):
                self.nickname_list.append(i[1].text)

    def show_rks_compose(self, master):
        tree = ET.parse(xmlpath)
        xmlroot = tree.getroot()
        rks = 0; phi1_level = 0
        rks_list = []
        
        for song in xmlroot:
            for diffyi in range(2, len(song)):
                try:
                    rks_list.append((float(song[diffyi][2].text), (song[1].text if song[1].text != '无'  else song[0].text) + '(' + song[diffyi].tag + ')'))#(rks,曲名(难度))
                    if(int(song[diffyi][1].text) ==  100 and float(song[diffyi][0].text) > phi1_level):#acc = 100
                        phi1 = song[0].text + '(' + song[diffyi].tag + '):' + song[diffyi][0].text
                        rks += float(song[diffyi][0].text)
                except:
                    pass
        dic = sorted(rks_list, key = lambda x : x[0], reverse = True)#根据rks排序

        scroll_frame = customtkinter.CTkScrollableFrame(master, width=500, height=550)
        scroll_frame.configure(fg_color = 'transparent')
        scroll_frame.grid(row = 0, column = 0, pady = 10, padx = 10, sticky = 'w')

        for i in range(19):
            rks += dic[i][0]
            b19_song_label = customtkinter.CTkLabel(scroll_frame, text = '{}.{}:{}'.format(i + 1, dic[i][1], dic[i][0]), font = (ctext_font, 24))
            b19_song_label.grid(row = i + 1, column = 0, pady = 10, padx = 10, sticky = 'w')

        phi1_song_label = customtkinter.CTkLabel(scroll_frame, text = 'phi1.{}'.format(phi1), font = (ctext_font, 23))
        phi1_song_label.grid(row = 20, column = 0, pady = 10, padx = 10, sticky = 'w')
        rks_label = customtkinter.CTkLabel(scroll_frame, text = f'rks={rks/20}', font = (ctext_font, 24))
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

        difficulty_choose = optionmenu_frame(self.add_attribution_window, '歌曲难度','增加难度', ('AT', 'IN', 'HD', 'EZ'), 'IN')
        difficulty_choose.grid(row = rowi, column = 0, pady = 10, padx = 10, sticky = 'nsew')
        rowi +=  1

        phigros_root.get_song_list()
        song_name_entry = entry_frame(self.add_attribution_window, '选择要添加的歌曲名称', 'mopemope')
        song_name_entry.grid(row = rowi, column = 0, pady = 10, padx = 10, sticky = 'nsew')
        rowi += 1

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
            song_name = song_name_entry.get()
            difficulty = difficulty_choose.get()
            nickname = nickname_entry.get()
            nickname = nickname if nickname else '无'
            level = level_entry.get()
            accuracy = accuracy_entry.get()
            song_text = song_text_entry.get()

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
            ET.SubElement(chafen, '单曲rks').text = str(round(float(level) * pow((float(accuracy) - 55) / 45, 2), 4))
            ET.SubElement(chafen, '简评').text = song_text
            # 写回文件，覆盖原文件
            print(f'{song_name}成功加入数据库')
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
        self.delete_attribution_window.set_size(450,250,200,1074)
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
            filtered = [item for item in phigros_root.song_list if input_text in item.lower()]
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
        for songi in xmlroot:
            if(songi[0].text == self.tip_song):
                if(self.tip_attri in ['定数', 'acc', '简评']):
                    diff = songi.find(self.tip_diffy)
                    if(self.tip_attri == '定数'):
                        show_text = diff[0].text
                    if(self.tip_attri == 'acc'):
                        show_text = diff[1].text
                    if(self.tip_attri == '简评'):
                        show_text = diff[3].text
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
        self.select_song_choose.grid(row = rowi, column = 0, pady = 10, padx = 10, sticky = 'nsew')
        rowi += 1
        def filter_values(event = None):
            input_text = self.select_song_choose.get().strip().lower()
            if not input_text:
                self.select_song_choose.option_menu.configure(values=phigros_root.song_list)
                return
            filtered = [item for item in phigros_root.song_list if input_text in item.lower()]
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
        seek_type_choose = optionmenu_frame(find_info_page, '选择查找方式', '查找方式', ['名称','俗称', '单曲rks', '定数', 'acc'])
        seek_type_choose.configure(fg_color = 'transparent')
        seek_type_choose.grid(row = rowi, column = 0, pady = 10, padx = 10, sticky = 'nsew')
        rowi += 1

root = App()
root.set_size(250, 250, 1068, 885)
root.mainloop()