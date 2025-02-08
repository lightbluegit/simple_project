import requests
import time
import pandas as pd
import customtkinter
from tkinter import ttk
import subprocess
from bs4 import BeautifulSoup
py_path = 'design of class/grab book information/grab book information.py'
output_path = 'design of class/grab book information/text/output.csv'
price_sort_path = 'design of class/grab book information/text/图书价格.csv'
star_sort_path = 'design of class/grab book information/text/图书评分.csv'
ctext_font = '华文楷体'; ctitle_font = '仿宋'

class entry_frame(customtkinter.CTkFrame):#输入框
    def __init__(self, master, title, placeholder_text = '', default_value = ''):
        super().__init__(master)
        self.grid_columnconfigure(0, weight=1)
        self.title = title

        self.title = customtkinter.CTkLabel(self, text=self.title, fg_color="gray70", font = (ctitle_font, 24), corner_radius=6)
        self.title.grid(row=0, column=0, padx=10, pady=5, sticky="w")

        self.ctkentry = customtkinter.CTkEntry(self, placeholder_text = placeholder_text, font = (ctext_font, 20))
        if default_value != '': self.ctkentry.insert(0, default_value)
        self.ctkentry.grid(row = 0, column = 1, padx=10, pady=5, sticky="nsew")

    def get(self):
        return self.ctkentry.get()
    
    def set_size(self, width = 140, height = 28):
        self.ctkentry.configure(width = width, height = height)

class radiobutton_frame(customtkinter.CTkFrame):#单选框
    def __init__(self, master, title, values, default_value = ''):
        super().__init__(master)
        self.values = values
        self.title = title
        self.radiobuttons = []
        self.variable = customtkinter.StringVar(value=default_value)

        self.title = customtkinter.CTkLabel(self, text=self.title, fg_color="gray70", font = (ctitle_font, 24), corner_radius=6)
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

class optionmenu_frame(customtkinter.CTkFrame):#下拉框
    def __init__(self, master, title, button_name, values, default_value = ''):
        super().__init__(master)
        self.values = values
        self.default_value = default_value
        self.title = title
        self.radiobuttons = []
        self.variable = customtkinter.StringVar(value = default_value)

        self.title = customtkinter.CTkLabel(self, text=self.title, fg_color="gray70", font = (ctitle_font, 24), corner_radius=6)
        self.title.grid(row=0, column=0, padx=10, pady=5, sticky="nsew")

        self.option_menu = customtkinter.CTkOptionMenu(self, values = self.values, variable = self.variable, font = (ctext_font, 24), command=lambda x: self.click(button_name))
        self.option_menu.grid(row = 0, column = 1, padx=10, pady=5)
    
    def get(self):
        return self.variable.get()

    def set_size(self, width = 140, height = 28):
        self.option_menu.configure(width = width, height = height)
        
    def click(self, button_name):
        pass

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

