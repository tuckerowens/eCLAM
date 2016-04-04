
######################################################################
## Imports
######################################################################

import os, DatasetCV2,Multiset, MultisetCV2

######################################################################
## DatasetFactory
######################################################################

def _identify_file(file):
    """

    @param file:
    @return
    """
    filetypes = [
        "CV2",
        "CV1"
    ]
    for t in filetypes:
        if t in file:
            return t
    return "Unknown"

def buildDataset(directory, filetype=""):
    """

    @param directory:
    @param filetype:
    @return
    """
    onlyfiles = os.listdir(directory)
    print(onlyfiles)
    files = {}
    for f in onlyfiles:
        if _identify_file(f) == "Unknown": continue
        if _identify_file(f) in files.keys():
            files[_identify_file(f)].append(f)
        else:
            files[_identify_file(f)] = [f]
    classType = ""
    if len(files.keys()) > 1:
        if filetype != "":
            if filetype in files.keys():
                classType = filetype
            else:
                raise Exception("File type was not found")
        else:
            raise Exception("More than one file extension found")
    else:
        print(files.keys())
        classType = list(files.keys())[0]

    if classType == "CV2":
        return DatasetCV2.DatasetCV2(directory)
    elif classType == "Unknown":
        raise Exception("Unknown file type")
    else:
        raise Exception()

def buildMultiset(filetype=""):
    """

    @param directory:
    @param filetype:
    @return
    """
    multiset = Multiset.Multiset()
    return multiset






