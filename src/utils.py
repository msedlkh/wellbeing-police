import numpy as np
import random
import re
import pandas as pd
import os
import spacy

from zipfile import ZipFile
from PIL import Image


class text_normalization:
    
    def __init__(self):
        ## read text abbreviations into dictionary
        self.d = {}
        self.new_dict = {}
        with open(os.path.join(os.path.join(os.getcwd(),"src/text_abbreviations.txt"))) as f:
            for line in f:
                (key, val) = line.rstrip('\n').lower().split(": ")
                key = rf"\b{key}\b"
                self.d[key] = val
        self.d_1 = {
            r"'em":"them",
            r"\buh+\b":"uh",
            r"\bah+\b":"ah",
            r"\bah(ah)+\b":"ah",
            r"\bha+(h+a+)+\b":"haha",
            r'\bhm+\b':"hmm",
            r'\bloo+l\b':"lol",
            r"\bohh+\b":"ho",
            r"\bnoo+\b":"noo",
            r"\byou{2,}\b":"you",
            r"/s\b":"sarcasm_emoticon",
            r"<3":"love_emoticon",
            r":p":'being_cute_emoticon',
            r":\)|:\'\)|:-\)|=\)":'smiley_emoticon',
            r":d":'happy_emoticon',
            r":\(":'sad_emoticon',
            r":/":'unsure_emoticon',
            r":o":'surprised_emoticon'
            }
        self.new_dict = {**self.d, **self.d_1}
            

    def normalize_data(self,df, headers = ["body"]):
        for header in headers:
            ## split list symbol with word e.g. -take 2,000mg fish oil      
            df[header] = df[header].apply(lambda text: re.sub(r"\s-([A-Za-z]+)\b",r" - \1", text, flags=0)) 

            ## further split number with word e.g., 6months, 28male, 2hrs
            df[header] = df[header].apply(lambda text: re.sub(r"(\d+)([A-Za-z]+)",r"\1 \2", text, flags=0)) 

            ## replace numbers with a generic placeholder "NUM"
            df[header] = df[header].apply(lambda text: re.sub(r"([0-9]+)",r"NUM",text,flags=0)) 

            df[header] = df[header].replace(self.new_dict,regex=True)

        return df
    

       
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