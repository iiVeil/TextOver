import tkinter
from tkinter import messagebox
import time
import json
import os
import sys
from sys import exit
import subprocess
import psutil
open_pins = {}


if len(sys.argv) >= 2:
    class Win(tkinter.Tk):

        def __init__(self,master=None):
            tkinter.Tk.__init__(self,master)
            self.overrideredirect(True)
            self._offsetx = -50
            self._offsety = 0
            self.bind('<Button-1>',self.clickwin)
            self.bind('<B1-Motion>',self.dragwin)

        def dragwin(self,event):
            x = self.winfo_pointerx() - self._offsetx
            y = self.winfo_pointery() - self._offsety
            self.geometry('+{x}+{y}'.format(x=x,y=y))

        def clickwin(self,event):
            self._offsetx = event.x
            self._offsety = event.y

    first_click = None
    text = sys.argv[1]

    win = Win()
    win.lift()
    win.wm_attributes("-topmost", True)
    win.wm_attributes("-transparentcolor", "gray")
    win.config(bg="gray")
    text = text.replace("%20", " ")
    pins = json.load(open("bin/json/pins.dat","r"))
    w = tkinter.Label(win, text=f'{text}', fg=f"{pins[text]['color']}", bg="gray", wraplength=750)
    grip = tkinter.Label(win, text="⬛", bg="gray")
    grip.config(font=("Roboto", 11))
    grip.pack(side="left")
    # font size
    w.config(font=("Roboto", pins[text]['font_size']))
    w.pack(side="right", expand=True)
    win.wm_attributes("-topmost", 1)
    win.wait_visibility()
    win.mainloop()
