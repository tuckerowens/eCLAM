
######################################################################
## Imports
######################################################################

import re, xml.etree.ElementTree as ET, os

######################################################################
## FileRecognizer
######################################################################

class FileRecognizer:

    # This function should be overridden
    def validFile(self, name, elements):
        """

        @param name
        @param elements
        @return
        """
        return False

    # This function should be overridden to
    # extract all the information elements from a file name
    def componentExtraction(self, name):
        """

        @param name
        @return
        """
        return {}

    # This needs to be updated when new
    # file recognizers are written
    @staticmethod
    def recognize(filename):
        """
        Recognize
        @param filename
        @return
        """
        if FileTypeCV2.validFile(filename):
            return FileTypeCV2
        return None


######################################################################
## Imports
######################################################################

#This object will take a config file and generate
class XmlFileRecognizer(FileRecognizer):

    configFile = ""
    recognizers = []
    tree = None

    def __init__(self, element):
        """

        @param element
        @return
        """
        self.element = element
        self.name = element.get("name")
        try:
            self.matchingPatternElem = element.find("RegexMatcher")
            self.matchingPattern = re.compile(element.find("RegexMatcher").text)
        except:
            print("Regex rule to match file name is invalid for recognizer %s" % (self.name))
            print("Building Blank Matcher")
            if self.matchingPatternElem == None:
                self.matchingPatternElem = ET.Element("RegexMatcher")
                element.insert(self.matchingPatternElem)
            self.matchingPattern = re.compile("")
        elementList = element.find("ExtractableElements")
        try:
            self.elementPattern = re.compile(elementList.find("RegexExpression").text)
        except:
            self.elementPattern = re.compile("")
            self.elementGroups = {}
            print("Regex rule to match file name components is invalid for recognizer %s" % (self.name))
            return
        self.elementGroups = {}
        for eg in elementList.iter("Element"):
            self.elementGroups[eg.get("name")] = eg.get("group")

        self.defaultSelection = element.find("DefaultSelection")
        if self.defaultSelection == None:
            print("DefaultSelection Tag not found, generating...")
            self.defaultSelection = ET.Element("DefaultSelection")
            element.append(self.defaultSelection)

    def __str__(self, *args, **kwargs):
        """
        Returns the name
        @param args
        @param kwargs
        @return
        """
        return self.name

    def updateMatcherRegex(self, regexStr):
        """

        :param regexStr:
        :return:
        """
        self.matchingPatternElem.text = regexStr

    def validFile(self, name, elements):
        """

        :param name:
        :param elements:
        :return:
        """
        if not self.matchingPattern.match(os.path.basename(name)): return False;
        selfElems = self.componentExtraction(os.path.basename(name))
        for k in selfElems.keys():
            if k in elements.keys():
                if not selfElems[k] in elements[k]: return False
        return True

    def setDefaultSelection(self, options):
        """

        :param options:
        :return:
        """
        self.defaultSelection.attrib = options

    def getDefaultSelection(self):
        """

        :return:
        """
        return self.defaultSelection.attrib

    def getMatcherRegex(self):
        """

        :return:
        """
        return self.matchingPatternElem.text


    def componentExtraction(self, name):
        """

        :param name:
        :return:
        """
        output = {}
        result = self.elementPattern.search(os.path.basename(name))
        if result == None:
            return output
        for k in self.elementGroups.keys():
            output[k] = result.group(int(self.elementGroups[k]))
        return  output

    @staticmethod
    def outputToFile(name):
        """

        :param name:
        :return:
        """
        XmlFileRecognizer.tree.write(name)


    @staticmethod
    def buildRecognizers():
        """

        :return:
        """
        XmlFileRecognizer.tree = ET.parse(XmlFileRecognizer.configFile)
        root = XmlFileRecognizer.tree.getroot()
        XmlFileRecognizer.recognizers = []
        for fileRecognizer in root.iter("FileRecognizer"):
            XmlFileRecognizer.recognizers.append(XmlFileRecognizer(fileRecognizer))

    @staticmethod
    def findRecognizerByName(name):
        """

        :param name:
        :return:
        """
        options = list(filter(lambda x: str(x) == name, XmlFileRecognizer.recognizers))
        if len(options) > 1:
            print("I'm confused, multiple recognizers have the name " + name)
        if len(options) == 0: return None
        return options[0]

    @staticmethod
    def recognizeBatch(files, definitionFile):
        """

        :param files:
        :param definitionFile:
        :return:
        """
        if definitionFile != XmlFileRecognizer.configFile:
            XmlFileRecognizer.configFile = definitionFile
            XmlFileRecognizer.buildRecognizers()
        output = {}
        for recognizer in XmlFileRecognizer.recognizers:
            output[recognizer] = []
            for file in files:
                if recognizer.validFile(os.path.basename(file), {}):
                    output[recognizer].append(file)
        return output


######################################################################
## FileTypeCV2
######################################################################

class FileTypeCV2(FileRecognizer):


    def validFile(name, elements=None):
        """

        :param elements:
        :return:
        """
        if elements == {} or elements == None:
            return "CV2" in name or "DTA" in name
        elems = FileTypeCV2.componentExtraction(name)
        for k in elements.keys():
            if k in elems.keys():
                if elems[k] != elements[k]:
                    return False
            else:
                return False
        return True


    def componentExtraction(name):
        """

        :return:
        """
        elems = re.search("([0-9]+)\s([A-Z]+)\s([1-9][0-9]+[n|u|m]M)\s([1-9]+)\s([A-F]+)\s([0-9]+)\s+CV2_#([0-9]+).DTA", name)
        output = {}
        output["Date"] = elems.group(1)
        output["Chem"] = elems.group(2)
        output["Concentration"] = elems.group(3)
        output["trial"] = elems.group((4))
        output["scientist"] = elems.group(5)
        output["idk"] = elems.group(6)
        output["fileno"] = int(elems.group(7))
        return output