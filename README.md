# TweetCloud-inator :cloud:

## Overview
This project uses the [twitter](https://developer.twitter.com/en/docs/tweets/search/api-reference/get-search-tweets.html) search API to generate colorful word clouds based on a user-based search query or trending topic. An example is shown <a href = 'computerscience.png'>here</a>, where the search query was *Computer Science*. 

### Note: 
  - You need to have/create a twitter API and insert your key into the script
  - Install these python libraries for functionality:
      - tweepy - used in authentication and retrieving tweet data
      - textblob - word tokenization
      - wordcloud - generates wordcloud using 'word':frequency dictionary
      - matplotlib - displays word cloud
      - pillow Image module - opens image we want to use as mask 
      - numpy - enables use of image mask

##### Next Steps:
- [ ] Ask user if they want to generate multiple word clouds from several queries
- [ ] Make this a Web App
