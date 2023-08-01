from Detect.Map import Map
from Detect.ActiveWindow import ActiveWindow
from Monitoring.ClientSide import ClientSide


class Status(Map, ClientSide, ActiveWindow):
    def __init__(self):
        super().__init__()
        self.__index = 153
        self.__status = {
            "player_position": {"x": 0, "y": 0},
            "player_location": "",
            "current_ore_type": "iron",
            "current_ore_position": {"x": 0, "y": 0},
            "current_ore_status": False,
            "hovered_ore": "",
            "position_for_mouse_click": {"x": 0, "y": 0},
            "current_action": "idle",
            "click_is_required": False,
            "area": 0
        }

    @property
    def status(self):
        return self.__status

    def update(self) -> None:
        self.update_frame()

        location_data = self.get_player_location_data()
        self.__status["area"] = location_data["area"]
        self.__status["player_position"] = location_data["player_coordinates"]

        if self.__status["player_position"]["x"] != "unknown":
            self.__status["distances"] = self.calculate_distances(
                area=self.__status["area"],
                player_position=self.__status["player_position"]
            )
            self.__status["player_location"] = self.player_location(
                distances=self.__status["distances"]
            )
        else:
            self.__status["distances"] = {
                "to_mine": "unknown",
                "to_furnace": "unknown",
                "to_forge_and_anvil": "unknown",
            }

        if self.__status["player_location"] == "mine":
            img = self.active_window_img
            ore_positions = self.get_ore_positions(img=img)
            position_deposit_data = self.get_position_of_a_specific_ore_deposit(
                img=img, ore_positions=ore_positions, ore_name=self.__status["current_ore_type"]
            )
            if position_deposit_data["found"]:
                self.__status["current_ore_status"] = True
                self.__status["current_ore_position"] = position_deposit_data["position"]
            else:
                self.__status["current_ore_status"] = False
                self.__status["current_ore_position"] = r"n\a"

            self.__status["hovered_ore"] = "plug"

        if self.__status["current_ore_status"]:
            x1, x2 = self.__status["current_ore_position"]["x1"], self.__status["current_ore_position"]["x2"]
            y1, y2 = self.__status["current_ore_position"]["y1"], self.__status["current_ore_position"]["y2"]
            self.__status["position_for_mouse_click"] = self.get_position_for_mouse_click(x1=x1, x2=x2, y1=y1, y2=y2)

        if self.__status["hovered_ore"] == self.__status["current_ore_type"] and \
                self.__status["current_action"] != "mining":
            self.__status["click_is_required"] = True
            self.__status["current_action"] = "waiting"
        else:
            self.__status["click_is_required"] = False
            self.__status["current_action"] = "idle"

        if self.__status["current_action"] == "mining":
            self.__status["click_is_required"] = False

        # if mining template is detected:
        #    self.__status["current_action"] = "mining"

        self.update_data_for_monitoring(file_name="status", value=self.__status)
