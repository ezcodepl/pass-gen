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


def generate_passwords():
    length = entry_length.get().strip()
    count = entry_count.get().strip()

    if not length:
        messagebox.showerror("Błąd", "Wprowadź długość hasła.")
        return
    if not count:
        messagebox.showerror("Błąd", "Wprowadź ilość haseł do wygenerowania.")
        return

    try:
        length = int(length)
        count = int(count)

        if length < 8:
            messagebox.showerror("Błąd", "Hasło musi mieć co najmniej 8 znaków.")
            return

        passwords = []
        for i in range(count):
            while True:
                password = ''.join(random.choices(DEFAULT_CHARACTERS, k=length))

                # Sprawdź, czy hasło spełnia warunki
                digit_count = sum(c.isdigit() for c in password)
                lower_count = sum(c.islower() for c in password)
                upper_count = sum(c.isupper() for c in password)
                special_count = sum(c in "~!@#%^&*()_+=\\-;,./<>?[]{}" for c in password)

                if (digit_count >= 2 and
                        lower_count >= 1 and
                        upper_count >= 1 and
                        special_count >= 2):
                    passwords.append(f"{i + 1}. {password}")
                    break

        text_output.delete("1.0", tk.END)
        text_output.insert(tk.END, "\n".join(passwords))

        # Aktualizacja paska siły hasła
        update_strength_indicator(length)

        # Aktualizacja informacji o wygenerowanych hasłach
        generated_info_label.config(
            text=f"Wygenerowano listę haseł: {count}")

    except ValueError:
        messagebox.showerror("Błąd", "Wprowadź poprawną liczbę znaków.")


def update_strength_indicator(length):
    strength = ""

    if length >= 8 and length < 15:
        strength = "Hasło średnie"
        progress_bar.config(value=33, style="MediumPassword.Horizontal.TProgressbar")
    elif length >= 15 and length <= 20:
        strength = "Hasło dobre"
        progress_bar.config(value=66, style="GoodPassword.Horizontal.TProgressbar")
    elif length > 20:
        strength = "Bardzo mocne hasło"
        progress_bar.config(value=100, style="StrongPassword.Horizontal.TProgressbar")
    else:
        strength = "Zbyt krótkie hasło"
        progress_bar.config(value=0, style="WeakPassword.Horizontal.TProgressbar")

    strength_label.config(text=f"Siła hasła: {strength}")


def save_to_file(file_type):
    passwords = text_output.get("1.0", tk.END).strip().split("\n")
    if not passwords or passwords == ['']:
        messagebox.showerror("Błąd", "Brak wygenerowanych haseł do zapisania.")
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


def about_program():
    messagebox.showinfo("O programie", "Generator Haseł\nAutor: Ernest Zając\nWersja: 1.0\nStrona: https://www.ezcode.pl")


def clear_fields():
    entry_length.delete(0, tk.END)
    entry_count.delete(0, tk.END)
    text_output.delete("1.0", tk.END)
    generated_info_label.config(text="")

    # Wyczyszczenie paska postępu
    progress_bar.config(value=0, style="TProgressbar")


# Tworzenie głównego okna
app = tk.Tk()
app.title("Generator Haseł")
app.geometry("800x600")
app.configure(bg="#008B8B")

# Tworzenie górnego menu
menu_bar = tk.Menu(app)

# Menu Plik
file_menu = tk.Menu(menu_bar, tearoff=0)
file_menu.add_command(label="Zapisz jako TXT", command=lambda: save_to_file("txt"))
file_menu.add_command(label="Zapisz jako CSV", command=lambda: save_to_file("csv"))
file_menu.add_command(label="Zapisz jako XLSX", command=lambda: save_to_file("xlsx"))
file_menu.add_separator()
file_menu.add_command(label="Zamknij", command=app.quit)
menu_bar.add_cascade(label="Plik", menu=file_menu)

# Menu Info
info_menu = tk.Menu(menu_bar, tearoff=0)
info_menu.add_command(label="O programie", command=about_program)
menu_bar.add_cascade(label="Info", menu=info_menu)

# Ustawienie menu górnego
app.config(menu=menu_bar)

# Tworzenie reszty interfejsu użytkownika
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

button_generate = tk.Button(frame, text="Generuj", command=generate_passwords, bg="#006666", fg="white")
button_generate.pack(side=tk.LEFT, padx=5)

button_clear = tk.Button(frame, text="Wyczyść", command=clear_fields, bg="#696969", fg="white")
button_clear.pack(side=tk.LEFT, padx=5)


# Tekst informujący o wygenerowanych hasłach
generated_info_label = tk.Label(app, text="", bg="#008B8B", fg="white")
generated_info_label.pack(pady=10, padx=10, anchor="w")

# Dodanie pola tekstowego z paskiem przewijania
text_frame = tk.Frame(app, bg="#008B8B")
text_frame.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)

text_output = tk.Text(text_frame, bg="black", fg="white", insertbackground="white")
text_output.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

scrollbar = tk.Scrollbar(text_frame, command=text_output.yview)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
text_output.config(yscrollcommand=scrollbar.set)

# Pasek siły hasła
strength_frame = tk.Frame(app, bg="#008B8B")
strength_frame.pack(pady=5, padx=10, fill=tk.X)

strength_label = tk.Label(strength_frame, text="Siła hasła:", bg="#008B8B", fg="white")
strength_label.pack(side=tk.LEFT, padx=10)

progress_style = ttk.Style()
progress_style.theme_use('default')

# Konfiguracja stylów paska postępu siły hasła
progress_style.configure("WeakPassword.Horizontal.TProgressbar", background='orange', thickness=20)
progress_style.configure("MediumPassword.Horizontal.TProgressbar", background='green yellow', thickness=20)
progress_style.configure("GoodPassword.Horizontal.TProgressbar", background='lime green', thickness=20)
progress_style.configure("StrongPassword.Horizontal.TProgressbar", background='dark green', thickness=20)

progress_bar = ttk.Progressbar(strength_frame, orient="horizontal", length=300, mode="determinate",
                               style="TProgressbar")
progress_bar.pack(side=tk.LEFT, padx=10)

# Główna pętla programu
app.mainloop()
