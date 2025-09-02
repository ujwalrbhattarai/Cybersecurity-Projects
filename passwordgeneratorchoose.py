import tkinter as tk
from tkinter import ttk, messagebox
import random
import string

class PasswordGeneratorApp:
    def __init__(self, master):
        self.master = master
        master.title("🔐 Strong Password Generator")
        master.geometry("600x600")
        master.resizable(False, False)

        # Title label
        ttk.Label(master, text="Strong Password Generator", font=("Arial", 16, "bold")).pack(pady=10)

        # Password length selection
        length_frame = ttk.Frame(master)
        length_frame.pack(pady=8, fill=tk.X, padx=20)
        ttk.Label(length_frame, text="Password Length:", font=("Arial", 12)).pack(side=tk.LEFT)
        self.length_var = tk.IntVar(value=16)
        self.length_spinbox = ttk.Spinbox(length_frame, from_=8, to=32, textvariable=self.length_var, width=5, font=("Arial", 12))
        self.length_spinbox.pack(side=tk.RIGHT)

        # Character options
        options_frame = ttk.LabelFrame(master, text="Include Characters", padding=(15,10))
        options_frame.pack(fill=tk.X, padx=20, pady=10)

        self.use_uppercase = tk.BooleanVar(value=True)
        self.use_lowercase = tk.BooleanVar(value=True)
        self.use_digits = tk.BooleanVar(value=True)
        self.use_special = tk.BooleanVar(value=True)

        ttk.Checkbutton(options_frame, text="Uppercase (A-Z)", variable=self.use_uppercase).pack(anchor=tk.W)
        ttk.Checkbutton(options_frame, text="Lowercase (a-z)", variable=self.use_lowercase).pack(anchor=tk.W)
        ttk.Checkbutton(options_frame, text="Digits (0-9)", variable=self.use_digits).pack(anchor=tk.W)
        ttk.Checkbutton(options_frame, text="Special (!@#$%&*)", variable=self.use_special).pack(anchor=tk.W)

        # Generate button
        self.generate_btn = ttk.Button(master, text="Generate Password", command=self.generate_password)
        self.generate_btn.pack(pady=15)

        # Password display (readonly entry)
        self.password_var = tk.StringVar()
        self.password_entry = ttk.Entry(master, textvariable=self.password_var, font=("Arial", 14), justify="center", state="readonly")
        self.password_entry.pack(fill=tk.X, padx=20, pady=(0,20))

    def generate_password(self):
        length = self.length_var.get()

        if length < 8 or length > 32:
            messagebox.showerror("Invalid Length", "Password length must be between 8 and 32.")
            return

        char_sets = []
        if self.use_uppercase.get():
            char_sets.append(string.ascii_uppercase)
        if self.use_lowercase.get():
            char_sets.append(string.ascii_lowercase)
        if self.use_digits.get():
            char_sets.append(string.digits)
        if self.use_special.get():
            char_sets.append("!@#$%&*?")

        if not char_sets:
            messagebox.showerror("No Character Sets Selected", "Please select at least one character type.")
            return

        # Guarantee at least 1 char from each selected set for strong password
        password_chars = [random.choice(cs) for cs in char_sets]

        all_chars = ''.join(char_sets)
        remaining_length = length - len(password_chars)

        if remaining_length > 0:
            password_chars += random.choices(all_chars, k=remaining_length)

        random.shuffle(password_chars)
        password = ''.join(password_chars)

        self.password_var.set(password)


if __name__ == "__main__":
    root = tk.Tk()
    style = ttk.Style(root)
    # Use a clean theme; adjust if needed
    style.theme_use('clam')
    app = PasswordGeneratorApp(root)
    root.mainloop()
