# -*- coding: utf-8 -*-
"""
Created on Tue Nov 12 01:00:37 2019

@author: VictorGueorguiev
"""
import numpy as np
import matplotlib.pyplot as plt
from subprocess import call
import pandas as pd
import time 

file_name = sys.argv[1]
output_file_name = 'matrix_results_df.txt'

input_file_def = open(file_name, 'w')
matrix_sizes = np.arange(100, 2800, 200)
subprocess.call(["gcc", "matrix_multiplication.c"])

for N in matrix_sizes:
    A = np.random.randint(0, 10, size = (N,N)) # generate matrix A as digits from 0-9 of size NxN
    B = np.random.randint(0, 10, size = (N,N)) # generate matrix B as digits from 0-9 of size NxN
    np.savetxt(fname = "m"+str(N)+"by"+str(N)+"A.txt", X = A, fmt="%s")
    np.savetxt(fname = "m"+str(N)+"by"+str(N)+"B.txt", X = B, fmt="%s")
    input_file_def.write(str(N) + " " + "m"+str(N)+"by"+str(N)+"A.txt " + "m"+str(N)+"by"+str(N)+"B.txt\n")

input_file_def.close()
    
input_file_def = open(file_name, 'r')

block_sizes = list(map(lambda block_size: int(block_size), [20,50,100, 500]))

print("This script executes matrix multiplication for the newly generated matrices in file",
        "'" + file_name + "'", "using the naive strategy and the blocked",
        "strategy for block sizes:", ", ".join(sys.argv[2:]))
print("The result of this script is a graph 'graph.png' in the current",
      "directory that shows the results with matrix size on the x-axis and",
      "time on the y-axis. Create one line for each block size and one line",
      "for the naive strategy.")

files = [line.strip().split(' ') for line in input_file_def.readlines()]
output_file = open(output_file_name, 'w')
output_file.write('method' + '\t' + 'n' + '\t' + 'time_spend' + '\t' + 'block_size')

for block_size in block_sizes:
    print("Now executing for block size: " + str(block_size))
    for args in files:
        if block_size >= int(args[0]):
            continue
        print("Matrix A: " + str(args[1]) + "\t\t" + "Matrix B: " + str(args[2]))
				start = time.time()
        call(["./matrix_multiplication", "blocked", str(args[0]),str(args[1]), str(args[2]), str(block_size)])
				duration = time.time() - start
				output_file.write('blocked' + '\t' + str(int(args[0])) + '\t' + str(duration) + '\t' + str(block_size))

## For the naive method
for args in files:
        print("Matrix A: " + str(args[1]) + "\t\t" + "Matrix B: " + str(args[2]))
        call(["./matrix_multiplication", "naive", str(args[0]),str(args[1]), str(args[2])])

data_df = pd.read_csv("matrix_results_df.txt", delimiter=r"\s+")
data_df['grouping_var'] = data_df.method + ' - ' + data_df.block_size.map(str)
data_df = data_df.assign(grouping_var2 = ['naive' if a == "naive - 1" else a for a in data_df['grouping_var']])

fig, ax = plt.subplots(figsize=(8,6))
for label, df in data_df.groupby('grouping_var'):
    df.time_spend.plot(kind="line", ax=ax, label=label)
plt.legend()
    
