import sys
import os
import json
import StringIO
from mrjob.protocol import JSONValueProtocol, JSONProtocol
from mrjob.job import MRJob
from mrjob.emr import 
from term_tools import get_terms


class MRSenderTF(MRJob):
	INPUT_PROTOCOL = JSONValueProtocol
	OUTPUT_PROTOCOL = JSONProtocol

	def mapper(self, key, email):
		for term in get_terms(email['text']):
			yield {'sender':email['sender'], 'term':term}, 1


	def reducer_init(self):
		# We want to create an overall dictionary of word, idf pairs 
		self.per_word_idfs =  {}
	
		# Create the S3 connection to get the list of intermediate idf parts	
		conn = S3Connection()
		bucket = conn.get_bucket('6885public')
		idf_parts = bucket.list('fsosa/term-idfs/part') # Ignore that _SUCCESS file 

		# Iterate over all the parts to build the entire word dictionary
		for part in idf_parts:
			part_string = part.get_contents_as_string()
			io = StringIO.StringIO(part_string)
			for line in io:
				pair = json.loads(line)
				word = pair["term"]
				idf = pair["idf"]

				self.per_word_idfs[word] = idf	

	def reducer (self, term, occurences):
		sender_tf = sum(occurences)
		word = term['term']
		sender = term['sender']
		per_word_idf = self.per_word_idfs[word]
	
		# Calculate the final TD-IDF	
		final_tf_idf = sender_tf * per_word_idf
		yield sender, {'word':word, 'tf-idf':final_tf_idf}

if __name__ == '__main__':
	MRSenderTF.run()
