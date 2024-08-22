from models.timer_model import TimerModel
from view.timer_view import *
import os

"""
This part ties everything together, connecting the models and views, and handling events and interactions.
"""
SOUND_PATH = os.path.join("sound", "uplifting_sound.mp3")


class TimerController:
    def __init__(self):
        self.window = create_center_window("Clock and Timer", 500, 250)
        self.model = TimerModel(self.window)

        self.alarm_tab, self.timer_tab = create_notebook_with_tabs(self.window)
        self.entry_hr, self.entry_min, self.entry_sec, entry_frame = create_entry_frame(
            self.timer_tab, self.validate_digit
        )
        self.start_button, self.reset_button = create_timer_control_frame(
            self.timer_tab, 
            entry_frame, 
            self.start_timer_logic, 
            self.reset_timer
        )

    def validate_digit(self, new_value):
        """
        Validates the entry:
        - Allows only digits or empty values (for deletion)
        - Limits the entry to two digits

        Param:
        new_value       - the value of the entry if the edit is allowed
        """
        return (new_value.isdigit() and len(new_value) <= 2) or new_value == ""

    def update_button(self, for_button: ttk.Button, text, updated_command):
        for_button["text"] = text
        for_button["command"] = updated_command

    def start_timer_logic(self):
        hour, min, sec = map(
            int, [self.entry_hr.get(), self.entry_min.get(), self.entry_sec.get()]
        )
        self.model.start_timer(
            hour, min, sec, self.update_time, self.time_up
        )
        self.update_button(self.start_button, "Pause", self.model.pause_timer)

    def update_time(self, hours: int, minutes: int, seconds: int):
        """
        Helper to update time on the timer
        """
        self.entry_hr.set(f"{hours:02d}")
        self.entry_min.set(f"{minutes:02d}")
        self.entry_sec.set(f"{seconds:02d}")

    def reset_timer(self):
        self.entry_hr.set("00")
        self.entry_min.set("00")
        self.entry_sec.set("00")

    def time_up(self):
        # Update display time
        self.reset_timer()

        # Play sound
        self.model.play_sound(SOUND_PATH)

        # Make a popup menu
        open_popup(stop_callback=self.model.stop_sound)

    def run(self):
        self.window.mainloop()


if __name__ == "__main__":
    controller = TimerController()
    controller.run()
