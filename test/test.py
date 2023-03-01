import os
import pandas as pd
import numpy as np

import cv2

arr = [0, 0, 0, 0, 0, 0, 0, 18000, 18000, 18000]
std = np.std(arr)
mean = np.mean(arr)

for a in arr:
    print((a - mean) / std)

print("\n")

for i in range(len(arr)):
    print((arr[i] - mean) / std)
