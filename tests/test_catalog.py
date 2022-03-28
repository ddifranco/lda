#! /usr/bin/python3

import unittest
import sys
import os
import pdb

sys.path.append(os.path.join(os.path.dirname(__file__), "..", "utils"))
from catalog import Catalog

class TestCatalog(unittest.TestCase):

    train = Catalog('/home/dandifranco/lda/data/20news-bydate-train') 
    test = Catalog('/home/dandifranco/lda/data/20news-bydate-test') 

    def test_group_count(self):
        self.assertEqual(len(self.test.get_groups()), 20)
        self.assertEqual(len(self.train.get_groups()), 20)

    def test_document_count(self):
        train_count = len(self.train.get_all_docs())
        test_count = len(self.test.get_all_docs())

        self.assertEqual(train_count, 11314)
        self.assertEqual(test_count, 7532)
        self.assertEqual(train_count + test_count, 18846)

    def test_singleline_format(self):
        sample = self.test.get_all_docs()[5]
        self.assertIsInstance(sample, str)

    def test_list_format(self):
        sample = self.test.get_all_docs(singleline=False)[5]
        self.assertIsInstance(sample, list)

if __name__ == "__main__":

    unittest.main()
