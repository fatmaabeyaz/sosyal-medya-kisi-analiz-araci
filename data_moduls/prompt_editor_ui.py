import tkinter as tk
from tkinter import messagebox

def get_output_format_from_file():
    with open("nlp.py", "r", encoding="utf-8") as file:
        lines = file.readlines()

    # Çıktı formatı kısmını bul
    start = end = None
    for i, line in enumerate(lines):
        if '"""' in line and "Çıktı formatı" in line:
            start = i
            break

    if start is not None:
        for j in range(start + 1, len(lines)):
            if '"""' in lines[j]:
                end = j
                break

    if start is not None and end is not None:
        # "Çıktı formatı:\n" dahil tüm satırları al
        raw_block = lines[start + 1:end]
        return "".join(raw_block).strip(), start, end, lines
    else:
        return "", None, None, lines

def save_changes():
    new_text = text_box.get("1.0", tk.END).strip().splitlines()
    _, start, end, lines = get_output_format_from_file()

    if start is not None and end is not None:
        updated_block = ['"""Çıktı formatı:\n'] + [line.rstrip() + '\n' for line in new_text] + ['"""\n']
        lines = lines[:start] + updated_block + lines[end + 1:]

        with open("nlp.py", "w", encoding="utf-8") as file:
            file.writelines(lines)

        messagebox.showinfo("Başarılı", "Çıktı formatı başarıyla güncellendi.")
    else:
        messagebox.showerror("Hata", "Çıktı formatı bölümü bulunamadı.")

# GUI Başlat
root = tk.Tk()
root.title("Prompt Alanı Düzenleyici")

label = tk.Label(root, text='Sadece "Çıktı formatı" kısmını düzenleyebilirsiniz:', font=("Arial", 12))
label.pack(pady=10)

text_box = tk.Text(root, height=20, width=100, wrap="word", font=("Courier", 11))
text_box.pack(padx=10, pady=10)

output_format, _, _, _ = get_output_format_from_file()
text_box.insert(tk.END, output_format)

btn = tk.Button(root, text="Kaydet", command=save_changes)
btn.pack(pady=10)

root.mainloop()
