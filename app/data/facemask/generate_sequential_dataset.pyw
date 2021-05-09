"""
    generate_sequential_dataset.pyw
    
    usage:
    
    `py generate_sequential_dataset.pyw ...args`
    
    inline args:
    
    ss 
"""

# maths and randoms
import math
import random as rand
import numpy as np

# dataset manipulation
import pandas as pd

# argument parsing
import argparse as ap

SampleSize: int
GlobalDataSet: pd.DataFrame

parser = ap.ArgumentParser(description="Generates a sequentially considered dataset")
parser.add_argument('-sample_size', metavar="SS", default=100,
                    type=int,
                    help="Specify the sample size to be generated.")

def create_mesh(size: int, minval, maxval):
    internal = []
    thresh = int(size)
    while thresh > 0:
        bluf = rand.randint(minval, maxval)
        internal.append(int(bluf))
        thresh =- 1
    return internal

def mesh_data(cols: list, data: list):
    internal = {}
    for i in range(len(cols)):
        internal[cols[i]] = data[i]
    return internal
    
if __name__ == "__main__":
    try:
        args = parser.parse_args()
        print("Creating sequentially generated dataset.")
        print("Size:", args.sample_size)
    except ap.ArgumentError:
        print("Argument Error")
