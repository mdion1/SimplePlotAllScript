from matplotlib import pyplot as plt
from sys import argv
import pandas as pd
import os
from typing import Tuple
from typing import List
import numpy as np

def plotfft(filename: str, samplingFreq: float, column: str, delimiter: str, skiprows: int = 0):
    data = pd.read_csv(filename,skiprows=skiprows, delimiter=delimiter)
    ydata = np.abs(np.fft.fft(data[column])) / len(data[column])
    xdata = np.linspace(0, samplingFreq, len(data[column]))
    fig, canvas = plt.subplots(1)
    canvas.set_yscale("log")
    plt.plot(xdata, ydata)
    plt.show(block=True)

    


if __name__ == '__main__':
    #filename = "C:/Users/Matt Dion/Desktop/junk data/debugging 60hz noise/Plus1920 100MOhm/3_2_2023 4_01 PM 33Hz 9.97833e+07Ohms.txt"
    filename = "C:/Users/Matt Dion/Desktop/junk data/debugging 60hz noise/Plus1894 100MOhm known bad/3_2_2023 10_50 AM 33Hz 1.00705e+08Ohms.txt"
    samplingFreq = 511.01207432044089 * 33  # in Hz
    #plotfft(filename, samplingFreq, "Current", '\t', skiprows=6)


    filename = "C:/Users/Matt Dion/Desktop/junk data/debugging 60hz noise/Plus1905 1_Chronoamperometry 20230302 170457.csv"
    #filename = "C:/Users/Matt Dion/Desktop/junk data/debugging 60hz noise/Plus1894 1_Chronoamperometry 20230302 132102.csv"
    samplingFreq = 1.0 / 200e-6
    plotfft(filename, samplingFreq, "Current (A)", ',')
    