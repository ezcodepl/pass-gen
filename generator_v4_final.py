import tkinter as tk
from tkinter import messagebox
from tkinter import filedialog
from tkinter import ttk
import random
import string
import csv
import pandas as pd
import os
from datetime import datetime

# Domyślne znaki używane do generowania haseł
DEFAULT_CHARACTERS = string.ascii_letters + string.digits + "~!@#%^&*()_+=\\-;,./<>?[]{}"

# Zmienne globalne do przechowywania wyboru języka
LANGUAGE = "PL"

def set_language(lang):
    global LANGUAGE
    LANGUAGE = lang
    root.destroy()

def translate(text):
    translations = {
        "PL": {
            "Password Length:": "Długość hasła:",
            "Number of Passwords:": "Ilość haseł:",
            "Generate": "Generuj",
            "Clear": "Wyczyść",
            "Password strength:": "Siła hasła:",
            "Error": "Błąd",
            "Enter password length.": "Wprowadź długość hasła.",
            "Enter number of passwords.": "Wprowadź ilość haseł do wygenerowania.",
            "Password must be at least 8 characters long.": "Hasło musi mieć co najmniej 8 znaków.",
            "Invalid input. Enter valid numbers.": "Wprowadź poprawną liczbę znaków.",
            "File": "Plik",
            "Save as TXT": "Zapisz jako TXT",
            "Save as CSV": "Zapisz jako CSV",
            "Save as XLSX": "Zapisz jako XLSX",
            "Close": "Zamknij",
            "About": "O programie",
            "Password Generator\nAuthor: Ernest Zając\nVersion: 1.0\nWebsite: https://www.ezcode.pl":
                "Generator Haseł\nAutor: Ernest Zając\nWersja: 1.0\nStrona: https://www.ezcode.pl",
            "Generated password list:": "Wygenerowano listę haseł:",
            "No passwords to save.": "Brak wygenerowanych haseł do zapisania.",
            "Success": "Sukces",
            "Passwords saved to file": "Hasła zapisane do pliku"
        },
        "EN": {
            "Password Length:": "Password Length:",
            "Number of Passwords:": "Number of Passwords:",
            "Generate": "Generate",
            "Clear": "Clear",
            "Password strength:": "Password strength:",
            "Error": "Error",
            "Enter password length.": "Enter password length.",
            "Enter number of passwords.": "Enter number of passwords.",
            "Password must be at least 8 characters long.": "Password must be at least 8 characters long.",
            "Invalid input. Enter valid numbers.": "Invalid input. Enter valid numbers.",
            "Save as TXT": "Save as TXT",
            "Save as CSV": "Save as CSV",
            "Save as XLSX": "Save as XLSX",
            "Close": "Close",
            "About": "About",
            "Password Generator\nAuthor: Ernest Zając\nVersion: 1.0\nWebsite: https://www.ezcode.pl":
                "Password Generator\nAuthor: Ernest Zając\nVersion: 1.0\nWebsite: https://www.ezcode.pl",
            "Generated password list:": "Generated password list:",
            "No passwords to save.": "No passwords to save.",
            "Success": "Success",
            "Passwords saved to file": "Passwords saved to file"
        }
    }
    return translations[LANGUAGE].get(text, text)

