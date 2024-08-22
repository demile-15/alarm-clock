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
            self.timer_tab, entry_frame, self.start_timer_logic, self.model.stop_sound
        )

    def validate_digit(self, new_value):
        """
        Check if the new value is a digit or empty (to allow deletion).
        Helper to validate time entries
        """
        return new_value.isdigit() or new_value == ""

    def start_timer_logic(self):
        hour, min, sec = map(
            int, [self.entry_hr.get(), self.entry_min.get(), self.entry_sec.get()]
        )
        self.model.start_timer(
            hour, min, sec, self.update_time, self.time_up
        )

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
        open_popup(reset_callback=self.model.stop_sound)

    def run(self):
        self.window.mainloop()


if __name__ == "__main__":
    controller = TimerController()
    controller.run()
