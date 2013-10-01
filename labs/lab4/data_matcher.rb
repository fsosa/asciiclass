#! /usr/bin/env ruby
require 'rubygems'
require 'json'
require 'csv'

# NOTE: Requires Ruby 1.9.2+ or the Ruby JSON gem ('gem install json')

def importJSON (filename) 
	raw_data = File.read(filename) 
	parsed = JSON.parse(raw_data)

	return parsed
end

def importCSVasHash (filename)
	csv_pairs = CSV.read(filename)
	pair_hash = {}
	
	csv_pairs.each do |pair|
		pair_hash[pair[0]] = pair[1]
	end

	return pair_hash
end

# Takes a list of [first_id, second_id] pairs and a hash of the ground truth
def scoreMatches (matches, truth)
	true_pos, true_neg, false_pos = 0, 0, 0
	
	matches.each do |match|
		first_id = match[0]
		if (truth.keys.include?(first_id) && truth[first_id] == match[1])
			true_pos += 1
		else
			false_pos += 1
		end	
	end

	precision = true_pos.to_f / (true_pos + false_pos)
	recall = true_pos.to_f / truth.length
	fscore = (2.0 * precision * recall) / (precision + recall)

	puts "TRUE_POS = #{true_pos}, FALSE_POS = #{false_pos}, PREC = #{precision}, RECALL = #{recall}, F = #{fscore}"
end


def createBucket (entry_list, key_name)
	bucket = {}
	# for each item, check if key exists, if so add to list under that key
	entry_list.each do |entry|
		if !entry[key_name].nil?
			key = entry[key_name]
			(bucket[key] ||= []) << entry 
		end	
	end

	return bucket
end


def normalized_phone (phone)
	unless phone.nil?
		phone.gsub(/\D/, "")
	end
end

def phones_match? (entry1, entry2)
	phone_1 = normalized_phone(entry1["phone"])
	phone_2 = normalized_phone(entry2["phone"])
	
	if phone_1.nil? || phone_2.nil? || phone_1.empty? || phone_2.empty?
		return false
	end
	
	if phone_1 == phone_2
		return phone_1 == phone_2	
	end
end

# Approach:
# 1. Filter down entries to compare by creating a hash of postal codes to entries with the same code
# 2. Compare entries first by phone numbers
# 	If no phone number, compare by normalized name
#	If no match, compare by Levenshtein distance according to some threshold

def findMatches (file_1, file_2)
	bucket_key_name = "postal_code"
	first_set = importJSON(file_1)
	second_set = importJSON(file_2)

	first_bucket = createBucket(first_set, bucket_key_name)
	second_bucket = createBucket(second_set, bucket_key_name)

	# Create a universal list of all the keys that we have to iterate through
	all_keys = first_bucket.keys + second_bucket.keys

	final_matches = []
	matched = []

	# Find the matches!
	all_keys.each do |key|
		if key.empty?
			next
		end
		
		# By default, we'll include the non-keyed buckets as the default set to search
		sub_bucket_1 = first_bucket[""]
		sub_bucket_2 = second_bucket[""]

		# Augment the search space by including the keyed-buckets in the search space
		if first_bucket.keys.include? key
			sub_bucket_1 += first_bucket[key]
		end			

		if second_bucket.keys.include? key
			sub_bucket_2 += second_bucket[key]
		end

		# Now SEARCH!
		sub_bucket_1.each do |entry_1|
			sub_bucket_2.each do |entry_2|
				# Compare phone numbers first
				if phones_match?(entry_1, entry_2) && !matched.include?(entry_1) && !matched.include?(entry_2)
					final_matches << [entry_1["id"], entry_2["id"]]
					matched << entry_1
					matched << entry_2
				end
			end

		end
	end

	return final_matches
end

if ARGV.length != 3 
	puts "NOTE: Requires Ruby 1.9.2+ or the Ruby JSON gem ('gem install json')"
	puts "USAGE: #{$0} file1.json file2.json"
end

if ARGV.length == 3
	results = findMatches ARGV[0], ARGV[1]
	truth = importCSVasHash ARGV[2]
	scoreMatches(results, truth)
end




