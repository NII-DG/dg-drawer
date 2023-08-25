from dg_drawer.research_flow.component.label import Label

class Node():
    """Nodeクラス
    """

    def __init__(self, id:int, parent_ids:list[int], start_time:int, node_name:str, status:str,cx:int=0, cy:int=0, cr:int=0, fill:str="", href:str="", stroke:str="black", stroke_width:int=2) -> None:
        """コンストラクタ

        Args:
            id (int): [ノードID]
            start_time (int): [作成開始時間(Unix時間)]
            node_name (str): [ノード名]
            cx (int, optional): [X軸位置]. Defaults to 0.
            cy (int, optional): [Y軸位置]. Defaults to 0.
            cr (int, optional): [半径]. Defaults to 0.
            fill (str, optional): [ノード色]. Defaults to "".
            href (str, optional): [リンク]. Defaults to "".
        """
        self._id = id
        self._start_time = start_time
        self._parent_ids = sorted(parent_ids)
        self._node_name = node_name
        self._status = status
        self._cx = cx
        self._cy = cy
        self._cr = cr
        self._fill = fill
        self._href = href
        self._node_name = node_name
        self._stroke = stroke
        self._stroke_width = stroke_width


    def generate_svg_component(self):
        '''
        SVGノードコンポーネントの生成
        '''
        circle = f'<circle cx="{self._cx}" cy="{self._cy}" r="{self._cr}" fill="{self._fill}" stroke="{self._stroke}" stroke-width="{self._stroke_width}"/>'
        if self._href == "":
            return circle
        else:
            return f'<a href="{self._href}" target="_blank">{circle}</a>'

    def get_lable_svg_component(self):
        """NodeインスタンスからLableのSVGコンポーネントを生成

        Returns:
            [type]: [description]
        """
        label = Label(value=self._node_name, x=self._cx, y=(self._cy - (self._cr + 5)))
        return label.generate_svg_component()

    '''
    setter/getter
    '''
    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, id):
        self._id = id


    @property
    def cx(self):
        return self._cx

    @cx.setter
    def cx(self, cx):
        self._cx = cx

    @property
    def cy(self):
        return self._cy

    @cy.setter
    def cy(self, cy):
        self._cy = cy

    @property
    def cr(self):
        return self._cr

    @cr.setter
    def cr(self, cr):
        self._cr = cr

    @property
    def fill(self):
        return self._fill

    @fill.setter
    def fill(self, fill):
        self._fill = fill

    @property
    def href(self):
        return self._href

    @href.setter
    def href(self, href):
        self._href = href

    @property
    def parent_ids(self):
        return self._parent_ids

    @parent_ids.setter
    def parent_ids(self, parent_ids):
        self._parent_ids = parent_ids

    @property
    def start_time(self):
        return self._start_time

    @property
    def node_name(self):
        return self._node_name

    @property
    def status(self):
        return self._status