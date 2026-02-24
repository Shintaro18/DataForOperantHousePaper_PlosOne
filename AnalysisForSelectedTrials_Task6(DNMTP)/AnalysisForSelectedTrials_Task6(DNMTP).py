import tkinter as tk
from tkinter import filedialog
import csv

#===========config===============
# Threshold is set by the following formula:
# (programmed delay) x DelayTh1 + DelayTh2
DelayTh1 = 1.3
DelayTh2 = 10
#================================


DebugMode = 0

if DebugMode == 1:
    FilePaths=[""]*3
    FilePaths[0] = "sample/2021_5_1 0h0m Task23 Touch.csv"
    FilePaths[1] = "sample/2021_5_2 0h0m Task23 Touch.csv"
    FilePaths[2] = "sample/2021_5_3 0h0m Task23 Touch.csv"

if DebugMode == 0:
    root = tk.Tk()
    root.withdraw()

    # Choose CSV file
    FilePaths = filedialog.askopenfilenames(
        title="Choose CSV files",
        filetypes=[("CSV files", "*.csv"), ("All files", "*.*")],
        multiple=True  # 複数選択を明示的に有効化
    )
    root.destroy()


if FilePaths:
    print("selected files:")
    for file in FilePaths:
        print(f"  - {file}")

WriterRes = open(FilePaths[0] + "_res.csv",'w')  # Initialize the text exporter
WriterRes.write("DelayA,,,,DelayB,,,,DelayA,,,,DelayB,,,,"+"\n")
WriterRes.write("All trials,,,,,,,,Selected trials,,,,,,,," + "\n")
WriterRes.write("Total trials,Correct trials,Incorrect trials,%Correct,Total trials,Correct trials,Incorrect trials,%Correct,Total trials,Correct trials,Incorrect trials,%Correct,Total trials,Correct trials,Incorrect trials,%Correct,FilePath\n")

