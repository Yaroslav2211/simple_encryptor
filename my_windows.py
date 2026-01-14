from tkinter import *
from tkinter import ttk
import db
from functions import *
import encryptions

def encrypt_window(con):
    root = Tk()
    root.title("Окно шифрования")
    root.geometry("600x500")

    # Create main frame
    main_frame = Frame(root)
    main_frame.pack(fill=BOTH, expand=True, padx=10, pady=10)

    # Create title label for the listbox
    title_label = Label(main_frame, text="Выберите пользователя", font=("Arial", 12, "bold"))
    title_label.pack(anchor=W, pady=(0, 5))

    # Create listbox with scrollbar
    listbox_frame = Frame(main_frame)
    listbox_frame.pack(fill=BOTH, expand=True, pady=(0, 10))

    user_listbox = Listbox(listbox_frame)
    user_listbox.pack(side=LEFT, fill=BOTH, expand=True)
    update_listbox(user_listbox,con,"receivers")

    scrollbar = Scrollbar(listbox_frame, orient=VERTICAL, command=user_listbox.yview)
    scrollbar.pack(side=RIGHT, fill=Y)
    user_listbox.config(yscrollcommand=scrollbar.set)

    def delete_user():
        """Callback to delete selected user from listbox"""
        selection = user_listbox.curselection()
        if selection:
            username = user_listbox.get(selection)
            db.del_user(con,username,"receivers")
            update_listbox(user_listbox,con,"receivers")
            print("deleted")
        else:
            show_toast("Сначала выберите пользователя!")

    def encrypt_for_user(mode="encrypt"):
        """Callback to handle encryption action for selected user"""
        selection = user_listbox.curselection()
        if selection:
            username = user_listbox.get(selection[0])
            show_encryption_dialog(username,con,root,mode)
        else:
            show_toast("Сначала выберите пользователя!")

    # Create button frame
    button_frame = Frame(main_frame)
    button_frame.pack(fill=X)

    # Create and pack buttons
    add_button = Button(button_frame, text="Add user", command=lambda: add_user(con,user_listbox))
    add_button.pack(side=LEFT, padx=(0, 5), fill=X, expand=True)

    delete_button = Button(button_frame, text="Delete user", command=delete_user)
    delete_button.pack(side=LEFT, padx=(0, 5), fill=X, expand=True)

    encrypt_button = Button(button_frame, text="Зашифровать для пользователя", command=encrypt_for_user)
    encrypt_button.pack(side=LEFT, padx=(0, 5), fill=X, expand=True)

    decrypt_button = Button(button_frame, text="Расшифровать от пользователя", command=lambda: encrypt_for_user("decrypt"))
    decrypt_button.pack(side=LEFT,fill=X, expand=True)

    root.mainloop()

