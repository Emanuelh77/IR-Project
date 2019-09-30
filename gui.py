import random
from tkinter import Tk, Label, Button, Entry, StringVar, DISABLED, NORMAL, END, W, E, Frame

class GoFind(Frame):
    def __init__(self, master):
        self.master = master
        master.title("GoFind")

        # self.message = "Guess a number from 1 to 100"
        # self.label_text = StringVar()
        # self.label_text.set(self.message)
        # self.label = Label(master, textvariable=self.label_text)

        #Buttons/Entry
        self.entry = Entry(master)
        self.guess_button = Button(master, text="Guess")

        self.entry.grid(row=1, column=0, columnspan=2, ipadx=50)
        self.guess_button.grid(row=2, column=0, columnspan=2, ipadx=50)



root = Tk()
root.minsize(600,400)
my_gui = GoFind(root)
root.mainloop()