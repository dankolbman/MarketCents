import twitter
from textblob import TextBlob

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
  search = api.GetSearch(term=term, count=100)
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
  return np.mean(group_sentiments), np.stdev(group_sentiments)


def write_sentiment( symbols, path='data/symbol_sentiments.txt' ):
  """
  Writes sentiments obtained by averaging textblob sentiments of twitter statuses
  to a file
  """
  with open(path, 'w') as f:
    for sym in sym_sent:
      f.write('{0} {1}\n'.format(sym, sym_sent[sym]))
    f.close()


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

  # Verify
  api = verify()
  # Load symbol keyword terms
  sym_terms = read_terms( 'terms.txt' )

  # Evaluate/Load setiments for symbols
  sym_sent = dict()
  for sym in sym_terms:
    sentiment = symbol_sentiment( api, sym_terms(sym) )
    sym_sent[sym] = sentiment

  # Write out sentiment evalulations to file
  write_sentiments( sym_sent )

  # Get groups
  `


if __name__ == '__main__':
  main()
