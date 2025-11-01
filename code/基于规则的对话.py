# -*- coding: utf-8 -*-
"""
简单聊天机器人
功能：基于规则的对话系统，可以进行基本问答和对话
"""

import tkinter as tk
from tkinter import ttk, scrolledtext
import random
import re
import datetime

class SimpleChatBot:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("🤖 简单聊天机器人")
        self.root.geometry("600x500")
        self.root.resizable(False, False)
        
        # 设置聊天机器人的个人信息
        self.bot_name = "小智"
        self.user_name = "你"
        
        # 定义对话规则和响应
        self.conversation_rules = {
            # 问候类
            'greeting': {
                'patterns': [r'你好', r'您好', r'hello', r'hi', r'hey'],
                'responses': [
                    "你好！很高兴见到你！",
                    "嗨！今天过得怎么样？",
                    "你好呀！有什么我可以帮你的吗？"
                ]
            },
            
            # 询问名字
            'ask_name': {
                'patterns': [r'你叫什么', r'你的名字', r'你是谁'],
                'responses': [
                    f"我是{self.bot_name}，一个简单的聊天机器人！",
                    f"你可以叫我{self.bot_name}，很高兴为你服务！"
                ]
            },
            
            # 询问时间
            'ask_time': {
                'patterns': [r'几点了', r'现在什么时间', r'时间'],
                'responses': [
                    "现在是 {time}",
                    "当前时间是 {time}"
                ]
            },
            
            # 询问日期
            'ask_date': {
                'patterns': [r'今天几号', r'今天日期', r'日期'],
                'responses': [
                    "今天是 {date}",
                    "日期是 {date}"
                ]
            },
            # 天气类
            'weather': {
                'patterns': [r'天气', r'气温', r'温度'],
                'responses': [
                    "我无法获取实时天气信息，建议你查看天气预报应用哦！",
                    "天气真好，适合出去走走呢！"
                ]
            },
            
            # 情绪类
            'emotion': {
                'patterns': [r'开心', r'高兴', r'快乐', r'难过', r'伤心', r'郁闷'],
                'responses': [
                    "情绪是生活的调味剂，保持好心情很重要！",
                    "无论开心还是难过，都是生活的一部分呢。"
                ]
            },
            
            # 感谢类
            'thanks': {
                'patterns': [r'谢谢', r'感谢', r'thank'],
                'responses': [
                    "不客气！很高兴能帮到你！",
                    "不用谢，这是我应该做的！"
                ]
            },
            
            # 道别类
            'goodbye': {
                'patterns': [r'再见', r'拜拜', r'bye', r'下次见'],
                'responses': [
                    "再见！期待下次和你聊天！",
                    "拜拜！祝你有美好的一天！"
                ]
            }
        }
        
        # 默认响应
        self.default_responses = [
            "很有趣！能告诉我更多吗？",
            "我明白了，还有别的吗？",
            "这个话题挺有意思的呢！",
            "谢谢和我分享这些！",
            "听起来不错！",
            "嗯，我懂你的意思。"
        ]
        
        self.create_widgets()
        
    def create_widgets(self):
        # 创建主框架
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # 标题
        title_label = ttk.Label(
            main_frame, 
            text="🤖 简单聊天机器人", 
            font=("微软雅黑", 16, "bold")
        )
        title_label.pack(pady=(0, 10))
        
        # 聊天显示区域
        chat_frame = ttk.LabelFrame(main_frame, text="聊天记录", padding="10")
        chat_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        
        self.chat_display = scrolledtext.ScrolledText(
            chat_frame,
            wrap=tk.WORD,
            width=60,
            height=15,
            font=("微软雅黑", 10)
        )
        self.chat_display.pack(fill=tk.BOTH, expand=True)
        self.chat_display.config(state=tk.DISABLED)
        
        # 用户输入区域
        input_frame = ttk.Frame(main_frame)
        input_frame.pack(fill=tk.X)
        
        ttk.Label(input_frame, text="你的消息:").pack(anchor=tk.W)
        
        self.user_input = ttk.Entry(input_frame, font=("微软雅黑", 10))
        self.user_input.pack(fill=tk.X, pady=(5, 10))
        self.user_input.bind('<Return>', self.send_message)
        
        # 按钮区域
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.X)
        
        send_btn = ttk.Button(
            button_frame, 
            text="发送消息", 
            command=self.send_message
        )
        send_btn.pack(side=tk.LEFT, padx=(0, 5))
        
        clear_btn = ttk.Button(
            button_frame, 
            text="清空聊天", 
            command=self.clear_chat
        )
        clear_btn.pack(side=tk.LEFT, padx=(0, 5))
        
        quit_btn = ttk.Button(
            button_frame, 
            text="退出程序", 
            command=self.root.quit
        )
        quit_btn.pack(side=tk.LEFT)
        
        # 初始化欢迎消息
        self.add_message(f"{self.bot_name}: 你好！我是{self.bot_name}，一个简单的聊天机器人！")
        self.add_message(f"{self.bot_name}: 你可以和我聊天，问我时间，或者随便聊聊都可以哦！")
        
    def add_message(self, message):
        """添加消息到聊天显示区域"""
        self.chat_display.config(state=tk.NORMAL)
        self.chat_display.insert(tk.END, message + "\n")
        self.chat_display.config(state=tk.DISABLED)
        self.chat_display.see(tk.END)
        
    def send_message(self, event=None):
        """发送用户消息并获取机器人回复"""
        user_message = self.user_input.get().strip()
        if not user_message:
            return
            
        # 显示用户消息
        self.add_message(f"{self.user_name}: {user_message}")
        self.user_input.delete(0, tk.END)
        
        # 获取机器人回复
        bot_response = self.get_response(user_message)
        self.add_message(f"{self.bot_name}: {bot_response}")
        
    def get_response(self, message):
        """根据用户消息获取机器人回复"""
        message = message.lower()
        
        # 检查各种对话规则
        for rule_name, rule_data in self.conversation_rules.items():
            for pattern in rule_data['patterns']:
                if re.search(pattern, message):
                    response = random.choice(rule_data['responses'])
                    # 处理特殊标记
                    if '{time}' in response:
                        current_time = datetime.datetime.now().strftime("%H:%M:%S")
                        response = response.replace('{time}', current_time)
                    if '{date}' in response:
                        current_date = datetime.datetime.now().strftime("%Y年%m月%d日")
                        response = response.replace('{date}', current_date)
                    return response
        
        # 如果没有匹配的规则，返回默认响应
        return random.choice(self.default_responses)
        
    def clear_chat(self):
        """清空聊天记录"""
        self.chat_display.config(state=tk.NORMAL)
        self.chat_display.delete(1.0, tk.END)
        self.chat_display.config(state=tk.DISABLED)
        # 重新显示欢迎消息
        self.add_message(f"{self.bot_name}: 你好！我是{self.bot_name}，一个简单的聊天机器人！")
        self.add_message(f"{self.bot_name}: 你可以和我聊天，问我时间，或者随便聊聊都可以哦！")
        
    def run(self):
        """运行聊天机器人"""
        # 设置焦点到输入框
        self.user_input.focus()
        self.root.mainloop()

if __name__ == "__main__":
    print("正在启动简单聊天机器人...")
    print("提示：在图形界面中输入消息并按回车或点击发送按钮")
    
    bot = SimpleChatBot()
    bot.run()
    
    print("程序已退出，再见！")