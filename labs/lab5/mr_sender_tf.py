import sys
import os
import json
import StringIO
from mrjob.protocol import JSONValueProtocol, JSONProtocol
from mrjob.job import MRJob
from mrjob.emr import EMRJobRunner 
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
	
		# Get the list of keys so that we can get the idf parts
		access_key ='AKIAJFDTPC4XX2LVETGA' 
		secret_key ='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'
		emr = EMRJobRunner(aws_access_key_id=access_key, aws_secret_access_key=secret_key)
		idf_parts = emr.get_s3_keys("s3://6885public/fsosa/term-idfs/")

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
