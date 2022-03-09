import sys
import matplotlib
import matplotlib.pyplot as plt
import numpy as np

try:
  matplotlib.use('module://drawilleplot')
except:
  print('Please install `drawilleplot` and `windows-curses` (the latter isn\'t required for Unix flavors):')
  print('\tpip install drawilleplot')
  print('\tpip install windows-curses')
  sys.exit(0)

def f1(t):
    return np.exp(-t) * np.cos(2*np.pi*t)
def f2(t):
    return np.cos(2*np.pi*t)
t = np.arange(0.0, 5.0, 0.1)

def table():
    print([x for x in zip(t,f1(t))])
    print([x for x in zip(t,f2(t))])

def plot():
    plt.figure()
    plt.subplot(2, 1, 1) # nrows, ncols, index
    plt.plot(t, f1(t), 'bo', t, f1(t), 'k')

    plt.subplot(212)
    plt.plot(t, f2(t), 'r--')
    plt.show()

    plt.close()

actions = {'T': table, 'P': plot}
choice = None
while not choice in actions.keys():
    choice = input('Choose one of [T (tabulate), P (plot)] > ').upper()
result = actions[choice]()
