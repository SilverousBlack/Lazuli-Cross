import os
from PIL import Image
import pathlib as pl
from random import randint

targetdir = r"G:/Git/Lazuli-Cross-Filter-Material-Density-Dataset/images"
outputdir = r"G:/Git/Lazuli-Cross-Filter-Material-Density-Dataset/temp"

if not pl.Path(targetdir).exists():
    raise Exception("Target directory does not exists.")
if not pl.Path(outputdir).exists():
    pl.Path(outputdir).mkdir()

targets = []
for i in os.listdir(targetdir):
    if pl.Path(targetdir + "/" + i).is_file():
        targets.append(i)

compressiontarget = 1024 # maximum length of either height or width of the image
totaltargetcount = len(targets)

def getcountstring(count: int):
    global totaltargetcount
    internal = str(count)
    while len(internal) < len(str(totaltargetcount * 12)):
        buf = internal
        del internal
        internal = "0" + buf
        del buf
    return str("0" + internal)

count = 1

while len(targets) > 0:
    i = randint(0, len(targets) - 1)
    capture = Image.open(targetdir + "/" + targets[i])
    height, width = capture.size
    ratio = min(height, width) / max(height, width)
    newh = compressiontarget if height > width else int(compressiontarget * ratio)
    neww = compressiontarget if width > height else int(compressiontarget * ratio)
    var = getcountstring(count)
    # angle: 0
    capture = capture.resize((newh, neww), Image.ANTIALIAS)
    capture.save("{0}/lazulicross_{1}.jpg".format(outputdir, var), "JPEG")
    del var
    count += 1
    var = getcountstring(count)
    (capture.transpose(Image.FLIP_LEFT_RIGHT)).save("{0}/lazulicross_{1}.jpg".format(outputdir, var), "JPEG")
    del var
    count += 1
    var = getcountstring(count)
    (capture.transpose(Image.FLIP_TOP_BOTTOM)).save("{0}/lazulicross_{1}.jpg".format(outputdir, var), "JPEG")
    # angle: 90
    capture = capture.transpose(Image.ROTATE_90)
    del var
    count += 1
    var = getcountstring(count)
    capture.save("{0}/lazulicross_{1}.jpg".format(outputdir, var), "JPEG")
    del var
    count += 1
    var = getcountstring(count)
    (capture.transpose(Image.FLIP_LEFT_RIGHT)).save("{0}/lazulicross_{1}.jpg".format(outputdir, var), "JPEG")
    del var
    count += 1
    var = getcountstring(count)
    (capture.transpose(Image.FLIP_TOP_BOTTOM)).save("{0}/lazulicross_{1}.jpg".format(outputdir, var), "JPEG")
    # angle: 180
    capture = capture.transpose(Image.ROTATE_90)
    del var
    count += 1
    var = getcountstring(count)
    capture.save("{0}/lazulicross_{1}.jpg".format(outputdir, var), "JPEG")
    del var
    count += 1
    var = getcountstring(count)
    (capture.transpose(Image.FLIP_LEFT_RIGHT)).save("{0}/lazulicross_{1}.jpg".format(outputdir, var), "JPEG")
    del var
    count += 1
    var = getcountstring(count)
    (capture.transpose(Image.FLIP_TOP_BOTTOM)).save("{0}/lazulicross_{1}.jpg".format(outputdir, var), "JPEG")
    # angle: 270
    capture = capture.transpose(Image.ROTATE_90)
    del var
    count += 1
    var = getcountstring(count)
    capture.save("{0}/lazulicross_{1}.jpg".format(outputdir, var), "JPEG")
    del var
    count += 1
    var = getcountstring(count)
    (capture.transpose(Image.FLIP_LEFT_RIGHT)).save("{0}/lazulicross_{1}.jpg".format(outputdir, var), "JPEG")
    del var
    count += 1
    var = getcountstring(count)
    (capture.transpose(Image.FLIP_TOP_BOTTOM)).save("{0}/lazulicross_{1}.jpg".format(outputdir, var), "JPEG")
    print("{0}: Original: {1}:{2} ({3} {4:.2f}) | Output: {5}:{6} ({7} {8:.2f}) | Verity: {9}".format(var,
                                                                                                      height, width, height * width, height / width,
                                                                                                      newh, neww, newh * neww, newh / neww,
                                                                                                      (round(height / width, 2) == round(newh / neww, 2))))
    count += 1
    targets.pop(i)
print("Done!")
