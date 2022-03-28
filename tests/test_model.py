#! /usr/bin/python3

import unittest
import sys
import os
import pdb

sys.path.append(os.path.join(os.path.dirname(__file__), "..", "utils"))
from catalog import Catalog
from model import TopicModel

class TestTopicModel(unittest.TestCase):

    def test_runthrough(self):

        train = Catalog('/home/dandifranco/lda/data/20news-bydate-train') 
        test = Catalog('/home/dandifranco/lda/data/20news-bydate-test') 
        tm = TopicModel(train)
        results = tm.self_assess() 
        self.assertEquals(len(results), 20)

if __name__ == "__main__":

    unittest.main()
