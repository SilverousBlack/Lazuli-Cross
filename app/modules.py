from argparse import ArgumentError
from io import open
import pathlib as pl
from PIL import Image
import sys
import utility

conf_search = ["meta/config.conf", 
               "app/meta/config.conf", 
               "G:/Git/Lazuli-Cross/app/meta/config.config"]

config_path: pl.Path
for conf in conf_search:
    if pl.Path(conf).exists():
        config_path = conf

config = open(config_path, "r")
options = (config.read()).split("\n")
yolodir: str
dmodeldir: str
tmodeldir: str
tempdir: str
resmode: str
ressz: int
detect_commands = ""
test_commands = ""

for opt in options:
    if (opt.split(" "))[0] == "yolodir:":
        yolodir = " ".join((opt.split(" "))[1:]) if len(opt) > 2 else (opt.split(" "))[1:]
    elif (opt.split(" "))[0] == "tempdir:":
        tempdir = " ".join((opt.split(" "))[1:]) if len(opt) > 2 else (opt.split(" "))[1:]
    elif (opt.split(" "))[0] == "resolutionmode:":
        resmode = opt.split(" ")[1]
    elif (opt.split(" "))[0] == "resolutionmaxwidth:":
        if resmode == "max-width":
            ressz = int(opt.split(" ")[1])
    elif (opt.split(" "))[0] == "resolutionmaxheight:":
        if resmode == "max-height":
            ressz = int(opt.split(" ")[1])
    elif (opt.split(" "))[0] == "autoresolution:":
        if resmode == "auto":
            ressz = int(opt.split(" ")[1])
    elif (opt.split(" "))[0] == "detectmodeldir:":
        dmodeldir = " ".join((opt.split(" "))[1:]) if len(opt) > 2 else (opt.split(" "))[1:]
    elif (opt.split(" "))[0] == "testmodeldir:":
        tmodeldir = " ".join((opt.split(" "))[1:]) if len(opt) > 2 else (opt.split(" "))[1:]
    elif (opt.split(" "))[0] == "detectmodeltargets:":
        temp = detect_commands + "--weights"
        for i in (opt.split(" "))[1:]:
            del detect_commands
            detect_commands = temp + " " + dmodeldir + "/" + i
            del temp
            temp = detect_commands
    elif (opt.split(" "))[0] == "testmodeltargets:":
        temp = test_commands + "--weights"
        for i in (opt.split(" "))[1:]:
            del test_commands
            test_commands = temp + " " + tmodeldir + "/" + i
            del temp
            temp = test_commands
    elif (opt.split(" "))[0] == "detectoverride:":
        temp = detect_commands + " ".join(opt.split(" "))[1:]
        del detect_commands
        detect_commands = temp
    elif (opt.split(" "))[0] == "testoverride:":
        temp = test_commands + " ".join(opt.split(" "))[1:]
        del test_commands
        test_commands = temp
    elif (opt.split(" "))[0] in ["#", " ", "", "\n"]:
        pass
    else:
        raise RuntimeError()

config.close()

def capture(path):
    global resmode, ressz
    local = Image.open(path)
    if resmode == "full":
        pass
    elif resmode == "half":
        height, width = local.size
        local = local.resize((int(height // 2), int(width // 2)), Image.ANTIALIAS)
    elif resmode == "max-width":
        

def detect():
    pass

print()
