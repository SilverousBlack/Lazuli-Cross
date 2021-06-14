import argparse
from io import open
import os
import pathlib as pl
from PIL import Image
from shutil import rmtree
import sys
from importlib import import_module

print("Resolving configuration.", end="\r")

imgproc = import_module("utility.image_process")
yolodetect: None

conf_search = [str(pl.Path(__file__).absolute().parent) + "/meta/config.conf",
               "meta/config.conf", 
               "app/meta/config.conf", 
               "G:/Git/Lazuli-Cross/app/meta/config.config",
               str(pl.Path(__file__).absolute().parent) + "/meta/default.conf"] # automatically includes default configuration

config_path: pl.Path
for conf in conf_search:
    if pl.Path(conf).exists():
        config_path = conf
        break

del conf_search

print(" " * 50, end="\r")
print("Reading configuration file...", end="\r")
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
        temp = detect_commands + " " + " ".join(opt.split(" ")[1:])
        del detect_commands
        detect_commands = temp
    elif (opt.split(" "))[0] == "testoverride:":
        temp = test_commands + " " + " ".join(opt.split(" ")[1:])
        del test_commands
        test_commands = temp
    elif (opt.split(" "))[0] in ["#", " ", "", "\n"]:
        pass
    else:
        raise RuntimeError()
config.close()
del config
print("Reading configuration file... OK", end="\r")
print(" " * 50, end="\r")

print("Checking directories...", end="\r")
if not pl.Path(yolodir).exists():
    raise FileExistsError("YOLO directory path [{}] does not exist in your system".format(yolodir))
elif not pl.Path(yolodir + "/detect.py").exists():
    raise FileExistsError("YOLO detection algorithm path [{}] does not exist in your system".format(yolodir + "/detect.py"))
else:
    sys.path.append(yolodir)
    yolodetect = import_module("detect")
    del yolodir
if not pl.Path(tempdir).exists():
    pl.Path(tempdir).mkdir()
if not pl.Path(tempdir + "/detected").exists():
    pl.Path(tempdir + "/detected").mkdir()
print("Checking directories... OK", end="\r")
print(" " * 50, end="\r")

temp = detect_commands + " --exist-ok --project " + tempdir + " --name detected"
del detect_commands
detect_commands = temp
del temp
temp = test_commands + " --exist-ok --project" + tempdir + " --name detected" + " --view-img"

# Argument Parser copy from the detect.py located at the YOLO directory
# modify accordingly if other YOLO detection algorithm implementation is used
# presently resonates to @ultralytics YOLO implementation 
parser = argparse.ArgumentParser()
parser.add_argument('--weights', nargs='+', type=str, default='yolov5s.pt', help='model.pt path(s)')
parser.add_argument('--source', type=str, default='data/images', help='file/dir/URL/glob, 0 for webcam')
parser.add_argument('--imgsz', '--img', '--img-size', type=int, default=640, help='inference size (pixels)')
parser.add_argument('--conf-thres', type=float, default=0.25, help='confidence threshold')
parser.add_argument('--iou-thres', type=float, default=0.45, help='NMS IoU threshold')
parser.add_argument('--max-det', type=int, default=1000, help='maximum detections per image')
parser.add_argument('--device', default='', help='cuda device, i.e. 0 or 0,1,2,3 or cpu')
parser.add_argument('--view-img', action='store_true', help='show results')
parser.add_argument('--save-txt', action='store_true', help='save results to *.txt')
parser.add_argument('--save-conf', action='store_true', help='save confidences in --save-txt labels')
parser.add_argument('--save-crop', action='store_true', help='save cropped prediction boxes')
parser.add_argument('--nosave', action='store_true', help='do not save images/videos')
parser.add_argument('--classes', nargs='+', type=int, help='filter by class: --class 0, or --class 0 2 3')
parser.add_argument('--agnostic-nms', action='store_true', help='class-agnostic NMS')
parser.add_argument('--augment', action='store_true', help='augmented inference')
parser.add_argument('--update', action='store_true', help='update all models')
parser.add_argument('--project', default='runs/detect', help='save results to project/name')
parser.add_argument('--name', default='exp', help='save results to project/name')
parser.add_argument('--exist-ok', action='store_true', help='existing project/name ok, do not increment')
parser.add_argument('--line-thickness', default=3, type=int, help='bounding box thickness (pixels)')
parser.add_argument('--hide-labels', default=False, action='store_true', help='hide labels')
parser.add_argument('--hide-conf', default=False, action='store_true', help='hide confidences')
parser.add_argument('--half', action='store_true', help='use FP16 half-precision inference')

