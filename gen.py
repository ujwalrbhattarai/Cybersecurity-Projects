import tkinter as tk
from tkinter import ttk
import random
import string
class PasswordGeneratorApp:
    def __init__(self, master):
        self.master = master
        master.title("🔐 Strong Password Generator")
        master.geometry("420x180")
        master.resizable(False, False)
        ttk.Label(master, text="Strong Password Generator", font=("Arial", 16, "bold")).pack(pady=10)
        ttk.Label(master, text="Generated Password:", font=("Arial", 12)).pack(pady=(10, 0))
        self.password_var = tk.StringVar()
        self.password_entry = ttk.Entry(master, textvariable=self.password_var, font=("Arial", 14), justify="center", state="readonly")
        self.password_entry.pack(fill=tk.X, padx=20, pady=10)
        # Generate the password once at startup
        self.generate_password()
    def generate_password(self):
        length = 16
        char_sets = [
            string.ascii_uppercase,
            string.ascii_lowercase,
            string.digits,
            "!@#$%&*?"
        ]
        # Ensure at least one character from each set
        password_chars = [random.choice(chars) for chars in char_sets]

        all_chars = "".join(char_sets)
        remaining_length = length - len(password_chars)
        password_chars += random.choices(all_chars, k=remaining_length)

        random.shuffle(password_chars)
        password = ''.join(password_chars)

        self.password_var.set(password)
if __name__ == "__main__":
    root = tk.Tk()
    style = ttk.Style(root)
    style.theme_use('clam')
    app = PasswordGeneratorApp(root)
    root.mainloop()
