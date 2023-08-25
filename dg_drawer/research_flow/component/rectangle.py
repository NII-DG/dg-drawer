
class Rectangle():
    """rectangle
    """

    def __init__(self, x:int, y:int, width:int, height:int, fill:str="none", text:str="", font_size:int=16, text_fill:str="black", stroke:str="black", stroke_width:int=2) -> None:
        """コンストラクタ

        Args:
            x (int): [左上座標]
            y (int): [左上座標]
            width (int): [幅]
            height (int): [高さ]
            fill (str): [塗り色]
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

    def generate_svg_component(self):
        if len(self._text) > 0:
            text_x = self._x + (self._width / 2)
            test_y = self._y + (self._height / 2)

            return f'<rect x="{self._x}" y="{self._y}" width="{self._width}" height="{self._height}" fill="{self._fill}" stroke="{self._stroke}" stroke-width="{self._stroke_width}" />\n<text x="{text_x}" y="{test_y}" text-anchor="middle" dominant-baseline="middle" font-size="{self._font_size}" fill="{self._text_fill}">{self._text}</text>'
        else:
            return f'<rect x="{self._x}" y="{self._y}" width="{self._width}" height="{self._height}" fill="{self._fill}" stroke="{self._stroke}" stroke-width="{self._stroke_width}" />'