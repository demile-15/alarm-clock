import tkinter as tk
from tkinter import ttk
import ttkbootstrap
from playsound import playsound
from datetime import datetime
import time as tm
import os

SOUND_PATH = os.path.join("sound", "uplifting_sound.mp3")


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

    w: int = 350 # width for the Tk window
    h: int = 500 # height for the Tk window

    # get screen width and height
    ws = window.winfo_screenwidth()  # width of screen
    hs = window.winfo_screenheight() # height of screen

    # calculate x and y coordinates for the Tk window
    x = round((ws/2) - (w/2))
    y = round((hs/2) - (h/2))

    # set the screen dimensions and where it is placed
    window.geometry(f"{w}x{h}+{x}+{y}")

    # set window title
    window.title("Clock") 


# Display the timer
def main() -> None:
    # window
    create_center_window()

    # title
    title_label = ttk.Label(master=window, text="Alarm", font="Calibri 20 bold")
    title_label.pack(pady= 10)

    # entry field
    input_frame = ttk.Frame(window, padding=10)
    input_frame.pack()

    entry_time_str = tk.StringVar()
    entry_wg = ttk.Entry(input_frame, textvariable=entry_time_str)
    entry_wg.pack(side="left")

    set_timer_button = ttk.Button(
        input_frame, 
        text="Set timer", 
        command=lambda: timer(entry_time_str.get()))
    set_timer_button.pack(side="left", padx = 10)
    
    # quit button
    quit_button = ttk.Button(window, text="Quit", command=window.destroy)
    quit_button.pack(pady=20)

    # Run
    window.mainloop()


if __name__ == "__main__":
    main()

