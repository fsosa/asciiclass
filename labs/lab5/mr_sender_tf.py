import sys
import os
import json
from mrjob.protocol import JSONValueProtocol, JSONProtocol
from mrjob.job import MRJob
from term_tools import get_terms
from boto.s3.connection import S3Connection

class MRSenderTF(MRJob):
	INPUT_PROTOCOL = JSONValueProtocol
	OUTPUT_PROTOCOL = JSONProtocol

	def mapper(self, key, email):
		for term in get_terms(email['text']):
			yield {'sender':email['sender'], 'term':term}, 1


	def get_parts_from_s3
		conn = S3Connection()
		bucket = conn.get_bucket('6885public')
		parts = bucket.list('fsosa/tf-idf')
		return parts		
	
	def reducer_init(self):
		# We want to create an overall dictionary of word, idf pairs 
		self.per_word_idfs =  {}

		# Iterate over all the parts to build the entire word dictionary
		idf_parts = os.listdir(per_term_dir)
		for parts in idf_parts:
			path = per_term_dir + "/" + parts
			part_file = open(path, 'r')
			for line in part_file:
				word_idf = json.loads(line)
				word = word_idf["term"]
				idf = word_idf["idf"]

				self.per_word_idfs[word] = idf	

	def reducer (self, term, occurences):
		sender_tf = sum(occurences)
		word = term['term']
		sender = term['sender']
		per_word_idf = self.per_word_idfs[word]
		
		final_tf_idf = sender_tf * per_word_idf
		yield sender, {'word':word, 'tf-idf':final_tf_idf}

if __name__ == '__main__':
	MRSenderTF.run()