else:
    if not os.path.exists("bin"):
        os.mkdir("bin")
    if not os.path.exists("bin/json"):
        os.mkdir("bin/json")
    if not os.path.exists("bin/json/pins.dat"):
        f = open("bin/json/pins.dat","w+")
        f.write("{}")
        f.close()
    if not os.path.exists("bin/json/cache.dat"):
        f = open("bin/json/cache.dat","w+")
        f.write("[]")
        f.close()
    def close_text(text):
        kill = None
        for item in open_pins:
            if item == text:
                kill = open_pins[text]
        proc = psutil.Process(kill)
        del open_pins[text]
        widget.deleteButtons()
        widget.createButtons()
        try:
            proc.kill()
        except Exception:
            pass

    def open_text(text):
        text= text.replace(" ", "%20")
        FNULL = open(os.devnull, 'w')
        #CHANGE THIS TO EXE BEFORE BUILD
        #open_pins[text.replace("%20", " ")] = subprocess.Popen(f"python36 main.pyw {text}", stdout=FNULL, stderr=FNULL, shell=False).pid
        open_pins[text.replace("%20", " ")] = subprocess.Popen(f"main.exe {text}", stdout=FNULL, stderr=FNULL, shell=False).pid
        widget.deleteButtons()
        widget.createButtons()
    def delete_text():
        time.sleep(.5)
        global check_boxes
        kill = None
        for item in check_boxes:
            if item in open_pins:
                kill = open_pins[item]
                proc = psutil.Process(kill)
                del open_pins[item]
                proc.kill()
        temp = []
        for item in check_boxes.values():
            temp.append(item.get())
        indexPosList = []
        indexPos = 0
        while True:
            try:
                # Search for item in list from indexPos to the end of list
                indexPos = temp.index(1, indexPos)
                # Add the index position in list
                indexPosList.append(indexPos)
                indexPos += 1
            except ValueError:
                break
        pins = json.load(open("bin/json/pins.dat","r"))
        pins = [value for value in pins.values()]
        seclist = []
        for item in indexPosList:
            seclist.append(pins[item])
        for item in seclist:
            pins.remove(item)
        new_dict = {}
        for item in pins:
           name = item['text']
           new_dict[name] = item
        f = open("bin/json/pins.dat","w")
        f.write(json.dumps(new_dict))
        f.close()
        widget.deleteButtons()
        widget.createButtons()
        
    check_boxes= {}

    def create_text():
        di = json.load(open("bin/json/pins.dat", "r"))
        text = entry.get("1.0",tkinter.END)
        text = text[:-1]
        if len(entry.get("1.0", tkinter.END)) <= 1:
            messagebox.showerror("Error", "No text inputted!")
        elif len(entry.get("1.0", tkinter.END)) > 150:
            messagebox.showerror("Error", "Limit of 150 characters broken!")
        elif variable.get() == "Pick a text color.":
            messagebox.showerror("Error", "Pick a color!")
        elif variable2.get() == "Font size.":
            messagebox.showerror("Error", "Pick a font size!")
        elif text in di:
            messagebox.showerror("Error", "You already have a pin for this text!")
        else:
            global check_boxes
            di[text] = {"text": text, "color": variable.get(), "font_size": int(variable2.get())}
            f = open("bin/json/pins.dat", "w")
            f.write(json.dumps(di))
            f.close()
            widget.createButtons()
            check_boxes[text] = tkinter.IntVar(respwin)

    def ask_quit():
        respwin.destroy()
    
    
    
    respwin = tkinter.Tk()
    respwin.protocol("WM_DELETE_WINDOW", ask_quit)
    class ScrollFrame(tkinter.Frame):
        def __init__(self, parent):
            super().__init__(parent) # create a frame (self)

            self.canvas = tkinter.Canvas(self, borderwidth=0, background="#ffffff")          #place canvas on self
            self.viewPort = tkinter.Frame(self.canvas, background="#ffffff")                    #place a frame on the canvas, this frame will hold the child widgets 
            self.vsb = tkinter.Scrollbar(self, orient="vertical", command=self.canvas.yview) #place a scrollbar on self 
            self.canvas.configure(yscrollcommand=self.vsb.set)                          #attach scrollbar action to scroll of canvas

            self.vsb.pack(side="right", fill="y")                                       #pack scrollbar to right of self
            self.canvas.pack(side="left", fill="both", expand=True)                     #pack canvas to left of self and expand to fil
            self.canvas_window = self.canvas.create_window((4,4), window=self.viewPort, anchor="nw",            #add view port frame to canvas
                                      tags="self.viewPort")

            self.viewPort.bind("<Configure>", self.onFrameConfigure)                       #bind an event whenever the size of the viewPort frame changes.
            self.canvas.bind("<Configure>", self.onCanvasConfigure)                       #bind an event whenever the size of the viewPort frame changes.

            self.onFrameConfigure(None)                                                 #perform an initial stretch on render, otherwise the scroll region has a tiny border until the first resize

        def onFrameConfigure(self, event):                                              
            '''Reset the scroll region to encompass the inner frame'''
            self.canvas.configure(scrollregion=self.canvas.bbox("all"))                 #whenever the size of the frame changes, alter the scroll region respectively.

        def onCanvasConfigure(self, event):
            '''Reset the canvas window to encompass inner frame when required'''
            canvas_width = event.width
            self.canvas.itemconfig(self.canvas_window, width = canvas_width)            #whenever the size of the canvas changes alter the window region respectively.
    class Example(tkinter.Frame):
        def deleteButtons(self):
            self.scrollFrame.destroy()
            self.scrollFrame = ScrollFrame(self)
            self.createButtons()
            tkinter.Button(self.scrollFrame.viewPort, text="DELETE SELECTED", command=delete_text, borderwidth="1", relief="solid").grid(row=0, column=1)
            tkinter.Button(self.scrollFrame.viewPort, text=f'REFRESH PINS', borderwidth="1", command=self.createButtons,relief="solid", wraplength=200).grid(row=0, column=0)
            self.scrollFrame.pack(side="top", fill="both", expand=True)
        def createButtons(self):
            row = 1
            with open("bin/json/pins.dat", "r") as f:
                pins = json.load(f)
            global check_boxes
            check_boxes = {}
            for pin in pins:
                dumb = False
                check_boxes[pin] = tkinter.IntVar(respwin)
                tkinter.Label(self.scrollFrame.viewPort, text=f'{pins[pin]["text"]}', fg=f'black', borderwidth="1", relief="solid", wraplength=200).grid(row=row, column=0, sticky=tkinter.W)
                for item in open_pins:
                    if item == pins[pin]["text"]:
                        dumb = True
                if not dumb:
                    tkinter.Button(self.scrollFrame.viewPort, text="PIN", command= lambda pin=pin: open_text(pin), borderwidth="1", relief="solid").grid(row=row, column=1, sticky=tkinter.E)
                else:
                    tkinter.Button(self.scrollFrame.viewPort, text="UNPIN", command= lambda pin=pin: close_text(pin), borderwidth="1", relief="solid").grid(row=row, column=1, sticky=tkinter.E)
                tkinter.Checkbutton(self.scrollFrame.viewPort, variable = check_boxes[pin]).grid(row=row, column=3, sticky=tkinter.E)
                row += 1
        def __init__(self, root):
            tkinter.Frame.__init__(self, root)
            self.scrollFrame = ScrollFrame(self) # add a new scrollable frame.
            # Now add some controls to the scrollframe. 
            # NOTE: the child controls are added to the view port (scrollFrame.viewPort, NOT scrollframe itself)
            self.createButtons()
            tkinter.Button(self.scrollFrame.viewPort, text="DELETE SELECTED", command=delete_text, borderwidth="1", relief="solid").grid(row=0, column=1)
            tkinter.Button(self.scrollFrame.viewPort, text=f'REFRESH PINS', borderwidth="1", command=self.createButtons,relief="solid", wraplength=200).grid(row=0, column=0)
            # when packing the scrollframe, we pack scrollFrame itself (NOT the viewPort)
            self.scrollFrame.pack(side="top", fill="both", expand=True)
    widget = Example(respwin)
    widget.grid(row=0, column=0, columnspan=60)
    variable = tkinter.StringVar(respwin)
    variable2 = tkinter.StringVar(respwin)
    variable.set("Pick a text color.")
    variable2.set("Font size.")
    w = tkinter.OptionMenu(respwin, variable, "Pick a text color.", "light blue", "orange", "yellow", "red", "white", "light green")
    w2 = tkinter.OptionMenu(respwin, variable2, "Font size.", 12, 18, 24, 30, 36)
    w.grid(row=3, column=0)
    w2.grid(row=4, column=0)

    tkinter.Label(respwin, text="What would you like to pin?").grid(row=1)
    b = tkinter.Button(respwin, text="Create Pin", command=create_text)
    entry = tkinter.Text(respwin, height=3, width=50)
    entry2 = tkinter.Text(respwin, height=1, width=2)

    b.grid(row=5, column=0)


    entry.grid(row=2, column=0, columnspan=60)

    tkinter.Label(respwin, text="PS. if you are using this for a game, make sure its in \"Fullscreen Windowed\"").grid(row=6)

    respwin.title("EasyPins")

    respwin.tk.call('wm', 'iconphoto', respwin._w, tkinter.PhotoImage(file='prog.ico'))

    respwin.mainloop()