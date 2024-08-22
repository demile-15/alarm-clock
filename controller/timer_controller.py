from models.timer_model import TimerModel
from view.timer_view import TimerView
from view.timer_view import *
import os

"""
This part ties everything together, connecting the models and views, and handling events and interactions.
"""
SOUND_PATH = os.path.join("sound", "uplifting_sound.mp3")


class TimerController:
    def __init__(self):
        # TODO: reconsider the logic for TimerView class here
        self.view = TimerView(500, 250)
        self.model = TimerModel(self.view.window)

        self.entry_hr, self.entry_min, self.entry_sec, self.entry_frame = (
            self.view.create_entry_frame(self.view.timer_tab, self._validate_digit)
        )

        self.view.create_timer_control_frame(
            self.view.timer_tab,
            self.entry_frame,
            self.start_timer_logic,
            self.reset_timer_logic,
        )

    def _validate_digit(self, new_value):
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

    def _set_entry_editable(self, editable=True):
        """
        Disable/enable entry fields

        Param: disabled - a boolean that disable the entry fields if is True
        """
        state = "disabled" if not editable else "normal"
        for entry in self.entry_frame.winfo_children():
            entry["state"] = state

    def start_timer_logic(self):
        self._set_entry_editable(False)
        hour, min, sec = map(
            int, [self.entry_hr.get(), self.entry_min.get(), self.entry_sec.get()]
        )
        self.model.start_timer(hour, min, sec, self.update_time, self.time_up)
        self.update_button(self.view.start_button, "Pause", self.pause_timer_logic)

    def update_time(self, hours: int, minutes: int, seconds: int):
        """
        Helper to update time on the timer
        """
        self.entry_hr.set(f"{hours:02d}")
        self.entry_min.set(f"{minutes:02d}")
        self.entry_sec.set(f"{seconds:02d}")

    def reset_timer_logic(self):
        self.model.pause_timer()
        self.update_time(0, 0, 0)
        self._set_entry_editable(True)
        self.update_button(self.view.start_button, "Start", self.start_timer_logic)

    def pause_timer_logic(self):
        self.model.pause_timer()
        self.update_button(self.view.start_button, "Resume", self.resume_timer_logic)

    def resume_timer_logic(self):
        self.model.resume_timer()
        self.update_button(self.view.start_button, "Pause", self.pause_timer_logic)

    def time_up(self):
        # Play sound
        self.model.play_sound(SOUND_PATH)

        # Make a popup menu
        self.view.create_popup(stop_callback=self.model.stop_sound)

        # Reset the timer
        self.reset_timer_logic()

    def run(self):
        self.view.window.mainloop()


if __name__ == "__main__":
    controller = TimerController()
    controller.run()
