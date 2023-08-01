from Detect.Backpack import Backpack
from Detect.ActiveWindow import ActiveWindow
from Detect.Map import Map


class Detect(ActiveWindow, Backpack, Map):
    def __init__(self):
        super().__init__()
