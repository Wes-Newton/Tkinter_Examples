# -*- coding: utf-8 -*-
'''
https://stackoverflow.com/questions/7546050/switch-between-two-frames-
in-tkinter

https://stackoverflow.com/questions/32212408/how-to-get-variable-
data-from-a-class

https://stackoverflow.com/questions/17466561/best-way-to-structure-a-
tkinter-application

https://stackoverflow.com/questions/33646605/how-to-access-variables-
from-different-classes-in-tkinter

https://stackoverflow.com/questions/63677625/updating-tkinter-label-
in-a-frame-object/63681373#63681373

https://stackoverflow.com/questions/21507178/tkinter-text-binding-a-
variable-to-widget-text-contents/21565476#21565476

http://effbot.org/tkinterbook/variable.htm

https://tkdocs.com/tutorial/onepage.html
'''

import tkinter as tk    
           
from tkinter import font as tkfont 

class MainApplication(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.title_font = tkfont.Font(family='Helvetica', size=18, weight="bold", slant="italic")
        
        self.Multi_Frames = []
        self.frames_count = tk.IntVar()
        
        self.frames_count.set(1)
        parent.title('--Main--')
        parent.geometry('300x200+50+50')
        main_frame = tk.Frame(self)# parent, *args, **kwargs)
        main_frame.pack(side="top", fill="both", expand=True)
        Frame_Label = tk.Label(main_frame, text="This is the main frame" ,
                               font=self.title_font)
        Frame_Label.pack(side="top", fill="x", pady=10)
        New_Frame_Btn = tk.Button(main_frame, text="Generate Frames",
                            command= lambda: self.generate())
        New_Frame_Btn.pack()
        Frame_Label.pack()
        print("init")
        
    def generate(self):
        print("Generating Frames")
        thisinstance = SampleApp(self.frames_count)
        ct = self.frames_count.get()
        ct += 1
        self.frames_count.set(ct)
        self.Multi_Frames.append(thisinstance)
       

class SampleApp(tk.Tk):

    def __init__(self, count, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.title_font = tkfont.Font(family='Helvetica', size=18, weight="bold", slant="italic")
        container = tk.Frame(self)   
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        self.count = count.get()
        self.frames = {}
        self.Label1_Text = tk.StringVar()
        self.Label1_Text.set("--This is page 1--")

        # loops through and initializes each frame
        for F in (StartPage, PageOne, PageTwo):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")
 
        self.PageOne_Ct = tk.IntVar()
        self.PageOne_Ct.set(0)
        self.show_frame("StartPage")

    def show_frame(self, page_name):
        '''Show a frame for the given page name'''
        frame = self.frames[page_name]
        frame.tkraise()
        print("Button clicked or intial show page on top is: ", page_name)
        
    def get_inst(self):
        return self.count
     
    def get_page1_cts(self):
        counts = self.PageOne_Ct.get() 
        return counts 
    
    def get_lbl_text(self):
        label1text = self.Label1_Text.get()
        return label1text

class StartPage(tk.Frame):
    
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        inst = self.controller.get_inst()
                
        label = tk.Label(self, text="This is the start page, instance {0}".\
                         format(inst), 
                         font=self.controller.title_font)
        
        label.pack(side="top", fill="x", pady=10)
        button1 = tk.Button(self, text="Go to Page One",
                            command= lambda: PageOne.Show_PageOne(self, parent, controller))
        button2 = tk.Button(self, text="Go to Page Two",
                            command=lambda: controller.show_frame("PageTwo"))
        
        print("StartPage initalized")
        button1.pack()
        button2.pack()
       
class PageOne(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        global label
        self.controller = controller
        #self.label = tk.Label(self, textvariable = self.controller.Label1_Text.get(),
        #yields blank label
        label = tk.Label(self, text = self.controller.Label1_Text.get(),
                              font=controller.title_font)
        label.pack(side="top", fill="x", pady=10)
        button = tk.Button(self, text="Go to the start page",
                           command=lambda: controller.show_frame("StartPage"))
        print("PageOne initialized")
        button.pack()
        
        
    def Show_PageOne(self, parent, controller):
        
        global label   # No success without using this global - see below
        count = self.controller.get_page1_cts()
        self.controller = controller
        count = self.controller.PageOne_Ct.get()
        count += 1
        self.controller.PageOne_Ct.set(count)
        inst = self.controller.get_inst()
        new_label1_text = "You have clicked page one, instance {0}, {1} times".format(inst, count)
        #fails to update Label 1 text
        self.update()
        self.controller.Label1_Text.set(new_label1_text)
        print(new_label1_text)
        label.configure(text=new_label1_text)
        #changing __init__ and this method to self.label yields:
        #AttributeError: '_tkinter.tkapp' object has no attribute 'label'
        controller.show_frame("PageOne")

        
class PageTwo(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="This is page 2", font=controller.title_font)
        label.pack(side="top", fill="x", pady=10)
        button = tk.Button(self, text="Go to the start page",
                           command=lambda: controller.show_frame("StartPage"))
        print("PageTwo initialized")
        button.pack()
        

if __name__ == "__main__":
    root = tk.Tk()
    app = MainApplication(root)
    app.pack(side="top", fill="both", expand=True)
    app.mainloop()

