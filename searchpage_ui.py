import tkinter as tk

LARGE_FONT = ("Verdana", 12)

#Inherits from tk.Tk
class GoFind(tk.Tk):

    def __init__(self):
        #Initializing tk.Tk as well
        tk.Tk.__init__(self)
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

        search_button = tk.Button(self, text="Search", command=lambda: controller.show_frame(SearchPage))
        search_button.pack()

class SearchPage(tk.Frame):

    def __init__(self, master, controller):
        tk.Frame.__init__(self, master)
        label = tk.Label(self, text="Results", font=LARGE_FONT)
        label.pack(pady=10, padx=10)

        search_button = tk.Button(self, text="Search", command=lambda: controller.show_frame(StartPage))
        search_button.pack()

app = GoFind()
app.mainloop()