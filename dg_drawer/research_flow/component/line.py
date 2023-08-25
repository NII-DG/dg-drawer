from dg_drawer.error.error import ArgError
from dg_drawer.research_flow.component.node import Node

class Line():

    def __init__(self, parent_node: Node, child_node:Node, stroke:str='gray', stroke_width:int=1) -> None:

        if parent_node.id not in child_node.parent_ids:
            raise ArgError(f'No relationship between parent [{parent_node.id}] and child [{child_node.id}] nodes')

        self._parent_node_x = parent_node.cx
        self._parent_node_y = parent_node.cy
        self._child_node_x = child_node.cx
        self._child_node_y = child_node.cy
        self._stroke = stroke
        self._stroke_width = stroke_width


    def generate_svg_component(self):
        return f'<line x1="{self._parent_node_x}" y1="{self._parent_node_y}" x2="{self._child_node_x}" y2="{self._child_node_y}" stroke="{self._stroke}" stroke-width="{self._stroke_width}" />'

    @classmethod
    def generate_svg_lines(cls, nodes_each_pahse:list[list[Node]])->str:
        line_svg = ''
        phase_num = len(nodes_each_pahse)
        nodes_each_pahse.reverse()
        for index, nodes in enumerate(nodes_each_pahse):
            if index < (phase_num -1) :
                for node in nodes:
                    for parent_id in node.parent_ids:
                        nodes_pre_phase = nodes_each_pahse[index+1]
                        for node_pre_phase in nodes_pre_phase:
                            if parent_id == node_pre_phase.id:
                                line = Line(parent_node=node_pre_phase, child_node=node)
                                line_svg = line_svg + line.generate_svg_component()
        return line_svg
