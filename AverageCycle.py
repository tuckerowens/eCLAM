
######################################################################
## AverageCycle
######################################################################

class AverageCycle:
    """
    Cycle data is stored in the CycleCV2.

    @field filename: The name of the file that data is pulled from
    @field metadata: List of entries in the header of the file
    @field labels: List of labels used in the table
    @field datatypes: List of strings storing the units used by each table column
    @field table:
    """
    def __init__(self, point_count, label_count ):
        """
        The constructor initializes the cycle data in class variables.
        @param filename: The name of the file to read the cycle data from.
        @return Nothing
        """
        self.filename = "average"
        self.metadata = ""
        self.labels = ""
        self.datatypes = ""
        self.table = [[] for _ in range(point_count)]

        for x in range(point_count):
            for y in range(label_count):
                self.table[x].append(0)

    def getDataAtPoint(self, point):
        """
        @param point: The point to query for data.
        @return The IM data contained at a point
        """
        return float(self.table[point][4])

    def getAllData(self):
        """
        Gets all of the data contained in the table.
        @return The entire IM data contained by the cycle
        """
        return list(map(lambda x: float(x[4]), self.table))

    def getVoltages(self):
        """
        Gets all of the voltages contained in the cycle.
        @return List of voltages associated with each point in the cycle
        """
        return list(map(lambda x: float(x[3]), self.table))

    def getTimes(self):
        """
        Gets a list of all the times at which each sample taken.
        @return List of times associated with each point in the cycle
        """
        return list(map(lambda x: float(x[2]), self.table))

    def print_labels(self):
        """
        Prints the labels contained by labels.
        @return null
        """
        print (self.labels)

    def print_table(self):
        """
        Prints the table of data.
        @return null
        """
        print (self.table)

