import requests
import json
import os
import tkinter as tk

API_ENDPOINT = os.environ.get('API_ENDPOINT', 'https://deep.haoda7.repl.co/translate')
SOURCE_LANG = 'auto'
TARGET_LANG = 'ZH'

def remote_translate(text, api_endpoint, source_lang, target_lang):
    payload = {
        'text': text,
        'source_lang': source_lang,
        'target_lang': target_lang
    }
    response = requests.post(api_endpoint, json=payload)
    response_json = json.loads(response.text)
    result = response_json['data']
    return result

def translate(text):
    text = text.replace('\n', ' ')
    result = remote_translate(text, API_ENDPOINT, SOURCE_LANG, TARGET_LANG)
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
        result = remote_translate(text, API_ENDPOINT, SOURCE_LANG, TARGET_LANG)
        self.output_text.delete("1.0", tk.END)
        self.output_text.insert(tk.END, result)

if __name__ == '__main__':
    root = tk.Tk()
    app = Translator(master=root)
    app.mainloop()