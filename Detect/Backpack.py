from Screen import Screen


class Backpack(Screen):
    def __init__(self):
        super().__init__()

    @property
    def backpack_element_images(self):
        resized_backpack_img = self.backpack_img
        elements = []
        row_height = 34
        element_width = 45

        for row_index in range(3):
            row_img = resized_backpack_img[row_height*row_index:row_height*(row_index+1), :]
            for element_index in range(11):
                if row_index == 2 and element_index > 6:
                    pass
                else:
                    element_img = row_img[:, 4+element_width*element_index:element_width*(element_index+1)]
                    elements.append(element_img)
        return elements
