from matplotlib import pyplot as plt
from sys import argv
import pandas as pd
import os
from typing import Tuple

LOGLOG = True
SEMILOG = False

def findBodeNames(data: pd.DataFrame) -> Tuple[str, str, str]:
    freqHdrStr: str = ""
    ZmodHdrStr: str = ""
    PhaseHdrStr: str = ""

    freqStrCandidates = ["Frequency (Hz)", "Frequency"]
    ZmodStrCandidates = ["|Z| (Ohms)", "Magnitude"]
    PhaseStrCandidtates = ["Phase (deg)", "Phase (degrees)"]
    for str in freqStrCandidates:
        if str in data.columns:
            freqHdrStr = str
            break
    for str in ZmodStrCandidates:
        if str in data.columns:
            ZmodHdrStr = str
            break
    for str in PhaseStrCandidtates:
        if str in data.columns:
            PhaseHdrStr = str
            break
    return (freqHdrStr, ZmodHdrStr, PhaseHdrStr)

def plotData(filename: str) -> None:
        data: pd.DataFrame = pd.read_csv(filename)
        frequency_str, impedance_str, phase_str = findBodeNames(data)

        #Average the results
        data = data.groupby(frequency_str).mean().reset_index()

        shortFilename = filename.split('\\')[-1]

        fig, canvas = plt.subplots(2)
        canvas[0].set_title(shortFilename)
        if LOGLOG:
            canvas[0].set_xscale("log")
            canvas[0].set_yscale("log")
            canvas[1].set_xscale("log")
        elif SEMILOG:
            canvas[0].set_xscale("log")
            canvas[1].set_xscale("log")
        canvas[0].plot(data[frequency_str], data[impedance_str], label = impedance_str,linestyle='--',marker='o')
        canvas[1].plot(data[frequency_str], data[phase_str], label = phase_str,linestyle='--',marker='o')
        
        canvas[0].legend()
        canvas[1].legend()
        plt.show(block=True)

def plotData_append(filename: str, canvas) -> None:
        data: pd.DataFrame = pd.read_csv(filename)
        frequency_str, impedance_str, phase_str = findBodeNames(data)

        #Average the results
        data = data.groupby(frequency_str).mean().reset_index()

        shortFilename = filename.split('\\')[-1]

        canvas[0].plot(data[frequency_str], data[impedance_str], label = impedance_str,linestyle='--',marker='o')
        canvas[1].plot(data[frequency_str], data[phase_str], label = phase_str,linestyle='--',marker='o')

def main():
    rootDir = argv[1]
    for root, dirs, files in os.walk(rootDir):
        for name in files:
            plotData(os.path.join(root, name))

def main2():
    rootDir = argv[1]
    fig, canvas = plt.subplots(2)
    if LOGLOG:
            canvas[0].set_xscale("log")
            canvas[0].set_yscale("log")
            canvas[1].set_xscale("log")
    elif SEMILOG:
        canvas[0].set_xscale("log")
        canvas[1].set_xscale("log")
    for root, dirs, files in os.walk(rootDir):
        for name in files:
            plotData_append(os.path.join(root, name), canvas)
    canvas[0].legend()
    canvas[1].legend()
    plt.show(block=True)


if __name__ == '__main__':
    #main()
    main2()