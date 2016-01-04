
import os, DatasetCV2

def _identify_file(file):
    filetypes = [
        "CV2",
        "CV1"
    ]
    for t in filetypes:
        if t in file:
            return t
    return "Unknown"

def buildDataset(directory, filetype=""):
    onlyfiles = os.listdir(directory)
    files = {}
    for f in onlyfiles:
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







