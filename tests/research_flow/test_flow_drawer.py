from unittest import TestCase
from dg_drawer.research_flow import FlowDrawer
from dg_drawer.research_flow import PhaseStatus, SubFlowStatus

class TestFlowDrawer(TestCase):
    # test exec : python -m unittest tests.research_flow.test_flow_drawer

    def test_draw(self):

        node_A_1 = SubFlowStatus(
                    id='1',
                    name='node_A_1',
                    link='',
                    parent_ids=[],
                    create_datetime=1672498800
                )

        phase_A = PhaseStatus(
            seq_number=1,
            name='phase_A',
            sub_flow_data=[node_A_1]
        )

        node_B_2 = SubFlowStatus(
                    id='2',
                    name='node_B_2',
                    link='',
                    parent_ids=['1'],
                    create_datetime= 1675177200
        )

        node_B_3 = SubFlowStatus(
                    id='3',
                    name='node_B_3',
                    link='https://www.google.com/',
                    parent_ids=['1'],
                    create_datetime= 1675263600
        )

        node_B_4 = SubFlowStatus(
                    id='4',
                    name='node_B_4',
                    link='',
                    parent_ids=['1'],
                    create_datetime= 1675350000
        )

        node_B_5 = SubFlowStatus(
                    id='5',
                    name='node_B_5',
                    link='',
                    parent_ids=['1'],
                    create_datetime= 1675522800
        )

        node_B_6 = SubFlowStatus(
                    id='6',
                    name='node_B_6',
                    link='',
                    parent_ids=['1'],
                    create_datetime= 1675609200
        )

        phase_B = PhaseStatus(
            seq_number=2,
            name='phase_B',
            sub_flow_data=[node_B_2, node_B_3, node_B_4, node_B_5, node_B_6]
        )

        node_C_7 = SubFlowStatus(
                    id='7',
                    name='node_C_7',
                    link='',
                    parent_ids=['2'],
                    create_datetime= 1677596400
        )

        node_C_8 = SubFlowStatus(
                    id='8',
                    name='node_C_8',
                    link='',
                    parent_ids=['4', '5'],
                    create_datetime= 1677682800
        )

        node_C_9 = SubFlowStatus(
                    id='9',
                    name='node_C_9',
                    link='https://www.google.com/',
                    parent_ids=['6'],
                    create_datetime= 1677769200
        )

        node_C_11 = SubFlowStatus(
                    id='11',
                    name='node_C_11',
                    link='',
                    parent_ids=['2', '3'],
                    create_datetime= 1677596400
        )

        phase_C = PhaseStatus(
            seq_number=3,
            name='phase_C',
            sub_flow_data=[node_C_7, node_C_8, node_C_9, node_C_11]
        )


        node_D_10 = SubFlowStatus(
                    id='10',
                    name='node_D_10',
                    link='',
                    parent_ids=['7'],
                    create_datetime= 1677769200
        )

        phase_D = PhaseStatus(
            seq_number=4,
            name='phase_D',
            sub_flow_data=[node_D_10]
        )

        research_flow_status = [phase_A, phase_B, phase_C, phase_D]
        fd = FlowDrawer(research_flow_status=research_flow_status)
        svg = fd.draw()
