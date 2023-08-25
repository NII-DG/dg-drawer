from dg_drawer.research_flow.component.rectangle import Rectangle
from dg_drawer.research_flow.enums.color import ColorType

class Frame():
    """Frame クラス
    """

    def __init__(self,
                 phase_data: list[dict],
                 phase_width:int,
                 header_height:int,
                 body_height:int,
                 ) -> None:
        self._phase_data = phase_data
        self._phase_width = phase_width
        self._header_height = header_height
        self._body_height = body_height

    def generate_headers(self)->list[Rectangle]:
        headers = list[Rectangle]()
        start_x = 0
        for index, phase_unit_data in enumerate(self._phase_data):
            phase_name = phase_unit_data['phase_name']
            header = Rectangle(
                        x=start_x,
                        y=0,
                        width=self._phase_width,
                        height=self._header_height,
                        fill=ColorType.get_phase_color_by_index(index=index),
                        text=phase_name,
                        text_fill='#ffffff',
                        stroke="black",
                        stroke_width=2,
                        )
            headers.append(header)
            start_x += self._phase_width

        return headers

    def generate_bodies(self)->list[Rectangle]:
        bodies = list[Rectangle]()
        start_x = 0
        for phase_unit_data in self._phase_data:
            body = Rectangle(
                        x=start_x,
                        y=self._header_height,
                        width=self._phase_width,
                        height=self._body_height,
                        fill='#ffffff',
                        stroke="black",
                        stroke_width=2,
                        )
            bodies.append(body)
            start_x += self._phase_width
        return bodies

    def generate_frame(self)->str:
        frame_svg = ''
        headers = self.generate_headers()
        for header in headers:
            frame_svg = frame_svg + header.generate_svg_component()

        bodies = self.generate_bodies()
        for body in bodies:
            frame_svg = frame_svg + body.generate_svg_component()

        return frame_svg
