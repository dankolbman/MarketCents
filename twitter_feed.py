# authenticates with twitter, searches for microsoft, evaluates overall
# sentiment for microsoft

import numpy as np
import twitter
from textblob import TextBlob

f = open('me.auth')
keys = f.readlines()

# Read in keys
keys = [x.strip('\n') for x in keys]

# Connect
api = twitter.Api(consumer_key = keys[0],
                      consumer_secret = keys[1],
                      access_token_key = keys[2],
                      access_token_secret = keys[3])

print 'logged in as ', api.VerifyCredentials().name

search = api.GetSearch(term='microsoft', )

# Make text blobs out of status content
blobs = [ TextBlob(status.text) for status in search ]

sentiments = [ blob.sentiment.polarity for blob in blobs ]

filtered_sentiments = filter(lambda a: a!=0.0, sentiments)

overall_sentiment = sum(filtered_sentiments)/len(filtered_sentiments)

print 'Overall sentiment for microsoft: {0}'.format(overall_sentiment)

