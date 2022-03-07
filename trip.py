import time
import networkx

import nodemap
import msgparse

import matplotlib
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation


def navigate(m, route):
    print(f'navigating route:\n{route}')