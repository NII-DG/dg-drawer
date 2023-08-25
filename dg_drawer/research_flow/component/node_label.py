
class NoneLabel():
    """NodeLabel class
    """

    def __init__(self, value: str, x:int, y:int, text_anchor:str="middle", font_size:int=12) -> None:
        """NodeLabel constructor

        Args:
            value (str): [label value]
            x (int): [X-axis position]
            y (int): [Y-axis position]
            text_anchor (str, optional): [character arrangement]. Defaults to "middle".
            font_size (int, optional): [Font size (px)]. Defaults to 12.
        """
        self._value = value
        self._x = x
        self._y = y
        self._text_anchor = text_anchor
        self._font_size = font_size

    def generate_svg_component(self)->str:
        """Generation of SVG node label components.

        Returns:
            str: [SVG node label components.]
        """

        return f'<text x="{self._x}" y="{self._y}" text-anchor="{self._text_anchor}" font-size="{self._font_size}">{self._value}</text>'