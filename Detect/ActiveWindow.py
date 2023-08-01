import os

from ultralytics import YOLO
import numpy as np
import pandas as pd
import cv2

from Screen import Screen
from Utility import Utility


class ActiveWindow(Screen, Utility):
    def __init__(self):
        super().__init__()
        self.__ore_detector_model = YOLO(r"C:\PycharmProjects\runeScape_bot\weights\ore_detector.pt")
        self.__classify_ore_deposits_model = YOLO(
            r"C:\PycharmProjects\runeScape_bot\weights\classify_ore_hover_template.pt"
        )

    def get_ore_positions(self, img: np.ndarray) -> pd.DataFrame:
        preds = self.__ore_detector_model(img)

        conf_list = preds[0].boxes.conf.tolist()
        xyxy_list = preds[0].boxes.xyxy.tolist()

        top_left_list = []
        bottom_right_list = []

        for x1, y1, x2, y2 in xyxy_list:
            top_left_list.append([int(x1), int(y1)])
            bottom_right_list.append([int(x2), int(y2)])

        df = pd.DataFrame({
            "conf": conf_list,
            "top_left": top_left_list,
            "bottom_right": bottom_right_list
        })

        return df

    def get_position_of_a_specific_ore_deposit(self,
            img: np.ndarray, ore_positions: pd.DataFrame, ore_name: str
        ) -> dict:
        for key, value in ore_positions.iterrows():
            x1, x2 = value['top_left'][0], value['bottom_right'][0]
            y1, y2 = value['top_left'][1], value['bottom_right'][1]
            single_deposit = img[y1:y2, x1:x2]
            single_deposit = cv2.resize(single_deposit, (250, 250))
            pred = self.__classify_ore_deposits_model(single_deposit, verbose=False)

            ore_names = pred[0].names
            ore_index = pred[0].probs.top1
            predicted_ore_name = ore_names[ore_index]

            if predicted_ore_name == ore_name:
                return {
                    "found": True,
                    "position": {"x1": x1, "x2": x2, "y1": y1, "y2": y2}
                }
        return {
            "found": False,
            "position": {}
        }
