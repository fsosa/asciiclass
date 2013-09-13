import twitter_pb2
import sys

# 1. Find the number of deleted messages in the dataset
def find_deleted_tweets(tweets):
	num_deleted_tweets = 0
	for tweet in tweets.tweets: 
		if tweet.is_delete:
			num_deleted_tweets += 1
	
	print "Number of deleted tweets: " + str(num_deleted_tweets)

			
# 2. Find the number of tweets that are replies to another tweet in this dataset	
def find_num_retweets(tweets):
	# Compile a list of tweet ids
	tweet_ids = []
	for tweet in tweets.tweets:
		tweet_ids.append(tweet.insert.id)
	
	# Loop through tweets and check if reply_to id in the list of ids
	num_replies = 0
	for tweet in tweets.tweets:
		if tweet.insert.reply_to in tweet_ids:
			num_replies += 1
	
	print "Number of tweets in reply: " + str(num_replies)
			
# 3. Find the five uids that have tweeted the most. 
def find_top_five_tweets(tweets):
	# Compile a hash of uids and their tweet counts
	user_freq = {}
	for tweet in tweets.tweets:
		uid = tweet.insert.uid
		is_delete = tweet.is_delete
		
		if is_delete:
			continue

		if uid in user_freq:
			user_freq[uid] += 1
		else:
			user_freq[uid] = 1

	# Find top five
	top_five = sorted(user_freq, key=user_freq.get, reverse=True)[:5]
	print "Top five tweeters: " + str(top_five)

# 4. Find the names of the top five places by number of tweets.
def find_top_five_places(tweets):
	# Compile a frequency of places
	place_freq = {}
	for tweet in tweets.tweets:
		if tweet.insert.HasField("place"):
			place_name = tweet.insert.place.name
			if place_name in place_freq:
				place_freq[place_name] += 1
			else:
				place_freq[place_name] = 1
	

	# Find top five
	top_five = sorted(place_freq, key=place_freq.get, reverse=True)[:5]
	print "Top five places: " + str(top_five)

			
#################################

f = open('twitter.pb', "rb")
tweets = twitter_pb2.Tweets()
tweets.ParseFromString(f.read())
print "Total number of tweets: " + str(len(tweets.tweets))
f.close()

find_deleted_tweets(tweets)
find_num_retweets(tweets)
find_top_five_tweets(tweets)
find_top_five_places(tweets)