# Main loop
for i in range(len(FilePaths)):

    #Load data
    data = []
    f = FilePaths[i]
    with open(f, 'r', encoding='utf-8') as file:
        csv_reader = csv.reader(file)
        for row in csv_reader:
            data.append(row)

    TotalTrials = len(data)/5
    SampleTouchTime =[0.0]*10000
    ChoiceTouchTime = [0.0] * 10000
    TrialDelay = [0] * 10000
    TrialRes = [0] * 10000
    TrialType = [0] * 10000
    ProgrammedDelay = [0.0]*10000
    DelayTh = [0.0]*10000

    EventTimeSec = [0.0] * 50000

    # Calculate event time in sec
    for row in range(len(data)):
        #print("s"+str(data[1][5]))
        EventTimeSec[row] = float(data[row][5])*24.0*60.0*60.0 + float(data[row][6])*60.0*60.0 + float(data[row][7])*60.0 + float(data[row][8])
        #print(str(EventTimeSec[row]))


    # Get information for each trials
    CorrectTrialsA=0
    WrongTrialsA = 0
    CorrectRateA = 0.0
    TotalTrialsSelectedA = 0
    CorrectTrialsSelectedA = 0
    WrongTrialsSelectedA = 0
    CorrectRateSelectedA = 0.0

    CorrectTrialsB = 0
    WrongTrialsB = 0
    CorrectRateB = 0.0
    TotalTrialsSelectedB = 0
    CorrectTrialsSelectedB = 0
    WrongTrialsSelectedB = 0
    CorrectRateSelectedB = 0.0

    CurrTrial=1
    for Trial in range(int(TotalTrials)):    # Loop for each trial
        # Scan csv
        for row in range(len(data)): # loop for each event
            #print("row:"+str(row))
            if data[row][0] == str(CurrTrial) and data[row][1] == "1":
                SampleTouchTime[CurrTrial] = EventTimeSec[row]
            if data[row][0] == str(CurrTrial):
                if data[row][1] == "4" or data[row][1] == "5":
                    ChoiceTouchTime[CurrTrial] = EventTimeSec[row]
                    if data[row][1] == "4":   #If this trial is correct
                        TrialRes[CurrTrial] = 1
                        TrialType[CurrTrial] = int(data[row][10])
                    if data[row][1] == "5":   #If this trial is incorrect
                        TrialRes[CurrTrial] = 2
                        TrialType[CurrTrial] = int(data[row][10])
                    ProgrammedDelay[CurrTrial] = float(data[row][9])
                    DelayTh[CurrTrial] = ProgrammedDelay[CurrTrial]*1.3 + 10.0
        TrialDelay[CurrTrial] = ChoiceTouchTime[CurrTrial]-SampleTouchTime[CurrTrial]

        if TrialRes[CurrTrial]==1:  # If this is a correct trial
            if TrialType[CurrTrial]==0:
                CorrectTrialsA += 1
            if TrialType[CurrTrial] == 1:
                CorrectTrialsB += 1
            if TrialDelay[CurrTrial] <= DelayTh[CurrTrial]: # If the actual delay is shorter than the threshold
                if TrialType[CurrTrial] == 0:
                    CorrectTrialsSelectedA += 1    # add number of correct response performed within the delay threshold
                if TrialType[CurrTrial] == 1:
                    CorrectTrialsSelectedB += 1    # add number of correct response performed within the delay threshold
        if TrialRes[CurrTrial]==2:  # If this is a wrong trial
            if TrialType[CurrTrial] == 0:
                WrongTrialsA += 1
            if TrialType[CurrTrial] == 1:
                WrongTrialsB += 1
            if TrialDelay[CurrTrial] <= DelayTh[CurrTrial]: # If the actual delay is shorter than the threshold
                if TrialType[CurrTrial] == 0:
                    WrongTrialsSelectedA += 1  # add number of incorrect response performed within the delay threshold
                if TrialType[CurrTrial] == 1:
                    WrongTrialsSelectedB += 1  # add number of incorrect response performed within the delay threshold

        print("Trial:"+str(CurrTrial)+" "+str(TrialRes[CurrTrial]))
        CurrTrial+=1


    TotalTrialsA = CorrectTrialsA + WrongTrialsA
    TotalTrialsB = CorrectTrialsB + WrongTrialsB
    TotalTrialsSelectedA = CorrectTrialsSelectedA + WrongTrialsSelectedA
    TotalTrialsSelectedB = CorrectTrialsSelectedB + WrongTrialsSelectedB
    if TotalTrialsA > 0:
        CorrectRateA = float(CorrectTrialsA) / float(TotalTrialsA) *100.0
    if TotalTrialsB > 0:
        CorrectRateB = float(CorrectTrialsB) / float(TotalTrialsB) *100.0
    if TotalTrialsSelectedA > 0:
        CorrectRateSelectedA = float(CorrectTrialsSelectedA) / float(TotalTrialsSelectedA) *100.0
    if TotalTrialsSelectedB > 0:
        CorrectRateSelectedB = float(CorrectTrialsSelectedB) / float(TotalTrialsSelectedB) *100.0

    # Export csv file
    WriterRes.write(str(TotalTrialsA) + "," + str(CorrectTrialsA) + "," + str(WrongTrialsA) + "," +str(CorrectRateA)  +","+  str(TotalTrialsB) + "," + str(CorrectTrialsB) + "," + str(WrongTrialsB) + "," +str(CorrectRateB) +
                    ","+ str(TotalTrialsSelectedA) + "," + str(CorrectTrialsSelectedA) + "," + str(WrongTrialsSelectedA)+","+str(CorrectRateSelectedA)  +","+  str(TotalTrialsSelectedB) + "," + str(CorrectTrialsSelectedB) + "," + str(WrongTrialsSelectedB)+","+str(CorrectRateSelectedB)+","+FilePaths[i]+"\n")

