import os
import pathlib as pl

targetimages = r"G:/Git/images/train"
targetlabels = r"G:/Git/labels/train"

targets = os.listdir(targetimages)

for i in targets:
    j = targetlabels + "/" + (os.path.splitext(i))[0] + ".txt"
    if not pl.Path(j).exists(): 
        print("File [{}] does not exist".format(j))
print("done!")
