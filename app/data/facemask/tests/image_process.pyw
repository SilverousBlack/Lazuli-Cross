# mathematicals and randoms
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

def ImprovedSecondDerivativeEdgeDetection(target: Image.Image):
    width, height = target.size
    blur_radius = int((min(width, height) * 0.05) if (min(width, height) * 0.05) > 0 else (min(width, height) * 0.1))
    pixel_radius = int((min(width, height) * 0.0075) if (min(width, height) * 0.0075) > 0 else (min(width, height) * 0.01))
    copy = target.filter(ImageFilter.UnsharpMask(blur_radius)).filter(ImageFilter.GaussianBlur(blur_radius))
    copy = (ImageEnhance.Contrast(target).enhance(1.75)).filter(ImageFilter.FIND_EDGES).convert("LA")
    copy = np.array(copy, np.uint32)
    internal = np.zeros((height, width), np.uint32)
    edgepx = copy[:, :, 0].max()
    # edge denoising routine
    for i in range(height):
        for j in range(width):
            if copy[i, j, 0] >= edgepx * 0.5:
                internal[i, j] = 255
            elif copy[i, j, 0] >= edgepx * 0.25 and copy[i, j, 0] < edgepx * 0.5:
                internal[i, j] = 127
            elif copy[i, j, 0] >= edgepx * 0.125 and copy[i, j, 0] < edgepx * 0.25:
                internal[i, j] = 63
    # probability edge enhancement with edge denoising
    copy = internal
    internal = np.zeros((height, width), np.uint32)
    for i in range(height):
        for j in range(width):
            density_prob = 0
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
            if density_prob >= 3.25:
                internal[i, j] = 255
            elif 2 <= density_prob < 3.25:
                internal[i, j] = 127
            elif 1 <= density_prob < 2:
                internal[i, j] = 63
    internal = np.expand_dims(internal, axis=2)
    internal = np.insert(internal, 1, 255, axis=2).astype('uint8')
    internal = Image.fromarray(internal, 'LA')
    return internal


def ColorDeisolateRoutine(target: Image.Image, edges: Image.Image):
    invr = np.array(ImageOps.invert(target))
    copy = np.array(target)
    edge = np.array(edges)[:, :, 0]
    height, width, depth = copy.shape
    internal = np.zeros((height, width, depth), np.uint32)
    for i in range(height):
        for j in range(width):
            temp = invr[i, j] * 0.25
            if edge[i, j] == 255:
                temp *= 4
            elif edge[i, j] == 127:
                temp *= 3
            elif edge[i, j] == 63:
                temp *= 2
            buf = np.mod(np.abs(temp - invr[i, j]), 256)
            internal[i, j] = buf
    sampsz = int(min(height, width) // 2)
    internal = ImageOps.invert(Image.fromarray(internal.astype("uint8"), "RGB"))
    samp = (internal.crop(((width - sampsz) // 2, (height - sampsz) // 2, (width + sampsz) // 2, (height + sampsz) // 2))).resize((sampsz * 2, sampsz * 2), Image.ANTIALIAS)
    return (internal, samp)
    
class ImageProcessor:
    _sesh_warn: str
    _sesh_copy: Image.Image
    _sesh_edge: Image.Image
    _sesh_proc: Image.Image
    _sesh_samp: np.array
    
    def __prot_process__(self):
        try:
            img_h, img_w = self._sesh_copy.size
            max_s = max(img_h, img_w)
            ratio = 1 / (max_s // 1000)
            self._sesh_copy = self._sesh_copy.resize((int(img_h * ratio), int(img_w * ratio)), Image.ANTIALIAS)
            self._sesh_edge = ImprovedSecondDerivativeEdgeDetection(self._sesh_copy)
            self._sesh_proc, self._sesh_samp = ColorDeisolateRoutine(self._sesh_copy, self._sesh_edge)
        except Exception as e:
            del self._sesh_warn
            self._sesh_warn = str(e)
    
    def __init__(self, other = None, **kwargs):
        if other is not None and isinstance(other, ImageProcessor):
            if other._sesh_warn == "No Warnings":
                self._sesh_warn = str(other._sesh_warn)
                self._sesh_copy = other._sesh_copy.copy()
                self._sesh_edge = other._sesh_edge.copy()
                self._sesh_proc = other._sesh_proc.copy()
                self._sesh_samp = np.array(other._sesh_samp)
            else:
                raise AttributeError(other._sesh_warn)
        elif other is not None and isinstance(other, Image.Image):
            self._sesh_warn = "No Warnings"
            self._sesh_coy = other.copy()
            self.__prot_process__()
        elif other is not None:
            self._sesh_warn = "No Warnings"
            self._sesh_copy = Image.open(other, **kwargs).convert('RGB')
            self.__prot_process__()
        else:
            self._sesh_warn = "No Image Initiated"

    def __repr__(self):
        return self._sesh_warn
    
    def get_capture(self):
        return self._sesh_copy
    
    def get_edges(self):
        return self._sesh_edge
    
    def get_processed(self):
        return self._sesh_proc
    
    def get_sample(self):
        return self._sesh_samp
