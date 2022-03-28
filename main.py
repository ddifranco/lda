#! /usr/bin/python3

import sys
import os
import pdb
import json

sys.path.append(os.path.join(os.path.dirname(__file__), ".", "utils"))
from catalog import Catalog
from preprocessor import Preprocessor
from model import TopicModel

cleaners = {
           "raw" : Preprocessor(routines=[], retained_pos=[]),
           "rplus_headers" : Preprocessor(routines=["filter_headers"], retained_pos=[]),
           "baseline" : Preprocessor(routines=["filter_headers", "basic", "lemmatize", "filter_stops"], retained_pos=[]),
           "bminus_hfilter" : Preprocessor(routines=["basic", "lemmatize", "filter_stops"], retained_pos=[]), 
           "bminus_basic" : Preprocessor(routines=["filter_headers", "lemmatize", "filter_stops"], retained_pos=[]), 
           "bminus_lemmatize" : Preprocessor(routines=["filter_headers", "basic", "filter_stops"], retained_pos=[]),
           "bminus_sfilter" : Preprocessor(routines=["filter_headers", "basic", "lemmatize"], retained_pos=[]),
           "bplus_posfilter" : Preprocessor(routines=["filter_headers", "basic", "lemmatize", "filter_by_pos", "filter_stops"], retained_pos=["NN", "NNS", "NNP", "NNPS", "JJ", "RBR", "JJR", "JJS"])
           }

for procedure_name, cleaner in cleaners.items():

    print(f"Trying {procedure_name} cleaning routine ...")

    data = Catalog('/home/dandifranco/lda/data/20news-bydate-train') 
    data.condition(cleaner)

    tm = TopicModel(data)
    results = tm.self_assess() 

    with open(f"{procedure_name}.json", "w") as f:
        f.write(json.dumps(results))
