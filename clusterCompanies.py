import datetime
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import finance
from matplotlib.collections import LineCollection	
from sklearn import cluster, covariance, manifold

def clusterCompanies():
	###############################################################################
	# Retrieve the data from Internet

	# Choose a time period 
	d1 = datetime.datetime(2013, 1, 1)
	d2 = datetime.datetime(2015, 1, 1)

	# symbol definitions
	symbol_dict = {
		'MSFT': 'Microsoft',
		'AAPL': 'Apple',
		'AMZN': 'Amazon',
		'IBM': 'IBM',
		'YHOO': 'Yahoo',
		'SNDK': 'Sandisk',
		'EA': 'Electronic Arts',
		'XRX': 'Xerox',
		'SNE': 'Sony',
		'FB': 'Facebook',
		'GOOGL': 'Google',
		'LNKD': 'LinkedIn',
		'PCRFY': 'Panasonic'}

	symbols, names = np.array(list(symbol_dict.items())).T

	quotes = [finance.quotes_historical_yahoo(symbol, d1, d2, asobject=True)
			  for symbol in symbols]

	open = np.array([q.open for q in quotes]).astype(np.float)
	close = np.array([q.close for q in quotes]).astype(np.float)

	# The daily variations of the quotes are what carry most information
	variation = close - open

	###############################################################################
	# Learn a graphical structure from the correlations
	edge_model = covariance.GraphLassoCV()

	# standardize the time series: using correlations rather than covariance
	# is more efficient for structure recovery
	X = variation.copy().T
	X /= X.std(axis=0)
	edge_model.fit(X)

	###############################################################################
	# Cluster using affinity propagation

	_, labels = cluster.affinity_propagation(edge_model.covariance_)
	n_labels = labels.max()
	#file = open("ClusterList.txt", "w")
	stockList = []
	for i in range(n_labels + 1):
		stockList.append(symbols[labels == i])
		
	np.savetxt('ClusterList.txt',stockList, delimiter = ' ', fmt="%s")
		#txtF.write('Cluster %i: %s' % ((i + 1), ', '.join(names[labels == i])))
	return stockList
		
clusterCompanies()