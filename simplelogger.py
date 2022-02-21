import datetime as dt
import traceback
from pathlib import Path

def get_datetime_string():
    return dt.strftime("%Y-%m-%d_%H-%M-%S", dt.datetime.now())

def create_default_filename(string_in=''):
    return f"{get_datetime_string()}{string_in}.csv"

########## Logging Functions ##########

def create_log_file(name_string = ''):
    log_filename = get_path_to_save_file(default_filename = create_default_filename(name_string))
    out_text = f"Saving logfile as {log_filename}..."
    # textbox.insert('end',out_text + '\n')
    print(out_text)

    try:
        with open(log_filename, 'w', encoding="utf-8") as logfile:
            logfile.write('')
    except:
        print("Write fail")
        print(f"log_filename: {log_filename}")
        print(traceback.format_esc())
        quit()
    
    return log_filename

def write_header_to_log(log_filename, header_string):
    write_line_to_log(log_filename, header_string)    

def stop_log(log_filename):
    out_text = f"Logging Stopped"
    print(out_text)
    log_filename = None
    # textbox.insert('end',out_text + '\n')
    return None

def write_line_to_log(log_filename, line_string):
    try:
        if log_filename != None:
            with open(log_filename, 'a', encoding="utf-8") as logfile:
                logfile.write(line_string + '\n')
    except:
        # note, this usually appears when b_logging is true, but the log_filename
        # hasn't bee returned by the file dialog yet (because of tkinter, this 
        # is kind of acting like threading)
        print("Write fail")
        print(f"log_filename: {log_filename}")
        print(f"line_string: {line_string}")
        print(traceback.format_esc())
        quit()


class SimpleLogger():
    def __init__(self):
        pass

    def create_log_file(self):
        """ create a new log file"""
        pass

    def start_logging(self):
        """ start logging """
        pass

    def pause_logging(self):
        """ stop logging, but do not close the file """
        pass

    def close_log(self):
        """ stop logging, close the file and purge the filename"""
        pass

    def write_line_to_log(self, line):
        """ write a string to a single line """
        pass

    def write_header_to_log(self, line):
        """ writes a header line to the log """

    def get_iso_timestamp_string(self):
        """ returns an iso local timestamp string for use as a log line timestamp """
        return dt.datetime.now().isoformat()
