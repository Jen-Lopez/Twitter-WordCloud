import tweepy, re
from textblob import TextBlob as tb
from wordcloud import WordCloud, STOPWORDS,ImageColorGenerator
import matplotlib.pyplot as plot
import numpy as np
from PIL import Image

# connects to twitter API
def authenticate():
	consumer_key = 'Enter your key'
	consumer_secret = 'Enter secret key'

	access_token = 'Enter access token'
	access_token_secret = 'Enter secret access token'

	auth = tweepy.OAuthHandler(consumer_key,consumer_secret)
	auth.set_access_token(access_token,access_token_secret)

	# variable that allows us to access many methods to extract twitter data
	API = tweepy.API(auth)
	return API

#TRENDING
def trend(API):
	trends = API.trends_place(1)
	trending = list(trend['name'] for trend in trends[0]['trends'])
	for t in range (10):
		print ("%d. %s\n" %(t+1,trending[t]))
	while True:
		try:
			num = int(input ('\nEnter the number you want to generate (1-10): '))
			if not(1 <= num <= 10):
				raise Exception('Not a number between 1-10')
			trend_search = trending[num-1]
			return trend_search
		except:
			print ('Try a number between 1-10')

# function that filters tweet (e.g. links, user mentions)
def clean(text):
	clean_links = re.sub(r"http\S+", "", text) # filter out links
	cleantw = re.sub(r"@\S+","", clean_links) # filter out user @
	return cleantw

# SEARCH
def search(query,API):
	query = query.lower()
	search_query = query + " -filter:retweets"

	# COMMON WORDS
	stopwords = set(STOPWORDS)
	listq = query.split()
	update_stopwords = ['retweet','rt','https','thing','things','twitter','tweet','tweets','they',
	'word','will','many','need','make','okay','place','something','said','much','think','know',
	'open','close','says','nothing','didn','amp','wasn','esta','going','come','wouldn','really','maybe',
	'sure','even','blah','always','feel','every','video','every','video','want','lmao','hello','knew',
	'please','today','tomorrow','yesterday','before']
	update_stopwords.extend(listq)
	stopwords.update(update_stopwords)

	# JSON RESULTS
	search_results = API.search(q = search_query, count=100,tweet_mode = 'extended')

	# String that contains all concatenated tweets
	all_tweets = ""

	# Filter out STOPWORDS, links, and usermentions from tweets
	for tweet in search_results:
		tweet = tweet.full_text
		clean_tweet = clean(tweet)
		all_tweets += clean_tweet.lower()

	# textblob object
	tb_obj = tb(all_tweets)

	# create dictionary where "word": "frequency"
	word_freq_dict = {}

	# iterate through each word and filter out STOPWORDS, words less than 3 letters, and characters besides letters
	for word in tb_obj.words:
		if (word in stopwords):
			continue
		if (len(word) <= 3):
			continue
		if not(word.isalpha()):
			continue
		word_freq_dict[word] = tb_obj.word_counts[word]

	# delete keys that have a frequency less than = 1
	for key in list(word_freq_dict.keys()):
	    if word_freq_dict[key] <= 1:
	        del word_freq_dict[key]
	return word_freq_dict

def generate(dict):
	# create image mask, mode RGB
	twitter_mask = np.array(Image.open('twitter.jpg').convert("RGBA"))

	# create cloud based on frequency
	print ("...Generating WordCloud...\n")
	wordcloud = WordCloud(
	        background_color = "white",
	        max_font_size = 150,
	        max_words = 150,
	        mask = twitter_mask
	).generate_from_frequencies(dict)

	# create color from image
	image_color = ImageColorGenerator(twitter_mask)

	# interpolation makes image appear more smoothly
	plot.figure(figsize=[7,7])
	plot.imshow(wordcloud.recolor(color_func = image_color),interpolation = "bilinear")
	plot.axis("off")
	plot.show()

def main():
	api = authenticate()
	print ("\nLet's Generate a twitter-based word cloud...")
	while True:
		try:
			res = (input("\nWant a trend-based(t) or search-based(s) cloud? ")).lower()
			if res == 't':
				# show trends
				print('\nThese are the top 10 trending topics~\n')
				trend_query = trend(api)
				trend_dict = search(trend_query,api)
				generate(trend_dict)
				break
			elif res == 's':
				# do search query
				query = (input('Enter a search query: ')).strip()
				search_dict = search(query,api)
				generate(search_dict)
				break
			raise Exception("Has to be 't' or 's'")
		except:
			print('Invalid Try again.')

# ------------------------ MAIN PROGRAM ------------------------
if __name__ == "__main__":
	main()
