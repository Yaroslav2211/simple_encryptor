from tkinter import *
from tkinter import ttk
import db
from functions import *
import encryptions
'''
def encrypt_window(con):
    encr_w = Tk()
    encr_w.title("Отправка")
    encr_w.geometry("400x200")
    users_listbox = Listbox(encr_w)
    update_listbox(users_listbox,con,"receivers")
    encr_but = Button(encr_w,text="Зашифровать для получателя", command= lambda: encr_button_handler(users_listbox,con))
    encr_but.pack(anchor=NW)
    del_but = Button(encr_w,text="Удалить",command= lambda: del_button_handler(users_listbox,con))
    del_but.pack(anchor=NW,side="left")
    add_but = Button(encr_w,text="Добавить",command= lambda: create_user_window(users_listbox,con))
    add_but.pack(anchor=NE,side="right")
    users_listbox.pack(fill=X,padx=5, pady=5,side="bottom")
'''
def encrypt_window(con):
    root = tk.Tk()
    root.title("Окно шифрования")
    root.geometry("400x500")

    # Create main frame
    main_frame = tk.Frame(root)
    main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

    # Create title label for the listbox
    title_label = tk.Label(main_frame, text="Выберите пользователя", font=("Arial", 12, "bold"))
    title_label.pack(anchor=tk.W, pady=(0, 5))

    # Create listbox with scrollbar
    listbox_frame = tk.Frame(main_frame)
    listbox_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 10))

    user_listbox = tk.Listbox(listbox_frame)
    user_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    scrollbar = tk.Scrollbar(listbox_frame, orient=tk.VERTICAL, command=user_listbox.yview)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    user_listbox.config(yscrollcommand=scrollbar.set)

'''
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
'''

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

def decrypt_window(con):
    decr_w = Tk()
    decr_w.title("Получение")
    decr_w.geometry("400x200")

def create_user_window():
    """
    Creates and displays a window with three text fields for user credentials.
    
    The window contains:
    - Username field (no auto-generation)
    - Public key field with generation button
    - Private key field with generation button (optional entry)
    """
    root = tk.Tk()
    root.title("Добавление пользователя")
    root.geometry("600x300")

    # Main container frame
    main_frame = tk.Frame(root, padx=20, pady=20)
    main_frame.pack(fill=tk.BOTH, expand=True)

    # Username field
    username_frame = tk.Frame(main_frame)
    username_frame.pack(fill=tk.X, pady=(0, 15))
    
    tk.Label(username_frame, text="Имя пользователя:", font=("Arial", 10, "bold")).pack(anchor=tk.W)
    
    username_entry = tk.Entry(username_frame, font=("Arial", 10))
    username_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))
    username_entry.insert(0, "")  # Placeholder hint in actual use would require additional code

    # Public Key field with generation button
    public_key_frame = tk.Frame(main_frame)
    public_key_frame.pack(fill=tk.X, pady=(0, 15))
    
    tk.Label(public_key_frame, text="Public key:", font=("Arial", 10, "bold")).pack(anchor=tk.W)
    
    public_key_entry = tk.Entry(public_key_frame, font=("Arial", 10))
    public_key_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))
    
    def generate_keys():
        """Generate a random public key string"""
        # Generate a 64-character alphanumeric key as an example
        keys = encryptions.get_keys()
        public_key_entry.delete(0, tk.END)
        public_key_entry.insert(0, keys[0])
        private_key_entry.delete(0, tk.END)
        private_key_entry.insert(0, keys[1])
    
    public_gen_btn = tk.Button(public_key_frame, text="Generate", command=generate_keys)
    public_gen_btn.pack(side=tk.RIGHT)

    # Private Key field with generation button
    private_key_frame = tk.Frame(main_frame)
    private_key_frame.pack(fill=tk.X, pady=(0, 15))
    
    tk.Label(private_key_frame, text="Private key (optional):", font=("Arial", 10, "bold")).pack(anchor=tk.W)
    
    private_key_entry = tk.Entry(private_key_frame, font=("Arial", 10), show="*")  # Hidden by default
    private_key_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))
    
    def toggle_private_visibility():
        """Toggle visibility of private key"""
        if private_key_entry.cget('show') == '*':
            private_key_entry.config(show='')
            visibility_btn.config(text='Hide')
        else:
            private_key_entry.config(show='*')
            visibility_btn.config(text='Show')
    
    # Frame for private key buttons
    private_btn_frame = tk.Frame(private_key_frame)
    private_btn_frame.pack(side=tk.RIGHT)
    
    visibility_btn = tk.Button(private_btn_frame, text="Show", command=toggle_private_visibility)
    visibility_btn.pack(side=tk.LEFT, padx=(0, 5))

    # Submit button at bottom
    submit_btn = tk.Button(main_frame, text="Submit", bg="#4CAF50", fg="white", 
                          font=("Arial", 10, "bold"), height=2,
                          command=lambda: print(f"Submitted:\nUsername: {username_entry.get()}\n"
                                              f"Public Key: {public_key_entry.get()}\n"
                                              f"Private Key: {'*' * len(private_key_entry.get()) if private_key_entry.get() else 'None'}"))
    submit_btn.pack(fill=tk.X, pady=(10, 0))
    return (public_key_entry.get(), private_key_entry.get())
