# -*- coding: utf-8 -*-
 
'''
References:
    
https://stackoverflow.com/questions/3085696/adding-a-scrollbar-to-a-group-
of-widgets-in-tkinter/3092341#3092341

https://stackoverflow.com/questions/17355902/tkinter-binding-mousewheel-
to-scrollbar

https://stackoverflow.com/questions/40617515/python-tkinter-text-
modified-callback

https://stackoverflow.com/questions/13832720/how-to-attach-a-scrollbar-
to-a-text-widget

https://stackoverflow.com/questions/17466561/best-way-to-structure-a-
tkinter-application

http://effbot.org/tkinterbook/text.htm

BO comments:
I suggest a simpler approach. You can set up a proxy for the widget, 
and within that proxy you can detect whenever anything was inserted or 
deleted. You can use that information to generate a virtual event, 
which can be bound to like any other event.

The proxy in this example does three things:

    1. First it calls the actual widget command, passing in all of the 
    arguments it received.
    2. Next it generates an event for every insert and every delete
    3. Then it then generates a virtual event
    4. And finally it returns the results of the actual widget command

You can use this widget exactly like any other Text widget, with the added 
benefit that you can bind to <<TextModified>>.

For example, if you wanted to display the number of characters in 
the text widget you could do something like this:
 
#3092341    
    
You can only associate scrollbars with a few widgets, and the root widget 
and Frame aren't part of that group of widgets. The most common solution is 
to create a canvas widget and associate the scrollbars with that widget. 
Then, into that canvas embed the frame that contains your label widgets. 
Determine the width/height of the frame and feed that into the canvas 
scrollregion option so that the scrollregion exactly matches the size 
of the frame. Why put the widgets in a frame rather than directly in the 
canvas? A scrollbar attached to a canvas can only scroll items 
created with one of the create_ methods. You cannot scroll items 
added to a canvas with pack, place, or grid. By using a frame, you 
can use those methods inside the frame, and then call create_window 
once for the frame. Drawing the text items directly on the canvas isn't 
very hard, so you might want to reconsider that approach if the 
frame-embedded-in-a-canvas solution seems too complex. Since you're 
creating a grid, the coordinates of each text item is going to be very 
easy to compute, especially if each row is the same height (which it 
probably is if you're using a single font). For drawing directly on the 
canvas, just figure out the line height of the font you're using 
(and there are commands for that). Then, each y coordinate 
is row*(lineheight+spacing). The x coordinate will be a fixed 
number based on the widest item in each column. If you give everything 
a tag for the column it is in, you can adjust the x coordinate and 
width of all items in a column with a single command.    
 
'''

import tkinter as tk
from tkinter import ttk
from tkinter import *
from tkinter import font as tkfont



