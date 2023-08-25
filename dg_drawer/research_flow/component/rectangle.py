
class Rectangle():
    """Rectangle class
    """

    def __init__(self, x:int, y:int, width:int, height:int, fill:str="none", text:str="", font_size:int=16, text_fill:str="black", stroke:str="black", stroke_width:int=2) -> None:
        """Rectangle constructor

        Args:
            x (int): [top left X coordinate]
            y (int): [Top left Y-coordinate]
            width (int): [width]
            height (int): [height]
            fill (str): [colour]
        """
        self._x = x
        self._y = y
        self._width = width
        self._height = height
        self._fill = fill
        self._stroke = stroke
        self._stroke_width = stroke_width
        self._text = text
        self._font_size = font_size
        self._text_fill = text_fill

    def generate_svg_component(self)->str:
        """Generation of SVG square components.

        Returns:
            str: [SVG square components]
        """
        if len(self._text) > 0:
            text_x = self._x + (self._width / 2)
            test_y = self._y + (self._height / 2)

            return f'<rect x="{self._x}" y="{self._y}" width="{self._width}" height="{self._height}" fill="{self._fill}" stroke="{self._stroke}" stroke-width="{self._stroke_width}" />\n<text x="{text_x}" y="{test_y}" text-anchor="middle" dominant-baseline="middle" font-size="{self._font_size}" fill="{self._text_fill}">{self._text}</text>'
        else:
            return f'<rect x="{self._x}" y="{self._y}" width="{self._width}" height="{self._height}" fill="{self._fill}" stroke="{self._stroke}" stroke-width="{self._stroke_width}" />'