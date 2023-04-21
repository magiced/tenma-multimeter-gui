from pathlib import Path
from easyfiledialogs import open_folder_path
import plotTenmaLog
import os

folder = open_folder_path()
files = os.listdir(folder)

for f in files:
    if f.endswith('.csv'):
        print(f"Plotting {f}")
        try:
            plotTenmaLog.plot_tenma_logfile(folder / f, show_plot = False)
        except KeyError:
            print("- FAILED: KeyError !!!!!!!!!!!!!!!!!!!!!!!!!!")   
    else:
        print(f'Skipping {f}')
    print('-------------------------------')

print('####################################\n')
print("Finished")

