import tkinter as tk
from tkinter import ttk
# import ttkbootstrap
import threading
from playsound import playsound
import pygame
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


def create_center_window() -> tk.Tk:
    """
    DONE
    Function to create a tkinter window in the center of the screen

    Returns a Tk window
    """
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

    return window


def validate_digit(new_value):
    """
    DONE
    Function to check if the new value is a digit or empty (to allow deletion).
    Used as a helper to validate time entries
    """
    return new_value.isdigit() or new_value == ""


def shift_to_next_entry(event):
    """
    DONE: Helper to shift focus to the next entry field after the user has entered values for hour/minute/second
    """
    # Get the widget that triggered the event
    widget = event.widget

    # Check if the content of the widget has 2 digits
    if len(widget.get()) == 2:
        # Move focus to the next widget
        widget.tk_focusNext().focus_set()


def create_entry(frame, textvariable, validate_cmd, width=2, font=("default bold", 25)) -> ttk.Entry:
    """
    DONE: Helper to create an entry widget with specified parameters.
    """
    entry = ttk.Entry(
        frame,
        textvariable=textvariable,
        width=width,
        font=font,
        justify="center",
        validate="key",
        validatecommand=(validate_cmd, "%P")
    )

    # OnFocus, delete text in the entry for user to type in new values
    entry.bind("<FocusIn>", func=lambda event: entry.delete(0, 'end'))

    # Bind the KeyRelease event to the shift_to_next_entry function
    entry.bind("<KeyRelease>", shift_to_next_entry)

    return entry


def create_entry_frame(parent):
    """
    TODO: change validate_cmd to controller
    Create and return a frame for the timer entries

    Param: 
    parent - the frame's master widget
    """
    frame = ttk.Frame(parent)
    frame.pack(pady=10)

    # Register the validation function: THIS SHOULD BE IN CONTROLLER
    validate_cmd = frame.register(validate_digit)

    entry_hr = tk.StringVar(value="00")
    entry_min = tk.StringVar(value="00")
    entry_sec = tk.StringVar(value="00")

    # Create entries using helper function
    entry_hr_wg = create_entry(frame, entry_hr, validate_cmd)
    entry_min_wg = create_entry(frame, entry_min, validate_cmd)
    entry_sec_wg = create_entry(frame, entry_sec, validate_cmd)
    
    # Pack entries
    entry_hr_wg.pack(side="left")
    ttk.Label(frame, text=":", font=("default bold", 25)).pack(side="left")
    entry_min_wg.pack(side="left")
    ttk.Label(frame, text=":", font=("default bold", 25)).pack(side="left")
    entry_sec_wg.pack(side="left")

    return entry_hr, entry_min, entry_sec, frame


def become_stop(original_button: ttk.Button):
    original_button["text"] = "Stop"
    original_button["command"] = stop_sound


def create_timer_control_frame(parent, entry_frame, timer_callback):
    """
    TODO: become_stop is inside start_timer in controller, reset_button needs
    a reset callback
    """
    frame = ttk.Frame(parent)
    frame.pack(pady=10)
    frame.columnconfigure(0, weight=1)
    frame.columnconfigure(1, weight=1)

    # 1st way to start timer: Keyboard-Enter event
    entry_frame.bind(
        '<KeyPress-Return>', 
        lambda event: timer_callback())
    
    # 2nd way to start timer: Start button
    start_button = ttk.Button(
        frame, 
        text="Start",
        command=lambda: [timer_callback(), become_stop(start_button)]) 
        # TODO: Change "start" button to "pause" after it's clicked
        # TODO: after alarm goes off, "pause" changes to "stop" to stop sound
    start_button.grid(column=0, row=0, sticky='e', padx=5)


    # TODO: reset button: reset timer to "00:00:00"; 
            # only available after "pause" or "stop"
    reset_button = ttk.Button(frame, text="Reset")
    reset_button.grid(column=1, row=0, sticky='w', padx=5)

    return frame


def play_sound():
    """DONE: Function to play the sound in a separate thread."""
    global playing
    pygame.mixer.music.load(SOUND_PATH)
    pygame.mixer.music.play(loops=0)  # Play once, no looping

    while pygame.mixer.music.get_busy() and playing:
        tm.sleep(0.1)  
        # Keep the thread alive while music plays to wait for stop signal
        # Else, the thread terminates right after music.play() and cannot call
        # music.stop() when user clicks the stop button


def start_sound():
    """ DONE: Starts the alarm sound in a new thread."""
    global playing
    playing = True  # Set the playing tag to True
    threading.Thread(target=play_sound, daemon=True).start() # Play sound in a Daemon thread that doesn't prevent the main program from exiting


def stop_sound():
    """DONE Stops the alarm sound"""
    global playing
    playing = False
    pygame.mixer.music.stop()


def start_timer():
    """TODO: account for entry_hr.get()"""
    hour, min, sec = map(
        int, [entry_hr.get(), entry_min.get(), entry_sec.get()])
    timer(hour, min, sec)


def timer(hour: int, min: int, sec: int) -> None:
    """
    TODO: the entry_hr.set in Controller
    
    Sets a countdown timer and plays sound when time is up

    Params - hour, min, sec (as integers)
    """
    total_seconds = hour*3600 + min*60 + sec

    def update_timer():
        nonlocal total_seconds
        if total_seconds > 0:
            hours, remainder = divmod(total_seconds, 3600)
            minutes, seconds = divmod(remainder, 60)

            entry_hr.set(f"{hours:02d}")
            entry_min.set(f"{minutes:02d}")
            entry_sec.set(f"{seconds:02d}")

            total_seconds -= 1
            window.after(1000, update_timer)  # Call this function again after 1 second
        else:
            entry_hr.set("00")
            entry_min.set("00")
            entry_sec.set("00")

            print("Timer's up!")
            window.after(100, start_sound) # Play sound when time is up (after the UI update)
            
    update_timer()


# DONE: window
window = create_center_window()

# DONE: create 2 tabs for alarm clock and timer
notebook = ttk.Notebook(window)
alarm_tab = ttk.Frame(notebook, width=175)
timer_tab = ttk.Frame(notebook, width=175) 
notebook.add(alarm_tab, text="Alarms", underline=0)
notebook.add(timer_tab, text="Timer", underline=0)
notebook.pack(side='top', expand=True, fill='both')

## ALARM CLOCK TAB
# title
alarm_title_label = ttk.Label(
    master=alarm_tab, 
    text="Alarms", 
    font="Calibri 20 bold")
alarm_title_label.pack(pady= 10)


## TIMER TAB
### Function frame
# TODO: Use function frame as parent!!!!
function_frame = ttk.Frame(master=timer_tab)
function_frame.pack(expand=True, fill='both')

# menu button for choosing which sound to be used
sound_menu = tk.Menubutton(function_frame, text='Sound')
sound_menu.pack(pady=10)

# TODO: move all the code for Timer to a separate class; refactoring please
# Create the entry frame and store entries in StringVars
entry_hr, entry_min, entry_sec, entry_frame = create_entry_frame(function_frame)


# Initialize pygame mixer
pygame.mixer.init()

# Global flag for stopping the sound
playing = False

# Create the control frame
control_frame = create_timer_control_frame(function_frame, entry_frame, start_timer)

    
### Progress bar
# TODO: User progress frame as parent!!


# Run
window.mainloop()


