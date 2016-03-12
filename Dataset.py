
######################################################################
## Dataset
######################################################################

class Dataset:
    """
    Dataset is an interface that provides several methods that subclasses need to implement.

    The reason that an interface is used is so that we can specify different datasets for different types of testing.
    """

    def getSize(self):
        """

        @return size 1
        """
        return 1

    # the big change in dataset is that i added option as a parameter to each of these methods
    # this is to allow some flexibility in querying datasets
    # I'm not sure this is the final form i want this to take, but it was a good way to get off
    # the ground and testing the multiset

    def getHorizontalAt(self, option, point):
        """
        @param option does nothing in dataset
        @param point
        @return
        """
        return NotImplemented

    def getVerticalAt(self, option, point):
        """
        @param option does nothing in dataset
        @param point
        @return
        """
        return NotImplemented

    def getPlane(self, option):
        """

        @param option does nothing in dataset
        @return
        """
        return  NotImplemented

    def getYUnits(self, option):
        """

        @param option does nothing in dataset
        @return
        """
        return NotImplemented

    def getXUnits(self, option):
        """

        @param option does nothing in dataset
        @return
        """
        return NotImplemented
