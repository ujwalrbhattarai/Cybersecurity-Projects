import tkinter as tk
from tkinter import messagebox, filedialog
import pikepdf
import os

class PDFlocker:

    def __init__(self,root):
        
        self.root = root
        self.root.title("PDF Locker")
        self.root.geometry("400x220")
        self.root.resizable(False, False)

        tk.Label(root, text = "PDF Locker",font=("",14,"bold"))
        self.select_btn=tk.Button(root, text="select PDF",command=self.select_pdf)
        self.select_btn.pack(pady=10)
        self.file_label = tk.Label(root,text="no file selected",fg="red")
        self.file_label.pack()
        self.password_entry = tk.Entry(root,show="*",width=30)
        self.password_entry.pack()
        self.lock_btn =tk.Button(root,text="lock PDF",command=self.lock_PDF)
        self.lock_btn.pack()
        self.file_path= None

    def select_pdf(self):
        file_path= filedialog.askopenfilename(
            title=("Select the PDF file"),
            filetypes=[("PDF Files","*.pdf")]
        )
        if file_path:
            self.file_path=file_path
            self.file_label.config(text=os.path.basename(file_path), fg = "green")
        else:
            self.file_label.config(text="No Files selected",fg="red")

    def lock_PDF(self):
        if not self.file_path:
            messagebox.showerror("Error","Please select a file")
            return
        
        password=self.password_entry.get()

        if not password:
            messagebox.showerror("Error","Please Enter a password")
            return
        
        save_path=filedialog.asksaveasfilename(
            title="Save PDF as:",
            defaultextension =".pdf",
            filetypes=["PDF Files","*.pdf"]
        )

        if not save_path:
            messagebox.showerror("Error","Please select a PDF file")
            return
        try:
            pdf=pikepdf.open(self.file_path)
            pdf.save(save_path,encaptulation=pikepdf(owner=password,user=password,R=6))
            messagebox.showinfo("Success","PDF Locked")
        except Exception as e:
            messagebox.showerror("Error",f"PDF couldnt be locked for {str(e)}")

def main():
    root = tk.Tk()
    app = PDFlocker(root)
    root.mainloop()

if __name__ == "__main__" :
    main()


