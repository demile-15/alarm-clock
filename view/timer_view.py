import tkinter as tk
from tkinter import ttk

"""
This part handles all the UI elements using Tkinter.
"""
class TimerView:
    def __init__(self, app_width, app_height, title="Clock and Timer"):
        self.window = tk.Tk()
        self.window.title(title)
        self.set_size_and_placement(self.window, app_width, app_height)
        self.create_function_tabs()

    # def create_center_window(self, title: str, w: int, h: int) -> tk.Tk:
    #     """Create a tkinter window in the center of the screen"""
    #     window = tk.Tk()
    #     window.title(title)
    #     self.set_size_and_placement(window, w, h)

    #     return window

    def set_size_and_placement(self, for_widget, w, h):
        # get screen width and height
        ws = for_widget.winfo_screenwidth()  # width of screen
        hs = for_widget.winfo_screenheight()  # height of screen
        # calculate x and y coordinates for the Tk window
        x = round((ws / 2) - (w / 2))
        y = round((hs / 2) - (h / 2))
        # set the screen dimensions and where it is placed
        for_widget.geometry(f"{w}x{h}+{x}+{y}")
        for_widget.resizable(False, False)

    def create_function_tabs(self):
        """
        Create 2 tabs for alarm clock and timer in the app window
        """
        notebook = ttk.Notebook(self.window)
        self.alarm_tab = ttk.Frame(notebook, width=175)
        self.timer_tab = ttk.Frame(notebook, width=175)
        notebook.add(self.alarm_tab, text="Alarms", underline=0)
        notebook.add(self.timer_tab, text="Timer", underline=0)
        notebook.pack(side="top", expand=True, fill="both")

    def create_entry_frame(self, parent, validate_func):
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
        entry_hr_wg = self.create_entry(frame, entry_hr, validate_cmd)
        entry_min_wg = self.create_entry(frame, entry_min, validate_cmd)
        entry_sec_wg = self.create_entry(frame, entry_sec, validate_cmd)

        entry_hr_wg.pack(side="left")
        ttk.Label(frame, text=":", font=("default bold", 25)).pack(side="left")
        entry_min_wg.pack(side="left")
        ttk.Label(frame, text=":", font=("default bold", 25)).pack(side="left")
        entry_sec_wg.pack(side="left")

        return entry_hr, entry_min, entry_sec, frame

    def create_entry(
        self, frame, textvariable, validate_cmd, width=2, font=("default bold", 25)
    ) -> ttk.Entry:
        """
        TODO: make these uneditable while the timer is running
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
        )  # %P - the value of the entry if the edit is allowed

        return entry

    def create_timer_control_frame(
        self, parent, entry_frame: ttk.Frame, start_logic_callback, reset_logic_callback
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
        self.start_button = ttk.Button(
            frame, text="Start", command=start_logic_callback
        )
        self.start_button.grid(column=0, row=0, sticky="e", padx=5)

        # Reset button to reset timer to "00:00:00"
        reset_button = ttk.Button(frame, text="Reset", command=reset_logic_callback)
        reset_button.grid(column=1, row=0, sticky="w", padx=5)

    # def set_focus_color(for_button: ttk.Button):
    #     def on_focus(event):
    #         style = ttk.Style()
    #         style.configure("TButton", background="lightblue")
    #         event.widget["style"] = "TButton"

    #     def out_focus(event):
    #         style = ttk.Style()
    #         style.configure("TButton", background="SystemButtonFace")
    #         event.widget["style"] = "TButton" # default button color

    #     for_button.bind("<FocusIn>", on_focus)
    #     for_button.bind("<FocusOut>", out_focus)

    def create_popup(self, stop_callback, width=200, height=100):
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
            ok_button = ttk.Button(master=parent, text="OK", command=on_button_click)
            ok_button.pack(pady=(8, 5))
            return ok_button

        def on_button_click():
            nonlocal stop_callback, popup
            stop_callback()
            popup.destroy()

        popup = tk.Toplevel()
        popup.title("Timer")
        self.set_size_and_placement(popup, width, height)

        # notification line
        create_popup_labels(popup)

        # OK button (stop music and reset timer)
        create_ok_button(popup)