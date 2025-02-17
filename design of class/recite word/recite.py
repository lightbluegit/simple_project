import sys
import pyautogui
import subprocess
import random
import customtkinter
import tkinter as tk
from tkinter import messagebox#design of class\recite word\recite.py
code_path = 'design of class/recite word/recite.py'
text_prefix = 'design of class/recite word/words data/'
words_path = text_prefix + 'words.txt'
wrongs_path = text_prefix + 'wrong.txt'
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

class entry_frame(customtkinter.CTkFrame):#单选框
    def __init__(self, master, title, placeholder_text = '', default_value = ''):
        super().__init__(master)
        self.grid_columnconfigure(0, weight=1)
        self.title = title

        self.title = customtkinter.CTkLabel(self, text=self.title, fg_color="gray70", font = (ctitle_font, 25),corner_radius=6)
        self.title.grid(row=0, column=0, padx=10, pady=5, sticky="w")

        self.ctkentry = customtkinter.CTkEntry(self, placeholder_text = placeholder_text, font = (ctext_font, 25))
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
        self.title("设置参数")
        def root_destroy(event):
            sys.exit()
                    
        def refresh_root(event):
            try:
                self.destroy()
                subprocess.run(['python', code_path])
            except:
                pass

        self.bind("<Escape>", root_destroy)
        self.bind('<F5>', refresh_root)
        pyautogui.moveTo(1438, 700)
        rowi = 0
        self.goal_word_num = 50
        self.num_entry = entry_frame(self, '输入背诵个数:')
        self.num_entry.set_size()
        self.num_entry.grid(row = rowi, column = 0, pady = 10, padx = 10, sticky = 'nsew')
        rowi += 1

        mode_var = tk.BooleanVar(value=False)
        self.mode_checkbox = customtkinter.CTkCheckBox(master=self,text="使用随机模式",variable=mode_var,font=(ctitle_font, 25))
        self.mode_checkbox.grid(row = rowi, column = 0, pady = 10, padx = 10, sticky = 'nsew')
        rowi += 1

        fi = open(words_path, 'r', encoding='utf-8')
        self.words_list = fi.readlines()
        for wordi in self.words_list:#预处理
            if(wordi and wordi[0] == '#'):
                del wordi

        def confirm():
            self.goal_word_num = self.num_entry.get()
            if(self.goal_word_num.isdigit()):
                self.goal_word_num = int(self.goal_word_num)
            else:
                messagebox.showwarning('','并非全数字')
                return
            self.goal_word_num = min(self.goal_word_num, len(self.words_list))
            rdm_mode = mode_var.get()
            # print(rdm_mode, self.goal_word_num)
            self.recite(rdm_mode)

        self.add_song = customtkinter.CTkButton(self, text = '开始背诵', command = confirm , font = (ctitle_font, 25))
        self.add_song.grid(row = rowi, column = 0, pady = 10, padx = 10, sticky = 'nsew')
        rowi += 1

    def set_size(self, x, y, dx, dy):
        self.width = x
        self.high = y
        self.geometry("{}x{}+{}+{}".format(x, y, dx, dy))

    def recite(self, rdm_mode):
        self.num_entry.destroy()
        self.mode_checkbox.destroy()
        self.add_song.destroy()
        self.set_size(700, 350, 1068, 600)

        recite_mode = '随机排列' if rdm_mode else '顺序排列'
        self.now_word_label = customtkinter.CTkLabel(self, text = f'{recite_mode}', font = (ctext_font, 50))
        self.now_word_label.place(relx=0.5, rely=0.5, anchor="center")
        self.now_word_idx = -1; self.show_mode = 'w'#w:单词 w+m:单词意思 sa:成功加入错题集 wa:加入错题集失败
        
        self.wrong_words_list = []
        self.wfo = open(wrongs_path, 'a+', encoding='utf-8')
        wfi = open(wrongs_path, 'r', encoding='utf-8')
        wrong_list = wfi.readlines()
        for wordi in wrong_list:#便于查找是否已存在
            word = wordi.split(':')
            self.wrong_words_list.append(word[0])

        if(recite_mode == '随机排列'):
            random.shuffle(self.words_list)
        
        self.bind("<Up>", self.add_wrong)
        self.bind("<Down>", self.show_mean)
        self.bind("<Left>", self.last_word)
        self.bind("<Right>", self.next_word)

    def add_wrong(self, event):
        if(self.show_mode == 'wa'):
            self.show_mode = 'w'
        if(self.now_word in self.wrong_words_list):
            self.show_mode = 'wa'
        else:
            self.show_mode = 'sa'
            self.wrong_words_list.append(self.now_word)
            self.wfo.write(f'{self.now_word}:{self.now_mean}')
        self.change_word()

    def show_mean(self, event):
        if(self.show_mode == 'w+m'):
            self.show_mode = 'w'
        elif(self.show_mode == 'w'):
            self.show_mode = 'w+m'
        self.change_word()
    
    def last_word(self, event):
        if(self.now_word_idx):#还有上一个
            self.now_word_idx -= 1
            self.show_mode = 'w'
            self.change_word()

    def next_word(self, event):
        if(self.now_word_idx < self.goal_word_num - 1):#还有下一个
            self.now_word_idx += 1
            self.show_mode = 'w'
            self.change_word()
        elif(self.now_word_idx == self.goal_word_num - 1):#结束
            messagebox.showinfo('','结束')
            self.destroy()

    def change_word(self):
        word = self.words_list[self.now_word_idx].split(':')
        self.now_word = word[0]; self.now_mean = word[1]
        if(self.show_mode == 'w'):
            show_text = self.now_word
        elif(self.show_mode == 'w+m'):
            show_text = f'{self.now_word}\n{self.now_mean}'
        elif(self.show_mode == 'sa'):
            show_text = f'{self.now_word}\n{self.now_mean}成功加入错题集'
        elif(self.show_mode == 'wa'):
            show_text = f'错误:{self.now_word}\n{self.now_mean}已在错题集'
        self.now_word_label.configure(text = f'{show_text}')

root = App()
root.set_size(550, 300, 1068, 600)
root.mainloop()