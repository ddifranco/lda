#! /usr/bin/python3

from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords
import re
import pdb
import nltk

class Preprocessor():

    alphanumeric = re.compile("^[a-zA-Z0-9']+$")
    lemmatizer = WordNetLemmatizer()
    stops = set(stopwords.words('english'))

    headers = {}
    headers["from"] = re.compile("^From:")
    headers["subject"] = re.compile("^Subject:")
    headers["organization"] = re.compile("^Organization:")
    headers["lines"] = re.compile("^Lines:")
    headers["host"] = re.compile("^NNTP-Posting-Host:")
    headers["writes"] = re.compile(".* writes:$")


    def __init__(self, routines, retained_pos):

        self.routine_router = {"filter_headers" : self.filter_headers, "basic" : self.basic, "lemmatize" :  self.lemmatize,  "filter_stops" : self.filter_stops, "filter_by_pos" : self.filter_by_pos }

        for routine in routines:
            if routine not in self.routine_router:
                raise ValueError (f'"{routine}" is not a valid cleaning routine.')

        self.routines = routines
        self.retained_pos = retained_pos

    def apply_cleaners(self, original_doc):

        processed_doc = []

        for ln in original_doc:
            processed_line = ln
            for routine in self.routines:
                processed_line = self.routine_router[routine](processed_line)

            if processed_line != "":
                processed_doc.append(processed_line)

        return processed_doc

    def basic(self, text):

        clean_tkns = []
        for tkn in word_tokenize(text):
            normalized = tkn.lower().strip().strip('"')
            alphanum = re.match(self.alphanumeric, tkn)
            if alphanum is None:
                continue
            clean_tkns.append(normalized)

        sanitized = " ".join(clean_tkns)

        return sanitized

    def lemmatize(self, text):

        clean_tkns = []
        for tkn in word_tokenize(text):
            normalized = self.lemmatizer.lemmatize(tkn)
            clean_tkns.append(normalized)

        sanitized = " ".join(clean_tkns)

        return sanitized

    def filter_headers(self, text):

        for htype, pattern in self.headers.items():
            test = re.match(pattern, text.strip())
            if test is not None:
                return ""

        return text

    def filter_by_pos(self, text):

        tkns = word_tokenize(text)
        spans = nltk.pos_tag(tkns)

        filtered_tkns = []

        for tkn, pos in spans:
            if pos in self.retained_pos:
                filtered_tkns.append(tkn)

        filtered = " ".join(filtered_tkns)

        return filtered

    def filter_stops(self, text):

        filtered_tkns = []

        for tkn in word_tokenize(text):
            if tkn.lower() in self.stops:
                continue
            filtered_tkns.append(tkn)

        filtered = " ".join(filtered_tkns)

        return filtered
