import requests
import json
import os
import tkinter as tk
from tkinter import ttk
import threading


API_ENDPOINTS = [
    'https://dep.haoda7.repl.co/translate', # API1
    'https://libretranslate.com/translate',  # API2
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
    raise Exception("All APIs failed to connect.")


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


def translate(text, target_lang):
    text = text.replace('\n', ' ')
    if target_lang == '中文':
        target_lang = 'ZH'
    elif target_lang == '英文':
        target_lang = 'EN'
    else:
        raise ValueError('Invalid target language')

    api_endpoint = check_apis(API_ENDPOINTS)
    result = remote_translate(text, api_endpoint, 'auto', target_lang)
    return result


class Translator(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master, bg='#F9F9F9', padx=20, pady=20)
        self.master = master
        self.master.title('翻译器')
        self.pack(fill='both', expand=True)
        self.create_widgets()

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


if __name__ == '__main__':
    root = tk.Tk()
    app = Translator(master=root)
    app.mainloop()