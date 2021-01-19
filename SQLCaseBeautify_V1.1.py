# This is a code that beautify case of oracle sql file
'''
    VERSION 1.1 : Pull-in the graphical operation interface,temporarily only support the text box to manually input the
                  source file and target folder path, and add the conversion log.
'''

import os
from tkinter import *
import time

LOG_LINE_NUM = 0  # 初始化日志行数


class Sql_Convert():
    def __init__(self, init_window, url_key):
        self.init_window = init_window
        self.url_key = url_key

    # 设置窗口
    def set_init_window(self):
        self.init_window.title("sql大小写美化工具_v1.1")  # 窗口名
        # 1068x681为窗口大小，+10 +10 定义窗口弹出时的默认展示位置
        self.init_window.geometry('1068x681+10+10')
        # 窗口背景色，其他背景色见：blog.csdn.net/chl0000/article/details/7657887
        self.init_window["bg"] = "SkyBlue"
        self.init_window.attributes("-alpha", 5)  # 虚化，值越小虚化程度越高
        # 标签
        self.src_data_label = Label(self.init_window, text="源文件路径", width=15, bg="GhostWhite", fg = "DarkCyan")
        self.src_data_label.grid(row=1, column=6)
        self.dest_data_label = Label(self.init_window, text="目标文件夹路径", width=15, bg="GhostWhite", fg = "DarkCyan")
        self.dest_data_label.grid(row=3, column=6)
        # 文本框
        self.src_data_text = Text(
            self.init_window,
            width=167,
            height=10)  # 源文件输入框
        self.src_data_text.grid(row=2, column=0, rowspan=1, columnspan=14)
        self.dest_data_text = Text(
            self.init_window,
            width=167,
            height=10)  # 目标文件输入框
        self.dest_data_text.grid(row=4, column=0, rowspan=1, columnspan=14)
        self.log_data_text = Text(self.init_window, width=66, height=9)  # 日志框
        self.log_data_text.grid(row=7, column=1, columnspan=11)
        # 按钮
        self.beautify_button = Button(
            self.init_window,
            text="美化",
            bg="GhostWhite",
            fg="DarkCyan",
            width=15,
            command=self.beautify_sql_case)  # 调用内部方法，加()为直接调用
        self.beautify_button.grid(row=6, column=6)

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
        global LOG_LINE_NUM
        current_time = self.get_current_time()
        log_info = str(current_time) + " " + str(log_info) + "\n"  # 换行
        if LOG_LINE_NUM <= 7:
            self.log_data_text.insert(END, log_info)
            LOG_LINE_NUM = LOG_LINE_NUM + 1
        else:
            self.log_data_text.delete(1.0, 2.0)
            self.log_data_text.insert(END, log_info)

    # 功能函数
    def beautify_sql_case(self):
        # 输入
        src = self.src_data_text.get(
            1.0, END).strip().replace(
            "\n", "")  # 加.encode()输入内容为byte类型
        # print("src =",src)
        desc = self.dest_data_text.get(1.0, END).strip().replace("\n", "")
        # print("desc =",desc)

        if src and desc:
            try:
                src_filename = os.path.split(src)[1]
                desc = desc + '\\' + src_filename
                # print("desc =",desc)
                try:
                    f1 = open(src, encoding='UTF-8')
                    # print("f1 =", f1)
                except BaseException:
                    self.write_log_into_text("ERROR:源文件不存在")
                try:
                    f2 = open(desc, 'w', encoding='UTF-8')
                    # print("f2 =", f2)
                except BaseException:
                    self.write_log_into_text("ERROR:目标文件夹不存在")
                dict_key = self.get_keyword()
                line1 = f1.readlines()
                f1.close()
                for i in line1:
                    spt1 = i.split(' ')
                    #print(spt1)
                    str1 = ''
                    for j in spt1:
                        spt2 = [
                            t.strip() for t in re.findall(
                                r"[\w']+|[().,!?;*-|/、，：]", j)]
                        #print(spt2)
                        for k in spt2:
                            if k.upper() in dict_key:
                                f2.write(k.upper())
                            else:
                                if '\'' in k:
                                    f2.write(k)
                                else:
                                    f2.write(k.lower())
                        if j != spt1[-1]:  # 判断j是否为当前行最后一个，是就跳过
                            f2.write(' ')
                    f2.write('\n')
                f2.close()
                self.write_log_into_text("INFO:sql_case_trans success")
            except BaseException:
                self.write_log_into_text("ERROR:文件不存在")
        else:
            self.write_log_into_text("ERROR:sql文件转换失败")


def program_start():
    init_window = Tk()  # 实例化出一个父窗口
    url_key = r'D:\sqlFile\src\keyword.txt'
    LWZ_PORTAL = Sql_Convert(init_window, url_key)
    # 设置根窗口默认属性
    LWZ_PORTAL.set_init_window()

    init_window.mainloop()  # 父窗口进入事件循环，可以理解为保持窗口运行，否则界面不展示


program_start()
