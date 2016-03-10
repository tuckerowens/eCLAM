
######################################################################
## Dataset
######################################################################

class Dataset:
    """
    Dataset is an interface that provides several methods that subclasses need to implement.

    The reason that an interface is used is so that we can specify different datasets for different types of testing.
    """

    def getHorizontalAt(self, point):
        """
        :param point:
        :return:
        """
        return NotImplemented

    def getVerticalAt(self, point):
        """
        :param point:
        :return:
        """
        return NotImplemented

    def getPlane(self):
        """

        :return:
        """
        return  NotImplemented

    def getYUnits(self):
        """

        :return:
        """
        return NotImplemented

    def getXUnits(self):
        """

        :return:
        """
        return NotImplemented
