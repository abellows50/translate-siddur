import tkinter as tk
from tkhtmlview import HTMLText
class GUI:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("My GUI")
        # self.window.geometry("300x300")
        self.clickFxn = lambda x: x
        self.label = tk.Label(self.window, text="Search")
        self.label.pack()

        self.searchTerm = tk.StringVar()
        self.searchTerm.set("")
        
        self.entry = tk.Entry(self.window, textvariable=self.searchTerm)
        self.entry.pack()

        self.button = tk.Button(self.window, text="Search", command=self.clicked)
        self.button.pack()
       
    def defPopUp(self, word, html):
        popup = tk.Tk()
        popup.wm_title(f"Definition of {word}")
        myhtml = HTMLLabel(popup, html=html)
        myhtml.pack(padx=20, pady=20)
        B1 = tk.Button(popup, text="Close Definition", command = popup.destroy)
        B1.pack()
        popup.mainloop()

    def setSearchFxn(self, fxn):
        self.clickFxn = fxn

    def clicked(self):
        word = self.searchTerm.get()
        html = self.clickFxn(word)
        self.defPopUp(word, html)
        
    
    def addHtml(self, html):
        myhtml = HTMLText(self.window, html=html)
        myhtml.pack(padx=20, pady=20)


    def display(self):
        self.window.mainloop()

