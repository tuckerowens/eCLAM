
######################################################################
## Imports
######################################################################

import os, DatasetCV2, Multiset, MultisetCV2

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

def buildDataset(files, info):
    """

    @param directory:
    @param filetype:
    @return
    """
    print(info)

    if info["recognizer"] == "CV2":
        return DatasetCV2.DatasetCV2(files, info=info)
    elif info["recognizer"] == "Unknown":
        raise Exception("Unknown file type")
    else:
        raise Exception("DatasetFactory: What just happened?!")

def buildMultiset(filetype=""):
    """

    @param directory:
    @param filetype:
    @return
    """
    multiset = Multiset.Multiset()
    return multiset






