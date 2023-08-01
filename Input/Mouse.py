import time
import win32api
import win32con

from Screen import Screen


class Mouse(Screen):
    def __init__(self):
        super().__init__()

    def rbm_click(self):
        self.__rbm_down()
        self.__rbm_up()

    @staticmethod
    def __rbm_down():
        x, y = win32api.GetCursorPos()
        win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTDOWN, x, y, 0, 0)
        time.sleep(0.1)

    @staticmethod
    def __rbm_up():
        x, y = win32api.GetCursorPos()
        win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTUP, x, y, 0, 0)
        time.sleep(0.1)

    def lbm_click(self):
        self.__lbm_down()
        self.__lbm_up()

    @staticmethod
    def __lbm_down():
        x, y = win32api.GetCursorPos()
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, x, y, 0, 0)
        time.sleep(0.1)

    @staticmethod
    def __lbm_up():
        x, y = win32api.GetCursorPos()
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, x, y, 0, 0)
        time.sleep(0.1)

    def move_cursor_to(self, target_x, target_y, speed=2):
        window_position = self.window_position
        window_shift_x, window_shift_y, _, _ = window_position
        temp_x, temp_y = win32api.GetCursorPos()
        temp_x -= window_shift_x
        temp_y -= window_shift_y
        shift_x, shift_y = (target_x - temp_x) // 30, (target_y - temp_y) // 30

        while abs(shift_x) != 0 or abs(shift_y) != 0:
            shift_x, shift_y = (target_x - temp_x) // 30, (target_y - temp_y) // 30
            temp_x += shift_x
            temp_y += shift_y
            win32api.SetCursorPos((temp_x + window_shift_x, temp_y + window_shift_y))
            time.sleep(0.01 / speed)
