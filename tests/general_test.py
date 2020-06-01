import pytest
from progettobioinf.dataprocessing.initial_setup import *
import matplotlib.pyplot as plt

import sys, os
myPath = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, myPath + '/../')

def test_create_folder():
    create_img_folder()

def test_save_img_plot():
    plt.plot([0, 1, 2, 3, 4], [0, 4, 5, 8, 12])
    plt.savefig('img/test_plot.png')