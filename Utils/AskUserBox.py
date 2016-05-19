
from threading import *
import _thread

import sys, time
if sys.version_info[0] < 3:
    from Tkinter import *
else:
    from tkinter import *


def AskUser(questions, defaults=[]):

    tk = Tk()
    box = AskUserBox(tk, questions, defaults=defaults)
    tk.update()
    tk.wait_window()
    res = box.responce()
    return res

class AskUserBox():

    def __init__(self, parent, questions, defaults=[]):
        super().__init__()
        self.questions = questions
        self.output = None
        self.frame = parent
        self.frame.wm_geometry("340x200")
        self.inputs = []
        for i in range(len(self.questions)):
            lbl = Label(self.frame, text=self.questions[i])
            lbl.grid(row=i+1, column=0, sticky=NSEW)
            self.inputs.append(Entry(self.frame))
            if len(defaults) > i:
                self.inputs[i].insert(0, defaults[i])
            self.inputs[i].grid(row=i+1, column=1)

        okay = Button(self.frame, text="Okay", command=self.okayClicked)
        okay.grid(sticky=E)



    def okayClicked(self):
        self.output = []
        for e in self.inputs:
            self.output.append(e.get())
        self.frame.destroy()


    def responce(self):
        return self.output

