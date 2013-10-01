#! /usr/bin/env ruby
require 'rubygems'
require 'json'

# NOTE: Requires Ruby 1.9.2+ or the Ruby JSON gem ('gem install json')

def importData (filename) 
	raw_data = File.read(filename) 
	parsed = JSON.parse(raw_data)

	return parsed
end


# TODO: FACTOR OUT INTO OWN CLASS
# Takes a list of [first_id, second_id] pairs and a hash of the ground truth
def scoreMatches (matches, truth)
	@true_pos, @true_neg, @false_pos = 0, 0, 0
	
	matches.each do |match|
		first_id = match[0]
		if (truth.include? first_id && truth[first_id] == match[1]) 
			true_pos += 1
		else
			false_pos += 1
		end	
	end

	@precision = true_pos.to_f / (true_pos + false_pos)
	@recall = true_pos.to_f / truth.length
	@fscore = (2.0 * precision * recall) / (precision + recall)

	puts "TRUE_POS = #{true_pos}, FALSE_POS = #{false_pos}, PREC = #{precision}, RECALL = #{recall}, F = #{fscore}"
end

# Approach:
# 1. Filter down entries to compare by creating a hash of postal codes to entries with the same code

def createBucket (entry_list, key_name)
	bucket = {}
	# for each item, check if key exists, if so add to list under that key
	entry_list.each do |entry|
		if !entry[key_name].nil?
			key = entry[key_name]
			(bucket[key] ||= []) << entry 
			#	bucket[key] = entry
			#else
			#	bucket[key].push(entry)
		end	
	end

	return bucket
end

def findMatches (file_1, file_2)
	bucket_key_name = "postal_code"
	first_set = importData(file_1)
	second_set = importData(file_2)

	first_bucket = createBucket(first_set, bucket_key_name)
	second_bucket = createBucket(second_set, bucket_key_name)
end

if ARGV.length != 2
	puts "NOTE: Requires Ruby 1.9.2+ or the Ruby JSON gem ('gem install json')"
	puts "USAGE: #{$0} file1.json file2.json"
end

if ARGV.length > 0
	puts ARGV	
	findMatches ARGV[0], ARGV[1]
	#puts "TRUE_POS = #{@true_pos}, FALSE_POS = #{@false_pos}, PREC = #{@precision}, RECALL = #{@recall}, F = #{@fscore}"
end




