import tkinter as tk
from tkinter import messagebox
import pyttsx3

#voice
engine = pyttsx3.init()
engine.setProperty("rate",140)

def narrate(text):
    engine.say(text)
    engine.runAndWait()


intersepted =""

root=tk.Tk()
root.title("MITM SIMULATION")
root.geometry("500x400")
root.config(bg="#1e1e1e")

title = tk.Label(root,text="SECURE LOGIN",font=("ARIAL", 16),fg="#1e1e1e",bg="#1e1e1e")
title.pack(pady=10)

status = tk.Label(root,text="connection: choose protocol",font=("Arial",12),fg="#1e1e1e",bg="#1e1e1e")
status.pack(pady=5)

protocol_var= tk.StringVar(value="HTTP")

def set_protocol(value):
    protocol_var.set(value)

    if value=="HTTPS":
        status.config(text="Connection Status: Encrypted (HTTPS)",fg="#1e1e1e")
        narrate("Secure protocol selected")
    else:
        status.config(text="Connected Status: Unsecured protocol selected.")

btn_https=tk.Button(root,text="HTTPS",bg="#1e1e1e",fg="white",command=lambda:set_protocol("HTTPS"))
btn_https.pack(pady=5)
