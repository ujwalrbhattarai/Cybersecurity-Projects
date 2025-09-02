import tkinter as tk
from tkinter import messagebox
import pyttsx3

# 🔊 Voice Narration Setup
engine = pyttsx3.init()
engine.setProperty("rate", 140)#change

def narrate(text):
    engine.say(text)
    engine.runAndWait()

# 🪪 Credentials Storage
intercepted = ""

# 🖼 GUI Setup
root = tk.Tk()
root.title("MITM Attack Simulation")
root.geometry("500x400")
root.config(bg="#ff0000")

title = tk.Label(root, text="🌐 Secure Portal Login", font=("Arial", 16), fg="#00ffcc", bg="#1e1e1e")#change
title.pack(pady=10)#change

status = tk.Label(root, text="Connection Status: Choose Protocol", font=("Arial", 12), fg="lightgreen", bg="#1e1e1e")
status.pack(pady=5)

# 🔒 Protocol Toggle
protocol_var = tk.StringVar(value="HTTP")

def set_protocol(value):
    protocol_var.set(value)
    if value == "HTTPS":
        status.config(text="Connection Status: Encrypted (HTTPS)", fg="#339966")
        narrate("Secure encrypted protocol selected.")
    else:
        status.config(text="Connection Status: Unsecured (HTTP)", fg="red")
        narrate("Unsecured protocol selected. Data is vulnerable.")

btn_http = tk.Button(root, text="☠ Use HTTP", bg="#ff3333", fg="white", command=lambda: set_protocol("HTTP"))
btn_http.pack(pady=5)

btn_https = tk.Button(root, text="✅ Use HTTPS", bg="#3399ff", fg="white", command=lambda: set_protocol("HTTPS"))
btn_https.pack(pady=5)

# 🧾 Login Fields
frame = tk.Frame(root, bg="#1e1e1e")
frame.pack(pady=15)

tk.Label(frame, text="Username:", font=("Arial", 12), fg="white", bg="#1e1e1e").grid(row=0, column=0)#change
username_entry = tk.Entry(frame, width=30)
username_entry.grid(row=0, column=1)

tk.Label(frame, text="Password:", font=("Arial", 12), fg="white", bg="#1e1e1e").grid(row=1, column=0)
password_entry = tk.Entry(frame, show="*", width=30)
password_entry.grid(row=1, column=1)

# 🔍 Simulation Trigger
def simulate_login():
    global intercepted
    user = username_entry.get()
    pwd = password_entry.get()

    if protocol_var.get() == "HTTP":
        intercepted = f"🛑 Attacker Intercepted: Username={user}, Password={pwd}"
        status.config(text="MITM ALERT: Credentials Sniffed!", fg="red")
        narrate("Man in the middle attack triggered. Credentials have been intercepted.")
        messagebox.showwarning("Interception", intercepted)
    else:
        status.config(text="Secure Login - Data Encrypted", fg="#33ffcc")
        narrate("Encrypted connection. Credentials safely transmitted.")
        messagebox.showinfo("Success", "✅ Logged in securely using HTTPS.")

btn_login = tk.Button(root, text="🔐 Login", font=("Arial", 12), bg="#ffcc00", command=simulate_login)
btn_login.pack(pady=10)

# 📘 Quiz Trigger
def launch_quiz():
    narrate("Launching awareness quiz. Choose the correct option.")
    q1 = messagebox.askquestion("Quiz",
        "Which protocol ensures encrypted data transmission?\nA. HTTP\nB. HTTPS")

    if q1 == "yes":
        messagebox.showinfo("Result", "✅ Correct! HTTPS encrypts your data.")
        narrate("Correct choice. HTTPS protects against man-in-the-middle attacks.")
    else:
        messagebox.showinfo("Result", "❌ Incorrect. HTTP does not provide encryption.")
        narrate("Incorrect answer. HTTP is unsafe on public networks.")

btn_quiz = tk.Button(root, text="📘 Take Quiz", bg="#006699", fg="white", font=("Arial", 11), command=launch_quiz)
btn_quiz.pack(pady=10)

root.mainloop()