import pygame
import threading
import time

"""
This part of the code contains the core functionality, such as the timer countdown and alarm sound control.
"""


class TimerModel:
    def __init__(self, root):
        # Root widget (to update time via .after)
        self.root = root

        # Initialize pygame mixer
        pygame.mixer.init()

        # Global flag for running the countdown
        self.counting = False

        # Global flag for playing the sound
        self.playing = False

    def start_timer(self, hour, min, sec, update_callback, finish_callback):
        self.counting = True
        self.total_seconds = hour * 3600 + min * 60 + sec
        self.update_callback = update_callback
        self.finish_callback = finish_callback
        self._countdown()

    def _countdown(self):
        if self.total_seconds > 0:
            if self.counting:
                hours, remainder = divmod(self.total_seconds, 3600)
                minutes, seconds = divmod(remainder, 60)
                self.update_callback(hours, minutes, seconds)

                self.total_seconds -= 1
                self.root.after(1000, self._countdown)
            return
        else:
            self.counting = False
            self.finish_callback()

    def pause_timer(self):
        self.counting = False

    def resume_timer(self):
        self.counting = True
        self._countdown()

    def play_sound(self, sound_path):
        """
        Starts the alarm sound in a new thread.
        
        Param:
        sound_path - path of the sound to play
        """
        self.playing = True  # Set the playing tag to True
        threading.Thread(
            target=self._play_sound_thread, args=(sound_path,), daemon=True
        ).start()  # A Daemon thread doesn't prevent the main program from exiting

    def _play_sound_thread(self, sound_path):
        """
        Function to play the sound in a separate thread.
        
        Param:
        sound_path - path of the sound to play
        """
        pygame.mixer.music.load(sound_path)
        pygame.mixer.music.play(loops=0)  # Play once, no looping

        while pygame.mixer.music.get_busy() and self.playing:
            time.sleep(0.1)
            # Keep the thread alive until music ends or flag changes to False,
            # aka when user clicks the Stop button.
            # Else, the thread terminates right after music.play() and
            # cannot stop the music on user's command

    def stop_sound(self):
        """Stops the alarm sound"""
        self.playing = False
        pygame.mixer.music.stop()
