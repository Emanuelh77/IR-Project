import tkinter as tk
from tkinter import ttk, Entry

import pandas as pd
import numpy as np
import math
import json
import yaml
import operator

from itertools import combinations
from collections import Counter as ctr

from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize
from nltk.corpus import wordnet

#import query_suggestions as qs
import candidate_resources_ranking as crr
#import snippets as snp

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

class StartPage(tk.Frame):

    def __init__(self, master, controller):
        tk.Frame.__init__(self, master)

        label = tk.Label(self, text="GoFind", font=LARGE_FONT)
        label.grid(row=0, column=0, sticky="w")

        self.entry = Entry(self)
        self.entry.grid(row=1, column=0, ipadx=50, padx=.75)

        search_button = ttk.Button(self, text="Search", command=self.input_handler)#lambda: controller.show_frame(SearchPage))
        search_button.grid(row=1, column=1, padx=10)

        #self.label2 = tk.Label(self)
        #self.label2.grid(row=2, column=0, padx=.75)

    def input_handler(self):
        query = self.entry.get()
        cand_res = crr.get_candidate_resources(query)
        top_three = crr.relevance_ranking(query, cand_res)
        i = 1
        #for docID in top_three:
            #sentence = crr.snippet(docID, query)
            #label = tk.Label(self, text=str(sentence[0]))
            #label.grid(row=1+i, column=0)


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
app.geometry("1280x640")
app.mainloop()