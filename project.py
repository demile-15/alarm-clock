import tkinter as tk
from tkinter import ttk
# import ttkbootstrap
from playsound import playsound
from datetime import datetime
import time as tm
import os

SOUND_PATH = os.path.join("sound", "uplifting_sound.mp3")
# TODO: music link: https://pixabay.com/sound-effects/search/alarm/

# Alarm clock
def alarm_clock(for_time):
    """
    Function takes in a time as a string and sets an alarm clock
    """
    current_time = datetime.now().strftime("%H:%M:%S")
    while current_time != for_time: 
        print("The current time is", current_time)
        tm.sleep(1)
        current_time = datetime.now().strftime("%H:%M:%S")
        
    print("Time to wake up!")
    playsound(SOUND_PATH)

# TODO: how to stop the sound when clicking Stop button?
# Countdown timer
def timer(for_time: str) -> None:
    """
    Function that takes in a time as a string HH:MM:SS, sets a countdown timer, 
    and plays sound when time is up
    """
    total_seconds = string_to_sec(for_time)
    tm.sleep(total_seconds)
    print("Timer's up!")
    playsound(SOUND_PATH)


# Helper to calculate seconds
def string_to_sec(time: str) -> int:
    """
    Helper to calculate the number of seconds in a period of time, 
    represented  as a string
    
    Param: 
    time -- a string to represent the input time, written in the form HH:MM:SS

    Return: 
    an integer that is the number of seconds in the given time
    """
    hr, mn, sec = map(int, time.split(":"))
    return hr*3600 + mn*60 + sec


# Helper to create a window in the middle of the screen
def create_center_window() -> None:
    """
    Function to create a tkinter window in the center of the screen
    """
    global window
    window = tk.Tk() # create the root window

    w: int = 500 # width for the Tk window
    h: int = 250 # height for the Tk window

    # get screen width and height
    ws = window.winfo_screenwidth()  # width of screen
    hs = window.winfo_screenheight() # height of screen

    # calculate x and y coordinates for the Tk window
    x = round((ws/2) - (w/2))
    y = round((hs/2) - (h/2))

    # set the screen dimensions and where it is placed
    window.geometry(f"{w}x{h}+{x}+{y}")
    window.resizable(False, False)

    # set window title
    window.title("Clock") 


# Display the timer
def main() -> None:
    # window
    create_center_window()

    # create 2 tabs for alarm clock and timer
    notebook = ttk.Notebook(window)
    alarm_tab = ttk.Frame(notebook, width=175)
    timer_tab = ttk.Frame(notebook, width=175) 
    notebook.add(alarm_tab, text="Alarms", underline=0)
    notebook.add(timer_tab, text="Timer", underline=0)
    notebook.pack(side='top', expand=True, fill='both')
    # notebook.grid(sticky='nsew')

    ## ALARM CLOCK TAB
    # title
    alarm_title_label = ttk.Label(
        master=alarm_tab, 
        text="Alarms", 
        font="Calibri 20 bold")
    alarm_title_label.pack(pady= 10)


    ## TIMER TAB
    # grid configure
    # timer_tab.columnconfigure(0, weight=1)
    # timer_tab.columnconfigure(1, weight=1)
    # timer_tab.rowconfigure(0, weight=1)
    # timer_tab.rowconfigure(1, weight=1)

    ### Function frame
    function_frame = ttk.Frame(master=timer_tab)
    function_frame.pack(expand=True, fill='both')

    ## Left frame
    # TODO: entry field that auto registers every 2 digits as part of hr, min
    #       and sec, gradually fills out the 00:00:00
    left_frame = ttk.Frame(master=function_frame)
    left_frame.pack(side='left', expand=True, fill='both')
        # grid configure
    # left_frame.columnconfigure((0, 2, 5), weight=1)
    # left_frame.columnconfigure((1, 3), weight=2)
    # left_frame.columnconfigure(2, weight=1)
    left_frame.columnconfigure((0, 1, 2, 3, 4, 5), weight=1)
    left_frame.rowconfigure((0, 2, 4), weight=1)
    left_frame.rowconfigure(1, weight=4)
    left_frame.rowconfigure(3, weight=2)


    # Entry frame
    # entry_frame = ttk.Frame(master=left_frame)
    # entry_frame.pack(side='top', expand=True, fill='both'
    entry_time = tk.StringVar(value="")
    entry_time_wg = ttk.Entry(
        left_frame, 
        textvariable=entry_time,
        width=15)
    #entry_time_wg.pack(side='top', pady=10)
    entry_time_wg.grid(row=1, column=1, columnspan=3, sticky='nsew')
        # keyboard Enter event
    entry_time_wg.bind(
        '<KeyPress-Return>', 
        lambda event: timer(entry_time.get()))

    
    # Start/reset frame
    # start_reset_frame = ttk.Frame(master=left_frame)
    # start_reset_frame.pack(side='top', expand=True, fill='both')
        # TODO: start-stop button: start button says 'Stop' once it's selected
    start_button = ttk.Button(
        left_frame, 
        text="Start",
        command=lambda: timer(entry_time.get()))
    # start_button.pack(side='left', padx=20)
    start_button.grid(row=3, column=1, sticky='nsew')
    
    
    # TODO: reset button: re-enter the input value, awaiting user to start timer
    reset_button = ttk.Button(left_frame, text="Reset")
    # reset_button.pack(side='left', padx=10)
    reset_button.grid(row=3, column=3, sticky='nsew')


    # menu button for choosing which sound to be used
    right_frame = ttk.Frame(master=function_frame)
    right_frame.pack(side='right', expand=True, fill='both')
    sound_menu = tk.Menubutton(right_frame, text='Sound')
    sound_menu.pack(side='top', expand=True, fill='x')


    ### Progress bar


    # Run
    window.mainloop()


if __name__ == "__main__":
    main()

