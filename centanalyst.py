import os
import numpy as np
import twitter
from textblob import TextBlob
from cluster_symbols import cluster_symbols, load_dictionary

def symbol_sentiment( api, terms ):
  """
  Evaluates a symbol's sentiment based on its terms
  
  Parameters
  ----------
  api
    the twitter api instance that has been validated by a user
  terms 
    the terms describing the stock symbol to be evaluated
  Returns
  -------
  A sentiment between -1.0 and 1.0
  """
  search = api.GetSearch(term=terms, count=100)
  blobs = [ TextBlob(status.text) for status in search ]
  sentiments = [ blob.sentiment.polarity for blob in blobs ]
  filtered_sentiments = filter(lambda a: a!=0.0, sentiments)
  #print 'evaluated {0} and found {1} non zeros'.format(term, len(filtered_sentiments))
  return  sum(filtered_sentiments)/len(filtered_sentiments)

def cluster_average( group, sentiments ):
  """
  Computes the average of a cluseter
  Parameters
  ----------
  group
    a list of symbols belonging to group who's sentiments are to be averaged
  sentiments
    a dict of sentiments keyed by symbol

  Returns
  -------
  average, standard deviation
  """
  group_sentiments = [ sentiments[sent] for sent in group ]
  return np.mean(group_sentiments), np.std(group_sentiments)


def write_sentiments( symbols, path='data/symbol_sentiments.txt' ):
  """
  Writes sentiments obtained by averaging textblob sentiments of twitter statuses
  to a file
  """
  with open(path, 'w') as f:
    for sym in symbols:
      f.write('{0} {1}\n'.format(sym, symbols[sym]))
    f.close()


def read_sentiments( path ):
  """
  Read sentiments from file into sentiment dictionary keyed by symbol

  Parameters
  ----------
  path
    the path of the sentiment data file
  """
  
  sentiments = dict()
  with open( path, 'r' ) as f:
    for line in f:
      if(line[0] != '#'):
        l = line.split()
        sentiments[l[0]] = l[1]
  return sentiments


def read_terms( path ):
  """
  Reads terms related to a symbol

  Example
  -------
  Input file:
  MSFT microsoft windows skype
  """
  f = open(path)
  rels = dict()
  for line in f:
    if(line[0] != '#'):
      l = line.split()
      terms = l[1:]
      rels[l[0]] = l[1:]
  return rels


def verify():
  """
  Verify with twitter api
  """
  f = open('me.auth')
  keys = f.readlines()

  # Read in keys
  keys = [x.strip('\n') for x in keys]

  # Connect
  api = twitter.Api(consumer_key = keys[0],
                      consumer_secret = keys[1],
                      access_token_key = keys[2],
                      access_token_secret = keys[3])
  return api

def main():
  """
  Clusters stock symbols into categories based on historical performance
  Performs sentiment analysis on each cluster via twitter
  Suggests action to take based on sentinent
  """

  SENTIMENT_PATH = 'data/symbol_sentiments.txt' 
  # Force sentiment analysis from statuses on twitter
  FORCE_TWITTER = True;

  # Verify with twitter
  api = verify()

  # Load symbol keyword terms
  sym_terms = read_terms( 'data/symbol_dictionary.txt' )

  # Evaluate/Load setiments for symbols
  sym_sent = dict()
  if os.path.exists( SENTIMENT_PATH ) and not FORCE_TWITTER:
    # Load sentiment from file and save twitter calls
    sym_sent = read_sentiments( SENTIMENT_PATH )
  else:
    # Create sentiment from twitter
    for sym in sym_terms:
      sentiment = symbol_sentiment( api, sym_terms[sym] )
      sym_sent[sym] = sentiment
    print 'Analyzed {0} tweets'.format(len(sym_terms))
    # Write out sentiment evalulations to file
    write_sentiments( sym_sent, SENTIMENT_PATH )
    print 'Wrote sentiment analysis to {0}'.format(SENTIMENT_PATH)

  # Get groups
  symbol_names = load_dictionary( 'data/symbol_dictionary.txt' )
  groups = cluster_symbols( symbol_names )

  group_avgs = [cluster_average(group, sym_sent) for group in groups]
  print group_avgs


if __name__ == '__main__':
  main()
