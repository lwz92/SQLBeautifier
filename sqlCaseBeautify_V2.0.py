# This is a code that beautify case of oracle sql file
'''
    VERSION 2.0 : Pull-in the graphical operation interface,
                  temporarily only support the text box to manually input the
                  source file contents, and add the conversion log.
'''

from tkinter import *
import time
from ScrolledText import ScrolledText

class Sql_Convert():
    def __init__(self, init_window, url_key):
        self.init_window = init_window
        self.url_key = url_key

    # 设置窗口
    def set_init_window(self):
        self.init_window.title("sql大小写美化工具_v2.0")  # 窗口名
        # 1068x681为窗口大小，+10 +10 定义窗口弹出时的默认展示位置
        self.init_window.geometry('1068x681+10+10')
        # 窗口背景色，其他背景色见：blog.csdn.net/chl0000/article/details/7657887
        self.init_window["bg"] = "SkyBlue"
        self.init_window.attributes("-alpha", 5)  # 虚化，值越小虚化程度越高
        # 标签
        self.src_data_label = Label(
            self.init_window,
            text="sql文件",
            width=15,
            bg="GhostWhite",
            fg = "DarkCyan")
        self.src_data_label.grid(row=1, column=1)
        self.dest_data_label = Label(
            self.init_window,
            text="转换结果",
            width=15,
            bg="GhostWhite",
            fg = "DarkCyan")
        self.dest_data_label.grid(row=1, column=3)
        # 文本框
        self.src_data_text = ScrolledText(
            self.init_window,
            width=75,
            height=45)  # 源文件输入框
        self.src_data_text.grid(row=2, column=1)
        self.dest_data_text = ScrolledText(
            self.init_window,
            width=75,
            height=45,
            state=DISABLED)  # 目标文件接收框
        self.dest_data_text.grid(row=2, column=3)
        # 按钮
        self.beautify_button = Button(
            self.init_window,
            text="美化",
            bg="lightblue",
            fg="DarkCyan",
            width=6,
            height=12,
            command=self.beautify_sql_case)  # 调用内部方法，加()为直接调用
        self.beautify_button.grid(row=2, column=2)

    # 获取keyword字典
    def get_keyword(self):
        '''
        function: put data of keyword file into dictionary
        return: dict
        '''
        try:
            file_key = open(self.url_key, encoding='UTF-8')
            dict_key = dict()
            for i in file_key:
                dict_key[i.strip()] = None
        except BaseException:
            self.write_log_into_text("ERROR:keyword文件不存在")
        return dict_key

    # 获取当前时间
    def get_current_time(self):
        current_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
        return current_time

    # 日志动态打印
    def write_log_into_text(self, log_info):
        self.dest_data_text.config(state=NORMAL)
        current_time = self.get_current_time()
        log_info = str(current_time) + " " + str(log_info) + "\n"  # 换行
        self.dest_data_text.delete(1.0, END)
        self.dest_data_text.insert(END, log_info)
        self.dest_data_text.config(state=DISABLED)

    # 功能函数
    def beautify_sql_case(self):
        self.dest_data_text.config(state=NORMAL)
        # 获取输入内容
        src = self.src_data_text.get(1.0, END).strip()  # 加.encode()输入内容为byte类型
        # 换行分割
        line1 = src.split('\n')
        #print(line1)

        if src:
            try:
                dict_key = self.get_keyword()
                for i in line1:
                    spt1 = i.split(' ')
                    #print(spt1)
                    for j in spt1:
                        spt2 = [
                            t.strip() for t in re.findall(
                                r"[\w']+|[().,!?;*-|/、，：]", j)]
                        #print(spt2)
                        for k in spt2:
                            if k.upper() in dict_key:
                                self.dest_data_text.insert(END, k.upper())
                            else:
                                if '\'' in k:
                                    self.dest_data_text.insert(END, k)
                                else:
                                    self.dest_data_text.insert(END, k.lower())
                        if j != spt1[-1]:  # 判断j是否为当前行最后一个，是就跳过
                            self.dest_data_text.insert(END, ' ')
                    self.dest_data_text.insert(END, '\n')
            except BaseException:
                self.write_log_into_text("ERROR:sql文件转换失败")
        else:
            self.write_log_into_text("ERROR:未检测到文件内容")
        self.dest_data_text.config(state=DISABLED)


def program_start():
    init_window = Tk()  # 实例化出一个父窗口
    url_key = r'D:\sqlFile\src\keyword.txt'
    LWZ_PORTAL = Sql_Convert(init_window, url_key)
    # 设置根窗口默认属性
    LWZ_PORTAL.set_init_window()

    init_window.mainloop()  # 父窗口进入事件循环，可以理解为保持窗口运行，否则界面不展示


program_start()