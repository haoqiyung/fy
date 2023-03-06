import requests
import json
import os
import tkinter as tk
from tkinter import ttk

API_ENDPOINTS = [
    'https://deep.haoda7.repl.co/translate',
    'https://libretranslate.com/translate',
    'https://api-free.deepl.com/v2/translate',
]

def remote_translate(text, api_endpoints, source_lang, target_lang):
    for api_endpoint in api_endpoints:
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
    raise Exception("All APIs failed to translate the text.")

def translate(text, target_lang):
    text = text.replace('\n', ' ')
    if target_lang == '中文':
        target_lang = 'ZH'
    elif target_lang == '英文':
        target_lang = 'EN'
    else:
        raise ValueError('Invalid target language')
    result = remote_translate(text, API_ENDPOINTS, 'auto', target_lang)
    return result

class Translator(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()
        self.create_widgets()

    def create_widgets(self):
        self.input_label = tk.Label(self, text="要翻译的文本:")
        self.input_label.pack()
        self.input_text = tk.Text(self, height=10, width=50)
        self.input_text.pack()

        self.lang_frame = tk.Frame(self)
        self.lang_frame.pack()

        self.target_lang_label = tk.Label(self.lang_frame, text="目标语言:")
        self.target_lang_label.pack(side=tk.LEFT)
        self.target_lang_input = ttk.Combobox(self.lang_frame, values=['中文', '英文'])
        self.target_lang_input.current(0)
        self.target_lang_input.pack(side=tk.LEFT)

        self.output_label = tk.Label(self, text="翻译结果:")
        self.output_label.pack()
        self.output_text = tk.Text(self, height=10, width=50)
        self.output_text.pack()

        self.translate_button = tk.Button(self, text="翻译", command=self.translate)
        self.translate_button.pack()

        self.quit_button = tk.Button(self, text="退出", command=self.master.destroy)
        self.quit_button.pack()

    def translate(self):
        text = self.input_text.get("1.0", tk.END)
        target_lang = self.target_lang_input.get()
        try:
            result = translate(text, target_lang)
            self.output_text.delete("1.0", tk.END)
            self.output_text.insert(tk.END, result)
        except ValueError as e:
            self.output_text.delete("1.0", tk.END)
            self.output_text.insert(tk.END, f"翻译失败：{str(e)}")
        except Exception as e:
            self.output_text.delete("1.0", tk.END)
            self.output_text.insert(tk.END, f"翻译失败：{str(e)}")

if __name__ == '__main__':
    root = tk.Tk()
    app = Translator(master=root)
    app.mainloop()