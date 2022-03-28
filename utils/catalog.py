#! /usr/bin/python3

from os import walk
import pdb
from tqdm import tqdm

class Catalog():

    def __init__(self, root):

        self.groups = {}

        for subdir in [x[0] for x in walk(root)][1:]:
            group = subdir.split("/")[6]
            self.groups[group] = {}
            for (_, __, posts) in walk(subdir):
                for docid in posts:
                    with  open(f"{subdir}/{docid}", "r", encoding="utf-8", errors="ignore") as f: 
                        data = f.readlines()
                        self.groups[group][docid] = data

    def condition(self, preprocessor):

        for group, documents in tqdm(self.groups.items()):
            for docid, document in documents.items():
                self.groups[group][docid] = preprocessor.apply_cleaners(document)

    def get_groups(self):
        return self.groups.keys()

    def get_all_docs(self, include_group=False, singleline=True):

        flat = []
        for group, docs in self.groups.items():
            for doc_id, text in docs.items():
                if singleline:
                    if include_group:
                        flat.append((group, " ".join(text)))
                    else:
                        flat.append(" ".join(text))
                else:
                    if include_group:
                        flat.append((group, text))
                    else:
                        flat.append(text)

        return flat
