import tkinter as tk
from tkinter import filedialog, messagebox, font, colorchooser
import win32print
import win32api

class TextEditor:
    def __init__(self, root):
        self.root = root
        self.root.title("Text Editor")
        self.root.geometry("800x600")

        self.text_area = tk.Text(self.root, wrap='word', font=("Arial", 12))
        self.text_area.pack(fill='both', expand=1)

        self.menu_bar = tk.Menu(self.root)
        self.root.config(menu=self.menu_bar)

        file_menu = tk.Menu(self.menu_bar, tearoff=0)
        file_menu.add_command(label="New", command=self.new_file)
        file_menu.add_command(label="Open", command=self.open_file)
        file_menu.add_command(label="Save", command=self.save_file)
        file_menu.add_command(label="Save As...", command=self.save_file_as)
        file_menu.add_command(label="Print", command=self.print_file)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.root.quit)
        self.menu_bar.add_cascade(label="File", menu=file_menu)

        edit_menu = tk.Menu(self.menu_bar, tearoff=0)
        edit_menu.add_command(label="Change Font", command=self.change_font)
        edit_menu.add_command(label="Change Font Size", command=self.change_font_size)
        edit_menu.add_command(label="Change Font Color", command=self.change_font_color)
        self.menu_bar.add_cascade(label="Edit", menu=edit_menu)

        self.file_path = None

    def new_file(self):
        self.text_area.delete(1.0, tk.END)
        self.file_path = None

    def open_file(self):
        self.file_path = filedialog.askopenfilename(defaultextension=".docu",
                                                    filetypes=[("Document files", "*.docu"), ("All files", "*.*")])
        if self.file_path:
            with open(self.file_path, "r") as file:
                self.text_area.delete(1.0, tk.END)
                self.text_area.insert(tk.END, file.read())

    def save_file(self):
        if self.file_path:
            with open(self.file_path, "w") as file:
                file.write(self.text_area.get(1.0, tk.END))
        else:
            self.save_file_as()

    def save_file_as(self):
        self.file_path = filedialog.asksaveasfilename(defaultextension=".docu",
                                                      filetypes=[("Document files", "*.docu"), ("All files", "*.*")])
        if self.file_path:
            with open(self.file_path, "w") as file:
                file.write(self.text_area.get(1.0, tk.END))

    def print_file(self):
        # Save the content to a temporary file
        if not self.file_path:
            messagebox.showerror("Error", "Save the document before printing.")
            return

        # Save the file
        self.save_file()

        # Print the file using the default printer
        win32api.ShellExecute(
            0,
            "print",
            self.file_path,
            None,
            ".",
            0
        )

    def change_font(self):
        fonts = list(font.families())
        selected_font = tk.simpledialog.askstring("Font", "Choose a font:", initialvalue="Arial")
        if selected_font in fonts:
            current_font_size = self.text_area.cget("font").split()[1]
            self.text_area.config(font=(selected_font, current_font_size))
        else:
            messagebox.showerror("Error", "Font not found!")

    def change_font_size(self):
        size = tk.simpledialog.askinteger("Font Size", "Enter a font size:", initialvalue=12)
        if size:
            current_font = self.text_area.cget("font").split()[0]
            self.text_area.config(font=(current_font, size))

    def change_font_color(self):
        color = colorchooser.askcolor()[1]
        if color:
            self.text_area.config(fg=color)

if __name__ == "__main__":
    root = tk.Tk()
    app = TextEditor(root)
    root.mainloop()
