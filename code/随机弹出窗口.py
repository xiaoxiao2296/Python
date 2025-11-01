import tkinter as tk
import random
import threading
import time

def show_warm_tip():
    # 创建窗口
    window = tk.Tk()

    # 获取屏幕宽高
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()

    # 随机窗口位置（确保窗口完全显示在屏幕内）
    window_width = 300
    window_height = 60
    x = random.randrange(0, screen_width - window_width)
    y = random.randrange(0, screen_height - window_height)

    # 设置窗口标题和大小位置
    window.title("来自骁骁的温馨提示")
    window.geometry(f"{window_width}x{window_height}+{x}+{y}")

    # 提示文字列表（已添加新内容）
    tips = [
        '记得多喝水哦~荣荣酱', '保持微笑呀！荣荣酱', '每天都要元气满满嗷~~荣荣酱！',
        '荣荣酱！记得吃水果！', '荣荣酱要天天保持好心情', '好好爱自己！荣荣酱！',
        '我想你了！荣荣酱！','爱你爱你！荣荣酱！',
        '祝荣荣酱 梦想成真！', '期待下一次见面！荣荣酱', '荣荣酱！赛高',
        '祝荣荣酱 顺顺利利！', '荣荣酱~早点休息哟', '愿荣荣所有烦恼都消失',
        '别熬夜', '荣荣酱~今天过得开心嘛？', '天冷了，荣荣酱要多穿衣服'
    ]
    tip = random.choice(tips)

    # 多样的背景颜色
    bg_colors = [
        'lightpink', 'skyblue', 'lightgreen',
        'lavender',
        'lightyellow', 'plum', 'coral', 'bisque',
        'aquamarine',
        'mistyrose', 'honeydew',
        'lavenderblush', 'oldlace'
    ]
    bg = random.choice(bg_colors)

    # 创建标签并显示文字
    tk.Label(
        window,
        text=tip,
        bg=bg,
        font=('微软雅黑', 18),
        width=30,
        height=3
    ).pack()

    # 窗口置顶显示
    window.attributes('-topmost', True)

    window.mainloop()

# 创建线程列表
threads = []

# 窗口数量（根据屏幕大小可调整）
for i in range(300):
    t = threading.Thread(target=show_warm_tip)
    threads.append(t)
    time.sleep(0.005) # 快速弹出窗口
    threads[i].start()