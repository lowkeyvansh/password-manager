import tkinter as tk
from tkinter import messagebox
import json
from cryptography.fernet import Fernet
import os

# Generate a key for encryption and decryption
# This is a one-time operation
def generate_key():
    key = Fernet.generate_key()
    with open("secret.key", "wb") as key_file:
        key_file.write(key)

def load_key():
    return open("secret.key", "rb").read()

# Generate the key
if not os.path.exists("secret.key"):
    generate_key()

key = load_key()
cipher_suite = Fernet(key)

def setup_window():
    root = tk.Tk()
    root.title("Password Manager")
    root.geometry("400x400")
    return root

def create_input_fields(root):
    tk.Label(root, text="Website:").pack(pady=5)
    website_entry = tk.Entry(root, width=40)
    website_entry.pack(pady=5)

    tk.Label(root, text="Username:").pack(pady=5)
    username_entry = tk.Entry(root, width=40)
    username_entry.pack(pady=5)

    tk.Label(root, text="Password:").pack(pady=5)
    password_entry = tk.Entry(root, width=40)
    password_entry.pack(pady=5)

    return website_entry, username_entry, password_entry

def create_buttons(root, save_password, retrieve_password):
    save_button = tk.Button(root, text="Save Password", command=save_password)
    save_button.pack(pady=10)

    retrieve_button = tk.Button(root, text="Retrieve Password", command=retrieve_password)
    retrieve_button.pack(pady=10)

    return save_button, retrieve_button

def save_password(website_entry, username_entry, password_entry):
    website = website_entry.get().strip()
    username = username_entry.get().strip()
    password = password_entry.get().strip()

    if website and username and password:
        encrypted_password = cipher_suite.encrypt(password.encode()).decode()
        data = {
            "website": website,
            "username": username,
            "password": encrypted_password
        }
        if os.path.exists("passwords.json"):
            with open("passwords.json", "r") as file:
                passwords = json.load(file)
        else:
            passwords = []

        passwords.append(data)

        with open("passwords.json", "w") as file:
            json.dump(passwords, file, indent=4)

        website_entry.delete(0, tk.END)
        username_entry.delete(0, tk.END)
        password_entry.delete(0, tk.END)
        messagebox.showinfo("Success", "Password saved successfully!")
    else:
        messagebox.showwarning("Warning", "Please fill in all fields.")

def retrieve_password():
    def show_password():
        website = website_search_entry.get().strip()
        if os.path.exists("passwords.json"):
            with open("passwords.json", "r") as file:
                passwords = json.load(file)
                for entry in passwords:
                    if entry["website"] == website:
                        decrypted_password = cipher_suite.decrypt(entry["password"].encode()).decode()
                        messagebox.showinfo("Password Found", f"Website: {entry['website']}\nUsername: {entry['username']}\nPassword: {decrypted_password}")
                        return
                messagebox.showwarning("Warning", "No password found for the specified website.")
        else:
            messagebox.showwarning("Warning", "No saved passwords found.")

    search_window = tk.Toplevel()
    search_window.title("Retrieve Password")
    search_window.geometry("300x200")
    tk.Label(search_window, text="Enter Website:").pack(pady=5)
    website_search_entry = tk.Entry(search_window, width=30)
    website_search_entry.pack(pady=5)
    tk.Button(search_window, text="Search", command=show_password).pack(pady=10)

def main():
    root = setup_window()

    website_entry, username_entry, password_entry = create_input_fields(root)
    save_button, retrieve_button = create_buttons(
        root,
        lambda: save_password(website_entry, username_entry, password_entry),
        retrieve_password
    )

    root.mainloop()

if __name__ == "__main__":
    main()
