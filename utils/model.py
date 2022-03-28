#! /usr/bin/python3

from gensim.corpora.dictionary import Dictionary
from gensim.models import LdaModel
import pdb

class TopicModel():

    def __init__(self, catalog):

        self.catalog = catalog
        self.corpus = [doc.split() for doc in catalog.get_all_docs()]
        self.common_dictionary = Dictionary(self.corpus)
        self.encoded_corpus = [self.common_dictionary.doc2bow(doc) for doc in self.corpus]

        print(f"Building lda model over {len(self.encoded_corpus)} documents")

        self.lda = LdaModel(self.encoded_corpus, num_topics=len(catalog.get_groups()))

    def self_assess(self):

        print("Performing self assessment")

        results = {}

        for group in self.catalog.get_groups():
            results[group] = [0]*20

        for group, text in self.catalog.get_all_docs(include_group=True):
            encoded_document = self.common_dictionary.doc2bow(text.split())
            predictions = sorted(self.lda[encoded_document], key = lambda x: x[1], reverse= True)
            best = predictions[0][0]
            results[group][best-1] += 1

        return results
