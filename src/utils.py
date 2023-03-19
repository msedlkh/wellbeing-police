import numpy as np
import random
import re

from zipfile import ZipFile
from PIL import Image


       
def color_func(word, font_size, position, orientation, random_state=None, **kwargs):
    return "hsl(210, 100%, 24%)"


def get_mask():
    return np.array(Image.open("src/oval-mask.png"))


def compute_sparsity(M):
    return M[M==0].size / M.size


def search(text,pattern,num=1,flags=0):
    counter = 0
    for idx,string in enumerate(text):
        matches = re.findall(pattern, string, flags)
#         print(', '.join(matches))
        if len(matches) == 0:
            continue
        else:
            counter+=1
            print(f"Doc number: {idx}\n",string)
        if counter==num:
            break
    if counter == 0:
        print("No match found.", "\n")