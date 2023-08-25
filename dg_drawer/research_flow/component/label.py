
class Label():
    """Node Labelクラス
    """

    def __init__(self, value: str, x:int, y:int, text_anchor:str="middle", font_size:int=12) -> None:
        """コンストラクタ

        Args:
            value (str): [ラベル値]
            x (int): [X軸位置]
            y (int): [Y軸位置]
            text_anchor (str, optional): [文字配置]. Defaults to "middle".
            font_size (int, optional): [フォントサイズ(px)]. Defaults to 12.
        """
        self._value = value
        self._x = x
        self._y = y
        self._text_anchor = text_anchor
        self._font_size = font_size

    def generate_svg_component(self):
        '''
        SVGノードコンポーネントの生成
        '''

        return f'<text x="{self._x}" y="{self._y}" text-anchor="{self._text_anchor}" font-size="{self._font_size}">{self._value}</text>'