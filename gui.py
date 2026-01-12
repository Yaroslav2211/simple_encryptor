import tkinter as tk
from tkinter import messagebox, simpledialog

def show_user_manager():
    """
    Creates and displays a window with a user listbox and management buttons.
    
    The window contains:
    - A titled listbox showing users ("Choose user")
    - Three buttons: Add User, Delete User, Encrypt for this user
    """
    root = tk.Tk()
    root.title("User Manager")
    root.geometry("400x500")

    # Create main frame
    main_frame = tk.Frame(root)
    main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

    # Create title label for the listbox
    title_label = tk.Label(main_frame, text="Choose user", font=("Arial", 12, "bold"))
    title_label.pack(anchor=tk.W, pady=(0, 5))

    # Create listbox with scrollbar
    listbox_frame = tk.Frame(main_frame)
    listbox_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 10))

    user_listbox = tk.Listbox(listbox_frame)
    user_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    scrollbar = tk.Scrollbar(listbox_frame, orient=tk.VERTICAL, command=user_listbox.yview)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    user_listbox.config(yscrollcommand=scrollbar.set)

    def add_user():
        """Callback to add a new user via dialog input"""
        new_user = simpledialog.askstring("Add User", "Enter username:")
        if new_user:
            if new_user.strip():
                user_listbox.insert(tk.END, new_user.strip())
            else:
                messagebox.showwarning("Invalid Input", "Username cannot be empty.")
        else:
            # User cancelled the dialog
            pass

    def delete_user():
        """Callback to delete selected user from listbox"""
        selection = user_listbox.curselection()
        if selection:
            user_listbox.delete(selection[0])
        else:
            messagebox.showwarning("No Selection", "Please select a user to delete.")

    def encrypt_for_user():
        """Callback to handle encryption action for selected user"""
        selection = user_listbox.curselection()
        if selection:
            selected_user = user_listbox.get(selection[0])
            messagebox.showinfo(
                "Encryption", 
                f"Encrypting data for user: {selected_user}\n(Placeholder for encryption logic)"
            )
        else:
            messagebox.showwarning("No Selection", "Please select a user first.")

    # Create button frame
    button_frame = tk.Frame(main_frame)
    button_frame.pack(fill=tk.X)

    # Create and pack buttons
    add_button = tk.Button(button_frame, text="Add user", command=add_user)
    add_button.pack(side=tk.LEFT, padx=(0, 5), fill=tk.X, expand=True)

    delete_button = tk.Button(button_frame, text="Delete user", command=delete_user)
    delete_button.pack(side=tk.LEFT, padx=(0, 5), fill=tk.X, expand=True)

    encrypt_button = tk.Button(button_frame, text="Зашифровать для пользователя", command=encrypt_for_user)
    encrypt_button.pack(side=tk.LEFT, fill=tk.X, expand=True)



# Example usage:
show_user_manager()