def generate_passwords():
    length = entry_length.get().strip()
    count = entry_count.get().strip()

    if not length:
        messagebox.showerror(translate("Error"), translate("Enter password length."))
        return
    if not count:
        messagebox.showerror(translate("Error"), translate("Enter number of passwords."))
        return

    try:
        length = int(length)
        count = int(count)

        if length < 8:
            messagebox.showerror(translate("Error"), translate("Password must be at least 8 characters long."))
            return

        passwords = []
        for i in range(count):
            while True:
                password = ''.join(random.choices(DEFAULT_CHARACTERS, k=length))

                digit_count = sum(c.isdigit() for c in password)
                lower_count = sum(c.islower() for c in password)
                upper_count = sum(c.isupper() for c in password)
                special_count = sum(c in "~!@#%^&*()_+=\\-;,./<>?[]{}" for c in password)

                if (digit_count >= 2 and lower_count >= 1 and upper_count >= 1 and special_count >= 2):
                    passwords.append(f"{i + 1}. {password}")
                    break

        text_output.delete("1.0", tk.END)
        text_output.insert(tk.END, "\n".join(passwords))
        update_strength_indicator(length)
        generated_info_label.config(text=f"{translate('Generated password list:')} {count}")

    except ValueError:
        messagebox.showerror(translate("Error"), translate("Invalid input. Enter valid numbers."))

def update_strength_indicator(length):
    strength = ""

    if length >= 8 and length < 15:
        strength = translate("Medium Password")
        progress_bar.config(value=33, style="MediumPassword.Horizontal.TProgressbar")
    elif length >= 15 and length <= 20:
        strength = translate("Good Password")
        progress_bar.config(value=66, style="GoodPassword.Horizontal.TProgressbar")
    elif length > 20:
        strength = translate("Strong Password")
        progress_bar.config(value=100, style="StrongPassword.Horizontal.TProgressbar")
    else:
        strength = translate("Weak Password")
        progress_bar.config(value=0, style="WeakPassword.Horizontal.TProgressbar")

    strength_label.config(text=f"{translate('Password strength:')} {strength}")

def save_to_file(file_type):
    passwords = text_output.get("1.0", tk.END).strip().split("\n")
    if not passwords or passwords == ['']:
        messagebox.showerror(translate("Error"), translate("No passwords to save."))
        return

    user_documents = os.path.join(os.path.expanduser('~'), 'Documents')
    default_filename = f"pass_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}"
    file_path = filedialog.asksaveasfilename(defaultextension=f".{file_type}",
                                             initialdir=user_documents,
                                             initialfile=default_filename,
                                             filetypes=[(f"{file_type.upper()} files", f"*.{file_type}"),
                                                        ("All files", "*.*")])
    if not file_path:
        return

    if file_type == "txt":
        with open(file_path, "w") as file:
            for password in passwords:
                file.write(password + "\n")
        messagebox.showinfo(translate("Success"), f"{translate('Passwords saved to file')} {file_path}")

    elif file_type == "csv":
        with open(file_path, "w", newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["Number", "Password"])
            for password in passwords:
                writer.writerow(password.split(". ", 1))
        messagebox.showinfo(translate("Success"), f"{translate('Passwords saved to file')} {file_path}")

    elif file_type == "xlsx":
        df = pd.DataFrame([password.split(". ", 1) for password in passwords], columns=["Number", "Password"])
        df.to_excel(file_path, index=False)
        messagebox.showinfo(translate("Success"), f"{translate('Passwords saved to file')} {file_path}")

def about_program():
    messagebox.showinfo(translate("About"), translate("Password Generator\nAuthor: Ernest Zając\nVersion: 1.0\nWebsite: https://www.ezcode.pl"))

def clear_fields():
    entry_length.delete(0, tk.END)
    entry_count.delete(0, tk.END)
    text_output.delete("1.0", tk.END)
    generated_info_label.config(text="")
    progress_bar.config(value=0, style="TProgressbar")

def center_window(window, width, height):
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    x = int((screen_width / 2) - (width / 2))
    y = int((screen_height / 2) - (height / 2))
    window.geometry(f'{width}x{height}+{x}+{y}')

# Tworzenie okna wyboru języka
root = tk.Tk()
root.title("Wybór języka / Select Language")
#root.geometry("400x250")
center_window(root, 400, 250)
root.configure(bg="#008B8B")
tk.Label(root, text="Wybierz język / Select Language", bg="#008B8B", fg="white", font=("Arial", 14)).pack(pady=20)
tk.Button(root, text="Polski", command=lambda: set_language("PL"), bg="#006666", fg="white", width=15, height=2, font=("Arial", 12)).pack(pady=10)
tk.Button(root, text="English", command=lambda: set_language("EN"), bg="#006666", fg="white", width=15, height=2, font=("Arial", 12)).pack(pady=10)
root.mainloop()