class App(customtkinter.CTk):#主窗口
    def __init__(self):
        super().__init__()
        self.title("爬虫")
        def root_destroy(event):
            self.destroy()
        self.bind("<Escape>", root_destroy)
        self.bind('<F5>', self.refresh)
        
        relyi = 0.2; dy = 0.16
        grab_data_button = customtkinter.CTkButton(self, text = "抓取数据", command = self.grab_data, font = (ctitle_font, 24))
        grab_data_button.place(relx=0.5, rely=relyi, anchor="center")
        relyi += dy

        analyse_data_button = customtkinter.CTkButton(self, text = "分析数据", command = self.analyse_data, font = (ctitle_font, 24))
        analyse_data_button.place(relx=0.5, rely=relyi, anchor="center")
        relyi += dy

    def set_size(self, x, y, dx, dy):
        self.width = x
        self.high = y
        self.geometry("{}x{}+{}+{}".format(x, y, dx, dy))
    
    def refresh(self, event):
        try:
            self.destroy()
            subprocess.run(['python', py_path])#下一关
        except:
            pass

    def init_data_base(self):
        data_base = pd.read_csv(output_path)
        # 为每列指定填充值
        fill_values = {
            '书名': 'error', 
            '作者': 'error', 
            '出版时间': 'error',
            '出版商' : 'error',
            '简介' : 'error',
            '评分' : -1,
            '评分人数' : -1,
            '电子版价格' : -1,
            '装帧' : 'error',
            '价格' : -1
        }
        data_base = data_base.fillna(fill_values)
        data_base['书名'] = data_base['书名'].astype(str)
        data_base['作者'] = data_base['作者'].astype(str)
        data_base['出版时间'] = data_base['出版时间'].astype(str)
        data_base['出版商'] = data_base['出版商'].astype(str)
        data_base['简介'] = data_base['简介'].astype(str)
        data_base['评分'] = data_base['评分'].astype(float)
        data_base['评分人数'] = data_base['评分人数'].astype(int)
        data_base['电子版价格'] = data_base['电子版价格'].astype(float)
        data_base['装帧'] = data_base['装帧'].astype(str)
        data_base['价格'] = data_base['价格'].astype(float)
        data_base.to_csv(output_path, index=False)
        return data_base

    def grab_data(self):
        grab_data_window = ctktoplevel_frame(self, "抓取参数设置")
        grab_data_window.set_size(450, 250, 100, 100)#页数 20本1页 选取抓取的书数量entry 抓取的tag entry
        def refresh_grab_data_window(event):
            grab_data_window.destroy()
            self.grab_data()
        grab_data_window.bind("<F5>", refresh_grab_data_window)

        rowi = 0
        book_page_entry = entry_frame(grab_data_window, "抓取网页的页数", '输入正整数', 1)
        book_page_entry.grid(row = rowi, column = 0, pady=5, padx = 10, sticky="nsew")
        rowi += 1

        book_tag_entry = entry_frame(grab_data_window, "抓取的标签", default_value = '时间')
        book_tag_entry.grid(row = rowi, column = 0, pady=5, padx = 10, sticky="nsew")
        rowi += 1
        
        def confrim():
            header = pd.read_csv(output_path, nrows=0).columns.tolist()#清空数据库
            empty_df = pd.DataFrame(columns=header)
            empty_df.to_csv(output_path, index=False)

            process = 0; rowi = 4
            progress_label = customtkinter.CTkLabel(grab_data_window, text=f"抓取进度:{process}本")
            progress_label.grid(row = rowi, column = 0, pady=5, padx = 10)
            rowi += 1

            book_page = int(book_page_entry.get())#!检查类型
            book_tag = book_tag_entry.get()
            
            data_base = self.init_data_base()
            base_url = 'https://book.douban.com/tag/{}?start={}&type=T'
            headers = {
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
                }
            progress_line = ttk.Progressbar(grab_data_window, orient="horizontal", length=300, mode="determinate")#创建进度条
            progress_line.grid(row = rowi, column = 0, pady=5, padx = 10)
            rowi += 1

            for page in range(0, book_page):
                url = base_url.format(book_tag, page * 20)
                response = requests.get(url, headers=headers)

                if(response.status_code == 200):#检查请求是否成功
                    soup = BeautifulSoup(response.text, 'html.parser')#解析 HTML
                    books = soup.find_all('div', class_='info')#查找所有div标签中数值为info的图书条目
                    for idx in range(len(books)):#遍历每个图书条目
                        process += 1
                        progress_label.configure(text=f"抓取进度:{process}本")

                        progress_line['value'] = int((process / (book_page * 20)) * 100)
                        grab_data_window.update()
                        time.sleep(0.01)
                        try:
                            profile = books[idx].find('p').text.strip().replace('\n', '')
                        except:
                            profile = 'error'

                        try:
                            title = books[idx].find('h2').find('a').text.strip().replace(' ', '').replace('\n', '')
                        except:
                            title = 'error'
                        
                        try:
                            pub_info = books[idx].find('div', class_='pub').text.strip().replace('\n', '').split('/')#作者 出版信息
                            price = pub_info[-1]
                            price = price.replace('元', '') if '元' in price else price#统一格式
                            try:
                                price = float(price)
                            except:
                                print(f'{title} 无效价格')
                                price = -1#!价格-1为错误

                            pub_time = pub_info[-2]#年-月

                            publicaiton = pub_info[-3]#出版社

                            author = pub_info[:len(pub_info) - 3:]
                            author = ','.join(author)#多作者
                        except:
                            price = -1
                            pub_time = 'error'
                            publicaiton = 'error'
                            author = 'error'

                        try:
                            rating_tag = books[idx].find('span', class_='rating_nums').text.strip()#提取评分
                            rating = rating_tag if rating_tag else -1
                        except:
                            rating = -1

                        try:
                            rating_person_pre = books[idx].find('span', class_='pl').text.strip()
                            rating_person = ''
                            for i in rating_person_pre:
                                if('0' <= i <= '9'):
                                    rating_person+=i
                        except:
                            rating_person = -1

                        try:
                            verson_and_ItsPrice = books[idx].find('span', class_='buy-info').find('a').text.strip().split()
                            ver_price = verson_and_ItsPrice[1]#处理一下类型
                            ver_price = ver_price.replace('元', '') if '元' in ver_price else ver_price#统一格式
                            verson = verson_and_ItsPrice[0]
                        except:
                            print(f'{title} 无版本')
                            ver_price = -1
                            verson = 'error'
                        
                        data_base.at[page * 20 + idx, '书名'] = title
                        data_base.at[page * 20 + idx, '作者'] = author
                        data_base.at[page * 20 + idx, '出版时间'] = pub_time
                        data_base.at[page * 20 + idx, '出版商'] = publicaiton
                        data_base.at[page * 20 + idx, '简介'] = profile
                        data_base.at[page * 20 + idx, '评分'] = rating
                        data_base.at[page * 20 + idx, '评分人数'] = rating_person
                        data_base.at[page * 20 + idx, '电子版价格'] = price
                        data_base.at[page * 20 + idx, '装帧'] = verson
                        data_base.at[page * 20 + idx, '价格'] = ver_price
                    data_base.to_csv(output_path, index=False)

                else:
                    print(f"请求失败，状态码: {response.status_code}")
            time.sleep(0.1)
            print(f'爬取目标{book_page * 20}本,实际爬取{process}本')
            grab_data_window.destroy()

        confrim_button = customtkinter.CTkButton(grab_data_window, text="开始抓取", command=confrim)
        confrim_button.grid(row = rowi, column = 0, pady=5, padx = 10)
        rowi += 1
    
    def analyse_data(self):
        analyse_data_window = ctktoplevel_frame(self, "分析参数设置")
        analyse_data_window.set_size(500, 250, 100, 600)
        def refresh_analyse_data_window(event):
            analyse_data_window.destroy()
            self.analyse_data()
        analyse_data_window.bind("<F5>", refresh_analyse_data_window)

        rowi = 0
        sort_type_choose = radiobutton_frame(analyse_data_window, "升降序:", ['升序', '降序'], "降序")
        sort_type_choose.grid(row=rowi, column=0, padx=10, pady=5, sticky="nsew")
        rowi += 1

        sort_according_choose = radiobutton_frame(analyse_data_window, "排序依据选择:", ['价格', '电子版价格'], "价格")
        sort_according_choose.grid(row=rowi, column=0, padx=10, pady=5, sticky="nsew")
        rowi += 1

        def confrim():
            data_base = self.init_data_base()
            sort_type = sort_type_choose.get()
            sort_type_record = sort_type
            sort_type = True if sort_type == '升序' else False
            sort_according = sort_according_choose.get()

            header = pd.read_csv(price_sort_path, nrows=0).columns.tolist()
            empty_df = pd.DataFrame(columns=header)
            empty_df.to_csv(price_sort_path, index=False)
            
            header = pd.read_csv(star_sort_path, nrows=0).columns.tolist()
            empty_df = pd.DataFrame(columns=header)
            empty_df.to_csv(star_sort_path, index=False)

            price_bins = [0, 20, 40, 60, 80, 100, float('inf')]
            price_labels = ['0~20元', '20~40元', '40~60元', '60~80元', '80~100元', '100元以上']
            data_base['价格区间'] = pd.cut(data_base[sort_according], bins=price_bins, labels=price_labels, right=False)#?right 左闭右开
            filtered_df = data_base[data_base['价格区间'].isin(price_labels)]#?
            sorted_df = filtered_df.sort_values(by=['价格区间', sort_according], ascending = sort_type)#?
            sorted_df.to_csv(price_sort_path, index=False)
            print(f"{sort_according}{sort_type_record}排行已完成")
            
            star_bins = [0, 4, 5, 6, 7, 8, 9, float('inf')]
            star_labels = ['0~4星', '4~5星', '5~6星', '6~7星', '7~8星', '8~9星', '9星以上']
            data_base['评分区间'] = pd.cut(data_base['评分'], bins=star_bins, labels=star_labels, right=False)
            filtered_df = data_base[data_base['评分区间'].isin(star_labels)]
            sorted_df = filtered_df.sort_values(by=['评分区间', '评分'], ascending = sort_type)
            sorted_df.to_csv(star_sort_path, index=False)
            print(f"评分{sort_type_record}排行已完成")

        confrim_button = customtkinter.CTkButton(analyse_data_window, text="开始抓取", command=confrim)
        confrim_button.grid(row = rowi, column = 0, pady=5, padx = 10)
        rowi += 1

