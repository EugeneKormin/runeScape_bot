import cv2
import pandas as pd
import math

from Screen import Screen
from Utility import Utility


class Map(Screen, Utility):
    def __init__(self):
        super().__init__()
        self.__static_player_position = {"x": 218, "y": 145}
        self.__coordinates = {
            "area_1": {
                "mine": {"x": 145, "y": -165},
                "furnace": {"x": 358, "y": -94},
                "forge_and_anvil": {"x": 315, "y": -78}
            },

            "area_2": {
                "mine": {"x": 61, "y": 34},
                "furnace": {"x": 240, "y": -519},
                "forge_and_anvil": {"x": 240, "y": -519}
            }
        }

    def get_player_location_data(self) -> dict:
        resized_map_img = self.map_img

        standard_point_index_list = []
        max_val_list = []
        max_pos_list = []

        for standard_point_index in range(1, 11):
            max_val, max_pos = self.match_template(
                img=resized_map_img, folder_name="standard_points", template_name=str(standard_point_index)
            )

            standard_point_index_list.append(standard_point_index)
            max_val_list.append(max_val)
            max_pos_list.append(max_pos)

        df = pd.DataFrame({
            "index": standard_point_index_list,
            "val": max_val_list,
            "pos": max_pos_list
        }).sort_values("val", ascending=False)

        row = df.iloc[0]
        index = row["index"]
        conf = round(row["val"], 3)
        x, y = row["pos"][0], row["pos"][1]

        if conf > 0.7:
            location = self.index_to_coordinates(
                index=index, static_player_position=self.__static_player_position, x=x, y=y
            )
        else:
            location = {
                "area": r"n\a",
                "player_coordinates": {"x": "unknown", "y": "unknown"}
            }

        return location

    def calculate_distances(self, area: int, player_position: dict):
        distances = {
            "to_mine": 0,
            "to_furnace": 0,
            "to_forge_and_anvil": 0,
        }

        if area == 1:
            mine = self.__coordinates["area_1"]["mine"]
            mine_x, mine_y = mine["x"], mine["y"]

            furnace = self.__coordinates["area_1"]["furnace"]
            furnace_x, furnace_y = furnace["x"], furnace["y"]

            forge_and_anvil = self.__coordinates["area_1"]["forge_and_anvil"]
            forge_and_anvil_x, forge_and_anvil_y = forge_and_anvil["x"], forge_and_anvil["y"]
        elif area == 2:
            mine = self.__coordinates["area_2"]["mine"]
            mine_x, mine_y = mine["x"], mine["y"]

            furnace = self.__coordinates["area_2"]["furnace"]
            furnace_x, furnace_y = furnace["x"], furnace["y"]

            forge_and_anvil = self.__coordinates["area_2"]["forge_and_anvil"]
            forge_and_anvil_x, forge_and_anvil_y = forge_and_anvil["x"], forge_and_anvil["y"]

        player_position_x, player_position_y = player_position["x"], player_position["y"]

        distances["to_mine"] = round(math.hypot(
            player_position_x - mine_x, player_position_y - mine_y, 2)
        )

        distances["to_furnace"] = round(math.hypot(
            player_position_x - furnace_x, player_position_y - furnace_y, 2)
        )

        distances["to_forge_and_anvil"] = round(math.hypot(
            player_position_x - forge_and_anvil_x, player_position_y - forge_and_anvil_y, 2)
        )

        return distances

    @staticmethod
    def player_location(distances: dict) -> str:
        player_location = "somewhere in between"
        if distances["to_mine"] < 50:
            player_location = "mine"
        elif distances["to_furnace"] < 25:
            player_location = "furnace"
        elif distances["to_forge_and_anvil"] < 10:
            player_location = "forge and anvil"
        return player_location
