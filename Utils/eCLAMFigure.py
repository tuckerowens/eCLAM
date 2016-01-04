

from matplotlib.figure import Figure


class eCLAMFigure(Figure):

    def __init__(self, type):
        super()
        self.type = type
