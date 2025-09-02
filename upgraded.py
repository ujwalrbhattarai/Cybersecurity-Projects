import tkinter as tk
from tkinter import messagebox, ttk
import pyttsx3

# ------------------------
# Voice Narration Setup
# ------------------------
engine = pyttsx3.init()
engine.setProperty("rate", 140)

def narrate(text):
    engine.say(text)
    engine.runAndWait()

# ------------------------
# Quiz Questions Data
# ------------------------
quiz_qs = [
    {
        "question": "Which protocol ensures encrypted data transmission?",
        "options": ["HTTP", "HTTPS", "FTP", "SMTP"],
        "answer": 1
    },
    {
        "question": "What type of attack is shown when credentials are intercepted between you and a website?",
        "options": ["DDoS", "MITM", "Phishing", "Ransomware"],
        "answer": 1
    },
    {
        "question": "What does HTTPS stand for?",
        "options": ["HyperText Transfer Service", "HyperText Transfer Protocol Secure", "High Transfer Secure Protocol", "Hyper Secure Text Protocol"],
        "answer": 1
    },
    {
        "question": "Which of these is NOT a feature of HTTPS?",
        "options": ["Encryption", "Authentication", "Data Integrity", "Unlimited Bandwidth"],
        "answer": 3
    },
    {
        "question": "To stay safe from MITM attacks, what should users do?",
        "options": ["Always use public Wi-Fi", "Share passwords openly", "Rely on HTTP", "Use only HTTPS sites, especially on public networks"],
        "answer": 3
    }
]

# ------------------------
# Quiz Dialog Class
# ------------------------
class QuizDialog(tk.Toplevel):
    def __init__(self, master):
        super().__init__(master)
        self.title("Cybersecurity Awareness Quiz")
        self.config(bg="#233b4e")
        self.geometry("600x600")
        self.resizable(True, True)

        self.vars = [tk.IntVar(value=-1) for _ in quiz_qs]

        lbl_header = tk.Label(self, text="Select the correct option for each question:",
                              font=("Arial", 13, "bold"), fg="#e1e7f5", bg="#31526a", pady=10)
        lbl_header.pack(fill=tk.X, pady=(0, 8))

        container = tk.Frame(self, bg="#233b4e")
        container.pack(fill=tk.BOTH, expand=True)

        canvas = tk.Canvas(container, bg="#233b4e", highlightthickness=0)
        scrollbar = ttk.Scrollbar(container, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg="#233b4e")

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Add questions and radio button answers
        for i, q in enumerate(quiz_qs):
            q_lbl = tk.Label(scrollable_frame, text=f"{i + 1}) {q['question']}",
                             font=("Arial", 11), fg="#c1f4fa", bg="#233b4e",
                             wraplength=550, justify="left", anchor="w")
            q_lbl.grid(row=6 * i, column=0, sticky="w", pady=(7 if i == 0 else 12, 2))

            for j, option in enumerate(q['options']):
                r_btn = tk.Radiobutton(scrollable_frame, text=option, variable=self.vars[i], value=j,
                                       font=("Arial", 10), fg="#e7ecef", bg="#233b4e",
                                       activebackground="#335a8a", selectcolor="#3e8f94", anchor="w")
                r_btn.grid(row=6 * i + j + 1, column=0, sticky="w")

        submit_btn = tk.Button(self, text="Submit Answers", bg="#11c160", fg="white",
                               font=("Arial", 12), width=16, command=self.evaluate)
        submit_btn.pack(pady=12)

    def evaluate(self):
        unanswered = [i+1 for i, v in enumerate(self.vars) if v.get() == -1]
        if unanswered:
            messagebox.showwarning("Incomplete", f"Please answer all questions. Questions missing: {unanswered}")
            return

        score = sum(1 for i, q in enumerate(quiz_qs) if self.vars[i].get() == q['answer'])
        narrate(f"You scored {score} out of {len(quiz_qs)} on the awareness quiz.")

        if score >= 4:
            msg = f"Excellent! You scored {score}/{len(quiz_qs)}.\nWell protected against cyber threats."
        elif score >= 2:
            msg = f"You scored {score}/{len(quiz_qs)}.\nConsider revising best practices."
        else:
            msg = f"Low score: {score}/{len(quiz_qs)}.\nRead more to secure your data!"

        messagebox.showinfo("Quiz Result", msg)
        self.destroy()

