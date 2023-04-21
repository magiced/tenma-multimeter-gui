import pandas as pd
import matplotlib.pyplot as plt
import datetime as dt
from pathlib import Path
from easyfiledialogs import get_path_to_open_file

def get_timestamp_from_string(string):
    return dt.datetime.fromisoformat(string)

### ========== PROGRAM ========== ###
def plot_tenma_logfile(filename, show_plot=True):
    filename = Path(filename)

    df = pd.read_csv(filename, index_col = False)

    # add check to make sure mode is the same all the way through the log

    df["datetime"] = df["Time"].apply(get_timestamp_from_string)
    df['elapsed time'] = df["Timestamp"].diff().cumsum()
    
    print()

    series_label = df.loc[1,'Mode']
    y_label = f'[{df.loc[1, "Display Unit"]}]'

    fig, ax = plt.subplots(dpi=200)
    fig.set_size_inches(8, 4)


    test_time = df['elapsed time'].max()

    if (test_time > (2 * 60 * 60)):
        # test is over 2 hours long
        # plot time in hours
        ax.plot(df['elapsed time']/(60*60),df['Display Value'], label=series_label)
        x_label = "Time [hours]"
        duration_string = f"Duration: {test_time/(60*60):.02f} hours"
    elif (test_time > (3 * 60)):
        # test is over 3 minutes
        # plot time in minutes
        ax.plot(df['elapsed time']/(60),df['Display Value'], label=series_label)
        x_label = "Time [mins]"
        duration_string = f"Duration: {test_time/(60):.02f} mins"
    else:
        # plot time in seconds
        ax.plot(df['elapsed time'],df['Display Value'], label=series_label)
        x_label = "Time [secs]"
        duration_string = f"Duration: {test_time:.02f} secs"

    #todo - turn this into annotation
    average_string = f"Average: {df['Display Value'].mean():.03f} {df.loc[1, 'Display Unit']}"
    min_string = f"Min: {df['Display Value'].min():.03f} {df.loc[1, 'Display Unit']}"
    max_string = f"Max: {df['Display Value'].max():.03f} {df.loc[1, 'Display Unit']}"
    
    # print(duration_string)
    # print(average_string)
    # print(min_string)
    # print(max_string)

    x_label = f"{x_label}, ({duration_string})\n{average_string}, {min_string}, {max_string}"

    title = filename.stem.replace("_", " ")
    ax.set_title(title)
    ax.set_ylabel(y_label)
    ax.set_xlabel(f"{x_label}")
    plt.xticks(rotation=30, ha='right')  
    fig.legend()
    fig.tight_layout()
    plt.savefig(filename.parent / (filename.stem +  '-GRAPH.png'),dpi=200)
    if show_plot:
        fig.show()

if __name__ == '__main__':
    plot_tenma_logfile(get_path_to_open_file())