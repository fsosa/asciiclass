#! /usr/bin/env ruby
require 'rubygems'
require 'json'

# NOTE: Requires Ruby 1.9.2+ or the Ruby JSON gem ('gem install json')

def importData (filename) 
	raw_data = File.read(filename) 
	parsed = JSON.parse(raw_data)

	return parsed
end


if ARGV.length != 2
	puts "USAGE: #{$0} file1.json file2.json"
end

if ARGV.length > 0
	importData ARGV[0] 
end




