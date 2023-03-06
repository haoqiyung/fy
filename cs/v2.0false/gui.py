import tkinter as tk
from tkinter import ttk
import threading
from translator import translate


API_ENDPOINTS = ['https://dep.haoda7.repl.co/translate', 'https://deep.haoda7.repl.co/translate', 'https://dp.haoda7.repl.co/translate']
class Translator(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master, bg='#F9F9F9', padx=20, pady=20)
        self.master = master
        self.master.title('翻译器')
        self.pack(fill='both', expand=True)
        self.create_widgets()
        self.load_history()  # 加载历史记录

    def create_widgets(self):
        # 头部栏
        self.header_frame = tk.Frame(self, bg='#F9F9F9')
        self.header_frame.pack(side='top', fill='x', padx=10, pady=10)

        self.title_label = tk.Label(self.header_frame, text="翻译器", font=('Arial', 18), bg='#F9F9F9')
        self.title_label.pack(side='left')

        self.api_frame = tk.Frame(self.header_frame, bg='#F9F9F9')
        self.api_frame.pack(side='right')

        self.api_index = 0
        self.api_label = tk.Label(self.api_frame, text=f"当前使用的 API: API{self.api_index + 1}", font=('Arial', 12), bg='#F9F9F9')
        self.api_label.pack(side='left')
        self.api_button = tk.Button(self.api_frame, text="切换 API", font=('Arial', 12), command=self.switch_api)
        self.api_button.pack(side='left', padx=10)

        # 左右布局
        self.main_frame = tk.Frame(self, bg='#F9F9F9')
        self.main_frame.pack(side='top', fill='both', expand=True)

        self.input_frame = tk.Frame(self.main_frame, bg='#F9F9F9')
        self.input_frame.pack(side='left', fill='both', expand=True, padx=10, pady=10)

        self.input_label = tk.Label(self.input_frame, text="要翻译的文本:", font=('Arial', 12), bg='#F9F9F9')
        self.input_label.pack(side='top', anchor='w')

        self.input_text = tk.Text(self.input_frame, height=10, width=50, font=('Arial', 12), bg='#FFFFFF', fg='#333333', wrap='word')
        self.input_text.pack(side='left', fill='both', expand=True)
        self.input_scrollbar = ttk.Scrollbar(self.input_frame, orient='vertical', command=self.input_text.yview)
        self.input_scrollbar.pack(side='right', fill='y')
        self.input_text.config(yscrollcommand=self.input_scrollbar.set)

        self.lang_frame = tk.Frame(self.main_frame, bg='#F9F9F9')
        self.lang_frame.pack(side='left', fill='y', padx=10)

        self.target_lang_label = tk.Label(self.lang_frame, text="目标语言:", font=('Arial', 12), bg='#F9F9F9')
        self.target_lang_label.pack(side='top', anchor='w', pady=10)
        self.target_lang_input = ttk.Combobox(self.lang_frame, values=['中文', '英文'], font=('Arial', 12))
        self.target_lang_input.current(0)
        self.target_lang_input.pack(side='top', padx=5)

        self.translate_button = tk.Button(self.lang_frame, text="翻译", font=('Arial', 12), command=self.translate)
        self.translate_button.pack(side='top', pady=10)

        # 添加一个头部栏
        self.output_header_frame = tk.Frame(self.main_frame, bg='#F9F9F9')
        self.output_header_frame.pack(side='top', fill='x', padx=10, pady=10)

        self.output_header_label = tk.Label(self.output_header_frame, text="翻译结果:", font=('Arial', 12), bg='#F9F9F9')
        self.output_header_label.pack(side='left')

        self.clear_button = tk.Button(self.output_header_frame, text="清空", font=('Arial', 12), command=self.clear_text)
        self.clear_button.pack(side='right', padx=10)

        self.output_frame = tk.Frame(self.main_frame, bg='#F9F9F9')
        self.output_frame.pack(side='left', fill='both', expand=True, padx=10, pady=10)

        self.output_text = tk.Text(self.output_frame, height=10, width=50, font=('Arial', 12), bg='#FFFFFF', fg='#333333', wrap='word')
        self.output_text.pack(side='left', fill='both', expand=True)
        self.output_scrollbar = ttk.Scrollbar(self.output_frame, orient='vertical', command=self.output_text.yview)
        self.output_scrollbar.pack(side='right', fill='y')
        self.output_text.config(yscrollcommand=self.output_scrollbar.set)

        self.history_button = tk.Button(self.header_frame, text="历史记录", font=('Arial', 12), command=self.show_history)
        self.history_button.pack(side='left', padx=10)
    def save_history(self, text, result):
        with open('history.txt', 'a') as f:
            f.write(f"{text}\t{result}\n")

    def load_history(self):
        try:
            with open('history.txt', 'r') as f:
                lines = f.readlines()
                self.history = [line.strip().split('\t') for line in lines]
        except:
            self.history = []

    def show_history(self):
        top = tk.Toplevel(self)
        top.title("历史记录")
        history_frame = tk.Frame(top)
        history_frame.pack(fill='both', expand=True)
        for i, (text, result) in enumerate(self.history):
            tk.Label(history_frame, text=f"{i+1}. {text} => {result}").pack(anchor='w')


    def switch_api(self):
        self.api_index = (self.api_index + 1) % len(API_ENDPOINTS)
        self.api_label.config(text=f"当前使用的 API: API{self.api_index + 1}")

    def translate_thread(self):
        text = self.input_text.get("1.0", tk.END)
        if text.strip() == '':
            return
        target_lang = self.target_lang_input.get()
        try:
            result = translate(text, target_lang)
            self.output_text.delete("1.0", tk.END)
            self.output_text.insert(tk.END, result)
            self.save_history(text, result)  # 保存历史记录
            self.input_text.delete("1.0", tk.END)
        except ValueError as e:
            self.output_text.delete("1.0", tk.END)
            self.output_text.insert(tk.END, f"翻译失败：{str(e)}")
        except Exception as e:
            self.output_text.delete("1.0", tk.END)
            self.output_text.insert(tk.END, f"翻译失败：{str(e)}")

    def translate(self):
        t = threading.Thread(target=self.translate_thread)
        t.start()

    def clear_text(self):
        self.output_text.delete('1.0', tk.END)