import numpy as np
from matplotlib import pyplot
sr_dict = {2: 11, 3: 5, 4: 6, 5: 4, 6: 13, 7: 2, 10: 1, 11: 1, 13: 1}
pcfg_dict = {2: 4, 3: 8, 4: 5, 5: 3, 6: 14, 7: 7, 10: 3, 11: 1, 13: 1}
y1 = np.array([0,0,11,5,6,4,13,2,0,0,1,0,0,1])
y2 = np.array([0,0,4,8,5,3,14,7,0,0,3,0,0,1])
x = np.arange(14)
print(x)

pyplot.bar(x, y1, alpha=0.5, label='SR Parser')
pyplot.bar(x, y2, alpha=0.5, label='PCFG Parser')
pyplot.legend(loc='upper right',prop={'size': 12})
pyplot.xlabel("Sentence Index",size=14)
pyplot.xticks(list(range(0,14)))
pyplot.ylabel("Number of incorrectly parsed words",size=14)
pyplot.show()