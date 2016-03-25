

import urllib.request as urlreq
from zipfile import ZipFile


VERSION_FILE = "version.txt"

def getCurrentVersion():
    return Version()

def setVersion(version):
    vf = open(VERSION_FILE, 'w')
    vf.write(version)
    vf.close()
    return version


class Version:
    def getCurrentVersion(self):
        vf = open(VERSION_FILE, 'r')
        version = vf.read()
        vf.close()
        return version
    def __str__(self, *args, **kwargs):
        return self.getCurrentVersion()

    def update(self):
        zip = open("resources/master.zip", "wb")
        with urlreq.urlopen("http://github.com/tuckerowens/eCLAM/archive/master.zip") as f:
            zip.write(f.read())
        zip.close()
        zip = ZipFile()
        zip.open("resources/master.zip")
        zip.extractall()
