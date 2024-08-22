import tkinter as tk
from tkinter import ttk

"""
This part handles all the UI elements using Tkinter.
"""


def create_center_window(title: str, w: int, h: int) -> tk.Tk:
    """TODO: allow resizing
    Create a tkinter window in the center of the screen"""
    window = tk.Tk()
    window.title(title)
    # get screen width and height
    ws = window.winfo_screenwidth()  # width of screen
    hs = window.winfo_screenheight()  # height of screen
    # calculate x and y coordinates for the Tk window
    x = round((ws / 2) - (w / 2))
    y = round((hs / 2) - (h / 2))
    # set the screen dimensions and where it is placed
    window.geometry(f"{w}x{h}+{x}+{y}")
    window.resizable(False, False)
    
    return window


def create_notebook_with_tabs(parent: tk.Tk):
    """
    TODO: finalize
    """
    # create 2 tabs for alarm clock and timer
    notebook = ttk.Notebook(parent)
    alarm_tab = ttk.Frame(notebook, width=175)
    timer_tab = ttk.Frame(notebook, width=175) 
    notebook.add(alarm_tab, text="Alarms", underline=0)
    notebook.add(timer_tab, text="Timer", underline=0)
    notebook.pack(side='top', expand=True, fill='both')

    return alarm_tab, timer_tab


def create_entry_frame(parent, validate_func):
    """
    Create and return a frame for the timer entries

    Params:
    parent          - the frame's master widget
    validate_cmd    - function to validate time input
    """
    frame = ttk.Frame(parent)
    frame.pack(pady=10)

    entry_hr = tk.StringVar(value="00")
    entry_min = tk.StringVar(value="00")
    entry_sec = tk.StringVar(value="00")

    validate_cmd = frame.register(validate_func)
    entry_hr_wg = create_entry(frame, entry_hr, validate_cmd)
    entry_hr_wg.bind("<KeyRelease>", shift_to_next_entry)
    entry_min_wg = create_entry(frame, entry_min, validate_cmd)
    entry_min_wg.bind("<KeyRelease>", shift_to_next_entry)
    entry_sec_wg = create_entry(frame, entry_sec, validate_cmd)

    entry_hr_wg.pack(side="left")
    ttk.Label(frame, text=":", font=("default bold", 25)).pack(side="left")
    entry_min_wg.pack(side="left")
    ttk.Label(frame, text=":", font=("default bold", 25)).pack(side="left")
    entry_sec_wg.pack(side="left")

    return entry_hr, entry_min, entry_sec, frame


def create_entry(
    frame, textvariable, validate_cmd, width=2, font=("default bold", 25)
) -> ttk.Entry:
    """
    Create an entry widget with specified parameters.

    Params:
    frame           - frame to create the Entry in
    textvariable    - text to display in the widget
    validate_cmd    - validate command for entry input
    width           - width of the widget
    font            - font of the text_variable
    """
    entry = ttk.Entry(
        frame,
        textvariable=textvariable,
        width=width,
        font=font,
        justify="center",
        validate="key",
        validatecommand=(validate_cmd, "%P"),
    )
    # OnFocus, delete text in the entry for user to type in new values
    entry.bind("<FocusIn>", lambda event: entry.delete(0, "end"))

    return entry


def shift_to_next_entry(event):
    """
    TODO: Consider if should keep this, or remove the shifting and deleting on
    focus feature (because it seems quite stupid to keep deleting entries when
    user wants to go back and fix the entered time). 

    How about use the same
    approach as Google, where theres only one entry field as the ":"'s are
    entered automatically

    Shift focus to the next entry field after the user has entered
    values for hour/minute/second
    Helper for creating entry fields
    """
    # Get the widget that triggered the event
    widget = event.widget
    # Check if the content of the widget has 2 digits
    if len(widget.get()) == 2:
        # Move focus to the next widget
        widget.tk_focusNext().focus_set()


def create_timer_control_frame(
    parent, entry_frame: ttk.Frame, start_logic_callback, reset_logic_callback
):
    """
    TODO: Fix docstring
    Create and return the timer's control buttons.

    Params:
    - parent: the frame's master widget
    - for_enter_keypress: a widget to bind the KeyPress-Return event to calling the timer_callback
    - timer_callback: the function to be called when user
    clicks the "Start" button

    Return: start and reset buttons
    """
    frame = ttk.Frame(parent)
    frame.pack(pady=10)
    frame.columnconfigure(0, weight=1)
    frame.columnconfigure(1, weight=1)

    # Bind Keyboard-Enter event to starting timer
    for widget in entry_frame.winfo_children():
        if isinstance(widget, ttk.Entry):
            widget.bind("<KeyPress-Return>", lambda event: start_logic_callback())

    # Start button
    start_button = ttk.Button(frame, text="Start", command=start_logic_callback)
    start_button.grid(column=0, row=0, sticky="e", padx=5)
    set_focus_color(start_button)

    # Reset button to reset timer to "00:00:00"
    reset_button = ttk.Button(frame, text="Reset", command=reset_logic_callback)
    reset_button.grid(column=1, row=0, sticky="w", padx=5)
    set_focus_color(reset_button)

    return start_button, reset_button


def set_focus_color(for_button: ttk.Button):
    def on_focus(event):
        style = ttk.Style()
        style.configure("TButton", background="lightblue")
        event.widget["style"] = "TButton"

    def out_focus(event):
        style = ttk.Style()
        style.configure("TButton", background="SystemButtonFace")
        event.widget["style"] = "TButton" # default button color

    for_button.bind("<FocusIn>", on_focus)
    for_button.bind("<FocusOut>", out_focus)
    

# def update_button(for_button: ttk.Button, text, updated_command):
#     for_button["text"] = "Stop"
#     for_button["command"] = stop_sound


def open_popup(reset_callback):
    """
    Create a popup window notifying user when timer goes off
    """
    def create_popup_labels(parent):
        """
        Create labels to display in the popup window
        """
        # TODO: allow for custom notification (entry field for user)
        emoji = ttk.Label(parent, text="⏰", font="20")
        emoji.pack(pady=(10, 0))
        label = ttk.Label(parent, text="Time is up!", font="bold 18")
        label.pack()

    def create_ok_button(parent):
        """
        Create a button that stop the alarm music and close the popup
        """
        ok_button = ttk.Button(
            master=parent, 
            text="OK", 
            command=on_button_click)
        ok_button.pack(pady=(8, 5))
        return ok_button

    def on_button_click():
        nonlocal reset_callback, popup
        reset_callback()
        popup.destroy()


    popup = tk.Toplevel()
    popup.title("Timer")

    # set popup's width and height and place in the center of screen
    w: int = 200
    h: int = 100
    ws = popup.winfo_screenwidth()
    hs = popup.winfo_screenheight()
    x = round((ws / 2) - (w / 2))
    y = round((hs / 2) - (h / 2))
    popup.geometry(f"{w}x{h}+{x}+{y}")
    popup.resizable(False, False)

    # notification line
    create_popup_labels(popup)

    # OK button (stop music and reset timer)
    create_ok_button(popup)