def add_user(con, user_listbox):
    """
    Creates and displays a window with three text fields for user credentials.
    
    The window contains:
    - Username field (no auto-generation)
    - Public key field with generation button
    - Private key field with generation button (optional entry)
    """
    root = Tk()
    root.title("Добавление пользователя")
    root.geometry("600x300")

    # Main container frame
    main_frame = Frame(root, padx=20, pady=20)
    main_frame.pack(fill=BOTH, expand=True)

    # Username field
    username_frame = Frame(main_frame)
    username_frame.pack(fill=X, pady=(0, 15))
    
    Label(username_frame, text="Имя пользователя:", font=("Arial", 10, "bold")).pack(anchor=W)
    
    username_entry = Entry(username_frame, font=("Arial", 10))
    username_entry.pack(side=LEFT, fill=X, expand=True, padx=(0, 10))
    username_entry.insert(0, "")  # Placeholder hint in actual use would require additional code

    # Public Key field with generation button
    public_key_frame = Frame(main_frame)
    public_key_frame.pack(fill=X, pady=(0, 15))
    
    Label(public_key_frame, text="Public key:", font=("Arial", 10, "bold")).pack(anchor=W)
    
    public_key_entry = Entry(public_key_frame, font=("Arial", 10))
    public_key_entry.pack(side=LEFT, fill=X, expand=True, padx=(0, 10))
    
    def derive():
        """Generate a random public key string"""
        # Generate a 64-character alphanumeric key as an example
        privkey = private_key_entry.get()
        if len(privkey) > 10 and "AGE-SECRET-KEY-" in privkey:
            public_key_entry.delete(0, END)
            public_key_entry.insert(0, encryptions.derive_publikey(privkey))
        else:
            show_toast("Неправильный ключ! Генерирую автоматически")
            generate_keypair()

    # generate keypair from scratch
    def generate_keypair():
        keys = encryptions.generate_keypair()
        public_key_entry.delete(0, END)
        public_key_entry.insert(0, keys[0])
        private_key_entry.delete(0, END)
        private_key_entry.insert(0, keys[1])
    
    public_gen_btn = Button(public_key_frame, text="Высчитать по приватному ключу", command=derive)
    public_gen_btn.pack(side=RIGHT)

    # Private Key field with generation button
    private_key_frame = Frame(main_frame)
    private_key_frame.pack(fill=X, pady=(0, 15))
    
    Label(private_key_frame, text="Private key (optional):", font=("Arial", 10, "bold")).pack(anchor=W)
    
    private_key_entry = Entry(private_key_frame, font=("Arial", 10), show="*")  # Hidden by default
    private_key_entry.pack(side=LEFT, fill=X, expand=True, padx=(0, 10))
    def toggle_private_visibility():
        """Toggle visibility of private key"""
        if private_key_entry.cget('show') == '*':
            private_key_entry.config(show='')
            visibility_btn.config(text='Hide')
        else:
            private_key_entry.config(show='*')
            visibility_btn.config(text='Show')
    
    # Frame for private key buttons
    private_btn_frame = Frame(private_key_frame)
    private_btn_frame.pack(side=RIGHT)

    priv_gen_btn = Button(private_btn_frame, text="Сгенерировать ключи", command=generate_keypair)
    
    visibility_btn = Button(private_btn_frame, text="Show", command=toggle_private_visibility)
    visibility_btn.pack(side=LEFT, padx=(0, 5))

    def submit_handler():
        if len(username_entry.get()) < 1:
            show_toast("Введите имя!")
        else:
            data = (username_entry.get(), public_key_entry.get(), private_key_entry.get())
            db.add_user(con, data, "receivers")
            update_listbox(user_listbox,con,"receivers")
            root.destroy()

    # Submit button at bottom
    submit_btn = Button(main_frame, text="Submit", bg="#4CAF50", fg="white", 
                          font=("Arial", 10, "bold"), height=2,
                          command=submit_handler)
    submit_btn.pack(fill=X, pady=(10, 0))    

def show_toast(message, duration=3000):
    """
    Display a toast notification window with the given message.
    
    Args:
        message (str): The text to display in the toast
        duration (int): Duration in milliseconds before auto-closing (default 3000ms)
    """
    # Create the main toast window
    toast = Toplevel()
    toast.title("Toast Notification")
    toast.overrideredirect(True)  # Remove window decorations
    toast.attributes('-topmost', True)  # Keep on top
    
    # Configure the background color
    toast.configure(bg='#2d2d2d')
    
    # Create a frame for padding
    padding_frame = Frame(toast, bg='#2d2d2d')
    padding_frame.pack(padx=20, pady=15)
    
    # Add the message label
    label = Label(
        padding_frame,
        text=message,
        fg='white',
        bg='#2d2d2d',
        font=('Arial', 10),
        wraplength=300
    )
    label.pack(side=LEFT, padx=(0, 10))
    
    # Add the close button
    close_btn = Button(
        padding_frame,
        text="Close",
        command=toast.destroy,
        bg='#444444',
        fg='white',
        relief='flat',
        overrelief='raised',
        padx=8,
        pady=4
    )
    close_btn.pack(side=RIGHT)
    
    # Update the idle tasks to get proper dimensions
    toast.update_idletasks()
    
    # Calculate position (bottom-right corner)
    screen_width = toast.winfo_screenwidth()
    screen_height = toast.winfo_screenheight()
    window_width = toast.winfo_width()
    window_height = toast.winfo_height()
    
    x = screen_width - window_width - 20
    y = screen_height - window_height - 50
    
    # Set the geometry
    toast.geometry(f"+{x}+{y}")
    
    # Schedule automatic closing if duration is positive
    if duration > 0:
        toast.after(duration, toast.destroy)

