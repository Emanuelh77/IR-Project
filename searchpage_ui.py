import tkinter as tk
from tkinter import ttk, Entry

LARGE_FONT = ("Verdana", 12)

#Inherits from tk.Tk
class GoFind(tk.Tk):

    def __init__(self):
        tk.Tk.__init__(self)

        tk.Tk.wm_title(self, "GoFind")

        container = tk.Frame(self)
        container.pack(side='top', fill='both', expand=True)

        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        for F in(StartPage, SearchPage):
            frame = F(container, self)
            self.frames[F] = frame

            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(StartPage)

    def show_frame(self, cont):

        frame = self.frames[cont]
        frame.tkraise()

def placeholder(msg):
    print(msg)

class StartPage(tk.Frame):

    def __init__(self, master, controller):
        tk.Frame.__init__(self, master)

        label = tk.Label(self, text="GoFind", font=LARGE_FONT)
        label.pack(pady=10, padx=10)

        entry = Entry(self)
        entry.pack()

        search_button = ttk.Button(self, text="Search", command=lambda: controller.show_frame(SearchPage))
        search_button.pack()

class SearchPage(tk.Frame):

    def __init__(self, master, controller):
        tk.Frame.__init__(self, master)
        label = tk.Label(self, text="Results", font=LARGE_FONT)
        label.grid(row=0, column=0, sticky="w")

        entry = Entry(self)
        entry.grid(row=1, column=0, ipadx=50, padx=.75) #ipadx=how long the entry is, padx=padding on the x axis

        search_button = ttk.Button(self, text="Search", command=lambda: controller.show_frame(StartPage))
        search_button.grid(row=1, column=1, padx=10)

app = GoFind()
app.mainloop()