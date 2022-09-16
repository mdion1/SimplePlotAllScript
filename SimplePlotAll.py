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

def plotData_append(filename: str, canvas) -> None:
        data: pd.DataFrame = pd.read_csv(filename)
        frequency_str, impedance_str, phase_str = findBodeNames(data)

        shortFilename = filename.split('\\')[-1]

        canvas[0].plot(data[frequency_str], data[impedance_str], label = impedance_str,linestyle='--',marker='o')
        canvas[1].plot(data[frequency_str], data[phase_str], label = phase_str,linestyle='--',marker='o')

def plot_sequentially(rootDir: str, filterStr:str = None):
    for root, dirs, files in os.walk(rootDir):
        for name in files:
            if filterStr is None:
                plotOne(os.path.join(root, name))
            elif filterStr in name:
                plotOne(os.path.join(root, name))

def plot_all(rootDir: str, filterStr:str = None, plotTitle: str = None):
    plotList: List[str] = []
    for root, dirs, files in os.walk(rootDir):
        for name in files:
            if filterStr is None:
                plotList.append(os.path.join(root, name))
            elif filterStr in name:
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
            plotData_append(item, canvas)
        if plotTitle is not None:
            canvas[0].set_title(plotTitle)
        canvas[0].legend()
        canvas[1].legend()
        plt.show(block=True)


if __name__ == '__main__':
    dumbPlot = False
    sequencedPlot = True

    for dirStr in argv[1:]:

        if dumbPlot:
            plot_sequentially(dirStr)
            #plot_all(dirStr)

        if sequencedPlot:
            #plot current ranges
            impedanceGroups: Tuple[str] = (
                "R100milliOhm", "R1Ohm", "R10Ohm", "R100Ohm",
                "R1kOhm", "R10kOhm", "R100kOhm",
                "R1MegaOhm", "R10MegaOhm", "R100MegaOhm",
                "R1GOhm", "R10GOhm", "R50GOhm"
            )

            currentRangeQADir = dirStr + '/ch1/QCTests_AC/CurrentRanges'
            gainStageQADir = dirStr + '/ch1/QCTests_AC/GainStages'
            
            for impedanceStr in impedanceGroups:
                plot_all(currentRangeQADir, filterStr=impedanceStr, plotTitle=impedanceStr)
            
            #plot gain stages
            plot_all(gainStageQADir, plotTitle="Gain Stages")

        print(f'Files in {dirStr} done plotting.')
