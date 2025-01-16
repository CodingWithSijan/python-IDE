import tkinter as tk
from tkinter import filedialog, messagebox
import subprocess
import os

class SimplePythonIDE:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Simple Python IDE")
        self.window.geometry("800x600")
        self.filename = None

        self.create_menu()
        self.create_editor()
        self.create_output_console()

    def create_menu(self):
        """Creates the menu bar."""
        menu_bar = tk.Menu(self.window)

        # File menu
        file_menu = tk.Menu(menu_bar, tearoff=0)
        file_menu.add_command(label="New", command=self.new_file)
        file_menu.add_command(label="Open", command=self.open_file)
        file_menu.add_command(label="Save", command=self.save_file)
        file_menu.add_command(label="Save As", command=self.save_file_as)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.window.quit)
        menu_bar.add_cascade(label="File", menu=file_menu)

        # Run menu
        run_menu = tk.Menu(menu_bar, tearoff=0)
        run_menu.add_command(label="Run", command=self.run_code)
        menu_bar.add_cascade(label="Run", menu=run_menu)

        self.window.config(menu=menu_bar)

    def create_editor(self):
        """Creates the text editor."""
        self.editor = tk.Text(self.window, wrap="none", font=("Courier New", 12))
        self.editor.pack(fill="both", expand=True)

    def create_output_console(self):
        """Creates the output console."""
        self.console = tk.Text(self.window, height=10, font=("Courier New", 12), bg="black", fg="white")
        self.console.pack(fill="x")
        self.console.insert("1.0", "Output console...\n")
        self.console.configure(state="disabled")

    def new_file(self):
        """Creates a new file."""
        self.filename = None
        self.editor.delete("1.0", tk.END)

    def open_file(self):
        """Opens an existing file."""
        self.filename = filedialog.askopenfilename(filetypes=[("Python Files", "*.py")])
        if self.filename:
            with open(self.filename, "r") as file:
                content = file.read()
            self.editor.delete("1.0", tk.END)
            self.editor.insert("1.0", content)

    def save_file(self):
        """Saves the current file."""
        if self.filename:
            with open(self.filename, "w") as file:
                content = self.editor.get("1.0", tk.END)
                file.write(content)
        else:
            self.save_file_as()

    def save_file_as(self):
        """Saves the current file as a new file."""
        self.filename = filedialog.asksaveasfilename(defaultextension=".py", filetypes=[("Python Files", "*.py")])
        if self.filename:
            self.save_file()

    def run_code(self):
        """Runs the code in the editor."""
        if not self.filename:
            messagebox.showerror("Error", "Please save the file before running.")
            return

        # Save the current code to the file
        self.save_file()

        # Execute the Python file
        try:
            process = subprocess.run(
                ["python", self.filename],
                capture_output=True,
                text=True
            )
            self.console.configure(state="normal")
            self.console.delete("1.0", tk.END)
            self.console.insert("1.0", process.stdout + process.stderr)
            self.console.configure(state="disabled")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred while running the code: {str(e)}")

    def run(self):
        """Runs the main event loop."""
        self.window.mainloop()


# Run the IDE
if __name__ == "__main__":
    SimplePythonIDE().run()
