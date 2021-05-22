# Image Process Testing Routine
# Not part of application, for research purposes only (comparison and algorithm testing)

import math
import random
import numpy as np
from numpy.lib.shape_base import expand_dims
import scipy as sp

# numerical manipulation and tensors
import pandas as pd

# image manipulation
from PIL import Image, ImageFilter, ImageEnhance, ImageOps
from scipy import ndimage

# file paths
import pathlib as pl
import os
import ntpath as ntp

# threading
from threading import Thread

# timing
from time import time_ns 

# argument parsing
import argparse as ap

# variable functions to be tested
import canny_edge_detection_fensiop as ced
import image_process as ip

GlobalDataFrame = pd.DataFrame(columns=["Name", "Process", "CaptureTime", "EdgesTime", "DeisolationTime", "TotalTime", "Author"])
GlobalDataFrame = GlobalDataFrame.astype({"Name":"object", "Process":"object", "CaptureTime":"float64", "EdgesTime":"float64", "DeisolationTime":"float64", "TotalTime":"float64", "Author":"object"})

def basic_routine(target: str, author: str):
    global GlobalDataFrame
    local = os.path.dirname(os.path.realpath(__file__)) + "\\results\\"
    result = {}
    result["Name"] = str(ntp.basename(target))[0:-(len(os.path.splitext(target)) + 2)]
    result["Process"] = "CED"
    start = time_ns()
    capture = Image.open(target)
    img_h, img_w = capture.size
    max_s = max(img_h, img_w)
    ratio = 1 / (max_s // 1000)
    capture = capture.resize((int(img_h * ratio), int(img_w * ratio)), Image.ANTIALIAS)
    capture.save(local +  "capture_" + result["Process"] + "_" + result["Name"] + ".jpg", "JPEG")
    result["CaptureTime"] = (time_ns() - start) / 1000000000
    end = time_ns()
    detector = ced.cannyEdgeDetector([np.array(capture.convert("LA"))[:, :, 0]])
    edges = detector.detect()[0]
    edges = np.expand_dims(edges, axis=2)
    edges = np.insert(edges, 1, 255, axis=2).astype('uint8')
    edges = Image.fromarray(edges, "LA")
    edges.save(local + "edges_" + result["Process"] + "_" + result["Name"] + ".png", "PNG")
    result["EdgesTime"] = (time_ns() - end) / 1000000000
    end = time_ns()
    deisolated, sample = ip.ColorDeisolateRoutine(capture, edges)
    deisolated.save(local + "deisolated_" + result["Process"] + "_" + result["Name"] + ".jpg", "JPEG")
    sample.save(local + "sample_" + result["Process"] + "_" + result["Name"] + ".jpg", "JPEG")
    result["DeisolationTime"] = (time_ns() - end) / 1000000000
    result["TotalTime"] = (time_ns() - start) / 1000000000
    result["Author"] = author
    GlobalDataFrame = GlobalDataFrame.append(result, ignore_index=True)
    
def basic_2d_routine(target: str, author: str):
    global GlobalDataFrame
    local = os.path.dirname(os.path.realpath(__file__)) + "\\results\\"
    result = {}
    result["Name"] = str(ntp.basename(target))[0:-(len(os.path.splitext(target)) + 2)]
    result["Process"] = "B2D"
    start = time_ns()
    capture = Image.open(target)
    img_h, img_w = capture.size
    max_s = max(img_h, img_w)
    ratio = 1 / (max_s // 1000)
    capture = capture.resize((int(img_h * ratio), int(img_w * ratio)), Image.ANTIALIAS)
    capture.save(local +  "capture_" + result["Process"] + "_" + result["Name"] + ".jpg", "JPEG")
    result["CaptureTime"] = (time_ns() - start) / 1000000000
    end = time_ns()
    edges = capture.filter(ImageFilter.FIND_EDGES).convert("LA")
    edges.save(local + "edges_" + result["Process"] + "_" + result["Name"] + ".png", "PNG")
    result["EdgesTime"] = (time_ns() - end) / 1000000000
    end = time_ns()
    deisolated, sample = ip.ColorDeisolateRoutine(capture, edges)
    deisolated.save(local + "deisolated_" + result["Process"] + "_" + result["Name"] + ".jpg", "JPEG")
    sample.save(local + "sample_" + result["Process"] + "_" + result["Name"] + ".jpg", "JPEG")
    result["DeisolationTime"] = (time_ns() - end) / 1000000000
    result["TotalTime"] = (time_ns() - start) / 1000000000
    result["Author"] = author
    GlobalDataFrame = GlobalDataFrame.append(result, ignore_index=True)

def filtered_2d_routine(target: str, author: str):
    global GlobalDataFrame
    local = os.path.dirname(os.path.realpath(__file__)) + "\\results\\"
    result = {}
    result["Name"] = str(ntp.basename(target))[0:-(len(os.path.splitext(target)) + 2)]
    result["Process"] = "F2D"
    start = time_ns()
    capture = Image.open(target)
    img_h, img_w = capture.size
    max_s = max(img_h, img_w)
    ratio = 1 / (max_s // 1000)
    capture = capture.resize((int(img_h * ratio), int(img_w * ratio)), Image.ANTIALIAS)
    capture.save(local +  "capture_" + result["Process"] + "_" + result["Name"] + ".jpg", "JPEG")
    result["CaptureTime"] = (time_ns() - start) / 1000000000
    end = time_ns()
    edges = (ImageEnhance.Contrast(capture).enhance(1.75)).filter(ImageFilter.FIND_EDGES).convert("LA")
    edges.save(local + "edges_" + result["Process"] + "_" + result["Name"] + ".png", "PNG")
    result["EdgesTime"] = (time_ns() - end) / 1000000000
    end = time_ns()
    deisolated, sample = ip.ColorDeisolateRoutine(capture, edges)
    deisolated.save(local + "deisolated_" + result["Process"] + "_" + result["Name"] + ".jpg", "JPEG")
    sample.save(local + "sample_" + result["Process"] + "_" + result["Name"] + ".jpg", "JPEG")
    result["DeisolationTime"] = (time_ns() - end) / 1000000000
    result["TotalTime"] = (time_ns() - start) / 1000000000
    result["Author"] = author
    GlobalDataFrame = GlobalDataFrame.append(result, ignore_index=True)
    
def improved_2d_routine(target: str, author: str):
    global GlobalDataFrame
    local = os.path.dirname(os.path.realpath(__file__)) + "\\results\\"
    result = {}
    result["Name"] = str(ntp.basename(target))[0:-(len(os.path.splitext(target)) + 2)]
    result["Process"] = "I2D"
    start = time_ns()
    capture = Image.open(target)
    img_h, img_w = capture.size
    max_s = max(img_h, img_w)
    ratio = 1 / (max_s // 1000)
    capture = capture.resize((int(img_h * ratio), int(img_w * ratio)), Image.ANTIALIAS)
    capture.save(local +  "capture_" + result["Process"] + "_" + result["Name"] + ".jpg", "JPEG")
    result["CaptureTime"] = (time_ns() - start) / 1000000000
    end = time_ns()
    edges = ip.ImprovedSecondDerivativeEdgeDetection(capture)
    edges.save(local + "edges_" + result["Process"] + "_" + result["Name"] + ".png", "PNG")
    result["EdgesTime"] = (time_ns() - end) / 1000000000
    end = time_ns()
    deisolated, sample = ip.ColorDeisolateRoutine(capture, edges)
    deisolated.save(local + "deisolated_" + result["Process"] + "_" + result["Name"] + ".jpg", "JPEG")
    sample.save(local + "sample_" + result["Process"] + "_" + result["Name"] + ".jpg", "JPEG")
    result["DeisolationTime"] = (time_ns() - end) / 1000000000
    result["TotalTime"] = (time_ns() - start) / 1000000000
    result["Author"] = author
    GlobalDataFrame = GlobalDataFrame.append(result, ignore_index=True)

def main(author: str):
    global GlobalDataFrame
    var = os.path.dirname(os.path.realpath(__file__))
    targets = os.listdir(var + "\\var\\")
    for target in targets:
        cedthr = Thread(target=basic_routine, args=(var + "\\var\\" + target,), kwargs={"author": author})
        b2dthr = Thread(target=basic_2d_routine, args=(var + "\\var\\" + target,), kwargs={"author": author})
        f2dthr = Thread(target=filtered_2d_routine, args=(var + "\\var\\" + target,), kwargs={"author": author})
        i2dthr = Thread(target=improved_2d_routine, args=(var + "\\var\\" + target,), kwargs={"author": author})
        cedthr.start()
        b2dthr.start()
        f2dthr.start()
        i2dthr.start()
        cedthr.join()
        b2dthr.join()
        f2dthr.join()
        i2dthr.join()
    
argparser = ap.ArgumentParser("Process Routine", description="A Routined Comparation of Processing Techniques")
argparser.add_argument("--author", nargs=1, help="Specify the routine result author")

if __name__ == "__main__":
    res = argparser.parse_args()
    author: str
    if hasattr(res, "AUTHOR"):
        author = res.AUTHOR
    else:
        author = input("Please enter result authorship name: ")
    main(author)
    print(GlobalDataFrame.head())
    GlobalDataFrame.to_csv("process_routine_results.csv", index=False)
    input("Press [Enter] to continue...")
