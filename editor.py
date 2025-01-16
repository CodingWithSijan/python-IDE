import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import subprocess
import re


class PythonIDEWithHighlighting:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Python IDE with Syntax Highlighting")
        self.window.geometry("900x600")
        self.filename = None

        self.create_style()
        self.create_menu()
        self.create_editor()
        self.create_output_console()

    def create_style(self):
        """Creates a custom style for the IDE."""
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("TFrame", background="#2b2b2b")
        style.configure("TButton", background="#4CAF50", foreground="white", font=("Helvetica", 10, "bold"))
        style.map("TButton", background=[("active", "#45a049")])
        style.configure("TLabel", background="#2b2b2b", foreground="white", font=("Helvetica", 12, "bold"))

    def create_menu(self):
        """Creates the menu bar."""
        menu_bar = tk.Menu(self.window, bg="#4CAF50", fg="white", font=("Helvetica", 10, "bold"))

        # File menu
        file_menu = tk.Menu(menu_bar, tearoff=0, bg="#4CAF50", fg="white", font=("Helvetica", 10))
        file_menu.add_command(label="New", command=self.new_file)
        file_menu.add_command(label="Open", command=self.open_file)
        file_menu.add_command(label="Save", command=self.save_file)
        file_menu.add_command(label="Save As", command=self.save_file_as)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.window.quit)
        menu_bar.add_cascade(label="File", menu=file_menu)

        # Run menu
        run_menu = tk.Menu(menu_bar, tearoff=0, bg="#4CAF50", fg="white", font=("Helvetica", 10))
        run_menu.add_command(label="Run", command=self.run_code)
        menu_bar.add_cascade(label="Run", menu=run_menu)

        self.window.config(menu=menu_bar)

    def create_editor(self):
        """Creates the text editor with syntax highlighting."""
        editor_frame = ttk.Frame(self.window)
        editor_frame.pack(fill="both", expand=True)

        self.editor = tk.Text(
            editor_frame,
            wrap="none",
            font=("Courier New", 12),
            bg="#1e1e1e",
            fg="white",
            insertbackground="white",
        )
        self.editor.pack(fill="both", expand=True, padx=5, pady=5)

        # Bind events for syntax highlighting
        self.editor.bind("<KeyRelease>", self.syntax_highlight)

    def create_output_console(self):
        """Creates the output console."""
        console_frame = ttk.Frame(self.window)
        console_frame.pack(fill="x")

        console_label = ttk.Label(console_frame, text="Output Console:")
        console_label.pack(anchor="w", padx=5)

        self.console = tk.Text(
            console_frame,
            height=10,
            font=("Courier New", 12),
            bg="#1e1e1e",
            fg="#00FF00",
            insertbackground="white",
        )
        self.console.pack(fill="x", padx=5, pady=5)
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
                text=True,
            )
            self.console.configure(state="normal")
            self.console.delete("1.0", tk.END)
            self.console.insert("1.0", process.stdout + process.stderr)
            self.console.configure(state="disabled")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred while running the code: {str(e)}")

    def syntax_highlight(self, event=None):
        """Applies syntax highlighting to the editor."""
        self.editor.tag_remove("Keyword", "1.0", tk.END)
        self.editor.tag_remove("String", "1.0", tk.END)
        self.editor.tag_remove("Comment", "1.0", tk.END)
        self.editor.tag_remove("Number", "1.0", tk.END)

        text = self.editor.get("1.0", tk.END)

        # Highlight keywords
        keywords = r"\b(import|from|class|def|return|if|else|elif|for|while|try|except|with|as|lambda|pass|break|continue)\b"
        for match in re.finditer(keywords, text):
            self.editor.tag_add("Keyword", f"1.0+{match.start()}c", f"1.0+{match.end()}c")
        self.editor.tag_configure("Keyword", foreground="orange")

        # Highlight strings
        strings = r"(['\"].*?['\"])"
        for match in re.finditer(strings, text):
            self.editor.tag_add("String", f"1.0+{match.start()}c", f"1.0+{match.end()}c")
        self.editor.tag_configure("String", foreground="green")

        # Highlight comments
        comments = r"(#.*?$)"
        for match in re.finditer(comments, text, re.MULTILINE):
            self.editor.tag_add("Comment", f"1.0+{match.start()}c", f"1.0+{match.end()}c")
        self.editor.tag_configure("Comment", foreground="grey")

        # Highlight numbers
        numbers = r"\b\d+\b"
        for match in re.finditer(numbers, text):
            self.editor.tag_add("Number", f"1.0+{match.start()}c", f"1.0+{match.end()}c")
        self.editor.tag_configure("Number", foreground="blue")

    def run(self):
        """Runs the main event loop."""
        self.window.mainloop()


# Run the Python IDE with Syntax Highlighting
if __name__ == "__main__":
    PythonIDEWithHighlighting().run()
