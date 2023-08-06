#! /usr/bin/env python
'''
@Author: xiaobaiTser
@email : 807447312@qq.com
@Time  : 2023/6/28 20:41
@File  : MonitorAndroidPackagePowser.py
'''
import os
import tkinter as tk
import subprocess
import threading
import time
from tkinter import filedialog, messagebox

import matplotlib.pyplot as plt
import csv

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class App:
    def __init__(self, master):
        CUR_PATH = os.path.dirname(os.path.abspath(__file__))
        self.master = master
        master.title('Android电量监控')
        master.geometry('700x500')
        master.iconbitmap(CUR_PATH + '\\..\\data\\favicon.ico')

        self.device_id = None
        # self.package_name = None
        self.power_data = []
        self.is_running = False

        # 创建开始、停止、导出按钮
        self.start_button = tk.Button(master, text='开始', command=self.start)
        self.start_button.pack(side='left', padx=10, pady=10)

        self.stop_button = tk.Button(master, text='停止', command=self.stop)
        self.stop_button.pack(side='left', padx=10, pady=10)

        self.export_button = tk.Button(master, text='导出', command=self.export)
        self.export_button.pack(side='left', padx=10, pady=10)

        # 创建tkinter标签，用于显示最新的电量数据
        self.label = tk.Label(master, text='当前电量：')
        self.label.pack(side='bottom', padx=10, pady=10)

        # 创建matplotlib图形区域
        self.fig = plt.figure(figsize=(6, 4))
        self.ax = self.fig.add_subplot(111)
        self.ax.set_xlabel('Time(s)')
        self.ax.set_ylabel('Power(%)')
        self.ax.set_xlim(0, 30)
        self.ax.set_ylim(0, 100)

        # 创建tkinter绘图区域
        self.canvas = FigureCanvasTkAgg(self.fig, master=master)
        self.canvas.get_tk_widget().pack(side='top', fill='both', expand=1)

    def start(self):
        self.start_time = time.time()
        if not self.is_running:
            self.is_running = True
            self.device_id = subprocess.check_output(['adb', 'devices']).decode('utf-8').split('\n')[1].split('\t')[0]
            # self.package_name = subprocess.check_output(['adb', 'shell', 'dumpsys', 'activity', 'activities']).decode('utf-8').split('\n')[0].split()[1]
            self.power_data = []

            # 在后台启动一个线程来获取电量数据
            self.power_thread = threading.Thread(target=self.get_power_data)
            self.power_thread.start()

    def stop(self):
        self.is_running = False

    def export(self):
        # 弹出文件对话框，获取用户选择的文件名和存储位置
        file_path = filedialog.asksaveasfilename(defaultextension='.csv', filetypes=(("CSV文件", "*.csv"),))
        if file_path:
            try:
                # 导出电量数据到CSV文件
                with open(file_path, 'w', newline='') as f:
                    writer = csv.writer(f)
                    writer.writerows([('时间（秒）', '电量（%）')])
                    writer.writerows(self.power_data)
                messagebox.showinfo("小白提醒：", "数据已经保存完成！")
            except PermissionError:
                messagebox.showerror("小白提示：", "文件无法访问！文件是否打开？请先关闭后重新尝试！")

    def get_power_data(self):
        while self.is_running:
            output = subprocess.check_output(['adb', '-s', self.device_id, 'shell', 'dumpsys', 'battery', '|', 'grep', 'level']).decode('utf-8').strip()
            power_level = int(output.split(':')[1])
            self.power_data.append((int(time.time()-self.start_time), power_level))
            self.update_power_data()
            time.sleep(1)

    def update_power_data(self):
        # 更新图表数据和电量标签
        if self.power_data:
            self.ax.clear()
            self.ax.set_xlabel('Time(s)')
            self.ax.set_ylabel('Power(%)')
            if self.power_data[-1][0] > 30:
                self.ax.set_xlim(max(0, self.power_data[-1][0] - 30), self.power_data[-1][0] + 1)
            else:
                self.ax.set_xlim(0, 30)
            self.ax.set_ylim(0, 100)

            if len(self.ax.lines) > 0:
                self.ax.lines.pop(0)
            if self.power_data[-1][0] > 30:
                self.ax.plot([t for t, _ in self.power_data[-30:]], [p for _, p in self.power_data[-30:]])
            else:
                self.ax.plot([t for t, _ in self.power_data], [p for _, p in self.power_data])
            self.canvas.draw()
            # 更新电量标签
            current_power = self.power_data[-1][1]
            self.label.config(text=f'当前电量：{current_power}%')

def power():
    root = tk.Tk()
    app = App(root)
    root.mainloop()

# if __name__ == '__main__':
#     power()