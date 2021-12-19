# -*- coding: utf-8 -*-
"""Homework 7 Kyle Arbide.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1R867Kod9zmABrOnh2nTyEY9iDYKq_TDa
"""

import pandas as pd

"""Dot Product From Scratch

"""

#vector
a = [5,6,10]
b = [3,2,6]

def dvector(x,y):
  if len(x) != len(y):
    raise Exception("Vectors must be same length")
  dotP = 0
  for i in range(len(x)):
    dotP += x[i]*y[i]
  return dotP

print(dvector(a,b))  
#check
aDF = pd.DataFrame(a).transpose()
bDF = pd.DataFrame(b)

print(aDF.dot(bDF))

# Matrix
a=pd.DataFrame([{"foo":5,"bar":6,"baz":10},{"foo":3,"bar":2,"baz":10}])
b=pd.DataFrame([{"foo":5,"bar":6,"baz":10},{"foo":3,"bar":2,"baz":10},{"foo":6,"bar":7,"baz":14}])

def dmatrix(x,y):
  if len(x.columns) != len(y.columns):
    raise Exception("Must have same shape")
  yT= y.transpose()
  dotM = pd.DataFrame()
  for i in range(len(x.columns)):
    for j in range(len(yT.columns)):
    dotM[i] = x.iloc[i]*yT.iloc[j]
    return(dotM) 
  

dmatrix(a,b)
#Couldn't quite get the dot product of matricies from scratch

#eucladian distance
a=pd.DataFrame([{"foo":5,"bar":6,"baz":10},{"foo":3,"bar":2,"baz":10},{"foo":5,"bar":6,"baz":10},{"foo":3,"bar":2,"baz":10},{"foo":6,"bar":7,"baz":14}])

def euDist(x,y):
  if x.shape != y.shape:
    raise Exception("Vectors must be same length")
  squareDist = 0
  for i in range(len(x)):
    squareDist += pow((x[i] - y[i]),2)

  return(pow(squareDist,0.5))

print(euDist(a.iloc[0],a.iloc[3]))

def sumOfSquares(x):
  return(pow(sum(pow(x,2)),0.5))


def CosDist(x,y):
  return(dvector(x,y)/(sumOfSquares(x)*sumOfSquares(y)))

CosDist(a.iloc[0],a.iloc[3])

def manDistance(x,y):
  mdis = 0
  for i in range(len(x)):
    mdis += abs(x[i]-y[i])

  return(mdis)

manDistance(a.iloc[0],a.iloc[3])

# One-Hot Encoding

hotDf = pd.DataFrame([{"vehicle_id":111,"color":"Red","Drive":"Four-Wheel", "make":"Jeep"},{"vehicle_id":112,"color":"White","Drive":"Front-Wheel", "make":"Honda"},{"vehicle_id":113,"color":"White","Drive":"Rear-Wheel", "make":"Honda"},
                      {"vehicle_id":114,"color":"Black","Drive":"Rear-Wheel", "make":"Toyota"},{"vehicle_id":115,"color":"Black","Drive":"Four-Wheel", "make":"Toyota"},{"vehicle_id":116,"color":"Black","Drive":"Four-Wheel", "make":"Jeep"}])
hotDf.set_index(hotDf["vehicle_id"],inplace = True)

colors = pd.get_dummies(hotDf.color, prefix="Color", dtype="int")
drives = pd.get_dummies(hotDf.Drive, prefix = "Drive", dtype = "int")
makes = pd.get_dummies(hotDf.make, dtype = "int")

main = colors.merge(drives, how = 'outer', on = "vehicle_id")
main = main.merge(makes, how = 'outer', on = "vehicle_id")

print(euDist(main.iloc[0],main.iloc[5]))
print(CosDist(main.iloc[0],main.iloc[5]))
print(euDist(main.iloc[0],main.iloc[1]))

#Kyle Distance
#takes the reciprocal 1/x to give weigth to low scores
golfScores = pd.DataFrame([{"One":3, "Two":3, "Three":6, "Four":7, "Five":4},{"One":5, "Two":4, "Three":7, "Four":7, "Five":5},{"One":3, "Two":2, "Three":4, "Four":5, "Five":3},{"One":1, "Two":3, "Three":3, "Four":4, "Five":2}])

def kyleDistance(x,y):
  kdis = 0
  for i in range(len(x)):
    kdis += abs(1/x[i] - 1/y[i])

  return(kdis)
print(kyleDistance(golfScores.iloc[0],golfScores.iloc[1]))
print(kyleDistance(golfScores.iloc[0],golfScores.iloc[3]))
print(kyleDistance(golfScores.iloc[2],golfScores.iloc[3]))