import http.client
import json
import tkinter as tk
from tkinter import ttk

# 定义翻译API的地址和key
api_list = [
    {
        "name": "百度翻译",
        "url": "api.fanyi.baidu.com",
        "path": "/api/trans/vip/translate",
        "key": "your_baidu_api_key"
    },
    {
        "name": "有道翻译",
        "url": "fanyi.youdao.com",
        "path": "/translate_o",
        "key": "your_youdao_api_key"
    }
]

conn = None # API连接

about_window = None

def detect_language(source_text):
    global conn
    payload = json.dumps({
        "text": source_text
    })
    headers = {
        'User-Agent': 'Mozilla/5.0',
        'Content-Type': 'application/json'
    }
    conn.request("POST", "/detect", payload, headers)
    res = conn.getresponse()
    data = res.read()
    json_data = json.loads(data)
    language = json_data["result"]["language"]
    return language

def translate_text(source_text, target_lang):
    global conn
    payload = json.dumps({
        "text": source_text,
        "target_lang": target_lang
    })
    headers = {
        'User-Agent': 'Mozilla/5.0',
        'Content-Type': 'application/json'
    }
    conn.request("POST", "/translate", payload, headers)
    res = conn.getresponse()
    data = res.read()
    try:
        json_data = json.loads(data)
        translation = json_data["result"]["texts"][0]["text"]
    except KeyError:
        translation = "翻译失败，请检查输入文本和目标语言是否正确。"
    return translation

def translate():
    global conn
    source_text = source_text_box.get("1.0", "end-1c")
    if source_text == "": # 输入框为空，不能进行翻译
        return
    source_lang = detect_language(source_text)
    if source_lang == "zh":
        target_lang = "en"
    else:
        target_lang = "zh"
    translation = translate_text(source_text, target_lang)
    target_text_box.delete("1.0", "end")
    target_text_box.insert("1.0", translation)
    history_listbox.insert(0, source_text) # 将翻译的源文本添加到历史记录中
    source_text_box.delete("1.0", "end") # 清空输入框中的内容

def toggle_history():
    if history_frame.winfo_ismapped():
        history_frame.grid_forget()
    else:
        history_frame.grid(row=1, column=1, sticky="nsew")

def fill_input(event):
    # 将历史记录中选中的文本填充到输入框中
    selected_text = history_listbox.get(history_listbox.curselection())
    source_text_box.delete("1.0", "end")
    source_text_box.insert("1.0", selected_text)

def clear_history():
    history_listbox.delete(0, "end")

def show_about():
    global about_window
    if about_window is None or not about_window.winfo_exists():
        about_window = tk.Toplevel(root)
        about_window.title("关于")
        about_window.geometry("200x100")
        about_label = tk.Label(about_window, text="AI语言翻译助手\n作者：xxx")
        about_label.pack(padx=20, pady=20)
    else:
        about_window.destroy()

def switch_api():
    global conn
    api_index = api_select.current()
    api = api_list[api_index]
    conn = http.client.HTTPSConnection(api["url"])
    conn.key = api["key"]
    conn.path = api["path"]
    print("已切换到" + api["name"] + "API")

root = tk.Tk()
root.title("翻译软件")

# 头部栏：标题、翻译按钮、历史记录按钮、清空历史记录按钮、关于按钮、翻译API选择框
header_frame = tk.Frame(root, padx=10, pady=10)
header_frame.grid(row=0, column=0, columnspan=2, sticky="nsew")

title_label = tk.Label(header_frame, text="AI 语言翻译助手", font=("Arial", 16))
title_label.grid(row=0, column=0, sticky="w")

translate_button = tk.Button(header_frame, text="翻译", command=translate, width=10)
translate_button.grid(row=0, column=1, sticky="e")

history_button = tk.Button(header_frame, text="历史记录", command=toggle_history, width=10)
history_button.grid(row=0, column=2, sticky="e")

about_button = tk.Button(header_frame, text="关于", command=show_about, width=10)
about_button.grid(row=0, column=4, sticky="e")

api_select = tk.ttk.Combobox(header_frame, values=[api["name"] for api in api_list], width=10)
api_select.current(0)
api_select.bind("<<ComboboxSelected>>", lambda event: switch_api())
api_select.grid(row=0, column=5, sticky="e")

# 左侧栏：输入框
left_frame = tk.Frame(root, padx=10, pady=10)
left_frame.grid(row=1, column=0, sticky="nsew")

source_text_label = tk.Label(left_frame, text="输入文本:")
source_text_label.grid(row=0, column=0, sticky="w")

source_text_box = tk.Text(left_frame, height=10, width=50)
source_text_box.grid(row=1, column=0, sticky="nsew")

# 右侧栏：翻译结果输出框、历史记录列表
right_frame = tk.Frame(root, padx=10, pady=10)
right_frame.grid(row=1, column=1, sticky="nsew")

target_text_label = tk.Label(right_frame, text="翻译结果:")
target_text_label.grid(row=0, column=0, sticky="w")

target_text_box = tk.Text(right_frame, height=10, width=50)
target_text_box.grid(row=1, column=0, sticky="nsew")

history_frame = tk.Frame(right_frame, bd=1, relief="solid")
history_frame.grid(row=2, column=0, sticky="nsew")

history_label = tk.Label(history_frame, text="历史记录", font=("Arial", 12))
history_label.grid(row=0, column=0, sticky="w")

clear_history_button2 = tk.Button(history_frame, text="清空历史记录", command=clear_history, width=10)
clear_history_button2.grid(row=0, column=1, sticky="e")

history_listbox = tk.Listbox(history_frame, height=10, width=50)
history_listbox.grid(row=1, column=0, columnspan=2, sticky="nsew")

history_scrollbar = tk.Scrollbar(history_frame, orient="vertical")
history_scrollbar.grid(row=1, column=2, sticky="ns")

history_listbox.config(yscrollcommand=history_scrollbar.set)
history_scrollbar.config(command=history_listbox.yview)

history_listbox.bind("<Double-Button-1>", fill_input) # 双击历史记录中的文本，填充到输入框中

root.columnconfigure(0, weight=1)
root.columnconfigure(1, weight=1)
root.rowconfigure(1, weight=1)

left_frame.rowconfigure(1, weight=1)

right_frame.rowconfigure(1, weight=1)
right_frame.rowconfigure(2, weight=1)

history_frame.grid_forget() # 初始状态下隐藏历史记录列表

# 初始化连接
switch_api()

root.mainloop()