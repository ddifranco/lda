#! /usr/bin/python3

import unittest
import sys
import os
import pdb

sys.path.append(os.path.join(os.path.dirname(__file__), "..", "utils"))
from preprocessor import Preprocessor
from catalog import Catalog

class TestPreprocessor(unittest.TestCase):

    cleaner = Preprocessor(routines=[], retained_pos=["NN", "NNS", "NNP", "NNPS", "JJ", "RBR", "JJR", "JJS"])

    def test_basic_clean(self):

        original_1 = "punc! And \n"
        expected_1 = "punc and"

        actual_1 = self.cleaner.basic(original_1)
        self.assertEqual(expected_1, actual_1)

        original_2 = "no cleaning needed"
        actual_2 = self.cleaner.basic(original_2)
        self.assertEqual(actual_2, original_2)

        original_3 = "I'll be back ..."
        expected_3 = "i 'll be back"
        actual_3 = self.cleaner.basic(original_3)
        self.assertEqual(expected_3, actual_3)

    def test_lemmatizer(self):

        original_1 = "Cats and Dogs"
        expected_1 = "Cats and Dogs"    #lemmatizer doesn't have an effect here

        actual_1 = self.cleaner.lemmatize(original_1)
        self.assertEqual(expected_1, actual_1)

        original_2 = "runs and stands"
        expected_2 = "run and stand"    

        actual_2 = self.cleaner.lemmatize(original_2)
        self.assertEqual(expected_2, actual_2)

    def test_pos_filter(self):

        original_1 = "the cat sat down heavily on the large mat and yawned"
        expected_1 = "cat large mat"

        actual_1 = self.cleaner.filter_by_pos(original_1)
        self.assertEqual(expected_1, actual_1)

    def test_filter_stops(self):

        original_1 = "The Cat sat down heavily on the large mat and yawned"
        expected_1 = "Cat sat heavily large mat yawned"

        actual_1 = self.cleaner.filter_stops(original_1)
        self.assertEqual(expected_1, actual_1)

    def test_header_filter(self):

        expected_1 = [
                "", "", "", "", "", "\n", "", "\n", 
                ">>Then why do people keep asking the same questions over and over?\n", 
                ">Because you rarely ever answer them.\n", 
                "\n", 
                "Nope, I've answered each question posed, and most were answered multiple\n", 
                "times.\n", 
                "\n", 
                "keith\n"
                ]

        train = Catalog('/home/dandifranco/lda/data/20news-bydate-train') 
        sample = train.get_all_docs(singleline=False)[5]
        actual_1 = []
        for ln in sample:
            actual_1.append(self.cleaner.filter_headers(ln))

        self.assertEqual(expected_1, actual_1)

    def test_multistep(self):

        expected_1 = ["people keep asking question", "rarely ever answer", "nope 've answered question posed answered multiple", "time", "keith"]

        train = Catalog('/home/dandifranco/lda/data/20news-bydate-train') 
        sample = train.get_all_docs(singleline=False)[5]
        cleaner = Preprocessor(routines=["filter_headers", "basic", "lemmatize", "filter_stops"], retained_pos=["NN", "NNS", "NNP", "NNPS", "JJ", "RBR", "JJR", "JJS"])
        actual_1 = cleaner.apply_cleaners(sample) 

        self.assertEqual(expected_1, actual_1)

if __name__ == "__main__":

    unittest.main()
