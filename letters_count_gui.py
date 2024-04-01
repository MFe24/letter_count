import csv
import tkinter as tk
from tkinter import messagebox

def load_char_counts(csv_file):
    char_counts = {}
    with open(csv_file, newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        next(reader)  # ヘッダー行をスキップ
        for row in reader:
            utf16_code = row[0]  # Unicode文字
            count = int(row[1])  # 出現回数
            char_counts[utf16_code] = count
    return char_counts

def update_char_counts(char_counts, input_str):
    ignored_chars = []  # 無視された文字のリスト
    already_counted = set()  # すでに数えた文字のセット
    for char in input_str:
        utf16_code = hex(ord(char)).upper()
        utf16_code = utf16_code[2:].zfill(4)  # 先頭に0を含む4桁の16進数文字列に変換
        check_code = "U+" + utf16_code
        if check_code in char_counts and check_code not in already_counted:
            char_counts[check_code] += 1
            already_counted.add(check_code)
        elif check_code not in char_counts:
            ignored_chars.append(char)
    return ignored_chars

def save_char_counts(char_counts, output_file):
    with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Unicode', 'Count'])  # ヘッダー行
        for utf16_code, count in char_counts.items():
            writer.writerow([utf16_code, count])

def calculate_char_counts(event=None):
    input_str = entry.get()  # テキストボックスから入力を取得
    char_counts = load_char_counts("code_count.csv")
    ignored_chars = update_char_counts(char_counts, input_str)
    save_char_counts(char_counts, "code_count.csv")
    messagebox.showinfo("処理完了", "文字の出現回数を更新しました。")
    if ignored_chars:
        ignored_str = ", ".join(ignored_chars)
        messagebox.showwarning("無視された文字", f"以下の文字は無視されました: {ignored_str}")
    entry.delete(0, tk.END)  # テキストボックスを空にする

# GUIを作成
root = tk.Tk()
root.title("文字数カウンター")

frame = tk.Frame(root)
frame.pack(padx=10, pady=10)

label = tk.Label(frame, text="文章を入力してください:")
label.grid(row=0, column=0)

entry = tk.Entry(frame, width=40)
entry.grid(row=0, column=1, padx=5, pady=5, ipady=10)  # テキストボックスを縦に広げる

button = tk.Button(frame, text="計算")
button.grid(row=0, column=2)

# Alt+Enterで処理するためのバインディングを追加
root.bind('<Alt-Return>', calculate_char_counts)

# ボタンがクリックされたときのイベントをバインド
button.config(command=calculate_char_counts)

root.mainloop()