class MainApplication(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.title_font = tkfont.Font(family='Helvetica', size=18, 
                                      weight="bold", slant="italic")
        self.parent = parent
        self.Multi_Frames = []
        self.frames_count = tk.IntVar()
        self.frames_count.set(1)
        self.parent.title('--Main--')
        #parent.geometry('300x200+50+50')   #root.geometry('300x200-20+40')
        #above will supercede this line at bottom ^^^^^^^^^^^^^^^
        main_frame = tk.Frame(self)# parent, *args, **kwargs)
        main_frame.pack(side="top", fill="both", expand=True)
        Frame_Label = tk.Label(main_frame, text="This is the main frame" ,
                               font=self.title_font)
        Frame_Label.pack(side="top", fill="x", pady=10)
        New_Frame_Btn = tk.Button(main_frame, text="Get text",
                            command= lambda: self.generate())
        New_Frame_Btn.pack()
        Frame_Label.pack()
        
    def generate(self):
        ct = self.frames_count.get()
        thisinstance = Example(ct)
        ct += 1
        self.frames_count.set(ct)
        self.Multi_Frames.append(thisinstance)
 
class Example(tk.Tk):
    
    def __init__(self, count, *args, **kwargs):

        tk.Tk.__init__(self, *args, **kwargs)
        self.count = count
        self.canvas = tk.Canvas(self, borderwidth=4, background="#ff0000") #red
        self.frame = tk.Frame(self.canvas, borderwidth = 8, 
                              background="#ffffff") #white
        self.title("Text Entry # {}".format(count))
        self.canvas.configure(width = 300, height = 200)
        #self.vsb.grid(row = 0, column = 2, sticky = 'NES', rowspan = 2)
        self.canvas.grid()
        self.canvas.create_window((4,4), window=self.frame, anchor="nw",
                                  tags="self.frame")
        self.canvas.bind_all('<MouseWheel>', 
                             lambda event: self.canvas.yview_scroll \
                                 (int(-1*(event.delta/120)), "units"))
        self.frame.bind("<Configure>", self.onFrameConfigure)
        self.populate() #add widgets
         
    def onFrameConfigure(self, event):
        
        '''Reset the scroll region to encompass the inner frame'''
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        
    def _on_mousewheel(self, event):    #17355902
        self.canvas.yview_scroll(-1*(event.delta/120), "units")    
      
    def populate(self):
                 
        self.Done = tk.Button(self.frame, text = "Done", 
                         command = self.PrintText)
        self.Done.grid(row = 0, column = 0)       
        self.label = tk.Label(self.frame)
        self.label.grid(row =3, column = 0, padx = 5, pady = 5)
        self.label.configure(text="16 chars") # hardcoded initially
        #self.text = Text(self.frame, width = 40, height = 20)
        self.text = CustomText(self.frame, width = 30, height = 6)
        self.text.grid(row = 1, column = 0)
        self.vsb2 = tk.Scrollbar(self.frame, orient = "vertical", command = self.text.yview)
        self.vsb2.grid(row = 1, column = 1, sticky ='NES', rowspan = 2)
        self.text['yscrollcommand'] = self.vsb2.set
        self.text.insert('1.0', "--InitialText----") #'1.0' is line 1 character 0
        self.text.insert('1.9', " ") #'1.0' is line 1 character 0
        self.text.delete('1.14', '1.16') #just using some text methods
        self.text.bind("<<TextModified>>", self.onModification)
        #self.update() #see below
        self.text.focus_set() # not sure this works

    # def update(self):        # keeps bottom of text visible
    #     self.text.see(END)
    #     self.after(1000, self.update)
    
    def onModification(self, event):
        chars = len(event.widget.get("1.0", "end-1c"))
        self.label.configure(text="%s chars" % chars)
        
    def PrintText(self):
        
        returnval = tk.messagebox.askokcancel(message="Print Results?",
                                              title = "Print Text Entered")
        if returnval:
            print("Print text")
            self.text.insert(END,  "\n-- Done was selected, Instance {} --".format(self.count))
            self.Contents = self.text.get('1.0', END)
            print(self.Contents)

class CustomText(tk.Text):    #40617515
    def __init__(self, *args, **kwargs):
        """A text widget that report on internal widget commands"""
        tk.Text.__init__(self, *args, **kwargs)
        # create a proxy for the underlying widget
        self._orig = self._w + "_orig"
        self.tk.call("rename", self._w, self._orig)
        self.tk.createcommand(self._w, self._proxy)

    def _proxy(self, command, *args):
        cmd = (self._orig, command) + args
        result = self.tk.call(cmd)
        if command in ("insert", "delete", "replace"):
            self.event_generate("<<TextModified>>")

        return result


if __name__ == "__main__":
    root=tk.Tk()
    root.geometry('300x200-20+40')
    root.title('Text Example')
    root.resizable(TRUE, TRUE) #resize width and height
    #from Roseman chapter 10 - format is widthxheight+/=x+/-y
    #size is 300 by 200 RHS is -20 from right top is 40 below top
    example = MainApplication(root)
    example.pack(side="top", fill="both", expand=True)

    root.mainloop()
