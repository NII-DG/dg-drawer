from unittest import TestCase
from dg_drawer.research_flow.component.node import Node
from dg_drawer.research_flow.flow_drawer import FlowDrawer

class TestFlowDrawer(TestCase):
    # test exec : python -m unittest tests.research_flow.test_flow_drawer

    def test_sort_dicts_by_seq_number(self):
        data_list = [
            {'seq_number': 3},
            {'seq_number': 1},
            {'seq_number': 2}
        ]
        f = FlowDrawer(raw_data={'phase_data':[]})
        sorted_data_list = f.sort_phase_data_by_seq_number(data_list)

        self.assertEqual(data_list[1]['seq_number'], sorted_data_list[0]['seq_number'])
        self.assertEqual(data_list[2]['seq_number'], sorted_data_list[1]['seq_number'])
        self.assertEqual(data_list[0]['seq_number'], sorted_data_list[2]['seq_number'])

    def test_draw(self):
        sample_json = {
        'phase_data': [
            {
                'seq_number' : 1,
                'phase_name' : 'フェーズA',
                'nodes' : [
                    {
                        'node_id' : 1,
                        'node_name' : 'node_A_1',
                        'status' : 'complete',
                        'link' : '',
                        'parent_ids' : [],
                        'start_time' : 1672498800
                    }
                ]
            },
            {
                'seq_number' : 2,
                'phase_name' : 'フェーズB',
                'nodes' : [
                    {
                        'node_id' : 2,
                        'node_name' : 'node_B_2',
                        'status' : 'complete',
                        'link' : '',
                        'parent_ids' : [1],
                        'start_time' : 1675177200
                    },
                    {
                        'node_id' : 3,
                        'node_name' : 'node_B_3',
                        'status' : 'working',
                        'link' : 'https://www.google.com/',
                        'parent_ids' : [1],
                        'start_time' : 1675263600
                    },
                    {
                        'node_id' : 4,
                        'node_name' : 'node_B_4',
                        'status' : 'complete',
                        'link' : '',
                        'parent_ids' : [1],
                        'start_time' : 1675350000
                    },
                    {
                        'node_id' : 5,
                        'node_name' : 'node_B_5',
                        'status' : 'complete',
                        'link' : '',
                        'parent_ids' : [1],
                        'start_time' : 1675522800
                    },
                    {
                        'node_id' : 6,
                        'node_name' : 'node_B_6',
                        'status' : 'complete',
                        'link' : '',
                        'parent_ids' : [1],
                        'start_time' : 1675609200
                    },
                ]
            },
            {
                'seq_number' : 3,
                'phase_name' : 'フェーズC',
                'nodes' : [
                    {
                        'node_id' : 7,
                        'node_name' : 'node_C_7',
                        'status' : 'complete',
                        'link' : '',
                        'parent_ids' : [2],
                        'start_time' : 1677596400
                    },
                    {
                        'node_id' : 8,
                        'node_name' : 'node_C_8',
                        'status' : 'complete',
                        'link' : '',
                        'parent_ids' : [4, 5],
                        'start_time' : 1677682800
                    },
                    {
                        'node_id' : 9,
                        'node_name' : 'node_C_9',
                        'status' : 'working',
                        'link' : 'https://www.google.com/',
                        'parent_ids' : [6],
                        'start_time' : 1677769200
                    },
                    {
                        'node_id' : 11,
                        'node_name' : 'node_C_11',
                        'status' : 'complete',
                        'link' : '',
                        'parent_ids' : [2, 3],
                        'start_time' : 1677596400
                    },
                ]
            },
            {
                'seq_number' : 4,
                'phase_name' : 'フェーズD',
                'nodes' : [
                    {
                        'node_id' : 10,
                        'node_name' : 'node_D_10',
                        'status' : 'complete',
                        'link' : '',
                        'parent_ids' : [7],
                        'start_time' : 1677769200
                    }
                ]
            },
        ]
    }
        fd = FlowDrawer(raw_data=sample_json)
        svg = fd.draw()
