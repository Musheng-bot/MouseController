import pynput as pnp
import time
import ctypes


class Application:
    pause = 1.5
    scale_factor = ctypes.windll.shcore.GetScaleFactorForDevice(0) / 100.0
    #print(f"当前DPI缩放比例: {scale_factor * 100}%")
    def __init__(self):
        self.is_started = False
        self.is_recording = False
        self.is_controlling = False
        self.record_positions = []
        self.mouse_listener = pnp.mouse.Listener(on_click=self.on_click,
                                                 on_move=self.on_move,
                                                 on_scroll=self.on_scroll)
        self.keyboard_listener = pnp.keyboard.Listener(on_press=self.on_press,
                                                       on_release=self.on_release)

        self.mode = 'OneTime'

    def __del__(self):
        print("Deleting Application")
        if self.is_started:
            self.stop()

    def start(self):
        self.is_started = True
        self.mouse_listener.start()
        self.keyboard_listener.start()

    def stop(self):
        print(self.record_positions)
        if not self.is_started:
            print("Not started yet!")
            return
        self.is_started = False
        self.mouse_listener.stop()
        self.keyboard_listener.stop()

    def start_record(self):
        print("Start recording")
        self.is_recording = True

    def stop_record(self):
        print("Stop recording")
        self.is_recording = False

    def start_control(self):
        self.is_controlling = True
        print("程序即将开始控制，请在5秒时间内准备好！")
        time.sleep(5)
        print("Start control")
        mouse = pnp.mouse.Controller()
        for x, y, button in self.record_positions:
            print(f"x = {x}, y = {y}, button = {button}")
            mouse.position = (round(x / Application.scale_factor), round(y / Application.scale_factor))
            mouse.click(button)
            time.sleep(Application.pause)

        self.stop_control()

    def stop_control(self):
        print("Stop control")
        self.is_controlling = False

    def on_scroll(self, x, y, dx, dy):
        print('滚动中... {} 至 {}'.format('向下：' if dy < 0 else '向上：', (x, y)))

    def on_click(self, x, y, button, pressed):
        if pressed and self.is_recording and not self.is_controlling:
            self.record_positions.append((x,y,button))
        print('鼠标按键：{}，在位置处 {}, {} '.format(button, (x, y), '按下了' if pressed else '释放了'))

    def on_move(self, x, y):
        #print('鼠标移动到了：{}'.format((x, y)))
        pass

    def on_press(self, key):
        print(str(key).capitalize() + ' key has been pressed')
        self.key_press_event(key)

    def on_release(self, key):
        print(str(key).capitalize() + ' key has been released')

    def key_press_event(self, key):
        if key == pnp.keyboard.Key.alt_l:
            self.start_record()
        elif key == pnp.keyboard.Key.f2:
            self.stop_record()
        elif key == pnp.keyboard.Key.ctrl_l:
            self.start_control()
        elif key == pnp.keyboard.Key.shift_l:
            self.stop()


