import requests 
import json 
import os 
import tkinter as tk 
from tkinter import ttk 
import threading 


API_ENDPOINTS = [ 
    'https://deep.haoda.repl.co/translate', # API1 
    'https://fy.haoda7.repl.co/translate', # API2 
    'https://deep.haoda7.repl.co/translate', # API3 
] 

def test_api(api_endpoint): 
    try: 
        payload = { 
            'text': 'test', 
            'source_lang': 'auto', 
            'target_lang': 'EN' 
        } 
        response = requests.post(api_endpoint, json=payload) 
        response_json = json.loads(response.text) 
        result = response_json['data'] 
        return True 
    except: 
        return False 

def check_apis(api_endpoints): 
    for api_endpoint in api_endpoints: 
        if test_api(api_endpoint): 
            return api_endpoint 
    raise Exception(f"Failed to translate using {api_endpoint}: {str(e)}")

def remote_translate(text, api_endpoint, source_lang, target_lang): 
    try: 
        payload = { 
            'text': text, 
            'source_lang': source_lang, 
            'target_lang': target_lang 
        } 
        response = requests.post(api_endpoint, json=payload) 
        response_json = json.loads(response.text) 
        result = response_json['data'] 
        return result 
    except Exception as e: 
        print(f"Failed to translate using {api_endpoint}: {str(e)}") 
        print(f"Response: {response.text}") 
        raise e 

def translate(text, target_lang, status_label): 
    text = text.replace('\n', ' ') 
    if target_lang == '中文': 
        target_lang = 'ZH' 
    elif target_lang == '英文': 
        target_lang = 'EN' 
    else: 
        raise ValueError('Invalid target language') 
    api_endpoint = check_apis(API_ENDPOINTS) 
    status_label.config(text=f"正在翻译，使用API{API_ENDPOINTS.index(api_endpoint)+1}...") 
    result = remote_translate(text, api_endpoint, 'auto', target_lang) 
    status_label.config(text=f"翻译完成，使用API{API_ENDPOINTS.index(api_endpoint)+1}") 
    return result 