def  flush():
    if pl.Path(tempdir + "/target.jpg").exists():
        os.remove(tempdir + "/target.jpg")
    loc = tempdir + "/detected"
    floc = os.listdir(tempdir + "/detected")
    for i in floc:
        if pl.Path(loc + "/" + i).is_file():
            os.remove(loc + "/" + i)
        elif pl.Path(loc + "/" + i).is_dir():
            rmtree(loc + "/" + i)
        
print("Cleaning temporary directory...", end="\r")
flush()
print("Cleaning temporary directory... OK", end="\r")
print(" " * 50, end="\r")

def capture(path):
    global resmode, ressz, detect_commands
    flush()
    name, extension = os.path.splitext(path)
    del name
    if not extension in [".png", ".jpg", ".jpeg"]:
        raise Exception("Only PNG and JPEG file types are allowed.")
    local = Image.open(path)
    if resmode == "full":
        pass
    elif resmode == "half":
        height, width = local.size
        local = local.resize((int(height // 2), int(width // 2)), Image.ANTIALIAS)
    elif resmode == "max-width":
        height, width = local.size
        ratio = height / width
        newh = int(ressz * ratio)
        local = local.resize((newh, ressz), Image.ANTIALIAS)
    elif resmode == "max-height":
        height, width = local.size
        ratio = width / height
        neww = int(ressz * ratio)
        local = local.resize((ressz, neww), Image.ANTIALIAS)
    elif resmode == "auto":
        height, width = local.size
        ratio = min(height, width) / max(height, width)
        newh = ressz if height >= width else ressz * ratio
        neww = ressz if width >= height else ressz * ratio
    local.convert("RGB")
    local.save(tempdir + "/target.jpg", "JPEG")
    temp = detect_commands
    del detect_commands
    detect_commands = temp + " --source " + tempdir + "/target.jpg"
    
def detect():
    global detect_commands
    dopt = parser.parse_known_args(detect_commands.split(" "))
    yolodetect.detect(**vars(dopt))

def test():
    topt = parser.parse_known_args((test_commands + " --source" + tempdir + "/detected/test").split(" "))
    loc = tempdir + "/detected/crops/Facemask"
    if not pl.Path(loc).exists():
        print("Found no detected supported images [class=\'Facemask\'] to test.")
    else:
        pl.Path(tempdir + "/detected/test").mkdir()
        floc = os.listdir(loc)
        print("Found {} detected supported images".format(len(floc)))
        print("Processing...", end="\r")
        for i in floc:
            print("Processing {}... ".format(i), end="\r")
            capture = Image.open(loc + "/" + i)
            edges = imgproc.ImprovedSecondOrderEdgeDetection(capture)
            deisolated, sample = imgproc.ColorDeisolationRoutine(capture, edges)
            deisolated.save(tempdir + "/detected/test/deisolated_" + i, "JPEG")
            sample.save(tempdir + "/detected/test/sample_" + i, "JPEG")
            print("Processing {}... OK".format(i), end="\r")
        print("Finished Processing Images")
        yolodetect.detect(**vars(topt))

print(" " * 50, end="\r")
print("Configuration resolved [{}]".format(str(pl.Path(config_path).relative_to(os.getcwd()))))
