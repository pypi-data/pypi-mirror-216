from threading import Thread, Event
import time
from pynput.mouse import Button, Controller


class Autoclicker:
    """
    Autoclicker object.

    ### Arguments

    delay: float
        Delay between each click
    
    mouseButton: pynupt.mouse.Button
        The mouse button that the autoclicker targets

    Attributes
    ----
    active: bool
        The current state of the autoclicker

    Methods
    ----
    start()
        Starts the autoclicker
    
    stop()
        Stops the autoclicker

    run( time: float )
        Runs the autoclicker for `time` seconds

    """
    def __init__(self, delay: float, mouseButton: Button) -> None:

        self.delay = delay
        self._mouse = Controller()
        self.mouseButton = mouseButton
        self._clickingThread = Thread(target=self._clicker, name="Clicker")
        self._stopEvent = Event()
        self.active = False

        
    def start(self):
        """Starts the autoclicker object
        """
        self._stopEvent.clear()
        self.active = True
        if not self._clickingThread.is_alive():
            self._clickingThread = Thread(target=self._clicker, name="Clicker")
            self._clickingThread.start()
    
    def stop(self):
        """Stops the autoclicker object
        """
        if self._stopEvent.is_set():
            return
        self.active = False
        self._stopEvent.set()
        if self._clickingThread.is_alive():
            self._clickingThread.join()


    def run(self, timeSec: float):
        """Starts the autoclicker for `timeSec` seconds

        Args:
            timeSec (float): The time the autoclicker is running
        
        Raises:
            ValueError: if `timeSec` <= 0
        """
        if timeSec <= 0:
            raise ValueError("Variable `timeSec` can't be 0 or below")

        self.start()
        time.sleep(timeSec)
        self.stop()

    def _clicker(self):
        # private! Not for public use
        
        while not self._stopEvent.is_set():
            self._mouse.click(self._mouseButton)
            time.sleep(self._delay)