def show_encryption_dialog(username, con, parent=None, mode="encrypt"):
    """
    Show an encryption dialog with file selection options and encrypt functionality.
    
    Args:
        parent: Parent window (optional)
    """
    filetypes_in = [
        ("All Files", "*.*"),
        ("Text Files", "*.txt"),
        ("Document Files", "*.doc;*.docx"),
        ("PDF Files", "*.pdf")
    ]
    filetypes_out = [
        ("Encrypted Files", "*.age"),
    ]
    if mode == "decrypt":
        temp = filetypes_in
        filetypes_in = filetypes_out
        filetypes_out = temp
        del temp
    def browse_input_file():
        file_path = filedialog.askopenfilename(
            title="Select Input File",
            filetypes = filetypes_in
        )
        if file_path:
            input_file_var.set(file_path)
    
    def browse_output_file():
        initial_dir = os.path.dirname(input_file_var.get()) if input_file_var.get() else ""
        initial_file = os.path.basename(input_file_var.get()).rsplit('.', 1)[0] + "_encrypted" if input_file_var.get() else "encrypted_file"
        
        file_path = filedialog.asksaveasfilename(
            title="Save Encrypted File As",
            defaultextension=".age",
            initialdir=initial_dir,
            initialfile=initial_file,
            filetypes=filetypes_out
        )
        if file_path:
            output_file_var.set(file_path)
    
    def start_encryption():
        input_path = input_file_var.get()
        output_path = output_file_var.get()
        
        # Validate inputs
        if not input_path:
            messagebox.showerror("Error", "Please select an input file.")
            return
        
        if not output_path:
            messagebox.showerror("Error", "Please specify where to save the encrypted file.")
            return
        
        if not os.path.exists(input_path):
            messagebox.showerror("Error", f"Input file does not exist:\n{input_path}")
            return
        
        # Perform encryption
        try:
            perform_encryption(input_path, output_path)
            dialog.destroy()
        except Exception as e:
            messagebox.showerror("Error", f"Encryption failed:\n{str(e)}")
    
    def perform_encryption(input_path, output_path):
        ifile = open(input_path, "rb")
        ofile = open(output_path, "wb")
        if mode == "encrypt":
            encryptions.encr(username,con,ifile,ofile)
        elif mode == "decrypt":
            encryptions.decr(username,con,ifile,ofile)

    # Create the main dialog window
    parent = parent or _default_root
    dialog = Toplevel(parent)
    dialog.title("File Encryption")
    dialog.geometry("500x200")
    dialog.resizable(False, False)
    dialog.transient(parent)
    dialog.grab_set()  # Modal behavior
    
    # Center the dialog on screen
    dialog.update_idletasks()
    x = (dialog.winfo_screenwidth() // 2) - (500 // 2)
    y = (dialog.winfo_screenheight() // 2) - (200 // 2)
    dialog.geometry(f"+{x}+{y}")
    
    # Variables to store file paths
    input_file_var = StringVar()
    output_file_var = StringVar()
    
    # Main container frame
    main_frame = ttk.Frame(dialog, padding="20")
    main_frame.grid(row=0, column=0, sticky=(W, E, N, S))
    
    # Input file selection
    ttk.Label(main_frame, text="Input File:").grid(row=0, column=0, sticky=W, pady=(0, 10))
    
    input_frame = ttk.Frame(main_frame)
    input_frame.grid(row=1, column=0, columnspan=2, sticky=(W, E), pady=(0, 10))
    
    ttk.Entry(input_frame, textvariable=input_file_var, width=50).pack(side=LEFT, fill=X, expand=True)
    ttk.Button(input_frame, text="Browse...", command=browse_input_file).pack(side=RIGHT, padx=(10, 0))
    
    # Output file selection
    ttk.Label(main_frame, text="Save As:").grid(row=2, column=0, sticky=W, pady=(0, 10))
    
    output_frame = ttk.Frame(main_frame)
    output_frame.grid(row=3, column=0, columnspan=2, sticky=(W, E), pady=(0, 10))
    
    ttk.Entry(output_frame, textvariable=output_file_var, width=50).pack(side=LEFT, fill=X, expand=True)
    ttk.Button(output_frame, text="Browse...", command=browse_output_file).pack(side=RIGHT, padx=(10, 0))
    
    # Encrypt button
    ttk.Button(main_frame, text="Encrypt!", command=start_encryption).grid(row=4, column=0, columnspan=2, pady=20)
    
    # Configure grid weights
    main_frame.columnconfigure(0, weight=1)
    input_frame.columnconfigure(0, weight=1)
    output_frame.columnconfigure(0, weight=1)
