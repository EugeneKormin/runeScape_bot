# outer libraries import
import os
import mss
from win32gui import GetWindowRect              # library for window position detection
from ctypes import windll                       # library that helps to find window by its name
import numpy as np
import cv2
from PIL import Image

# own libraries import
from Config.ConfigReader import window_name


class Screen(object):
    def __init__(self) -> None:
        self.__img: np.ndarray = np.asarray([])
        self.__rect: tuple[int, int, int, int] = (0, 0, 0, 0)

    @staticmethod
    def save_screen(array: np.ndarray, folder_name: str = "images", index: int = 0) -> None:
        array = array[:, :, ::-1]  # BGR -> RGB
        img: Image = Image.fromarray(array)
        os.makedirs(folder_name) if not os.path.exists(folder_name) else ...
        img.save(f"./{folder_name}/{index}.jpg")

    @staticmethod
    def __grab(x: int, y: int, w: int, h: int) -> np.ndarray:
        """
        Frame retrieval for further analysis
        :param x: int: window upper border coordinate
        :param y: int: window left border coordinate
        :param w: int: window width
        :param h: int: window height
        :return: np.ndarray: frame in array format
        """
        # getting of image in rgb format
        with mss.mss() as sct:
            monitor = {"top": y, "left": x, "width": w, "height": h}
            img_array: np.ndarray = np.asarray(sct.grab(monitor))                      # getting of frame in RGBA format
            rgb_image_array: np.ndarray = cv2.cvtColor(img_array, cv2.COLOR_RGBA2RGB)  # BGRA -> BGR
            rgb_image_array = cv2.resize(rgb_image_array, (1044, 808))

            return rgb_image_array

    @property
    def window_position(self) -> tuple:
        # getting of inner window number
        inner_window_index: int = windll.user32.FindWindowW(0, window_name)

        # getting of window coordinates
        self.__rect: tuple[int, int, int, int] = GetWindowRect(inner_window_index)

        # data parsing
        x: int = self.__rect[0] + 5
        y: int = self.__rect[1] + 30
        w: int = self.__rect[2] - self.__rect[0] + 15
        h: int = self.__rect[3] - self.__rect[1] - 5
        return x, y, w, h

    def update_frame(self) -> None:
        x, y, w, h = self.window_position
        self.__img: np.ndarray = self.__grab(x=x, y=y, w=w, h=h)

    @property
    def map_img(self):
        map_img = self.__img[50:320, 650:]
        resized_map_img = cv2.resize(map_img, (500, 250))
        return resized_map_img

    @property
    def backpack_img(self):
        backpack_img = self.__img[410:550, 655:1013]
        resized_backpack_img = cv2.resize(backpack_img, (500, 100))
        return resized_backpack_img

    @property
    def active_window_img(self):
        active_window_img = self.__img[60:770, 205:650]
        resized_active_window_img = cv2.resize(active_window_img, (500, 500))
        return resized_active_window_img

    @property
    def action_template_img(self):
        template_img = self.__img[:70, 490:533]
        resized_template_img = cv2.resize(template_img, (100, 100))
        return resized_template_img
