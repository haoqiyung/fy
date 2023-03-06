import http.client
import json
import tkinter as tk
from tkinter import filedialog
import threading
from tkinter import ttk 

conn = http.client.HTTPSConnection("fy.haoda.repl.co")

def translate_text(source_text, source_lang, target_lang):
    payload = json.dumps({
        "text": source_text,
        "source_lang": source_lang,
        "target_lang": target_lang
    })
    headers = {
        'Content-Type': 'application/json',
        'Accept': '/',
    }
    progress = ttk.Progressbar(root, orient="horizontal", length=100, mode="indeterminate")
    progress.grid(row=2, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")
    progress.start()
    conn.request("POST", "/translate", payload, headers)
    res = conn.getresponse()
    data = res.read()
    progress.stop()
    progress.grid_forget()
    try:
        json_data = json.loads(data)
        translation = json_data["result"]["texts"][0]["text"]
    except KeyError:
        translation = "翻译失败，请检查输入文本和目标语言是否正确。"
    return translation

def translate():
    source_text = source_text_box.get("1.0", "end-1c")
    if not source_text.strip():
        return
    if all(ord(c) < 128 for c in source_text.strip()):
        source_lang, target_lang = "EN", "ZH"
    else:
        source_lang, target_lang = "ZH", "EN"
    threading.Thread(target=do_translate, args=(source_text, source_lang, target_lang)).start()

def do_translate(source_text, source_lang, target_lang): 
    translation = translate_text(source_text, source_lang, target_lang)
    target_text_box.delete("1.0", "end")
    target_text_box.insert("1.0", translation)
    history_listbox.insert(0, f"{source_text.strip()} -> {translation.strip()}")
    source_text_box.delete("1.0", "end")

def toggle_history():
    if history_frame.winfo_ismapped():
        history_frame.grid_forget()
    else:
        history_frame.grid(row=1, column=1, sticky="nsew")
        history_listbox.config(height=5)

def fill_input(event):
    selected_text = history_listbox.get(history_listbox.curselection())
    source_text_box.delete("1.0", "end")
    source_text_box.insert("1.0", selected_text)

def clear_history():
    history_listbox.delete(0, "end")

def export_history():
    file_path = filedialog.asksaveasfilename(defaultextension=".txt")
    if file_path:
        with open(file_path, "w", encoding="utf-8") as f:
            for item in history_listbox.get(0, "end"):
                f.write(item + "\n")

about_window = None

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

root = tk.Tk()
root.title("翻译软件")

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

left_frame = tk.Frame(root, padx=10, pady=10)
left_frame.grid(row=1, column=0, sticky="nsew")

source_text_label = tk.Label(left_frame, text="输入文本:")
source_text_label.grid(row=0, column=0, sticky="w")

source_text_box = tk.Text(left_frame, height=10, width=50)
source_text_box.grid(row=1, column=0, sticky="nsew")

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

history_listbox.bind("<Double-Button-1>", fill_input)

root.columnconfigure(0, weight=1)
root.columnconfigure(1, weight=1)
root.rowconfigure(1, weight=1)
left_frame.rowconfigure(1, weight=1)
right_frame.rowconfigure(1, weight=1)
right_frame.rowconfigure(2, weight=1)

history_frame.grid_forget()

root.mainloop()