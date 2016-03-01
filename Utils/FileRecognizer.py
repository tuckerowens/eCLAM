
import re
from dateutil.parser import parse

class FileRecognizer:

    @staticmethod
    def validFile(name, elements):
        return False

    @staticmethod
    def componentExtraction(name):
        return {}


class FileTypeCV2(FileRecognizer):

    @staticmethod
    def validFile(name, elements):
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


    @staticmethod
    def componentExtraction(name):
        elems = re.search("([0-9]+)\s([A-Z]+)\s([1-9][0-9]+[n|u|m]M)\s([1-9]+)\s([A-F]+)\s([0-9]+)\s+CV2_#([0-9]+).DTA", name)
        output = {}
        output["Date"] = parse(elems.group(0))
        output["Chem"] = elems.group(1)
        output["Concentration"] = elems.group(2)
        output["trial"] = int(elems.group((3)))
        output["scientist"] = elems.group(4)
        output["idk"] = elems.group(5)
        output["fileno"] = int(elems.group(6))
        return output