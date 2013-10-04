import sys
import math
from mrjob.protocol import JSONValueProtocol
from mrjob.job import MRJob
from term_tools import get_terms

class MRPerTermIDF(MRJob):
    INPUT_PROTOCOL = JSONValueProtocol
    OUTPUT_PROTOCOL = JSONValueProtocol

    def mapper(self, key, email):
	# Only iterate over the unique terms to avoid double-counting
	terms = get_terms(email['text'])
	unique_terms = set(terms)
        for term in unique_terms: 
            yield term, 1

    def reducer(self, term, occurences):
	doc_occurences = sum(occurences)
	idf = math.log(516893.0 / doc_occurences) 
        yield None, {'term': term, 'idf': idf}

if __name__ == '__main__':
        MRPerTermIDF.run()
