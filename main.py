import matplotlib.pyplot as plt
import csv
import sys
import math
from itertools import groupby
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

def print_similar(similar, common, lbl):
  values = similar.values()
  keys = similar.keys()
  plt.plot(values, common.values(), 'ro', label='sine')
  fix, ax = plt.subplots()
  ax.scatter(values, common.values())
  plt.ylabel('Number of common ranked movies')
  plt.xlabel('Similarity')
  for i, txt in enumerate(keys):
    if(values[i] > 0.3):
      ax.annotate(txt, (values[i], common.values()[i]))
  plt.show()

def euclidean_distance(moviesUser1, moviesUser2, threshold = 3):
  movies1 = map(lambda x: x['movieId'], moviesUser1)
  movies2 = map(lambda x: x['movieId'], moviesUser2)
  intersection = [val for val in movies1 if val in movies2]
  # if the users do not have at least (threshold) common ranked movies
  # we say that the distance between them are Infinite
  if(len(intersection) < threshold):
    return float('inf')

  sum = 0
  for key in intersection:
      match1 = filter(lambda x: x['movieId'] == key, moviesUser1)
      match2 = filter(lambda x: x['movieId'] == key, moviesUser2)
      sum += math.sqrt(pow(float(match1[0]['rating']) - float(match2[0]['rating']), 2))
  return 1 / (1+sum)

def manhattan_distance(moviesUser1, moviesUser2, threshold = 3):
  movies1 = map(lambda x: x['movieId'], moviesUser1)
  movies2 = map(lambda x: x['movieId'], moviesUser2)
  intersection = [val for val in movies1 if val in movies2]
  # if the users do not have at least (threshold) common ranked movies
  # we say that the distance between them are Infinite
  if(len(intersection) < threshold):
    return float('inf')

  sum = 0
  for key in intersection:
      match1 = filter(lambda x: x['movieId'] == key, moviesUser1)
      match2 = filter(lambda x: x['movieId'] == key, moviesUser2)
      sum += math.sqrt(pow(float(match1[0]['rating']) - float(match2[0]['rating']), 2))
  return 1 / (1+sum)

with open('ratings_small.csv') as csvfile:
  reader = csv.DictReader(csvfile)
  moviesPerUser = {}
  baseKey = str(sys.argv[1]) if len(sys.argv) > 1 else '1'
  similar = {}
  common = {}
  for key, row in groupby(list(reader), lambda x: x['userId']):
    moviesPerUser[key] = list(row)
    movies1 = map(lambda x: x['movieId'], moviesPerUser[baseKey])
    movies2 = map(lambda x: x['movieId'], moviesPerUser[key])
    intersection = [val for val in movies1 if val in movies2]

    d = euclidean_distance(moviesPerUser[baseKey], moviesPerUser[key])
    if(d<float('inf') and key != baseKey):
      similar[key] = d
      common[key] = len(intersection)
    
  print_similar(similar, common, "Euclidean Distance")
