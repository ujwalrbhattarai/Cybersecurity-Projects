import os
import shutil
import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog
import json

UNIVERSAL_KEY = "MasterUnlock123!"  # Universal key for unlocking all folders

# A simple storage file to save info about locked folders and their passwords
DATA_FILE = "folder_lock_data.json"


def load_data():
    if os.path.isfile(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    return {}


def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)


def hide_folder_windows(folder_path):
    """Hide folder in Windows using attrib command."""
    os.system(f'attrib +h "{folder_path}"')


def unhide_folder_windows(folder_path):
    """Unhide folder in Windows using attrib command."""
    os.system(f'attrib -h "{folder_path}"')


def lock_folder(folder_path):
    """Lock folder by hiding it."""
    hide_folder_windows(folder_path)


def unlock_folder(folder_path):
    """Unlock folder by unhiding it."""
    unhide_folder_windows(folder_path)


class FolderLockerApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Folder Locker")
        self.geometry("450x300")
        self.resizable(False, False)

        self.data = load_data()

        self.folder_path = None
        self.danger_location = None

        self.create_widgets()

    def create_widgets(self):
        tk.Label(self, text="Folder Locker", font=("Arial", 20, "bold")).pack(pady=10)

        self.btn_select_folder = tk.Button(self, text="Select Folder to Lock", command=self.select_folder)
        self.btn_select_folder.pack(pady=5)

        self.label_folder = tk.Label(self, text="No folder selected.")
        self.label_folder.pack()

        self.btn_select_danger = tk.Button(self, text="Select Danger Folder (Move location if locked)", command=self.select_danger_folder)
        self.btn_select_danger.pack(pady=5)

        self.label_danger = tk.Label(self, text="No danger location selected.")
        self.label_danger.pack()

        self.btn_lock = tk.Button(self, text="Lock Folder", command=self.lock_folder_action)
        self.btn_lock.pack(pady=5)

        self.btn_unlock = tk.Button(self, text="Unlock Folder", command=self.unlock_folder_action)
        self.btn_unlock.pack(pady=5)

    def select_folder(self):
        folder = filedialog.askdirectory()
        if folder:
            self.folder_path = folder
            self.label_folder.config(text=f"Folder selected: {folder}")

    def select_danger_folder(self):
        location = filedialog.askdirectory()
        if location:
            self.danger_location = location
            self.label_danger.config(text=f"Danger location: {location}")

    def lock_folder_action(self):
        if not self.folder_path:
            messagebox.showerror("Error", "Please select a folder to lock first.")
            return
        if not self.danger_location:
            messagebox.showerror("Error", "Please select a danger location folder first.")
            return

        # Ask the user for password for locking
        password = simpledialog.askstring("Set Password", "Enter password to lock the folder:", show="*")
        if not password:
            messagebox.showerror("Error", "Password cannot be empty.")
            return

        folder_key = self.folder_path.lower()

        if folder_key in self.data:
            messagebox.showerror("Error", "This folder is already locked.")
            return

        # Save the lock info
        self.data[folder_key] = {
            "password": password,
            "danger_location": self.danger_location,
            "wrong_attempts": 0,
            "locked": True,
            "moved": False
        }
        save_data(self.data)

        # Lock the folder by hiding it
        lock_folder(self.folder_path)

        messagebox.showinfo("Success", f"Folder locked successfully!\nDon't forget your password.")

    def unlock_folder_action(self):
        folder = filedialog.askdirectory(title="Select Folder to Unlock")
        if not folder:
            return

        folder_key = folder.lower()

        if folder_key not in self.data:
            messagebox.showerror("Error", "This folder is not locked by this program.")
            return

        folder_info = self.data[folder_key]

        if folder_info["moved"]:
            # Folder moved to danger location, user must use universal key to unlock
            password = simpledialog.askstring("Universal Key Required",
                                              "Folder locked permanently due to 10 wrong attempts.\nEnter Universal Key to unlock:",
                                              show="*")
            if password != UNIVERSAL_KEY:
                messagebox.showerror("Error", "Incorrect universal key. Cannot unlock folder.")
                return

            # Move folder back to original location
            dest = folder_key
            try:
                dest_folder_path = dest
                moved_folder_path = os.path.join(folder_info["danger_location"], os.path.basename(dest))
                shutil.move(moved_folder_path, dest_folder_path)
                self.data[folder_key]["moved"] = False
                self.data[folder_key]["locked"] = False
                self.data[folder_key]["wrong_attempts"] = 0
                save_data(self.data)
                unlock_folder(dest_folder_path)

                messagebox.showinfo("Unlocked", f"Folder has been moved back and unlocked using universal key.")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to move folder back: {e}")

            return

        if not folder_info["locked"]:
            messagebox.showinfo("Info", "Folder is already unlocked.")
            return

        # Ask user for password or universal key
        password = simpledialog.askstring("Password", "Enter password or universal key to unlock:", show="*")
        if not password:
            return

        if password == folder_info["password"] or password == UNIVERSAL_KEY:
            # Correct password, unlock folder
            self.data[folder_key]["locked"] = False
            self.data[folder_key]["wrong_attempts"] = 0
            save_data(self.data)
            unlock_folder(folder)

            messagebox.showinfo("Success", "Folder unlocked successfully!")
        else:
            # Increment wrong attempts
            self.data[folder_key]["wrong_attempts"] += 1
            if self.data[folder_key]["wrong_attempts"] >= 10:
                messagebox.showwarning("Locked Permanently",
                                       "Wrong password entered 10 times! Folder is permanently locked and moved.")
                # Move folder to danger location
                try:
                    dest_path = os.path.join(folder_info["danger_location"], os.path.basename(folder))
                    shutil.move(folder, dest_path)
                    self.data[folder_key]["moved"] = True
                    self.data[folder_key]["locked"] = True
                    save_data(self.data)
                except Exception as e:
                    messagebox.showerror("Error", f"Failed to move folder: {e}")
            else:
                attempts_left = 10 - self.data[folder_key]["wrong_attempts"]
                messagebox.showerror("Incorrect Password",
                                     f"Password is incorrect. {attempts_left} attempts left.")
                save_data(self.data)


if __name__ == "__main__":
    app = FolderLockerApp()
    app.mainloop()
