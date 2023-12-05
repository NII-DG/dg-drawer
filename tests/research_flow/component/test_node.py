from unittest import TestCase
from dg_drawer.research_flow.component.node import Node

class TestNode(TestCase):

    # test exec : python -m unittest tests.research_flow.component.test_node

    def test_constructor_min(self):
        id = '1'
        parent_ids = ['2','3','4']
        create_datetime = 1234
        node_name = 'node A'
        node = Node(id=id, parent_ids=parent_ids, create_datetime=create_datetime, node_name=node_name)

        self.assertEqual(id, node.id)
        self.assertEqual(parent_ids, node.parent_ids)
        self.assertEqual(create_datetime, node.create_datetime)
        self.assertEqual(node_name, node.node_name)
        self.assertEqual(0, node.cx)
        self.assertEqual(0, node.cy)
        self.assertEqual(0, node.cr)
        self.assertEqual("", node.fill)
        self.assertEqual("", node.href)

    def test_constructor(self):
        id = '1'
        parent_ids = ['2','3','4']
        create_datetime = 1234
        node_name = 'node A'
        cx = 45
        cy = 67
        cr = 89
        fill = "lightcoral"
        href = "https://sample"
        node = Node(id=id, parent_ids=parent_ids, create_datetime=create_datetime, node_name=node_name, cx=cx, cy=cy, cr=cr, fill=fill, href=href)

        self.assertEqual(id, node.id)
        self.assertEqual(parent_ids, node.parent_ids)
        self.assertEqual(create_datetime, node.create_datetime)
        self.assertEqual(node_name, node.node_name)
        self.assertEqual(cx, node.cx)
        self.assertEqual(cy, node.cy)
        self.assertEqual(cr, node.cr)
        self.assertEqual(fill, node.fill)
        self.assertEqual(href, node.href)

    def test_generate_svg_component_with_href(self):
        id = '1'
        parent_ids = ['2','3','4']
        create_datetime = 1234
        status = 'complete'
        node_name = 'node A'
        cx = 45
        cy = 67
        cr = 89
        fill = "lightcoral"
        href = "https://sample"
        node = Node(id=id, parent_ids=parent_ids, create_datetime=create_datetime, node_name=node_name, cx=cx, cy=cy, cr=cr, fill=fill, href=href)

        result = node.generate_svg_component()
        expected_value = f'<a href="{href}" target="_self"><circle cx="{cx}" cy="{cy}" r="{cr}" fill="{fill}" stroke="black" stroke-width="1"/></a>'

        self.assertEqual(expected_value,result)

    def test_generate_svg_component_without_href(self):
        id = '1'
        parent_ids = ['2','3','4']
        create_datetime = 1234
        status = 'complete'
        node_name = 'node A'
        cx = 45
        cy = 67
        cr = 89
        fill = "lightcoral"
        node = Node(id=id, parent_ids=parent_ids, create_datetime=create_datetime, node_name=node_name, cx=cx, cy=cy, cr=cr, fill=fill)

        result = node.generate_svg_component()
        expected_value = f'<circle cx="{cx}" cy="{cy}" r="{cr}" fill="{fill}" stroke="black" stroke-width="1"/>'

        self.assertEqual(expected_value,result)

    def test_get_lable_svg_component(self):
        id = '1'
        parent_ids = ['2','3','4']
        create_datetime = 1234
        node_name = 'node A'
        cx = 45
        cy = 67
        cr = 89
        fill = "lightcoral"
        node = Node(id=id, parent_ids=parent_ids, create_datetime=create_datetime, node_name=node_name, cx=cx, cy=cy, cr=cr, fill=fill)

        result = node.get_lable_svg_component()
        expected_value =f'<text x="{cx}" y="{(cy - (cr + 5))}" text-anchor="middle" font-size="12">{node_name}</text>'
        self.assertEqual(expected_value, result)
