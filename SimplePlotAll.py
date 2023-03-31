from matplotlib import pyplot as plt
from sys import argv
import pandas as pd
import os
from typing import Tuple
from typing import List

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

def plotOne(filename: str) -> None:
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

def checkJsonHdr(filename: str) -> int:
    file = open(filename, 'r')
    data = file.readlines()
    file.close()

    for idx, line in enumerate(data):
        if('}' in line):
            return idx +1
    return 0

def plotData_append(filename: str, canvas, isReference: bool = False) -> None:
    
    skipLines = checkJsonHdr(filename)

    data: pd.DataFrame = pd.read_csv(filename, skiprows=skipLines)

    frequency_str, impedance_str, phase_str = findBodeNames(data)
    data = data.groupby(frequency_str).mean(numeric_only=True).reset_index()

    shortFilename = filename.split('\\')[-1]

    if isReference:

        canvas[0].plot(data[frequency_str], data[impedance_str], label = shortFilename,linestyle='-', marker='x', color='red')
        canvas[1].plot(data[frequency_str], data[phase_str], label = shortFilename, linestyle='-', marker='x', color='red')
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

def plot_all(rootDir: str, filterStr:str = None, plotTitle: str = None, refPlotDir: str = None):
    
    
    plotList: List[str] = []
    for root, dirs, files in os.walk(rootDir):
        for name in files:
            if filterStr is None:
                plotList.append(os.path.join(root, name))
            elif f'{filterStr}Ohm' in name:
                plotList.append(os.path.join(root, name))

    if refPlotDir is not None:
        for root, dirs, files in os.walk(refPlotDir):
            for name in files:
                if filterStr is None:
                    plotList.append(os.path.join(root, name))
                elif f'{filterStr}.csv' in name:
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
        for item in plotList:
            _isReference = False
            if refPlotDir is not None:
                _isReference = (refPlotDir in item)
            plotData_append(item, canvas, isReference=_isReference)
        if plotTitle is not None:
            canvas[0].set_title(plotTitle)
        canvas[0].legend()
        canvas[1].legend()
        figManager = plt.get_current_fig_manager()
        #figManager.full_screen_toggle()
        figManager.resize(2000,4000)
        fig.canvas.toolbar.zoom()
        plt.show(block=False)


if __name__ == '__main__':
    dumbPlot = False
    #dumbPlot = True
    sequencedPlot = True

    if dumbPlot:
        #plot_sequentially(dirStr)
        dirStr = argv[1]
        plot_all(dirStr)

    elif sequencedPlot:
        for idx, arg in enumerate(argv[1::2]):
            dirStr = argv[idx + 1]
            RAdirStr = argv[idx + 2]

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
                plot_all(currentRangeQADir, filterStr=impedanceStr, plotTitle=impedanceStr, refPlotDir=RAdirStr)
            
            #plot gain stages
            plot_all(gainStageQADir, plotTitle="Gain Stages")

            input("hello")

            print(f'Files in {dirStr} done plotting.')
