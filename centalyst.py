import twitter
from textblob import TextBlob

def sentiment_of( api, term ):
  """
  Evaluates  the sentiment of a term by submitting a search query to twitter,
  evaluating the sentiment of each status returned, and averaging the non
  zero sentiments.
  """
  search = api.GetSearch(term=term, count=100)
  blobs = [ TextBlob(status.text) for status in search ]
  sentiments = [ blob.sentiment.polarity for blob in blobs ]
  filtered_sentiments = filter(lambda a: a!=0.0, sentiments)
  print 'evaluated {0} and found {1} non zeros'.format(term, len(filtered_sentiments))
  return  sum(filtered_sentiments)/len(filtered_sentiments)

def read_terms( path ):
  f = open(path)
  rels = dict()
  for line in f:
    if(line[0] != '#'):
      l = line.split()
      terms = l[1:]
      rels[l[0]] = l[1:]
  return rels


def verify():
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

  api = verify()

  sym_terms = read_terms( 'relations.txt' )

  sym_sent = dict()

  for sym in sym_terms:
    avg = 0.0
    for term in sym_terms[sym]:
      sent = sentiment_of(api, term)
      avg += sent
    avg /= len(sym_terms[sym])
    sym_sent[sym] = avg

  f = open('symbol_sentiments.txt', 'w')
  for sym in sym_sent:
    f.write('{0} {1}\n'.format(sym, sym_sent[sym]))
  f.close()

if __name__ == '__main__':
  main()
