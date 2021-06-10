import os
from math import sqrt
from PIL import Image
import random
from shutil import copyfile

targetdir = "app/data/facemask/load"
outputdir = "app/data/facemask/temp"

targets = os.listdir(targetdir)
for i in targets:
    if not i.endswith(".jpg") or os.path.isdir(targetdir + "/" + i):
        targets.remove(i)

if not os.path.exists(outputdir):
    os.makedirs(outputdir)
    
compressiontarget = 1000000 # image size in square pixels
totaltargetcount = len(targets)

def getcountstring(count: int):
    global totaltargetcount
    internal = str(count)
    while len(internal) < len(str(totaltargetcount)):
        buf = internal
        del internal
        internal = "0" + buf
        del buf
    return str("0" + internal)

count = 1

while len(targets) > 0:
    i = random.randint(0, len(targets) - 1)
    capture = Image.open(targetdir + "/" + targets[i])
    height, width = capture.size
    maxlen = int(sqrt(compressiontarget) / (min(height, width) / max(height, width)))
    minlen = int(sqrt(compressiontarget) / (max(height, width) / max(height, width)))
    newh = maxlen if height > width else minlen
    neww = maxlen if width > height else minlen
    var = getcountstring(count)
    capture = capture.resize((newh, neww), Image.ANTIALIAS)
    capture.save("{0}/lazulicross_{1}.jpg".format(outputdir, var), "JPEG")
    print("{0}: Original: {1}:{2} ({3} {4:.2f}) | Output: {5}:{6} ({7} {8:.2f}) | Verity: {9}".format(var,
                                                                                                      height, width, height * width, height / width,
                                                                                                      newh, neww, newh * neww, newh / neww,
                                                                                                      (round(height / width, 2) == round(newh / neww, 2))))
    count += 1
    targets.pop(i)
print("done")
