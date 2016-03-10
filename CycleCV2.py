
######################################################################
## CycleV2
######################################################################

class CycleCV2:
    """
    Cycle data is stored in the CycleCV2.

    @field filename: The name of the file that data is pulled from
    @field metadata: List of entries in the header of the file
    @field labels: List of labels used in the table
    @field datatypes: List of strings storing the units used by each table column
    @field table:
    """
    def __init__(self, filename):
        """
        The constructor initializes the cycle data in class variables.
        @param filename: The name of the file to read the cycle data from.
        @return: Nothing
        """
        file = open(filename, 'r')
        self.filename = filename
        line = file.readline()
        self.metadata = list()
        while not "TABLE" in line:
            attr_array = line.split("\t")
            if len(attr_array) > 3:
                elements = {}
                elements["varname"] = attr_array[0]
                elements["type"] = attr_array[1]
                elements["data"] = attr_array[2]
                elements["name"] = attr_array[len(attr_array) - 1]
                self.metadata.append(elements)
            line = file.readline()

        temp_table = ""
        self.labels = file.readline().split("\t")
        self.datatypes = file.readline().split("\t")

        line = file.readline()
        while not "TABLE" in line:
            temp_table += line + '\n'
            line = file.readline()

        rows = temp_table.split("\n")
        #converts the data to 2D
        self.table = map(lambda x: x.split("\t"), rows)
        self.table = [i for i in self.table if len(i) > 1]

    def getDataAtPoint(self, point):
        """
        :param point: The point to query for data.
        :return: The IM data contained at a point
        """
        return float(self.table[point][4])

    def getAllData(self):
        """
        Gets all of the data contained in the table.
        :return: The entire IM data contained by the cycle
        """
        return list(map(lambda x: float(x[4]), self.table))

    def getVoltages(self):
        """
        Gets all of the voltages contained in the cycle.
        :return: List of voltages associated with each point in the cycle
        """
        return list(map(lambda x: float(x[3]), self.table))

    def getTimes(self):
        """
        Gets a list of all the times at which each sample taken.
        :return: List of times associated with each point in the cycle
        """
        return list(map(lambda x: float(x[2]), self.table))

    def print_labels(self):
        """
        Prints the labels contained by labels.
        :return: null
        """
        print (self.labels)

    def print_table(self):
        """
        Prints the table of data.
        :return: null
        """
        print (self.table)