root = App()
root.set_size(300, 300, 900, 400)
root.mainloop()

'''html
<li class="subject-item">

    <div class="pic">
      <a class="nbg" href="https://book.douban.com/subject/37142217/" 
  onclick="moreurl(this,{i:'1',query:'',subject_id:'37142217',from:'book_subject_search'})">
        <img class="" src="https://img3.doubanio.com/view/subject/s/public/s35025322.jpg"
          width="90">
      </a>
    </div>

    <div class="info">
      <h2 class="">
  <a href="https://book.douban.com/subject/37142217/" title="黄仁勋：英伟达之芯" 
  onclick="moreurl(this,{i:'1',query:'',subject_id:'37142217',from:'book_subject_search'})">
    黄仁勋：英伟达之芯
  </a>
      </h2>

      <div class="pub">
  [美] 斯蒂芬·威特 / 周健工 / 中国财政经济出版社 / 2024-12-4 / 89.90元
      </div>

  <div class="star clearfix">
        <span class="allstar40"></span>
        <span class="rating_nums">7.5</span>
    <span class="pl">
        (405人评价)
    </span>
  </div>

    <p>本书不仅是一部科技企业家的传记，更是一部关于如何在全球科技舞台上取得成功的范本。跨越30年的科技发展历程，我们可以看到人工智能技术是如何发展的，人工智能将会... </p>

      <div class="ft">

  <div class="collect-info">
  </div>

          <div class="cart-actions">
    <span class="buy-info">
      <a href="https://book.douban.com/subject/37142217/buylinks">
        纸质版 59.80元
      </a>
    </span>
          </div>

  <div class="ebook-link">
    <a target="_blank" href="https://read.douban.com/ebook/488994817/?dcs=tag-buylink&amp;dcm=douban&amp;dct=37142217">去看电子版</a>
  </div>

      </div>

    </div>

  </li>
'''