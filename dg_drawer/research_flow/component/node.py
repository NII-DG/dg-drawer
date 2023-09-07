from typing import List
from dg_drawer.research_flow.component.node_label import NoneLabel

class Node():
    """Node class
    """

    def __init__(self, id:int, parent_ids:List[int], start_time:int, node_name:str, status:str,cx:int=0, cy:int=0, cr:int=0, fill:str="", href:str="", stroke:str="black", stroke_width:int=2) -> None:
        """Node constructor

        Args:
            id (int): [node ID]

            start_time (int): [Creation start time (Unix time)]

            node_name (str): [node name]

            cx (int, optional): [X-axis position]. Defaults to 0.

            cy (int, optional): [Y-axis position]. Defaults to 0.

            cr (int, optional): [radius]. Defaults to 0.

            fill (str, optional): [node colour]. Defaults to "".

            href (str, optional): [link]. Defaults to "".
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


    def generate_svg_component(self, target:str='_blank')->str:
        """Generation of SVG node components.

        Returns:
            str : [SVG node components]
        """
        circle = f'<circle cx="{self._cx}" cy="{self._cy}" r="{self._cr}" fill="{self._fill}" stroke="{self._stroke}" stroke-width="{self._stroke_width}"/>'
        if self._href == "":
            return circle
        else:
            return f'<a href="{self._href}" target="{target}">{circle}</a>'

    def get_lable_svg_component(self)->str:
        """Get Lable's SVG component from the Node instance.

        Returns:
            str: [Lable's SVG component]
        """
        label = NoneLabel(value=self._node_name, x=self._cx, y=(self._cy - (self._cr + 5)))
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