from matplotlib import pyplot as plt
from sys import argv
import pandas as pd
import os
from typing import Tuple
from typing import List

# Globals
LOGLOG = True
SEMILOG = False
LEGEND = True
# LEGEND = False

dumbPlot = False
averageEachFreq = True
# dumbPlot = True
# averageEachFreq = False

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

def plotOne(filename: str) -> None:
    global averageEachFreq
    data: pd.DataFrame = pd.read_csv(filename)
    frequency_str, impedance_str, phase_str = findBodeNames(data)

    #Average the results
    if averageEachFreq:
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
    
    if LEGEND:
        canvas[0].legend()
        canvas[1].legend()
    plt.show(block=True)

def checkJsonHdr(filename: str) -> int:
    file = open(filename, 'r')
    data = file.readlines()
    file.close()

    for idx, line in enumerate(data):
        if('}' in line):
            return idx +1
    return 0

def plotData_append(filename: str, canvas, isReference: bool = False) -> None:
    global averageEachFreq
    skipLines = checkJsonHdr(filename)

    data: pd.DataFrame = pd.read_csv(filename, skiprows=skipLines)

    frequency_str, impedance_str, phase_str = findBodeNames(data)
    if averageEachFreq:
        data = data.groupby(frequency_str).mean(numeric_only=True).reset_index()

    shortFilename = filename.split('\\')[-1]

    if isReference:
        expectedZCol_str = "Expected |Z| (Ohms)"
        expectedPhaseCol_str = "Expected Phase (deg)"
        if (not(expectedZCol_str in data.columns)) or not(expectedPhaseCol_str in data.columns):
            print(f"Expected |Z| (Ohms) or Expected Phase (deg) not found in {filename}.")
            return
        canvas[0].plot(data[frequency_str], data[expectedZCol_str], label = shortFilename,linestyle='-', marker='x', color='red')
        canvas[1].plot(data[frequency_str], data[expectedPhaseCol_str], label = shortFilename, linestyle='-', marker='x', color='red')
    else:
        canvas[0].plot(data[frequency_str], data[impedance_str], label = shortFilename, linestyle='--', marker='o')
        canvas[1].plot(data[frequency_str], data[phase_str], label = shortFilename, linestyle='--', marker='o')

def plot_sequentially(rootDir: str, filterStr:str = None):
    for root, dirs, files in os.walk(rootDir):
        for name in files:
            if filterStr is None:
                plotOne(os.path.join(root, name))
            elif filterStr in name:
                plotOne(os.path.join(root, name))

def plot_all(rootDir: str, filterStr:str = None, plotTitle: str = None, plotExpectedZCol: bool = False):
    
    plotList: List[str] = []
    for root, dirs, files in os.walk(rootDir):
        for name in files:
            # skip everything but csv files
            if not name.endswith('.csv'):
                continue
            if filterStr is None:
                plotList.append(os.path.join(root, name))
            elif f'{filterStr}Ohm' in name:
                plotList.append(os.path.join(root, name))
    
    if len(plotList) > 0:
        
        fig, canvas = plt.subplots(2)
        if LOGLOG:
            canvas[0].set_xscale("log")
            canvas[0].set_yscale("log")
            canvas[1].set_xscale("log")
        elif SEMILOG:
            canvas[0].set_xscale("log")
            canvas[1].set_xscale("log")

        once = plotExpectedZCol # Just append one reference plot
        for item in plotList:
            if once:
                once = False
                plotData_append(item, canvas, True)
            plotData_append(item, canvas, False)
        if plotTitle is not None:
            canvas[0].set_title(plotTitle)
        if LEGEND:
            canvas[0].legend()
            canvas[1].legend()
        figManager = plt.get_current_fig_manager()
        #figManager.full_screen_toggle()
        figManager.resize(2000,4000)
        fig.canvas.toolbar.zoom()
        plt.show(block=False)


if __name__ == '__main__':
    dirStr = argv[1]

    if dumbPlot:
        #plot_sequentially(dirStr)
        
        plot_all(dirStr)
        input("hello")

    else:

        #plot current ranges
        impedanceGroups: List[str] = [
            "R100micro", "R1milli", "R15milli", "R100milli",
            "R1", "R10", "R100",
            "R1k", "R10k", "R100k",
            "R1Mega", "R10Mega", "R100Mega",
            "R1G", "R10G", "R50G"
        ]

        currentRangeQADir = dirStr + '/ch1/QCTests_AC/CurrentRanges'
        gainStageQADir = dirStr + '/ch1/QCTests_AC/GainStages'
        
        for impedanceStr in impedanceGroups:
            plot_all(currentRangeQADir, filterStr=impedanceStr, plotTitle=impedanceStr, plotExpectedZCol=True)
        
        #plot gain stages
        plot_all(gainStageQADir, plotTitle="Gain Stages")

        input("hello")  # because we are not using plt.show(block=True) anymore

        print(f'Files in {dirStr} done plotting.')
