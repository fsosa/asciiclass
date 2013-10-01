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

if ARGV.length != 2
	puts "NOTE: Requires Ruby 1.9.2+ or the Ruby JSON gem ('gem install json')"
	puts "USAGE: #{$0} file1.json file2.json"
end

if ARGV.length > 0
	importData ARGV[0] 
	puts "TRUE_POS = #{@true_pos}, FALSE_POS = #{@false_pos}, PREC = #{@precision}, RECALL = #{@recall}, F = #{@fscore}"
end




