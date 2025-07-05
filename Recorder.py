import time
from PyQt5.QtCore import QThread, pyqtSignal
from pynput import mouse, keyboard


class MacroRecorder(QThread):
    recording_updated: pyqtSignal | pyqtSignal = pyqtSignal(str)
    recording_stopped: pyqtSignal | pyqtSignal = pyqtSignal(list)

    def __init__(self):
        super().__init__()
        self.actions = []
        self.is_recording = False
        self.mouse_listener = None
        self.keyboard_listener = None
        self.start_time = 0

    def run(self):
        self.is_recording = True
        self.actions = []
        self.start_time = time.time()

        self.mouse_listener = mouse.Listener(
            on_move=self.on_mouse_move,
            on_click=self.on_mouse_click,
            on_scroll=self.on_mouse_scroll
        )

        self.keyboard_listener = keyboard.Listener(
            on_press=self.on_key_press,
            on_release=self.on_key_release
        )

        self.mouse_listener.start()
        self.keyboard_listener.start()

        self.mouse_listener.join()
        self.keyboard_listener.join()

        self.recording_stopped.emit(self.actions)

    def stop_recording(self):
        self.is_recording = False
        if self.mouse_listener is not None:
            self.mouse_listener.stop()
        if self.keyboard_listener is not None:
            self.keyboard_listener.stop()

    def on_mouse_move(self, x, y):
        if not self.is_recording:
            return

        timestamp = time.time() - self.start_time
        action = {
            'type': 'move',
            'timestamp': timestamp,
            'x': x,
            'y': y
        }
        self.actions.append(action)
        self.recording_updated.emit(f"移动到: ({x}, {y})")

    def on_mouse_click(self, x, y, button, pressed):
        if not self.is_recording:
            return

        timestamp = time.time() - self.start_time
        action = {
            'type': 'click',
            'timestamp': timestamp,
            'x': x,
            'y': y,
            'button': str(button),
            'pressed': pressed
        }
        self.actions.append(action)
        event_type = "按下" if pressed else "释放"
        self.recording_updated.emit(f"{event_type} {button} 键: ({x}, {y})")

    def on_mouse_scroll(self, x, y, dx, dy):
        if not self.is_recording:
            return

        timestamp = time.time() - self.start_time
        action = {
            'type': 'scroll',
            'timestamp': timestamp,
            'x': x,
            'y': y,
            'dx': dx,
            'dy': dy
        }
        self.actions.append(action)
        self.recording_updated.emit(f"滚动: ({x}, {y}), 方向: ({dx}, {dy})")

    def on_key_press(self, key):
        if not self.is_recording:
            return

        if key == keyboard.Key.f8:
            self.stop_recording()
            return

        timestamp = time.time() - self.start_time
        try:
            key_char = key.char
        except AttributeError:
            key_char = str(key)

        action = {
            'type': 'key_press',
            'timestamp': timestamp,
            'key': key_char
        }
        self.actions.append(action)
        self.recording_updated.emit(f"按下键: {key_char}")

    def on_key_release(self, key):
        if not self.is_recording:
            return

        timestamp = time.time() - self.start_time
        try:
            key_char = key.char
        except AttributeError:
            key_char = str(key)

        action = {
            'type': 'key_release',
            'timestamp': timestamp,
            'key': key_char
        }
        self.actions.append(action)
        self.recording_updated.emit(f"释放键: {key_char}")
