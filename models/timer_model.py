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

        # Global flag for starting the countdown
        self.countdown = False

        # Global flag for playing the sound
        self.playing = False

    def start_timer(self, hour, min, sec, update_callback, finish_callback):
        self.countdown = True
        total_seconds = hour * 3600 + min * 60 + sec
        self._countdown(total_seconds, update_callback, finish_callback)

    def _countdown(self, total_seconds, update_callback, finish_callback):
        def update_timer():
            nonlocal total_seconds
            if total_seconds > 0:
                hours, remainder = divmod(total_seconds, 3600)
                minutes, seconds = divmod(remainder, 60)

                update_callback(hours, minutes, seconds)
                
                total_seconds -= 1
                self.root.after(1000, update_timer)
            else:
                finish_callback()

        update_timer()

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
