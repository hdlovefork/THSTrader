import threading

import pyttsx4


class Voice:
    def __init__(self):
        self.play_lock = threading.Lock()

    def _say(self, text):
        with self.play_lock:
            engine = pyttsx4.init()
            engine.say(text)
            engine.runAndWait()

    def say(self, text):
        threading.Thread(target=self._say, args=(text,)).start()
