# -*- coding: utf-8 -*-
"""
Created on Tue Jul 21 09:13:18 2020

"""

#This tkinter example code is based in part on these Stackoverflow examples 
#and questions and the book "Modern Tkinter for Busy Python Developers"
#by Mark Roseman

#https://stackoverflow.com/questions/3085696/adding-a-scrollbar-to-a-group-
#of-widgets-in-tkinter/3092341#3092341

#https://stackoverflow.com/questions/39490247/how-can-we-use-a-loop-to-create-
#checkbuttons-from-an-array-and-print-the-values

#https://stackoverflow.com/questions/17355902/tkinter-binding-
#mousewheel-to-scrollbar

#Entry-Mousewheel-Resizing Frames-Frame location-Programatically populating
#checkbutton-Resizing frame-Widget inside labeframe-Messagebox




import tkinter as tk
from tkinter import ttk
from tkinter import *
from tkinter import font


class Example(tk.Frame):
    
    def __init__(self, parent):

        tk.Frame.__init__(self, parent)
        
        self.canvas = tk.Canvas(self, borderwidth=0, background="#ffffff")
        self.frame = tk.Frame(self.canvas, background="#ffffff")
        self.vsb = tk.Scrollbar(self, orient="vertical",
                                command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=self.vsb.set)
        self.vsb.pack(side="right", fill="y")
        self.canvas.pack(side="left", fill="both", expand=True)
        self.canvas.create_window((4,4), window=self.frame, anchor="nw",
                                  tags="self.frame")
        #self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)
        self.canvas.bind_all('<MouseWheel>', 
                             lambda event: self.canvas.yview_scroll \
                                 (int(-1*(event.delta/120)), "units"))
        self.frame.bind("<Configure>", self.onFrameConfigure)
        self.t = []
        self.select =[]
        self.buttons =[]
        self.message = StringVar()
        #for row in range(20):
            
        LF = ttk.LabelFrame(self.frame, text = "Checkbuttons", height = 50,
                            cursor = 'pencil') #, font = myBoldFont)
        LF.grid(row = 0, column = 0, columnspan= 4, sticky = (N,W,E))
        Message = tk.Entry(LF, width = 40, textvariable =self.message,
                           cursor = 'pencil')
        Message.grid(row=0, column=0, columnspan =4, sticky = (W,E))
        Sep = ttk.Separator(self.frame, orient = HORIZONTAL)
        Sep.grid(row = 1, column = 0, columnspan = 4, sticky = (W,E))
        self.populate()
        
    def populate(self):
                 
        fontcount = 0
        for newfont in font.families():
            self.newFont = font.Font(family = newfont, size = 12, weight = 'bold')
            row = fontcount
            tk.Label(self.frame, text="%s" % row, width=3, borderwidth="1",
                     relief="solid").grid(row=row + 2, column=0)
            self.select.append(StringVar())
            self.select[row].set('off')
            self.t.append("This is font %s " %newfont)
            c = tk.Checkbutton(self.frame, text=self.t[row], 
                               variable=self.select[row],
                               onvalue='on', offvalue='off',
                               font = self.newFont) 
            c.grid(row = row + 2, column = 1)
            fontcount += 1
        Done = tk.Button(self.frame, text = "Done", 
                         command = self.PrintSelected)
        Done.grid(row = 2, column = 3)
    
    def onFrameConfigure(self, event):
        
        '''Reset the scroll region to encompass the inner frame'''
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        
    def _on_mousewheel(self, event):
        self.canvas.yview_scroll(-1*(event.delta/120), "units")    
        
    def PrintSelected(self):
        
        returnval = tk.messagebox.askokcancel(message="Print Results?",
                                              title = "Print Data Selected")
        if returnval:
            index = 0
            print(self.message.get())
            for newfont in font.families():
                selected = self.select[index].get()
                if selected == 'on':
                    print("You selected the font in row %s it is %s" % (index, newfont))
                self.select[index].set('off')
                index += 1

if __name__ == "__main__":
    root=tk.Tk()
    root.geometry('300x200-20+40')
    root.title('Pop_Up_Checkbutton')
    root.resizable(TRUE, FALSE) #resize width not height
    #from Roseman chapter 10 - format is widthxheight+/=x+/-y
    #size is 300 by 200 RHS is -20 from right top is 40 below top
    example = Example(root)
    example.pack(side="top", fill="both", expand=True)
    root.mainloop()
    
    