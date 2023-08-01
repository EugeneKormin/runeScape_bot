import win32api
import win32con
import time
import ast

from Screen import Screen


class Keyboard(Screen):
    def __init__(self):
        super().__init__()
        with open(r'C:\PycharmProjects\aion_bot\Input\keys.json') as f:
            self.__keys = ast.literal_eval(f.read())

    def __encode_key(self, key: str) -> str:
        return self.__keys[key.lower()]

    def key_up(self, key: str):
        key_num: str = self.__encode_key(key=key)
        win32api.keybd_event(key_num, 0, win32con.KEYEVENTF_KEYUP, 0)

    def key_down(self, key: str):
        key_num: str = self.__encode_key(key=key)
        win32api.keybd_event(key_num, 0, 0, 0)

    def key_press(self, key, pressed_time=0.1):
        self.key_down(key)
        time.sleep(pressed_time)
        self.key_up(key)
