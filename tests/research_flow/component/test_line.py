from unittest import TestCase
from dg_drawer.research_flow.component.line import Line
from dg_drawer.research_flow.component.node import Node
from dg_drawer.error.error import ArgError


class TestLabel(TestCase):
    # test exec : python -m unittest tests.research_flow.component.test_line

    def test_constructor(self):
        p_id = '100'
        p_parent_ids = []
        p_start_time = 1234
        p_node_name = 'node A'
        p_cx = 11
        p_cy = 12
        p_cr = 13
        p_node = Node(id=p_id, parent_ids=p_parent_ids, create_datetime=p_start_time, node_name=p_node_name, cx=p_cx, cy=p_cy, cr=p_cr)

        c_id = '200'
        c_parent_ids = ['100','101','102']
        c_start_time = 1234
        c_node_name = 'node A'
        c_cx = 21
        c_cy = 22
        c_cr = 23
        c_node = Node(id=c_id, parent_ids=c_parent_ids, create_datetime=c_start_time, node_name=c_node_name,cx=c_cx, cy=c_cy, cr=c_cr)

        stroke = 'red'
        stroke_width = 10

        line = Line(parent_node=p_node, child_node=c_node, stroke=stroke, stroke_width=stroke_width)

        self.assertEqual(p_cx, line._parent_node_x)
        self.assertEqual(p_cy, line._parent_node_y)
        self.assertEqual(c_cx, line._child_node_x)
        self.assertEqual(c_cy, line._child_node_y)
        self.assertEqual(stroke, line._stroke)
        self.assertEqual(stroke_width, line._stroke_width)

    def test_constructor_err(self):
        p_id = '100'
        p_parent_ids = []
        p_start_time = 1234
        p_node_name = 'node A'
        p_cx = 11
        p_cy = 12
        p_cr = 13
        p_node = Node(id=p_id, parent_ids=p_parent_ids, create_datetime=p_start_time, node_name=p_node_name, cx=p_cx, cy=p_cy, cr=p_cr)

        c_id = '200'
        c_parent_ids = ['101','102','103']
        c_start_time = 1234
        c_node_name = 'node A'
        c_cx = 21
        c_cy = 22
        c_cr = 23
        c_node = Node(id=c_id, parent_ids=c_parent_ids, create_datetime=c_start_time, node_name=c_node_name,cx=c_cx, cy=c_cy, cr=c_cr)

        stroke = 'red'
        stroke_width = 10

        expected_err_msg = f'No relationship between parent [{p_id}] and child [{c_id}] nodes'
        with self.assertRaises(ArgError, msg=expected_err_msg):
            line = Line(parent_node=p_node, child_node=c_node, stroke=stroke, stroke_width=stroke_width)



    def test_generate_svg_component(self):
        p_id = '101'
        p_parent_ids = []
        p_start_time = 1234
        p_node_name = 'node A'
        p_cx = 11
        p_cy = 12
        p_cr = 13
        p_node = Node(id=p_id, parent_ids=p_parent_ids, create_datetime=p_start_time, node_name=p_node_name, cx=p_cx, cy=p_cy, cr=p_cr)

        c_id = '200'
        c_parent_ids = ['101','102','103']
        c_start_time = 1234
        c_node_name = 'node A'
        c_cx = 21
        c_cy = 22
        c_cr = 23
        c_node = Node(id=c_id, parent_ids=c_parent_ids, create_datetime=c_start_time, node_name=c_node_name,cx=c_cx, cy=c_cy, cr=c_cr)

        stroke = 'red'
        stroke_width = 10

        line = Line(parent_node=p_node, child_node=c_node, stroke=stroke, stroke_width=stroke_width)

        result = line.generate_svg_component()
        expected_value = f'<line x1="{p_cx}" y1="{p_cy}" x2="{c_cx}" y2="{c_cy}" stroke="{stroke}" stroke-width="{stroke_width}" />'

        self.assertEqual(expected_value,result)
