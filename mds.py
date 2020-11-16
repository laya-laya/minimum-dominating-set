#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov 16 17:04:47 2020

@author: layaparkavousi
"""

import pulp 
import networkx as nx
from numpy import genfromtxt
import pandas as pd
import matplotlib.pyplot as plt
import time
## preparing the dataset and the adjacency matrix
mydata = genfromtxt('chrom.csv', delimiter=',')
mydata = mydata[1:,1:]
m = len(mydata)

for i in range(0,m):
    for j in range(0,m):
        if mydata[i][j] ==1:
            mydata[i][j] = 0
        elif mydata[i][j]==2:
            mydata[i][j] = 1
        elif mydata[i][j]==3:
            mydata[i][j] = 0.5
            

## make graph from the data with NetworkX and plot it
            
G = nx.Graph(mydata)
plt.figure(3,figsize=(12,12)) 
nx.draw(G,node_color="b", node_size=7,width=0.05)

## finding minimum dominating set

# define the problem
prob = pulp.LpProblem("minimum_dominating_set", pulp.LpMinimize)

# define the variables
x = pulp.LpVariable.dicts("x", G.nodes(), cat=pulp.LpBinary)

# define the objective function
start_time = time.time()


for (v,u) in G.edges():
    
    prob += pulp.lpSum(x)
    
# define the constraints
for v in G.nodes():
       prob += x[v] + pulp.lpSum([x[u] for u in G.neighbors(v)]) >= 1
        
        
# solve
prob.solve()
end_time = time.time()
print("%s seconds" % (end_time - start_time))

# display solution
for v in G.nodes():
    if pulp.value(x[v]) > 0.99:
         print("node %s selected"%v)
         
         
for v in prob.variables():
    if v.varValue == 1:
        print(v.name, "=", v.varValue)