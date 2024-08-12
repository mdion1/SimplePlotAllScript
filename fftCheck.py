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

def plotfftAvg(filenameList: List[str], samplingFreq: float, column: str, delimiter: str, skiprows: int = 0):
    ydata: List = []
    for filename in filenameList:
        data = pd.read_csv(filename,skiprows=skiprows, delimiter=delimiter)
        ydata.append(np.fft.fft(data[column]) / len(data[column]))
    ydataAvg = np.mean(ydata, axis=0)
    xdata = np.linspace(0, samplingFreq, len(data[column]))
    fig, canvas = plt.subplots(1)
    canvas.set_yscale("log")
    plt.plot(xdata, ydataAvg)
    plt.show(block=True)

def plotfftAll(filenameList: List[str], samplingFreq: float, column: str, delimiter: str, skiprows: int = 0):
    fig, canvas = plt.subplots(1)
    canvas.set_yscale("log")

    ydata: List = []
    for filename in filenameList:
        shortFilename = filename.split('/')[-1]
        data = pd.read_csv(filename,skiprows=skiprows, delimiter=delimiter)
        xdata = np.linspace(0, samplingFreq, len(data[column]))
        ydata = np.abs(np.fft.fft(data[column])) / len(data[column])
        plt.plot(xdata, ydata, label=shortFilename)
    canvas.legend()
    plt.show(block=True)

if __name__ == '__main__':
    samplingFreq = 9.62E+05  # in Hz
    varNames: List[str] = ["Current", "Voltage"]
    for varName in varNames:
        plotfftAll(
            argv[1::-2],    # all files listed in argv (skip first and last element)
            samplingFreq, varName, '\t', skiprows=6
        )