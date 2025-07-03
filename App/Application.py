import pynput as pnp
import time
import ctypes


class Application:
    start_record_key = pnp.keyboard.Key.alt_l
    stop_record_key = pnp.keyboard.Key.f2
    stop_key = pnp.keyboard.Key.shift_l
    start_control_key = pnp.keyboard.Key.ctrl_l
    save_data_key = pnp.keyboard.Key.f6
    load_data_key = pnp.keyboard.Key.f7

    prepare_seconds = 8 #启动控制前的准备时间

    scale_factor = ctypes.windll.shcore.GetScaleFactorForDevice(0) / 100.0

    button_str_prefix = "Button_"

    def __init__(self):
        print("Initializing...")
        self.is_started = False
        self.is_recording = False
        self.is_controlling = False
        self.record_positions = []
        self.mouse_listener = pnp.mouse.Listener(on_click=self.on_click,
                                                 on_move=self.on_move,
                                                 on_scroll=self.on_scroll)
        self.keyboard_listener = pnp.keyboard.Listener(on_press=self.on_press,
                                                       on_release=self.on_release)

        #self.mode = 'OneTime'
        self.last_time = time.time()
        print("Initialization complete.")

    def __del__(self):
        print("Deleting Application")
        if self.is_started:
            self.stop()


    def start(self):
        self.is_started = True
        self.mouse_listener.start()
        self.keyboard_listener.start()

    def stop(self):
        print("Stopping Application")
        print(self.record_positions)
        if self.is_recording:
            self.stop_record()
        if self.is_controlling:
            self.stop_control()
        if not self.is_started:
            print("Not started yet!")
            return

        self.is_started = False
        self.mouse_listener.stop()
        self.keyboard_listener.stop()

    def start_record(self):
        print("Start recording")
        self.last_time = time.time()
        self.is_recording = True

    def stop_record(self):
        print("Stop recording")
        self.is_recording = False

    def start_control(self):
        self.is_controlling = True
        print(f"程序即将开始控制，请在{Application.prepare_seconds}秒时间内准备好！")
        time.sleep(Application.prepare_seconds/2)
        print("将要执行的命令为: {}".format(self.record_positions))
        time.sleep(Application.prepare_seconds/2)
        print("Start control")
        mouse = pnp.mouse.Controller()
        for x, y, button, duration in self.record_positions:
            if not self.is_controlling:
                break
            print(f"x = {x}, y = {y}, button = {button}")
            mouse.position = (round(x / Application.scale_factor), round(y / Application.scale_factor))
            mouse.click(button)
            time.sleep(duration)


        self.stop_control()

    def stop_control(self):
        print("Stop control")
        self.is_controlling = False

    def on_scroll(self, x, y, dx, dy):
        #print('滚动中... {} 至 {}'.format('向下：' if dy < 0 else '向上：', (x, y)))
        pass

    def on_click(self, x, y, button, pressed):
        now_time = time.time()
        if pressed and self.is_recording and not self.is_controlling:
            self.record_positions.append((x,y,button, now_time - self.last_time))
        #print('鼠标按键：{}，在位置处 {}, {} '.format(button, (x, y), '按下了' if pressed else '释放了'))
        self.last_time = time.time()

    def on_move(self, x, y):
        #print('鼠标移动到了：{}'.format((x, y)))
        pass

    def on_press(self, key):
        #print(str(key).capitalize() + ' key has been pressed')
        self.key_press_event(key)

    def on_release(self, key):
        #print(str(key).capitalize() + ' key has been released')
        pass

    def key_press_event(self, key):
        if key == Application.start_record_key:
            self.start_record()
        elif key == Application.stop_record_key:
            self.stop_record()
        elif key == Application.start_control_key:
            self.start_control()
        elif key == Application.stop_key:
            self.stop()
            print("The shift key has been pressed, the program will stop.")
        elif key == Application.save_data_key:
            #self.save_data()
            pass
        elif key == Application.load_data_key:
            #self.load_data()
            pass

    @staticmethod
    def turn_button_to_str(button: pnp.mouse.Button) -> str:
        s = ''
        if button == pnp.mouse.Button.left:
            s = "left"
        elif button == pnp.mouse.Button.right:
            s = "right"
        elif button == pnp.mouse.Button.middle:
            s = "middle"
        return "{}{}".format(Application.button_str_prefix, s)

    @staticmethod
    def turn_str_to_button(string: str) -> pnp.mouse.Button:
        string = string[len(Application.button_str_prefix):]
        if string == "left":
            return pnp.mouse.Button.left
        elif string == "right":
            return pnp.mouse.Button.right
        elif string == "middle":
            return pnp.mouse.Button.middle
        raise Exception(f"{string} is not a valid button.")



