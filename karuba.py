import numpy as np

colors = ['brown', 'purple', 'blue', 'yellow']
tokens = ['adventurer', 'temple']

for token in tokens:
    xi = np.random.choice(np.arange(10,120, step=10, dtype=int), size=4, replace=False)
    idx = np.random.choice(np.arange(0,4,dtype=int), size=4, replace=False)
    for n,i in enumerate(idx):
          print '%s %s in %d'%(token, colors[i], xi[n])
