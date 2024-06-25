import tkinter as tk
from tkinter import messagebox
from tkinter import filedialog
import random
import string
import csv
import pandas as pd
import os


def generate_passwords():
    try:
        length = int(entry_length.get())
        count = int(entry_count.get())

        if length < 10 or length > 24:
            messagebox.showerror("Błąd", "Hasło musi mieć od 10 do 24 znaków.")
            return

        passwords = []
        for i in range(count):
            while True:
                password = ''.join(random.choices(
                    string.ascii_letters + string.digits + "~!@#%^&*()_+=\\-;,./<>?[]{}", k=length))

                # Sprawdź, czy hasło spełnia nowe warunki
                if (sum(c.isdigit() for c in password) >= 2 and
                        any(c.islower() for c in password) and
                        any(c.isupper() for c in password) and
                        sum(c in "~!@#%^&*()_+=\\-;,./<>?[]{}" for c in password) >= 2):
                    passwords.append(f"{i + 1}. {password}")
                    break

        text_output.delete("1.0", tk.END)
        text_output.insert(tk.END, "\n".join(passwords))
    except ValueError:
        messagebox.showerror("Błąd", "Wprowadź poprawną liczbę znaków.")


def save_to_file(file_type):
    passwords = text_output.get("1.0", tk.END).strip().split("\n")
    if not passwords or passwords == ['']:
        messagebox.showerror("Błąd", "Brak wygenerowanych haseł do zapisania.")
        return

    user_documents = os.path.join(os.path.expanduser('~'), 'Documents')
    file_path = filedialog.asksaveasfilename(defaultextension=f".{file_type}",
                                             initialdir=user_documents,
                                             filetypes=[(f"{file_type.upper()} files", f"*.{file_type}"),
                                                        ("All files", "*.*")])
    if not file_path:
        return

    if file_type == "txt":
        with open(file_path, "w") as file:
            for password in passwords:
                file.write(password + "\n")
        messagebox.showinfo("Sukces", f"Hasła zapisane do pliku {file_path}")

    elif file_type == "csv":
        with open(file_path, "w", newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["Number", "Password"])
            for password in passwords:
                writer.writerow(password.split(". ", 1))
        messagebox.showinfo("Sukces", f"Hasła zapisane do pliku {file_path}")

    elif file_type == "xlsx":
        df = pd.DataFrame([password.split(". ", 1) for password in passwords], columns=["Number", "Password"])
        df.to_excel(file_path, index=False)
        messagebox.showinfo("Sukces", f"Hasła zapisane do pliku {file_path}")


app = tk.Tk()
app.title("Generator Haseł")
app.configure(bg="#008B8B")

frame = tk.Frame(app, bg="#008B8B")
frame.pack(pady=10)

label_length = tk.Label(frame, text="Długość hasła:", bg="#008B8B", fg="white")
label_length.pack(side=tk.LEFT, padx=5)

entry_length = tk.Entry(frame, width=5, bg="#008B8B", fg="white", insertbackground="white")
entry_length.pack(side=tk.LEFT, padx=5)

label_count = tk.Label(frame, text="Ilość haseł:", bg="#008B8B", fg="white")
label_count.pack(side=tk.LEFT, padx=5)

entry_count = tk.Entry(frame, width=5, bg="#008B8B", fg="white", insertbackground="white")
entry_count.pack(side=tk.LEFT, padx=5)

button_generate = tk.Button(frame, text="Generuj", command=generate_passwords, bg="#008B8B", fg="white")
button_generate.pack(side=tk.LEFT, padx=5)

# Dodanie pola tekstowego z paskiem przewijania
text_frame = tk.Frame(app, bg="#008B8B")
text_frame.pack(pady=10)

scrollbar = tk.Scrollbar(text_frame)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

text_output = tk.Text(text_frame, height=35, width=70, bg="#000000", fg="white", insertbackground="white",
                      yscrollcommand=scrollbar.set)
text_output.pack(side=tk.LEFT, fill=tk.BOTH)

scrollbar.config(command=text_output.yview)

button_frame = tk.Frame(app, bg="#008B8B")
button_frame.pack(pady=5)

button_save_txt = tk.Button(button_frame, text="Zapisz jako TXT", command=lambda: save_to_file("txt"), bg="#008B8B",
                            fg="white")
button_save_txt.pack(side=tk.LEFT, padx=5)

button_save_csv = tk.Button(button_frame, text="Zapisz jako CSV", command=lambda: save_to_file("csv"), bg="#008B8B",
                            fg="white")
button_save_csv.pack(side=tk.LEFT, padx=5)

button_save_xlsx = tk.Button(button_frame, text="Zapisz jako XLSX", command=lambda: save_to_file("xlsx"), bg="#008B8B",
                             fg="white")
button_save_xlsx.pack(side=tk.LEFT, padx=5)

app.mainloop()
