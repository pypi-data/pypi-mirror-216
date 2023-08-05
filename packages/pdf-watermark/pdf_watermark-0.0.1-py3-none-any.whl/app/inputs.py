from typing import Union
from reportlab.lib.colors import HexColor


class UserInputs:
    def __init__(
        self,
        file: str,
        text: str = "watermark",
        color: str = "#000000",
        opacity=0.1,
        angle: float = 45,
        font: str = "Helvetica",
        size: int = 12,
        horizontal_boxes: int = 3,
        vertical_boxes: int = 6,
        margin: bool = False,
        save_to: Union[None, str] = None,
    ) -> None:
        self.file = file
        self.text = text
        self.color = HexColor(color)
        self.opacity = opacity
        self.angle = angle
        self.font = font
        self.size = size
        self.horizontal_boxes = horizontal_boxes
        self.vertical_boxes = vertical_boxes
        self.margin = margin
        self.save_to = save_to
