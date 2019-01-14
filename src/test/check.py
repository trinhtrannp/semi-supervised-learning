import matplotlib.pyplot as plt
import numpy as np

plt.figure(1)
a = np.array([1, 2, 3, 4])
b = np.array([1, 4, 9, 16])
bm = [b.mean()]*len(b)
b = np.append(b, [100])
print bm
print b