class Translator(tk.Frame):
    about_window = None

    def __init__(self, master=None): 
        super().__init__(master, bg='#F9F9F9', padx=20, pady=20) 
        self.master = master 
        self.master.title('Haoの翻译器') 
        self.pack(fill='both', expand=True) 
        self.history = [] 
        self.master.geometry("640x280")
        self.target_lang = tk.StringVar(value="中文") 
        self.create_widgets() 
        self.create_menu() 

    def create_menu(self): 
        menu_bar = tk.Menu(self.master) 
        lang_menu = tk.Menu(menu_bar, tearoff=0) 
        lang_menu.add_radiobutton(label="中文", variable=self.target_lang, value="中文") 
        lang_menu.add_radiobutton(label="英文", variable=self.target_lang, value="英文") 
        menu_bar.add_cascade(label="翻译语言", menu=lang_menu) 
        menu_bar.add_command(label="历史记录", command=self.show_history)
        self.master.config(menu=menu_bar)
        about_menu = tk.Menu(menu_bar, tearoff=0)
        about_menu.add_command(label="关于", command=self.show_about)
        menu_bar.add_cascade(label="帮助", menu=about_menu)

    def show_about(self):
        if self.about_window and self.about_window.winfo_exists():
            self.about_window.lift()  # 如果已经打开则将窗口置顶
            return
        self.about_window = tk.Toplevel(self.master)
        self.about_window.title("关于")
        self.about_window.geometry("300x200")
        about_frame = tk.Frame(self.about_window, bg='#F9F9F9', padx=20, pady=20)
        about_frame.pack(fill='both', expand=True)
        about_label = tk.Label(about_frame, text="Haoの翻译器", font=('Arial', 18), bg='#F9F9F9')
        about_label.pack(side='top', pady=10)
        version_label = tk.Label(about_frame, text="版本号：1.0", font=('Arial', 12), bg='#F9F9F9')
        version_label.pack(side='top', pady=5)
        author_label = tk.Label(about_frame, text="作者：Hao", font=('Arial', 12), bg='#F9F9F9')
        author_label.pack(side='top', pady=5)
        close_button = tk.Button(about_frame, text="关闭", font=('Arial', 12), command=self.about_window.destroy)
        close_button.pack(side='bottom', pady=10)

    def create_widgets(self): 
        self.main_frame = tk.Frame(self, bg='#F9F9F9') 
        self.main_frame.pack(side='top', fill='both', expand=True) 
        self.input_frame = tk.Frame(self.main_frame, bg='#FFFFFF', bd=1, relief='solid') 
        self.input_frame.grid(row=0, column=0, sticky='nsew', padx=10, pady=10) 
        self.input_label = tk.Label(self.input_frame, text="要翻译的文本:", font=('Arial', 12), bg='#FFFFFF') 
        self.input_label.pack(side='top', anchor='w', padx=10, pady=10) 
        self.input_text = tk.Text(self.input_frame, height=5, width=25, font=('Arial', 12), bg='#FFFFFF', fg='#333333', wrap='word') 
        self.input_text.pack(side='left', fill='both', expand=True) 
        self.input_scrollbar = ttk.Scrollbar(self.input_frame, orient='vertical', command=self.input_text.yview) 
        self.input_scrollbar.pack(side='right', fill='y') 
        self.input_text.config(yscrollcommand=self.input_scrollbar.set) 
        self.translate_button = tk.Button(self.main_frame, text="翻译", font=('Arial', 12), command=self.translate) 
        self.translate_button.grid(row=0, column=1, sticky='n', padx=10, pady=10)
        self.output_frame = tk.Frame(self.main_frame, bg='#FFFFFF', bd=1, relief='solid') 
        self.output_frame.grid(row=0, column=2, sticky='nsew', padx=10, pady=10)
        self.output_header_label = tk.Label(self.output_frame, text="翻译结果:", font=('Arial', 12), bg='#FFFFFF') 
        self.output_header_label.pack(side='top', anchor='w', padx=10, pady=10) 
        self.output_text = tk.Text(self.output_frame, height=5, width=25, font=('Arial', 12), bg='#FFFFFF', fg='#333333', wrap='word')  
        self.output_text.pack(side='left', fill='both', expand=True) 
        self.output_scrollbar = ttk.Scrollbar(self.output_frame, orient='vertical', command=self.output_text.yview) 
        self.output_scrollbar.pack(side='right', fill='y') 
        self.output_text.config(yscrollcommand=self.output_scrollbar.set) 
        self.status_frame = tk.Frame(self, bg='#F9F9F9') 
        self.status_frame.pack(side='bottom', fill='x', padx=10, pady=10) 
        self.status_label = tk.Label(self.status_frame, text="准备就绪", font=('Arial', 12), bg='#F9F9F9') 
        self.status_label.pack(side='left') 
        self.main_frame.columnconfigure(0, weight=1, minsize=200)
        self.main_frame.columnconfigure(2, weight=1, minsize=200)
        self.main_frame.rowconfigure(0, weight=1)

    def insert_result(self, result):
        self.output_text.delete('1.0', tk.END)
        self.output_text.insert(tk.END, result)

    def translate_thread(self):
        text = self.input_text.get("1.0", tk.END)
        if text.strip() == '':
            return
        target_lang = self.target_lang.get()
        try:
            result = translate(text, target_lang, self.status_label)
            self.after(100, self.insert_result, result)
            self.history.append({'input': text.strip(), 'output': result.strip()})
            self.after(100, self.clear_text)
        except ValueError as e:
            self.after(100, self.output_text.delete, '1.0', tk.END)
            self.after(100, self.insert_result, f"翻译失败：{str(e)}")
        except Exception as e:
            self.after(100, self.output_text.delete, '1.0', tk.END)
            self.after(100, self.insert_result, f"翻译失败：{str(e)}")

    def clear_text(self): 
        if self.input_text.get("1.0", tk.END).strip() != '':
            self.input_text.delete('1.0', tk.END)

    def translate(self):
        t = threading.Thread(target=self.translate_thread)
        t.start()

    def show_history(self):
        if hasattr(self, 'history_window') and self.history_window.winfo_exists():
            self.history_window.lift()
            return
        self.history_window = tk.Toplevel(self.master)
        self.history_window.title("历史记录")
        history_frame = tk.Frame(self.history_window, bg='#F9F9F9')
        history_frame.pack(side='top', fill='both', expand=True, padx=10, pady=10)
        history_label = tk.Label(history_frame, text="历史记录", font=('Arial', 18), bg='#F9F9F9')
        history_label.pack(side='top')
        history_text = tk.Text(history_frame, height=10, width=50, font=('Arial', 12), bg='#FFFFFF', fg='#333333', wrap='word')
        history_text.pack(side='left', fill='both', expand=True)
        history_scrollbar = ttk.Scrollbar(history_frame, orient='vertical', command=history_text.yview)
        history_scrollbar.pack(side='right', fill='y')
        history_text.config(yscrollcommand=history_scrollbar.set)
        for item in self.history:
            history_text.insert(tk.END, f"输入文本：{item['input']}\n翻译结果：{item['output']}\n\n")

if __name__ == '__main__': 
    root = tk.Tk() 
    app = Translator(master=root) 
    app.mainloop()