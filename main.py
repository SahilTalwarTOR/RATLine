from itertools import count
from os.path import exists

import pandas as pd
import matplotlib.pyplot as plt
import openpyxl
from datetime import datetime
import time
import os
import matplotlib.patches as mpatches
import psutil, os

p = psutil.Process(os.getpid())  # Get current process
p.nice(psutil.HIGH_PRIORITY_CLASS)  # Windows: HIGH_PRIORITY_CLASS
# p.nice(-10)  # Linux/Mac: Set priority (-20 is highest, 19 is lowest)
print("CPU priority set to highest")

pd.options.mode.chained_assignment = None  # Reduce warning overhead
print("Enabled multi threading")


#Setting up our config file
while True:
    try:
        file = "config.txt"

        with open(file, 'r') as f:
            lines = f.readlines()
        colors = {}
        for line in lines:
            key, value = line.strip().split(':')
            colors[key.strip()] = value.strip()
        break
    except FileNotFoundError:
        print("The config file for colours does not exist, did you include it in the current directory?", __file__)

print("Colours Configured")

print("PLEASE ENSURE ALL EXCEL FILES ARE LOCATED IN THE SAME FOLDER AS THIS SCRIPT")
print("Current Script Location:", __file__)
while True:
    try:
        excel_name = str(input("Enter the excel file name (without .xlsl)"))
        if os.path.isfile(excel_name + ".xlsx"):
            break
        else:
            raise FileNotFoundError()
    except FileNotFoundError:
        print("The file does not exist, make sure the excel file is typed without .xlsx, and is included in the same directory as the script\nCurrent Directory: ", __file__)


start = time.time()
df = pd.DataFrame()
fig, ax = plt.subplots(figsize=(10,4))


maxX = len(pd.ExcelFile(excel_name + ".xlsx").sheet_names)
iterator = 0

##FIRST TIMELINE
print("CREATING BASE GRAPHS")

for x in pd.ExcelFile(excel_name + ".xlsx").sheet_names:
    excelFile = pd.read_excel(excel_name + ".xlsx", sheet_name=x, engine="openpyxl")
    excelFile = excelFile.query('`base key`.isna() == False')
    excelFile = excelFile.filter(items=['base key', 'base t1adj', 'base t2adj', 'base Δt'])
    print("Working on Sheet ", x, iterator, "/", maxX)
    iterator += 1

    data = {
        'RAT_ID': [x] * len(excelFile),
        'Behaviour': excelFile['base key'],
        'Start_Time': excelFile['base t1adj'],
        'End_Time': excelFile['base t2adj'],
    }

    convertedDf = pd.DataFrame(data)

    df = pd.concat([df, convertedDf], ignore_index=True)
    df['Duration'] = df['End_Time'] - df['Start_Time']

    rats = df['RAT_ID'].unique()


    for idx, rat in enumerate(rats):
        rat_data = df[df['RAT_ID'] == rat]

        ax.broken_barh(list(zip(rat_data['Start_Time'], rat_data['Duration'])),
                           (idx-0.4,0.8), facecolors=[colors.get(behavior, 'tab:gray') for behavior in rat_data['Behaviour']])


ax.set_yticks(range(len(rats)))
ax.set_yticklabels(rats)
ax.set_title("RAT Base Timeline")

legend_patches = [mpatches.Patch(color=color, label=behavior) for behavior, color in colors.items()]

ax.legend(handles=legend_patches, title="Letter Colours",loc='upper center', bbox_to_anchor=(0.5, -0.05),
          fancybox=True, shadow=True, ncol=5)


ax.grid(True, axis='x', linestyle='--', alpha=0.7)
ax.set_ylim(-1, len(rats))  # Adjust to fit all rats

print("COMPLETED BASE TIMELINE")
print("STARTING TEST TIMELINE")
iterator = 0

df2 = pd.DataFrame()
fig2, ax2 = plt.subplots(figsize=(10,4))
plt.tight_layout()


for x in pd.ExcelFile(excel_name + ".xlsx").sheet_names:
    excelNext = pd.read_excel(excel_name + ".xlsx", sheet_name=x, engine="openpyxl")
    excelNext = excelNext.query('`test key`.isna() == False')
    excelNext = excelNext.filter(items=['test key', 'test t1adj', 'test t2adj', 'test Δt'])
    print("Working on Sheet ", x, iterator, "/", maxX)
    iterator += 1

    data2 = {
        'RAT_ID': [x] * len(excelNext),
        'Behaviour': excelNext['test key'],
        'Start_Time': excelNext['test t1adj'],
        'End_Time': excelNext['test t2adj'],
    }

    convertedDf2 = pd.DataFrame(data2)
    df2 = pd.concat([df2, convertedDf2], ignore_index=True)
    df2['Duration'] = df2['End_Time'] - df2['Start_Time']

    rats2 = df2['RAT_ID'].unique()

    for idx, rat in enumerate(rats2):
        rat_data2 = df2[df2['RAT_ID'] == rat]

        ax2.broken_barh(list(zip(rat_data2['Start_Time'], rat_data2['Duration'])),
                           (idx - 0.4, 0.8),
                           facecolors=[colors.get(behavior, 'tab:gray') for behavior in rat_data2['Behaviour']])


ax2.set_yticks(range(len(rats2)))
ax2.set_yticklabels(rats2)
ax2.set_title("RAT Test Timeline")

ax2.legend(handles=legend_patches, title="Letter Colours",loc='upper center', bbox_to_anchor=(0.5, -0.05),
          fancybox=True, shadow=True, ncol=5)


ax2.grid(True, axis='x', linestyle='--', alpha=0.7)
ax2.set_ylim(-1, len(rats2))  # Adjust to fit all rats


plt.tight_layout()
end = time.time()
fig.savefig("Base_Timeline_" + datetime.now().strftime("%Y-%m-%d_%H-%M-%S") + ".png", dpi=300, bbox_inches='tight')
fig2.savefig("Test_Timeline_" + datetime.now().strftime("%Y-%m-%d_%H-%M-%S") + ".png", dpi=300, bbox_inches='tight')
plt.show()

print("Execution: ", end - start, "s")

