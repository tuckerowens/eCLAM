
import re, xml.etree.ElementTree as ET, os


class FileRecognizer:

    # This function should be overridden
    def validFile(self, name, elements):
        return False

    # This function should be overridden to
    # extract all the information elements from a file name
    def componentExtraction(self, name):
        return {}

    # This needs to be updated when new
    # file recognizers are written
    @staticmethod
    def recognize(filename):
        if FileTypeCV2.validFile(filename):
            return FileTypeCV2
        return None

#This object will take a config file and generate
class XmlFileRecognizer(FileRecognizer):

    configFile = ""
    recognizers = []

    def __init__(self, element):
        self.name = element.get("name")
        try:
            self.matchingPattern = re.compile(element.find("RegexMatcher").text)
        except:
            print("Regex rule to match file name is invalid for recognizer %s" % (self.name))
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

    def __str__(self, *args, **kwargs):
        return self.name

    def validFile(self, name, elements):
        if not self.matchingPattern.match(name): return False;
        selfElems = self.componentExtraction(name);
        for k in selfElems.keys():
            if k in elements.keys():
                if not selfElems[k] in elements[k]:
                    return False
        return True

    def componentExtraction(self, name):
        output = {}
        result = self.elementPattern.search(name)
        if result == None:
            return output
        for k in self.elementGroups.keys():
            output[k] = result.group(int(self.elementGroups[k]))
        return  output


    @staticmethod
    def buildRecognizers():
        tree = ET.parse(XmlFileRecognizer.configFile)
        root = tree.getroot()
        XmlFileRecognizer.recognizers = []
        for fileRecognizer in root.iter("FileRecognizer"):
            XmlFileRecognizer.recognizers.append(XmlFileRecognizer(fileRecognizer))

    @staticmethod
    def findRecognizerByName(name):
        options = list(filter(lambda x: str(x) == name, XmlFileRecognizer.recognizers))
        if len(options) > 1:
            print("I'm confused, multiple recognizers have the name " + name)
        if len(options) == 0: return None
        return options[0]

    @staticmethod
    def recognizeBatch(files, definitionFile):
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




class FileTypeCV2(FileRecognizer):

    def validFile(name, elements=None):
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