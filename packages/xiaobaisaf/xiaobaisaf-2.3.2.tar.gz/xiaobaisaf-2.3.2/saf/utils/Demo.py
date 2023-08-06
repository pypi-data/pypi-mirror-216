#! /usr/bin/env python
'''
@Author: xiaobaiTser
@Email : 807447312@qq.com
@Time  : 2023/6/16 0:04
@File  : Demo.py
'''
'''
Python3.9+tkinter+adb+matplotlib等库；实现一下功能：用户界面显示连接设备当前APP的实时耗电量，横坐标为Time(s),纵坐标为Powser(%)，横坐标只显示最近的30秒内的耗电量情况，图像使用折线图显示数据，图像下方有三个按钮（开始按钮、停止按钮、导出按钮分别对应三个功能）；请实现完整可用的代码！
'''

import tkinter as tk
from tkinter import ttk
import adbutils
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np

# 连接Android设备
adb = adbutils.AdbClient()
device = adb.device()

# 设置GUI
root = tk.Tk()
root.title('Android电量监控')

# 初始化变量
x = []  # 时间轴
y = []  # 电量数据
isRunning = False  # 线程运行控制


# 定义绘图函数
def plot_power():
    global x, y

    # 限制x轴范围为最近30s
    if len(x) > 30:
        x = x[-30:]
        y = y[-30:]

    # 绘图

    plt.xlabel('Time/s')
    plt.ylabel('Power/%')
    print(5)
    # plt.clf()  # 清除之前的图像
    plt.plot(x, y, '-r')

# 更新图形
def update_graph():
    global x, y, isRunning
    if isRunning:
        print(4)
        # 获取当前电量
        output = device.shell('dumpsys battery | grep level')
        power_level = int(output.split(':')[1].strip())
        print(f'powser: {power_level}')
        # 添加新的数据
        x.append(len(x))
        y.append(power_level)

        # 更新图像
        plot_power()
        draw.draw()

        print(6)
        # 每0.5s获取一次数据
        root.after(500, update_graph)


# 开始按钮
def start():
    print(1)
    global isRunning
    print(2)
    isRunning = True
    print(3)
    update_graph()


# 停止按钮
def stop():
    global isRunning
    isRunning = False


# 导出按钮
def export():
    plt.savefig('power.png')


# 绘制图像
fig = plt.Figure()
plot_power()
draw = FigureCanvasTkAgg(fig, master=root)
draw.get_tk_widget().grid(row=0, columnspan=3)

# 添加按钮
tk.Button(root, text="Start", command=start).grid(row=1, column=0)
tk.Button(root, text="Stop", command=stop).grid(row=1, column=1)
tk.Button(root, text="Export", command=export).grid(row=1, column=2)

# 事件循环
root.mainloop()