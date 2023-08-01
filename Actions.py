from Status import Status
from Detect.ActiveWindow import ActiveWindow
from Screen import Screen
from Input.Mouse import Mouse
from Utility import Utility


class Actions(Status, ActiveWindow, Screen):
    def __init__(self):
        super().__init__()
        self.__mining_in_progress = False
        self.__mouse = Mouse()
        self.__utility = Utility()

    def do(self):
        self.update()
        '''
        status = self.__utility.read_json(json_name="status")
        
        if status["current_action"] != "mining" and status["click_required"] is not True:
            x = status["position_for_mouse_click"]["x"]
            y = status["position_for_mouse_click"]["y"]
            self.__mouse.move_cursor_to(target_x=x, target_y=y)
            
        if status["click_is_required"] and status["current_action"] != "waiting":
            self.__mouse.lbm_click()
        '''
