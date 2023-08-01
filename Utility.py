import numpy as np
import cv2
import json
from random import randint


class Utility(object):
    def __init__(self):
        ...

    @staticmethod
    def match_template(img: np.ndarray, folder_name: str, template_name: str):
        template = cv2.imread(fr'C:\PycharmProjects\runeScape_bot\templates\{folder_name}\{template_name}.png')
        img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        template_gray = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)
        res = cv2.matchTemplate(img_gray, template_gray, cv2.TM_CCOEFF_NORMED)
        _, max_val, _, max_pos = cv2.minMaxLoc(res)
        return max_val, max_pos

    def read_json(self, json_name: str) -> dict:
        try:
            with open(fr"C:\PycharmProjects\runeScape_bot\Monitoring\{json_name}.json") as json_data:
                data = json.load(json_data)
        except:
            data = self.read_json(json_name=json_name)
        return data

    @staticmethod
    def get_position_for_mouse_click(x1, x2, y1, y2):
        rand = randint(0, 25)
        return {"x": (x1+x2)//2, "y": (y1+y2)//2}
    
    @staticmethod
    def index_to_coordinates(index: int, x: float, y: float, static_player_position: dict) -> dict:
        spot = 0
        if index in [1, 2, 3]:
            spot = 1
        elif index in [4, 5, 6, 7, 8, 9, 10]:
            spot = 2

        if index == 1:
            player_coordinates = {
                "x": static_player_position["x"] - x,
                "y": y - static_player_position["y"]
            }
        elif index == 2:
            # 341 is abs x distance between standard point 1 and standard point 2
            # 7 is abs y distance between standard point 1 and standard point 2
            player_coordinates = {
                "x": static_player_position["x"] - (x - 341),
                "y": (y - 7) - static_player_position["y"]
            }
        elif index == 3:
            # 131 is abs x distance between standard point 1 and standard point 3
            # 189 is abs y distance between standard point 1 and standard point 3
            player_coordinates = {
                "x": static_player_position["x"] - (x - 131),
                "y": (y - 189) - static_player_position["y"]
            }
        elif index == 4:
            player_coordinates = {
                "x": static_player_position["x"] - x,
                "y": y - static_player_position["y"]
            }
        elif index == 5:
            player_coordinates = {
                "x": static_player_position["x"] - (x - 131),
                "y": (y - 65) - static_player_position["y"]
            }
        elif index == 6:
            player_coordinates = {
                "x": static_player_position["x"] - (x + 45),
                "y": (y - 131) - static_player_position["y"]
            }
        elif index == 7:
            player_coordinates = {
                "x": static_player_position["x"] - (x + 110),
                "y": (y - 241) - static_player_position["y"]
            }
        elif index == 8:
            player_coordinates = {
                "x": static_player_position["x"] - (x - 55),
                "y": (y - 313) - static_player_position["y"]
            }
        elif index == 9:
            player_coordinates = {
                "x": static_player_position["x"] - (x - 204),
                "y": (y - 412) - static_player_position["y"]
            }
        elif index == 10:
            player_coordinates = {
                "x": static_player_position["x"] - (x - 72),
                "y": (y + 149) - static_player_position["y"]
            }
        else:
            player_coordinates = {"x": "unknown", "y": "unknown"}

        player_location = {
            "area": spot,
            "player_coordinates": player_coordinates
        }
        
        return player_location

    @staticmethod
    def put_text(img, text, pos, img_name="img"):
        cv2.putText(img, text, pos, cv2.FONT_HERSHEY_SIMPLEX,
                    0.5, (255, 255, 0), 1, 2)
        cv2.imshow(img_name, img)

    @staticmethod
    def draw_circle(img, pos, img_name="img"):
        cv2.circle(img=img, radius=4, thickness=4, center=pos, color=(255, 255, 10), lineType=1)
        cv2.imshow(img_name, img)
