import matplotlib.pyplot as plt
import csv
import math
from itertools import groupby
import matplotlib.pyplot as plt

def get_common_movies(person1, person2):
  movies1 = map(lambda x: x['movieId'], person1)
  movies2 = map(lambda x: x['movieId'], person2)
  return [val for val in movies1 if val in movies2]

def pearson_similarity(person1, person2):
  intersection = get_common_movies(person1, person2)
  n = len(intersection)

  m1 = [[x for x in person1 if x['movieId'] == item] for item in intersection ]
  n1 = map(lambda x: float(x[0]['rating']), m1)
  numPow = map(lambda x: pow(x,2), n1)
  s1 = sum(n1)
  ss1 = sum(numPow)

  m2 = [[x for x in person2 if x['movieId'] == item] for item in intersection ]
  n2 = map(lambda x: float(x[0]['rating']), m2)
  numPow2 = map(lambda x: pow(x,2), n2)
  s2 = sum(n2)
  ss2 = sum(numPow2)

  movies1 = {}
  movies2 = {}
  for item in person1:
    movies1[item['movieId']] = float(item['rating'])
  for item in person2:
    movies2[item['movieId']] = float(item['rating'])

  ps = sum([movies1[c] * movies2[c] for c in intersection])
  num = n*ps - (s1*s2)
  den = math.sqrt((n*ss1 - math.pow(s1,2))*(n*ss2 - math.pow(s2,2)))
  return num/den if den != 0 else 0



with open('ratings_small.csv') as csvfile:
  reader = csv.DictReader(csvfile)
  moviesPerUser = {}
  baseKey = '1'
  list1 = []
  list2 = []
  for key, row in groupby(list(reader), lambda x: x['userId']):
    moviesPerUser[key] = list(row)
    intersection = get_common_movies(moviesPerUser[baseKey], moviesPerUser[key])
    list1.append(pearson_similarity(moviesPerUser[baseKey], moviesPerUser[key]))
    list2.append(len(intersection))

  plt.plot(list1, list2, 'ro')
  plt.axis([min(list1), max(list1), min(list2), max(list2)])
  plt.show()
