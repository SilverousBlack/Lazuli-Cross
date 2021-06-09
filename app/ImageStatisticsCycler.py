import argparse as ap
import concurrent.futures as fut
import getpass as gp
import numpy as np
import os
import pathlib as pl
import pandas as pd
from PIL import Image, ImageEnhance, ImageFilter, ImageOps
import sys
from time import sleep, time_ns

CurrentUser = gp.getuser()
bar = "===== ===== ===== ===== ===== ====="
GlobalDataFrame: pd.DataFrame
GlobalProcessPool: fut.ProcessPoolExecutor

parser = ap.ArgumentParser(prog="Image Process Cycler",
                              description="Cycles through images in target folder")
parser.add_argument("-target_folder", type=str,
                       metavar="TF", nargs="+",
                       help="Folder containing images to be processed.")
parser.add_argument("-output_folder", type=str,
                       metavar="OF", nargs="+",
                       help="Folder destination of processed images.")
parser.add_argument("-statistics_path", type=str,
                       metavar="SP", nargs="+",
                       help="File location for recorded statistics.")
parser.add_argument("-author", type=str,
                       metavar="AU", nargs="+", default=CurrentUser,
                       help="Statistics authorship.")
parser.add_argument("-pool_limit", type=int,
                       metavar="TPL", default=int(os.cpu_count() // 2),
                       help="The limit of worker processes in the thread pool.")
parser.add_argument("--disregard_records",
                       action="store_true", default=False,
                       help="Disregard previously recorded statistics.")

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

def ColorDeisolationRoutine(target: Image.Image, edges: Image.Image):
    invr = np.array(ImageOps.invert(target), np.uint32)
    copy = np.array(target, np.uint32)
    edge = np.array(edges, np.uint32)[:, :, 0]
    height, width, depth = copy.shape
    internal = np.zeros((height, width, depth), np.uint32)
    for i in range(height):
        for j in range(width):
            buf = copy[i, j] * 0.25
            if edge[i, j] == 127:
                buf *= 2
            elif edge[i, j] == 64:
                buf *= 3
            elif edge[i, j] == 0:
                buf *= 4
            buf = (buf + (np.max(buf) - buf)) + abs(np.max(invr[i, j]) - np.max(buf))
            internal[i, j] = buf.astype("uint32")
    sampsz = int(min(height, width) // 2)
    internal = ImageOps.invert(Image.fromarray(internal.astype("uint8"), "RGB"))
    samp = (internal.crop(((width - sampsz) // 2, (height - sampsz) // 2, (width + sampsz) // 2, (height + sampsz) // 2))).resize((sampsz * 2, sampsz * 2), Image.ANTIALIAS)
    return (internal, samp)

def process(target, targetfolder: pl.Path, outputfolder: pl.Path, author: str):
    capture: Image.Image
    edges: Image.Image
    deisolated: Image.Image
    sample: Image.Image
    results = {"Target": target, "Author": author}
    start = time_ns()
    try: 
        capture = Image.open(str(targetfolder) + "/" + target)
        width, height = capture.size
        results["Width"] = width
        results["Height"] = height
        results["PixelCount"] = int(height * width)
        (capture.transpose(Image.ROTATE_270)).save(str(outputfolder) + "/capture_" + target, "JPEG" )
        edges = ImprovedSecondDerivativeEdgeDetection(capture)
        ((edges.transpose(Image.ROTATE_270)).convert("RGB")).save(str(outputfolder) + "/edges_" + target, "JPEG")
        deisolated, sample = ColorDeisolationRoutine(capture, edges)
        (deisolated.transpose(Image.ROTATE_270)).save(str(outputfolder) + "/deisolated_" + target, "JPEG")
        (sample.transpose(Image.ROTATE_270)).save(str(outputfolder) + "/sample_" + target, "JPEG")
    except Exception as e:
        results["Status"] = "Bad [%s]" % (str(e))
    else:
        results["Status"] = "Good"
    results["TotalTime"] = (time_ns() - start) / 1000000
    return results

def main(targetfolder: pl.Path, outputfolder: pl.Path, statistics_path: pl.Path, author: str):
    global GlobalDataFrame, GlobalProcessPool
    start = time_ns()
    targets = os.listdir(targetfolder)
    threads = {GlobalProcessPool.submit(process, target, targetfolder, outputfolder, author): target for target in targets}
    pending_work = len(GlobalProcessPool._pending_work_items)
    max_workers = GlobalProcessPool._max_workers
    pending = pending_work - max_workers if (pending_work - max_workers) >= 0 else 0
    ongoing = max_workers if pending_work >= max_workers else pending_work
    completed = len(targets) - (pending + ongoing)
    while (pending > 0 and ongoing > 0) and completed != len(targets):
        print(" " * 90, end="\r")
        print("Pending {0} of {1} images | Ongoing: {2} | Completed: {3} | Time: {4:.2f}".format(pending, len(targets), ongoing, completed, (time_ns() - start) / 1000000000), end="\r")
        pending_work = len(GlobalProcessPool._pending_work_items)
        max_workers = GlobalProcessPool._max_workers
        pending = pending_work - max_workers if (pending_work - max_workers) >= 0 else 0
        ongoing = max_workers if pending_work >= max_workers else pending_work
        completed = len(targets) - (pending + ongoing)
        sleep(0.5)
    for future in fut.as_completed(threads):
        thr = threads[future]
        result = {}
        try:
            result = future.result()
            GlobalDataFrame = GlobalDataFrame.append(result, ignore_index=True)
        except Exception as e:
            print("Process [%r] raised error: %s" % (thr, e))
    print(" " * 90, end="\r")
    print("Processed {0} images | Time: {1:.2f}".format(len(targets), (time_ns() - start) / 1000000000))
    GlobalDataFrame.to_csv(str(statistics_path), index=False)
    GlobalProcessPool.shutdown(wait=True, cancel_futures=False)

if __name__ == "__main__":
    print(bar)
    res = parser.parse_args()
    TF: pl.Path
    OF: pl.Path
    SP: pl.Path
    author = res.author if isinstance(res.author, str) else " ".join(res.author)
    TPL = res.pool_limit if res.pool_limit <= os.cpu_count() else os.cpu_count()
    GlobalProcessPool = fut.ProcessPoolExecutor(max_workers=TPL)
    if res.target_folder == None:
        TF = pl.Path(input("Input target folder path: "))
    else:
        TF = pl.Path(res.target_folder if isinstance(res.target_folder, str) else " ".join(res.target_folder))
    while not TF.exists():
        print("Target folder path does not exist. Please input a path that exists.")
        TF = pl.Path(input("Input new target folder location: "))
    if res.output_folder == None:
        OF = pl.Path(input("Input output folder path: "))
    else:
        OF = pl.Path(res.output_folder if isinstance(res.output_folder, str) else " ".join(res.output_folder))
    if res.statistics_path == None:
        SP = pl.Path(input("Input statistics file path: "))
    else:
        SP = pl.Path(res.statistics_path if isinstance(res.statistics_path, str) else " ".join(res.statistics_path))
    if not OF.exists(): 
        OF.mkdir()
    if not SP.parent.exists():
        SP.parent.mkdir()
    if SP.exists() and not res.disregard_records:
        GlobalDataFrame = pd.DataFrame(pd.read_csv(str(SP)))
    else:
        GlobalDataFrame = pd.DataFrame(columns=["Target", "Status",
                                                "Width", "Height", "PixelCount",
                                                "TotalTime", "Author"])
    GlobalDataFrame = GlobalDataFrame.astype({"Target": "object", "Status": "object",
                                              "Width": "int64", "Height": "int64", "PixelCount": "int64",
                                              "TotalTime": "float64", "Author": "object"})
    print(bar)
    print("Target folder: {}".format(str(TF.absolute())))
    print("Output folder: {}".format(str(OF.absolute())))
    print("Statistics path: {}".format(str(SP.absolute())))
    print("Process Pool limit: {0} of {1} CPUs".format(TPL, os.cpu_count()))
    print("Author: {}".format(author))
    print(bar)
    try:
        main(TF, OF, SP, author)
    except Exception as e:
        print(str(e))
        GlobalProcessPool.shutdown(wait=False, cancel_futures=True)
    input("Press [Enter] to continue...")