# ------------------------
# MITM Attack Simulation Main App
# ------------------------
class MITMSimulationApp:
    def __init__(self, master):
        self.master = master
        self.master.title("MITM Attack Simulation")
        self.master.geometry("560x520")
        self.master.config(bg="#203843")
        self.intercepted = ""

        # Title
        self.title_lbl = tk.Label(master, text="🌐 Secure Portal Login",
                                  font=("Arial Rounded MT Bold", 18),
                                  fg="#91e3dd", bg="#294352", pady=10)
        self.title_lbl.pack(fill=tk.X)

        # Status Label
        self.status = tk.Label(master, text="Connection Status: Choose Protocol",
                               font=("Arial", 12), fg="#11c160", bg="#294352", pady=5)
        self.status.pack(fill=tk.X, pady=5)

        # Protocol toggle frame
        toggle_frame = tk.Frame(master, bg="#203843")
        toggle_frame.pack(pady=5)

        self.protocol_var = tk.StringVar(value="HTTP")

        btn_http = tk.Button(toggle_frame, text="☠ Use HTTP", bg="#ee5253", fg="white",
                             activebackground="#fe7e74", command=lambda: self.set_protocol("HTTP"), width=14)
        btn_http.pack(side=tk.LEFT, padx=10)

        btn_https = tk.Button(toggle_frame, text="✅ Use HTTPS", bg="#30a3e2", fg="white",
                              activebackground="#69c8fa", command=lambda: self.set_protocol("HTTPS"), width=14)
        btn_https.pack(side=tk.LEFT)

        # Login Frame
        frame = tk.Frame(master, bg="#203843")
        frame.pack(pady=20)

        tk.Label(frame, text="Username:", font=("Arial", 12), fg="#f6f1f1", bg="#203843").grid(row=0, column=0, sticky=tk.E, pady=4)
        self.username_entry = tk.Entry(frame, width=32, font=("Arial", 11))
        self.username_entry.grid(row=0, column=1, padx=12, pady=4)

        tk.Label(frame, text="Password:", font=("Arial", 12), fg="#f6f1f1", bg="#203843").grid(row=1, column=0, sticky=tk.E, pady=4)
        self.password_entry = tk.Entry(frame, show="*", width=32, font=("Arial", 11))
        self.password_entry.grid(row=1, column=1, padx=12, pady=4)

        # Login button
        btn_login = tk.Button(master, text="🔐 Login", font=("Arial", 12), bg="#b195fc",
                              fg="#222", command=self.simulate_login)
        btn_login.pack(pady=10)

        # Take Quiz button
        btn_quiz = tk.Button(master, text="📘 Take Quiz", bg="#4267b2", fg="white",
                             font=("Arial", 12), command=self.launch_quiz)
        btn_quiz.pack(pady=14)

    def set_protocol(self, protocol):
        self.protocol_var.set(protocol)
        if protocol == "HTTPS":
            self.status.config(text="Connection Status: Encrypted (HTTPS)", fg="#00dbaa")
            narrate("Secure encrypted protocol selected.")
        else:
            self.status.config(text="Connection Status: Unsecured (HTTP)", fg="#f75f43")
            narrate("Unsecured protocol selected. Data is vulnerable.")

    def simulate_login(self):
        user = self.username_entry.get()
        pwd = self.password_entry.get()
        if self.protocol_var.get() == "HTTP":
            self.intercepted = f"🛑 Attacker Intercepted: Username={user}, Password={pwd}"
            self.status.config(text="MITM ALERT: Credentials Sniffed!", fg="#ee5253")
            narrate("Man in the middle attack triggered. Credentials have been intercepted.")
            messagebox.showwarning("Interception", self.intercepted)
        else:
            self.status.config(text="Secure Login - Data Encrypted", fg="#8efcb1")
            narrate("Encrypted connection. Credentials safely transmitted.")
            messagebox.showinfo("Success", "✅ Logged in securely using HTTPS.")

    def launch_quiz(self):
        narrate("Launching awareness quiz. Please select your answers and submit.")
        QuizDialog(self.master)

# ------------------------
# Main program start
# ------------------------
if __name__ == "__main__":
    root = tk.Tk()
    app = MITMSimulationApp(root)
    root.mainloop()
