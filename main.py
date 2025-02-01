import pandas as pd
import matplotlib.pyplot as plt
import openpyxl
from conda.base.constants import ValueEnum

print("PLEASE ENSURE ALL EXCEL FILES ARE LOCATED IN THE SAME FOLDER AS THIS SCRIPT")
print("Current Script Location:", __file__)
while True:
    try:
        excel_name = str(input("Enter the excel file name (without .xlsl)"))
        break
    except FileNotFoundError:
        print("The file does not exist.")

df = pd.DataFrame()
fig, ax = plt.subplots(figsize=(10,4))

colors = {
    'W': 'tab:blue',
    'R': 'tab:orange',
    'S': 'tab:green',
    'G': 'magenta',
    'D': 'tab:red'
}


for x in pd.ExcelFile(excel_name + ".xlsx").sheet_names:
    excelFile = pd.read_excel(excel_name + ".xlsx", sheet_name=x)
    excelFile = excelFile.query('`base key`.isna() == False')
    excelFile = excelFile.filter(items=['base key', 'base t1adj', 'base t2adj', 'base Δt'])
    print("Working on Sheet ", x)

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
        for _, rows in rat_data.iterrows():
            ax.broken_barh([(rows['Start_Time'], rows['Duration'])],
                           (idx-0.4,0.8), facecolors=colors.get(rows['Behaviour'], 'tab:gray'))


ax.set_yticks(range(len(rats)))
ax.set_yticklabels(rats)

ax.grid(True, axis='x', linestyle='--', alpha=0.7)
ax.set_ylim(-1, len(rats))  # Adjust to fit all rats

plt.tight_layout()
plt.show()
plt.savefig("Shee")

