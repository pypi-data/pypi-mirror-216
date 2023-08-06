import tkinter as tk
from tkinter import ttk
''' Progress bar for loading with one input '''

class progressLoadBar(tk.Tk):
    ''' Progress bar for loading with one input '''
    def __init__(self):
        super().__init__()
        self.geometry("400x50")
        self.title("Loading...")
        self.progress = ttk.Progressbar(self, orient="horizontal", length=350, mode="determinate")
        self.progress.pack(pady=20)

    def load_update(self,new_value):
        ''' Change bar to specific value '''
        self.progress["value"] = new_value
        self.progress.start()
        self.progress.update()
        self.progress.stop()

class UpDownButton(tk.Frame):
    '''special type of button'''
    def __init__(self, master,value=5):
        super().__init__(master)

        self.font = value
        self.up_button = tk.Button(self, text="▲", width=1, height=1, command=self.increment)
        self.up_button.pack(side="top")

        self.label = tk.Label(self, width=1, height=1, text=self.font)
        self.label.pack(side="top")

        self.down_button = tk.Button(self, text="▼", width=1, height=1, command=self.decrement)
        self.down_button.pack(side="top")

    def increment(self):
        if self.font < 50:
            self.font += 1
            self.label.config(text=self.font)

    def decrement(self):
        if self.font > 1:
            self.font -= 1
            self.label.config(text=self.font)

    def get_val(self):
        return self.font