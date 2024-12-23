import tkinter as tk
from tkinter import ttk
import tkinter.messagebox
import urllib.request

class SimpleBrowser:
    def __init__(self, root):
        self.root = root
        self.root.title("jocarsa | ghostwhite")
        self.root.geometry("1024x768")
        self.root.configure(bg="ghostwhite")

        # URL Entry and Navigation
        self.url_frame = tk.Frame(self.root, bg="ghostwhite")
        self.url_frame.pack(side=tk.TOP, fill=tk.X, padx=10, pady=10)

        self.url_entry = ttk.Entry(self.url_frame, width=80)
        self.url_entry.pack(side=tk.LEFT, padx=5, pady=5, fill=tk.X, expand=True)
        self.url_entry.insert(0, "http://")

        style = ttk.Style()
        style.configure("TButton", background="ghostwhite", font=("Arial", 10))

        self.go_button = ttk.Button(self.url_frame, text="Go", command=self.load_url)
        self.go_button.pack(side=tk.LEFT, padx=5)

        self.back_button = ttk.Button(self.url_frame, text="Back", command=self.go_back)
        self.back_button.pack(side=tk.LEFT, padx=5)

        self.forward_button = ttk.Button(self.url_frame, text="Forward", command=self.go_forward)
        self.forward_button.pack(side=tk.LEFT, padx=5)

        self.content_frame = tk.Frame(self.root, bg="ghostwhite")
        self.content_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        self.content_text = tk.Text(
            self.content_frame, wrap=tk.WORD, state=tk.DISABLED, bg="ghostwhite", fg="black",
            font=("Arial", 12), relief=tk.FLAT
        )
        self.content_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        # History stack
        self.history = []
        self.history_index = -1

    def load_url(self):
        url = self.url_entry.get().strip()
        if not url.startswith("http://") and not url.startswith("https://"):
            url = "http://" + url

        try:
            response = urllib.request.urlopen(url)
            content = response.read().decode("utf-8")

            # Update history
            self.history = self.history[:self.history_index + 1]
            self.history.append(url)
            self.history_index += 1

            # Display content
            self.display_content(content)
        except Exception as e:
            tkinter.messagebox.showerror("Error", f"Failed to load URL: {e}")

    def display_content(self, content):
        self.content_text.config(state=tk.NORMAL)
        self.content_text.delete(1.0, tk.END)
        self.content_text.insert(tk.END, content)
        self.content_text.config(state=tk.DISABLED)

    def go_back(self):
        if self.history_index > 0:
            self.history_index -= 1
            self.url_entry.delete(0, tk.END)
            self.url_entry.insert(0, self.history[self.history_index])
            self.load_url()

    def go_forward(self):
        if self.history_index < len(self.history) - 1:
            self.history_index += 1
            self.url_entry.delete(0, tk.END)
            self.url_entry.insert(0, self.history[self.history_index])
            self.load_url()

if __name__ == "__main__":
    root = tk.Tk()
    browser = SimpleBrowser(root)
    root.mainloop()
