import http.client
import json
import tkinter as tk
from tkinter import filedialog
import threading
from tkinter import ttk 
import time
import sys

conn = http.client.HTTPSConnection("fy.haoda.repl.co")

about_window = None

def translate_text(source_text, source_lang, target_lang):
    # 发送翻译请求
    payload = json.dumps({
        "text": source_text,
        "source_lang": source_lang,
        "target_lang": target_lang
    })
    headers = {
        'User-Agent': 'APIFOX/1.0.0 (https://www.apifox.com)',
        'Content-Type': 'application/json',
        'Accept': '/',
        'Host': 'fy.haoda.repl.co',
        'Connection': 'keep-alive'
    }
    # 创建进度条对象
    progress = ttk.Progressbar(root, orient="horizontal", length=100, mode="indeterminate")
    progress.grid(row=2, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")
    progress.start()
    conn.request("POST", "/translate", payload, headers)
    res = conn.getresponse()
    data = res.read()
    # 关闭进度条对象
    progress.stop()
    progress.grid_forget()
    # 解析翻译结果
    try:
        json_data = json.loads(data)
        translation = json_data["result"]["texts"][0]["text"]
    except KeyError:
        translation = "翻译失败，请检查输入文本和目标语言是否正确。"
    return translation

def translate():
    # 获取源语言、目标语言和源文本，并进行翻译
    source_text = source_text_box.get("1.0", "end-1c")
    if not source_text.strip(): # 输入框为空，不能进行翻译
        return
    if all(ord(c) < 128 for c in source_text.strip()): # 全部是 ASCII 字符，说明是英文
        source_lang = "EN"
        target_lang = "ZH"
    else: # 否则认为是中文
        source_lang = "ZH"
        target_lang = "EN"

    # 将翻译请求放到一个单独的线程中进行，避免阻塞主线程 
    threading.Thread(target=do_translate, args=(source_text, source_lang, target_lang)).start()

def do_translate(source_text, source_lang, target_lang): 
    # 调用 translate_text 函数进行翻译，并获取翻译结果
    translation = translate_text(source_text, source_lang, target_lang)
    # 将翻译结果显示在输出框中，并将翻译文本添加到历史记录中
    target_text_box.delete("1.0", "end")
    target_text_box.insert("1.0", translation)
    history_listbox.insert(0, f"{source_text.strip()} -> {translation.strip()}")
    # 清空输入框中的内容
    source_text_box.delete("1.0", "end")

def toggle_history():
    # 切换历史记录列表的显示状态
    if history_frame.winfo_ismapped():
        history_frame.grid_forget()
    else:
        history_frame.grid(row=1, column=1, sticky="nsew")
        history_listbox.config(height=5)

def fill_input(event):
    # 将历史记录中选中的文本填充到输入框中
    selected_text = history_listbox.get(history_listbox.curselection())
    source_text_box.delete("1.0", "end")
    source_text_box.insert("1.0", selected_text)

def clear_history():
    # 清空历史记录列表
    history_listbox.delete(0, "end")

def export_history():
    # 导出历史记录到文件
    file_path = filedialog.asksaveasfilename(defaultextension=".txt")
    if file_path:
        with open(file_path, "w", encoding="utf-8") as f:
            for item in history_listbox.get(0, "end"):
                f.write(item + "\n")

def show_about():
    # 显示关于窗口
    global about_window
    if about_window is None or not about_window.winfo_exists():
        about_window = tk.Toplevel(root)
        about_window.title("关于")
        about_window.geometry("200x100")
        about_label = tk.Label(about_window, text="AI语言翻译助手\n作者：xxx")
        about_label.pack(padx=20, pady=20)
    else:
        about_window.destroy()

root = tk.Tk()
root.title("翻译软件")

# 头部栏：标题、翻译按钮、历史记录按钮、关于按钮
header_frame = tk.Frame(root, padx=10, pady=10)
header_frame.grid(row=0, column=0, columnspan=2, sticky="nsew")

title_label = tk.Label(header_frame, text="AI 语言翻译助手", font=("Arial", 15))
title_label.grid(row=0, column=0, sticky="w")

translate_button = tk.Button(header_frame, text="翻译", command=translate, width=10)
translate_button.grid(row=0, column=1, sticky="e")

history_button = tk.Button(header_frame, text="历史记录", command=toggle_history, width=10)
history_button.grid(row=0, column=2, sticky="e")

about_button = tk.Button(header_frame, text="关于", command=show_about, width=10)
about_button.grid(row=0, column=3, sticky="e")



# 左侧栏：输入框
left_frame = tk.Frame(root, padx=10, pady=10)
left_frame.grid(row=1, column=0, sticky="nsew")

source_text_label = tk.Label(left_frame, text="输入文本:")
source_text_label.grid(row=0, column=0, sticky="w")

source_text_box = tk.Text(left_frame, height=10, width=50)
source_text_box.grid(row=1, column=0, sticky="nsew")

# 右侧栏：翻译结果输出框、历史记录列表和导出历史记录按钮
right_frame = tk.Frame(root, padx=10, pady=10)
right_frame.grid(row=1, column=1, sticky="nsew")

target_text_label = tk.Label(right_frame, text="翻译结果:")
target_text_label.grid(row=0, column=0, sticky="w")

target_text_box = tk.Text(right_frame, height=10, width=50)
target_text_box.grid(row=1, column=0, sticky="nsew")

history_frame = tk.Frame(right_frame, bd=1, relief="solid")
history_frame.grid(row=1, column=1, sticky="nsew")

history_label = tk.Label(history_frame, text="历史记录", font=("Arial", 12))
history_label.grid(row=0, column=0, sticky="w")

export_button = tk.Button(history_frame, text="导出历史记录", command=export_history, width=10)
export_button.grid(row=0, column=1, sticky="e")

clear_history_button = tk.Button(history_frame, text="清空历史记录", command=clear_history, width=10)
clear_history_button.grid(row=0, column=2, sticky="e")

history_listbox = tk.Listbox(history_frame, height=10, width=50)
history_listbox.grid(row=1, column=0, columnspan=3, sticky="nsew")

history_scrollbar = tk.Scrollbar(history_frame, orient="vertical")
history_scrollbar.grid(row=1, column=3, sticky="ns")

history_listbox.config(yscrollcommand=history_scrollbar.set)
history_scrollbar.config(command=history_listbox.yview)

history_listbox.bind("<Double-Button-1>", fill_input) # 双击历史记录中的文本，填充到输入框中

# 设置窗口的布局和大小
root.columnconfigure(0, weight=1)
root.columnconfigure(1, weight=1)
root.rowconfigure(1, weight=1)
left_frame.rowconfigure(1, weight=1)
right_frame.rowconfigure(1, weight=1)
right_frame.rowconfigure(2, weight=1)

history_frame.grid_forget() # 初始状态下隐藏历史记录列表

root.mainloop()