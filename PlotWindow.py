
######################################################################
## Imports
######################################################################

import matplotlib
matplotlib.use('TkAgg')

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
from matplotlib.backend_bases import key_press_handler

import sys
if sys.version_info[0] < 3:
    from Tkinter import *
else:
    from tkinter import *

######################################################################
## PlotWindow
######################################################################

class PlotWindow(Frame):
    """

    """

    def __init__(self, parent, figure, plotType=None):
        """
        Constructor

        :param parent:
        :param figure:
        :param plotType:
        :return:
        """
        Frame.__init__(self, parent)
        # a tk.DrawingAre
        self.plotType = plotType
        self.canvas = FigureCanvasTkAgg(figure, master=self)
        self.canvas.show()
        self.canvas.get_tk_widget().pack(side=TOP, fill=BOTH, expand=1)

        self.toolbar = NavigationToolbar2TkAgg(self.canvas, self)
        self.toolbar.update()
        self.canvas._tkcanvas.pack(side=TOP, fill=BOTH, expand=1)

        self.canvas.mpl_connect('key_press_event', self.on_key_event)

    def getPlotType(self):
        """

        :return:
        """
        return self.plotType

    def updateFigure(self, figure):
        """

        :param figure:
        :return:
        """

        self.canvas._tkcanvas.pack_forget()

        self.canvas = FigureCanvasTkAgg(figure, master=self)
        self.canvas.show()
        self.canvas.get_tk_widget().pack(side=TOP, fill=BOTH, expand=1)

        self.toolbar = NavigationToolbar2TkAgg(self.canvas, self)
        self.toolbar.update()
        self.canvas._tkcanvas.pack(side=TOP, fill=BOTH, expand=1)

        self.canvas.mpl_connect('key_press_event', self.on_key_event)

    def on_key_event(self, event):
        """

        :param event:
        :return:
        """
        print('you pressed %s' % event.key)
        key_press_handler(event, self.canvas, self.toolbar)