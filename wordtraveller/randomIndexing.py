import numpy as np


class RandomIndexing:
    DOCUMENT_DIMENSION = 10
    TERM_DIMENSION = DOCUMENT_DIMENSION
    NON_ZEROS_START = 3
    NON_ZEROS_END = 8

    terms_done = dict()

    def __init__(self, term_dimension=1000, start=2, end=10):
        self.documents = {}
        self.voc_doc = {}
        self.TERM_DIMENSION = term_dimension
        self.DOCUMENT_DIMENSION = term_dimension
        self.NON_ZEROS_START = start
        self.NON_ZEROS_END = end

    def setDimensions(self, doc_dim, term_dim, non_z_start, non_z_end):
        self.DOCUMENT_DIMENSION = doc_dim
        self.TERM_DIMENSION = term_dim
        self.NON_ZEROS_START = non_z_start
        self.NON_ZEROS_END = non_z_end

    def getTermDimension(self):
        return self.TERM_DIMENSION

    def setDocumentVector(self, docId):
        self.documents[docId] = np.zeros((self.DOCUMENT_DIMENSION,), dtype=int)
        non_zeros = np.random.random_integers(
            self.NON_ZEROS_START, self.NON_ZEROS_END)
        for x in range(0, non_zeros):
            index = np.random.random_integers(self.DOCUMENT_DIMENSION-1,)
            if index % 2:
                self.documents[docId][index] = -1
            else:
                self.documents[docId][index] = 1

    def addTermVector(self, term, docId):
        if(term != '***NumberDifferentDocs***'):
            if term not in self.voc_doc:
                self.voc_doc[term] = np.zeros(
                    (self.TERM_DIMENSION,), dtype=int)
                self.terms_done[term] = []
            if docId not in self.terms_done[term]:
                self.terms_done[term].append(docId)
                self.voc_doc[term] = self.voc_doc[term] + self.documents[docId]

    def getTermsVectors(self):
        return self.voc_doc
