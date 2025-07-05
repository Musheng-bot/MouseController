import time

from PyQt5.QtCore import QThread, pyqtSignal
from pynput import mouse, keyboard
from pynput.keyboard import Controller as KeyboardController
from pynput.mouse import Controller as MouseController


class MacroPlayer(QThread):
    progress_updated: pyqtSignal | pyqtSignal = pyqtSignal()
    playback_finished: pyqtSignal | pyqtSignal = pyqtSignal()

    def __init__(self, actions, speed=1.0, loops=1):
        super().__init__()
        self.actions = actions
        self.speed = speed
        self.loops = loops
        self.is_playing = False
        self.mouse = MouseController()
        self.keyboard = KeyboardController()

    def run(self):
        self.is_playing = True

        for loop in range(self.loops):
            if not self.is_playing:
                break

            self.progress_updated.emit(f"循环 {loop + 1}/{self.loops}")

            prev_time = 0
            for i, action in enumerate(self.actions):
                if not self.is_playing:
                    break

                if i > 0:
                    wait_time = (action['timestamp'] - prev_time) / self.speed
                    time.sleep(wait_time)

                prev_time = action['timestamp']

                if action['type'] == 'move':
                    self.mouse.position = (action['x'], action['y'])
                    self.progress_updated.emit(f"移动到: ({action['x']}, {action['y']})")

                elif action['type'] == 'click':
                    button = mouse.Button.left if "left" in action['button'] else \
                        mouse.Button.right if "right" in action['button'] else \
                            mouse.Button.middle

                    if action['pressed']:
                        self.mouse.press(button)
                        self.progress_updated.emit(f"按下 {button} 键")
                    else:
                        self.mouse.release(button)
                        self.progress_updated.emit(f"释放 {button} 键")

                elif action['type'] == 'scroll':
                    self.mouse.scroll(action['dx'], action['dy'])
                    self.progress_updated.emit(f"滚动: 方向 ({action['dx']}, {action['dy']})")

                elif action['type'] == 'key_press':
                    try:
                        self.keyboard.press(action['key'])
                    except:
                        key = getattr(keyboard.Key, action['key'].replace('Key.', ''))
                        self.keyboard.press(key)

                    self.progress_updated.emit(f"按下键: {action['key']}")

                elif action['type'] == 'key_release':
                    try:
                        self.keyboard.release(action['key'])
                    except:
                        key = getattr(keyboard.Key, action['key'].replace('Key.', ''))
                        self.keyboard.release(key)

                    self.progress_updated.emit(f"释放键: {action['key']}")

        self.playback_finished.emit()

    def stop_playback(self):
        self.is_playing = False