# Tworzenie głównego okna
app = tk.Tk()
app.title(translate("Password Generator"))
center_window(app, 800, 600)
app.configure(bg="#008B8B")

menu_bar = tk.Menu(app)

file_menu = tk.Menu(menu_bar, tearoff=0)
file_menu.add_command(label=translate("Save as TXT"), command=lambda: save_to_file("txt"))
file_menu.add_command(label=translate("Save as CSV"), command=lambda: save_to_file("csv"))
file_menu.add_command(label=translate("Save as XLSX"), command=lambda: save_to_file("xlsx"))
file_menu.add_separator()
file_menu.add_command(label=translate("Close"), command=app.quit)
menu_bar.add_cascade(label=translate("File"), menu=file_menu)

info_menu = tk.Menu(menu_bar, tearoff=0)
info_menu.add_command(label=translate("About"), command=about_program)
menu_bar.add_cascade(label=translate("Info"), menu=info_menu)

app.config(menu=menu_bar)

frame = tk.Frame(app, bg="#008B8B")
frame.pack(pady=10)

label_length = tk.Label(frame, text=translate("Password Length:"), bg="#008B8B", fg="white")
label_length.pack(side=tk.LEFT, padx=5)

entry_length = tk.Entry(frame, width=5, bg="#008B8B", fg="white", insertbackground="white")
entry_length.pack(side=tk.LEFT, padx=5)

label_count = tk.Label(frame, text=translate("Number of Passwords:"), bg="#008B8B", fg="white")
label_count.pack(side=tk.LEFT, padx=5)

entry_count = tk.Entry(frame, width=5, bg="#008B8B", fg="white", insertbackground="white")
entry_count.pack(side=tk.LEFT, padx=5)

button_generate = tk.Button(frame, text=translate("Generate"), command=generate_passwords, bg="#006666", fg="white")
button_generate.pack(side=tk.LEFT, padx=5)

button_clear = tk.Button(frame, text=translate("Clear"), command=clear_fields, bg="#696969", fg="white")
button_clear.pack(side=tk.LEFT, padx=5)

generated_info_label = tk.Label(app, text="", bg="#008B8B", fg="white")
generated_info_label.pack(pady=10, padx=10, anchor="w")

text_frame = tk.Frame(app, bg="#008B8B")
text_frame.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)

text_output = tk.Text(text_frame, bg="black", fg="white", insertbackground="white")
text_output.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

scrollbar = tk.Scrollbar(text_frame, command=text_output.yview)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
text_output.config(yscrollcommand=scrollbar.set)

strength_frame = tk.Frame(app, bg="#008B8B")
strength_frame.pack(pady=5, padx=10, fill=tk.X)

strength_label = tk.Label(strength_frame, text=translate("Password strength:"), bg="#008B8B", fg="white")
strength_label.pack(side=tk.LEFT, padx=10)

progress_style = ttk.Style()
progress_style.theme_use('default')

progress_style.configure("WeakPassword.Horizontal.TProgressbar", background='orange', thickness=20)
progress_style.configure("MediumPassword.Horizontal.TProgressbar", background='green yellow', thickness=20)
progress_style.configure("GoodPassword.Horizontal.TProgressbar", background='lime green', thickness=20)
progress_style.configure("StrongPassword.Horizontal.TProgressbar", background='dark green', thickness=20)

progress_bar = ttk.Progressbar(strength_frame, orient="horizontal", length=300, mode="determinate", style="TProgressbar")
progress_bar.pack(side=tk.LEFT, padx=10)

app.mainloop()
