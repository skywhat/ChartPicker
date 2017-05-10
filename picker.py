'''
from matplotlib.pyplot import figure, show
import numpy as npy
from numpy.random import rand


if 1: # picking on a scatter plot (matplotlib.collections.RegularPolyCollection)

    x, y, c, s = rand(4, 100)
    def onpick3(event):
        ind = event.ind

        print 'onpick3 scatter:', ind, npy.take(x, ind), npy.take(y, ind)

    fig = figure()
    ax1 = fig.add_subplot(111)
    col = ax1.scatter(x, y, 100*s, c, picker=True)
    #fig.savefig('pscoll.eps')
    fig.canvas.mpl_connect('pick_event', onpick3)

show()
'''
'''
import matplotlib.pyplot as plt
import numpy as np

def onpick3(event):
    index = event.ind
    xy = event.artist.get_offsets()
    print '--------------'
    print xy[index]


fig, ax = plt.subplots()

x, y = np.random.random((2, 10))
x1, y1 = np.random.random((2, 10))

p = ax.scatter(x, y, marker='*', s=60, color='r', picker=True)
p1 = ax.scatter(x1, y1, marker='*', s=60, color='b', picker=True)

fig.canvas.mpl_connect('pick_event', onpick3)
plt.show()
'''
import numpy as np
import matplotlib.pyplot as plt

fig,ax=plt.subplots()
ax.plot(np.random.rand(100), 'o', picker=5)  # 5 points tolerance

def on_pick(event):
    line = event.artist
    xdata, ydata = line.get_data()
    ind = event.ind
    print('on pick line:', np.array([xdata[ind], ydata[ind]]).T)

cid = fig.canvas.mpl_connect('pick_event', on_pick)
plt.show()