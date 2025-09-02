import tkinter as tk
from tkinter import scrolledtext

class KeyLoggerDemo:
    def __init__(self, master):
        self.master = master
        master.title("📝 Educational Key Capturer Demo")
        master.geometry("500x300")

        info_label = tk.Label(master, text="Press keys inside this window.\nKeys pressed will appear below.",
                              font=("Arial", 12))
        info_label.pack(pady=10)

        self.text_area = scrolledtext.ScrolledText(master, width=60, height=10, font=("Consolas", 12))
        self.text_area.pack(padx=10, pady=10)
        self.text_area.insert(tk.END, "Start typing...\n")
        self.text_area.config(state='disabled')  # start readonly

        # Bind key press events
        master.bind("<Key>", self.record_key)

    def record_key(self, event):
        # Enable text area temporarily to insert characters
        self.text_area.config(state='normal')

        # Special handling to show printable keys
        if event.keysym == "BackSpace":
            current_text = self.text_area.get("1.0", tk.END)
            if len(current_text) > 1:
                # Delete character before the end newline
                self.text_area.delete(f"{tk.END}-2c")
        elif event.keysym == "Return":
            self.text_area.insert(tk.END, "\n")
        elif len(event.char) == 1:
            self.text_area.insert(tk.END, event.char)
        else:
            # Non-printable keys ignore or you can show names, e.g.
            # self.text_area.insert(tk.END, f"[{event.keysym}]")
            pass

        self.text_area.see(tk.END)  # Scroll to end
        self.text_area.config(state='disabled')  # Make readonly again

if __name__ == "__main__":
    root = tk.Tk()
    app = KeyLoggerDemo(root)
    root.mainloop()
