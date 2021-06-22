import numpy as np
import pandas as pd
import pathlib as pl
from PIL import Image, ImageOps, ImageEnhance, ImageFilter
from time import time_ns

targetimg = r"doc/assets/sample01.jpg"
outputimg = r"doc/assets/sample02.jpg"
outputcsv = r"doc/assets/samplestatistics.csv"
GlobalDataFrame = pd.DataFrame(columns=["Source", "Locus",
                                        "ORed", "OGreen", "OBlue",
                                        "IRed", "IGreen", "IBlue",
                                        "EdgeIntensity",
                                        "RRed", "RGreen", "RBlue"])
GlobalDataFrame = GlobalDataFrame.astype({"Source": "object","Locus": "int64",
                                          "ORed": "int64", "OGreen": "int64", "OBlue": "int64",
                                          "IRed": "int64", "IGreen": "int64", "IBlue": "int64",
                                          "EdgeIntensity": "int64",
                                          "RRed": "int64", "RGreen": "int64", "RBlue": "int64"})
if pl.Path(outputcsv).exists():
    GlobalDataFrame = pd.DataFrame(pd.read_csv(outputcsv))
GlobalDataFrame = GlobalDataFrame.set_index("Source", "Locus")

def GetLocus(x, y, xmax, ymax):
    xbuf = "0" + "0" * (len(str(xmax)) - len(str(x))) + str(x)
    ybuf = "0" + "0" * (len(str(ymax)) - len(str(y))) + str(y)
    return xbuf + ybuf

def ImprovedSecondDerivativeEdgeDetection(target: Image.Image):
    width, height = target.size
    blur_radius = int((min(width, height) * 0.05) if (min(width, height) * 0.05) > 0 else (min(width, height) * 0.1))
    copy = target.filter(ImageFilter.UnsharpMask(blur_radius)).filter(ImageFilter.GaussianBlur(blur_radius))
    copy = (ImageEnhance.Contrast(target).enhance(1.75)).filter(ImageFilter.FIND_EDGES).convert("LA")
    copy = np.array(copy, np.uint32)[:, :, 0]
    edgepx = copy[:, :].max() + 1
    # edge denoising routine
    #for i in range(height):
    #    for j in range(width):
    #        if copy[i, j] >= (edgepx * 0.5):
    #            copy[i, j] = 255
    #        elif (edgepx * 0.25) <= copy[i, j] < (edgepx * 0.5):
    #            copy[i, j] = 127
    #        elif (edgepx * 0.125) <= copy[i, j] < (edgepx * 0.25):
    #            copy[i, j] = 63
    #        else:
    #           copy[i, j] = 0
    copy[copy >= (edgepx * 0.5)] = 255
    copy[(copy >= (edgepx * 0.25)) & (copy < edgepx * 0.5)] = 127
    copy[(copy >= (edgepx * 0.125)) & (copy < (edgepx * 0.25))] = 63
    copy[copy < (edgepx * 0.125)] = 0
    # probability edge enhancement with edge denoising
    internal = np.zeros((height, width), np.uint32)
    for i in range(height):
        for j in range(width):
            density_prob = 0.0
            try:
                density_prob += ((copy[i - 1, j - 1] + 1) // 64) / 4
                density_prob += ((copy[i, j - 1] + 1) // 64) / 4
                density_prob += ((copy[i + 1, j - 1] + 1) // 64) / 4
                density_prob += ((copy[i - 1, j] + 1) // 64) / 4
                density_prob += ((copy[i, j] + 1) // 64) / 4
                density_prob += ((copy[i + 1, j] + 1) // 64) / 4
                density_prob += ((copy[i - 1, j + 1] + 1) // 64) / 4
                density_prob += ((copy[i, j + 1] + 1) // 64) / 4
                density_prob += ((copy[i + 1, j + 1] + 1) // 64) / 4
            except:
                pass
            if density_prob >= 3:
                internal[i, j] = 255
            elif 2 <= density_prob < 3:
                internal[i, j] = 127
            elif 1 <= density_prob < 2:
                internal[i, j] = 63
            else:
                internal[i, j] = 0
    internal = np.expand_dims(internal, axis=2)
    internal = np.insert(internal, 1, 255, axis=2).astype('uint8')
    internal = Image.fromarray(internal, 'LA')
    return internal.copy()

if not pl.Path(targetimg).exists():
    print("Target image not found")
    print("Exiting.")
    exit()
capture = Image.open(targetimg).convert("RGB")
print("Applying Improved Second Derivative Edge Detection...", end="\r")
edges = ImprovedSecondDerivativeEdgeDetection(capture)
print(" " * 90, end="\r")
print("Improved Second Derivative Edge Detection Applied")
height, width = capture.size
print("Image Size: {}px x {}px".format(height, width))
invr = np.array(ImageOps.invert(capture), np.uint32)
copy = np.array(capture, np.uint32)
edges = np.array(edges, np.uint32)[:, :, 0]
height, width, depth = copy.shape
internal = np.zeros((height, width, depth), np.uint32)
start = time_ns() 
for i in range(height):
    for j in range(width):
        locus = GetLocus(i, j, height, width)
        result = {"Locus": int(locus), "Source": targetimg}
        buf = copy[i, j] * 0.25
        if edges[i, j] == 127:
            buf *= 2
        elif edges[i, j] == 64:
            buf *= 3
        elif edges[i, j] == 0:
            buf *= 4
        result["EdgeIntensity"] = edges[i, j]
        result["ORed"] = buf[0]
        result["OGreen"] = buf[1]
        result["OBlue"] = buf[2]
        result["IRed"] = invr[i, j, 0]
        result["IGreen"] = invr[i, j,1]
        result["IBlue"] = invr[i, j, 2]
        buf = 255 - (buf + (np.max(buf) - buf)) + abs(np.max(invr[i, j]) - np.max(buf))
        result["RRed"] = buf[0]
        result["RGreen"] = buf[1]
        result["RBlue"] = buf[2]
        internal[i, j] = buf.astype("uint32")
        print("{}: {:.2f}s".format(locus, ((time_ns() - start) / 1000000000)), end="\r")
        GlobalDataFrame = GlobalDataFrame.append(result, ignore_index=True)
print("Processed {0}px x {1}px ({2}) in {3:.2f}s".format(width, height, height * width, ((time_ns() - start) / 1000000000)))
internal = Image.fromarray(internal.astype("uint8"), "RGB")
internal.save(outputimg, "JPEG")
GlobalDataFrame.to_csv(outputcsv, index=False)
