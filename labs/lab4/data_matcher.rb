#! /usr/bin/env ruby
require 'rubygems'
require 'json'
require 'csv'
require 'levenshtein'

def importJSON (filename) 
	raw_data = File.read(filename) 
	parsed = JSON.parse(raw_data)

	return parsed
end

def importCSV (filename)
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
	
	return phone_1 == phone_2	
end

# Computes the Levenshtein distance between the addresses of two entries
def leven_dist (entry1, entry2, key)
	first = entry1[key]
	second = entry2[key]
	
	if first.empty? ||  second.empty? || first.nil? || second.nil?
		return 10000
	end
	
	# Get rid of any junk characters
	first = first.gsub(/[!?:,&\.\'\-()\s]/, "").downcase
	second = second.gsub(/[!?:,&\.\'\-()\s]/, "").downcase

	return Levenshtein.distance(first, second)
end

def key_match? (entry1, entry2, key)
	val1 = entry1[key]
	val2 = entry2[key]
	
	# Get rid of any junk characters
	val1 = val1.gsub(/[!?:,&\.\'\-()\s]/, "").downcase
	val2 = val2.gsub(/[!?:,&\.\'\-()\s]/, "").downcase

	if val1.nil? || val2.nil? || val1.empty? || val2.empty?
		return false
	end

	return val1 == val2

end

# Approach:
# 1. Filter down entries to compare by creating a hash of postal codes to entries with the same code
# 2. Compare entries first by name 
#			Then by phone number; Finally by levenshtein distance 

def findMatches (file_1, file_2)
	bucket_key_name = "postal_code"
	first_set = importJSON(file_1)
	second_set = importJSON(file_2)

	first_bucket = createBucket(first_set, bucket_key_name)
	second_bucket = createBucket(second_set, bucket_key_name)

	# Create a universal list of all the keys that we have to iterate through
	all_keys = first_bucket.keys + second_bucket.keys

	final_matches = []

	# Keep track of matched entries so we don't repeat matches
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

		sub_bucket_1.each do |entry_1|
			sub_bucket_2.each do |entry_2|
					first_id = entry_1["id"]
					second_id = entry_2["id"]

					if matched.include?(first_id) && matched.include?(second_id)
						break
					end

					# Perform these comparisons separately to avoid the costly Levenshtein calculation			
		
					# Compare names directly
					if key_match?(entry_1, entry_2, "name") 
						final_matches << [first_id, second_id]
						matched << first_id
						matched << second_id
						break		
					end

					# Then normalized phone numbers
					if phones_match?(entry_1, entry_2) 
						final_matches << [first_id, second_id]
						matched << first_id
						matched << second_id
						break
					end

					# Finally Leven distance
					if leven_dist(entry_1, entry_2, 'name') < 3  
						final_matches << [first_id, second_id]
						matched << first_id
						matched << second_id	
						break	
					end
			end
		end
	end

	return final_matches
end

if ARGV.length < 2
	puts "NOTE: Requires Ruby 1.9.2+ or the Ruby JSON gem ('gem install json')"
	puts "Also requires the levenshtein-ffi gem ('gem install levenshtein-ffi')"
	puts "USAGE: #{$0} file1.json file2.json {optional: truth.csv}"
end

if ARGV.length == 3
	begin_time = Time.now
	results = findMatches ARGV[0], ARGV[1]
	truth = importCSV ARGV[2]
	scoreMatches(results, truth)
	end_time = Time.now
	elapsed = (end_time - begin_time) * 1000
	puts "Time elapsed #{elapsed} ms"
end

if ARGV.length == 2
	results = findMatches ARGV[0], ARGV[1]
	CSV.open("matches_test.csv", "w") do |csv|
		results.each do |pair|
			csv << pair	
		end
	end
end




