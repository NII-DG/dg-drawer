from unittest import TestCase
from dg_drawer.research_flow.component.node_label import NoneLabel

class TestLabel(TestCase):
    # test exec : python -m unittest tests.research_flow.component.test_node_label

    def test_constructor_min(self):
        value = 'node A'
        x = 10
        y = 20
        label = NoneLabel(value=value, x=x, y=y)

        self.assertEqual(value, label._value)
        self.assertEqual(x, label._x)
        self.assertEqual(y, label._y)
        self.assertEqual("middle", label._text_anchor)
        self.assertEqual(12, label._font_size)

    def test_constructor(self):
        value = 'node A'
        x = 10
        y = 20
        text_anchor = 'a'
        font_size = 100
        label = NoneLabel(value=value, x=x, y=y, text_anchor=text_anchor, font_size=font_size)

        self.assertEqual(value, label._value)
        self.assertEqual(x, label._x)
        self.assertEqual(y, label._y)
        self.assertEqual(text_anchor, label._text_anchor)
        self.assertEqual(font_size, label._font_size)

    def test_generate_svg_component(self):
        value = 'node A'
        x = 10
        y = 20
        text_anchor = 'a'
        font_size = 100
        label = NoneLabel(value=value, x=x, y=y, text_anchor=text_anchor, font_size=font_size)
        result = label.generate_svg_component()
        expected_value = f'<text x="{x}" y="{y}" text-anchor="{text_anchor}" font-size="{font_size}">{value}</text>'

        self.assertEqual(expected_value,result)