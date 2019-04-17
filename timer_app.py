import sys
import time

from kivy.app import App
from kivy.clock import Clock
from kivy.properties import ObjectProperty
from kivy.uix.widget import Widget
from win10toast import ToastNotifier


class TimerWidget(Widget):
    time_label = ObjectProperty(None)
    start_pause_button = ObjectProperty(None)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.timer_event = None
        self.seconds_left = 0  # TODO create a callback to update label if modified
        self.total_time_elapsed = 0  # TODO DEBUG

    def reset_timer(self):
        if self.timer_event is not None:
            self.timer_event.cancel()
            self.timer_event = None

        self.seconds_left = 0
        self.time_label.text = TimerWidget._format_time_text()
        self.start_pause_button.text = 'Start'

    def start_pause(self):
        if self.seconds_left == 0:
            return

        if self.timer_event is None:
            Clock.schedule_once(self._tick, 0)
            self.timer_event = Clock.schedule_interval(self._tick, 0.1)
            self.start_pause_button.text = 'Pause'
        else:
            self.timer_event.cancel()
            self.timer_event = None
            self.start_pause_button.text = 'Resume'

    def add_time(self, seconds=0, minutes=0, hours=0):
        self.seconds_left += seconds + 60 * minutes + 3600 * hours
        self.seconds_left = max(self.seconds_left, 0)
        self.time_label.text = TimerWidget._format_time_text(self.seconds_left)

    def _tick(self, interval=None):
        self.seconds_left -= interval
        self.time_label.text = TimerWidget._format_time_text(self.seconds_left)
        if self.seconds_left < 0.05:
            self._notify_timer_done()


    def _notify_timer_done(self):
        self.reset_timer()
        if sys.platform == 'win32':
            ToastNotifier().show_toast("Timer Done",
                                       "Your timer has finished!",
                                       duration=5,
                                       threaded=True)

        print("Timer done")

    @staticmethod
    def _format_time_text(seconds=0, minutes=0, hours=0):
        seconds = int(seconds)
        minutes += seconds // 60
        seconds = seconds % 60
        hours += minutes // 60
        minutes = minutes % 60
        if hours == 0:
            return "[b]{}:{}[/b]".format(str(minutes).zfill(2), str(seconds).zfill(2))
        else:
            return "[b]{}:{}:{}[/b]".format(str(hours).zfill(2), str(minutes).zfill(2), str(seconds).zfill(2))


class TimerApp(App):
    def build(self):
        return TimerWidget()


if __name__ == '__main__':
    TimerApp().run()
