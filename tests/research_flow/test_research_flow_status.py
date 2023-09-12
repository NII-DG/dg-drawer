from unittest import TestCase
import os

from dg_drawer.research_flow.research_flow_status import ResearchFlowStatus

class TestResearchFlowStatus(TestCase):
    # test exec : python -m unittest tests.research_flow.test_research_flow_status

    def test_load_from_json(self):

        test_data_path = './tests/test_data/test_1_research_flow_status.json'

        rfs = ResearchFlowStatus.load_from_json(os.path.normpath(test_data_path))

        ## pahse list num
        self.assertEqual(3, len(rfs))

        ## research_preparation
        rp = rfs[0]
        self.assertEqual(1, rp._seq_number)
        self.assertEqual("research_preparation", rp._name)
        rp_sf = rp._sub_flow_data
        self.assertEqual(1, len(rp_sf))
        self.assertEqual("rp_sf_1", rp_sf[0]._id)
        self.assertEqual("rp_sf_1 name", rp_sf[0]._name)
        self.assertEqual("rp_sf_1 link", rp_sf[0]._link)
        self.assertEqual(0, len(rp_sf[0]._parent_ids))
        self.assertEqual(1, rp_sf[0]._create_datetime)

        ## experiments
        ex = rfs[1]
        self.assertEqual(2, ex._seq_number)
        self.assertEqual("experiments", ex._name)
        ex_sf = ex._sub_flow_data
        self.assertEqual(3, len(ex_sf))

        self.assertEqual("ex_sf_1", ex_sf[0]._id)
        self.assertEqual("ex_sf_1 name", ex_sf[0]._name)
        self.assertEqual("ex_sf_1 link", ex_sf[0]._link)
        self.assertEqual(1, len(ex_sf[0]._parent_ids))
        self.assertEqual(10, ex_sf[0]._create_datetime)

        self.assertEqual("ex_sf_2", ex_sf[1]._id)
        self.assertEqual("ex_sf_2 name", ex_sf[1]._name)
        self.assertEqual("ex_sf_2 link", ex_sf[1]._link)
        self.assertEqual(1, len(ex_sf[1]._parent_ids))
        self.assertEqual(11, ex_sf[1]._create_datetime)

        self.assertEqual("ex_sf_3", ex_sf[2]._id)
        self.assertEqual("ex_sf_3 name", ex_sf[2]._name)
        self.assertEqual("ex_sf_3 link", ex_sf[2]._link)
        self.assertEqual(1, len(ex_sf[2]._parent_ids))
        self.assertEqual(12, ex_sf[2]._create_datetime)


        ## paper_writing
        pw = rfs[2]
        self.assertEqual(3, pw._seq_number)
        self.assertEqual("paper_writing", pw._name)
        pw_sf = pw._sub_flow_data
        self.assertEqual(2, len(pw_sf))

        self.assertEqual("pw_sf_1", pw_sf[0]._id)
        self.assertEqual("pw_sf_1 name", pw_sf[0]._name)
        self.assertEqual("pw_sf_1 link", pw_sf[0]._link)
        self.assertEqual(2, len(pw_sf[0]._parent_ids))
        self.assertEqual(100, pw_sf[0]._create_datetime)

        self.assertEqual("pw_sf_2", pw_sf[1]._id)
        self.assertEqual("pw_sf_2 name", pw_sf[1]._name)
        self.assertEqual("pw_sf_2 link", pw_sf[1]._link)
        self.assertEqual(1, len(pw_sf[1]._parent_ids))
        self.assertEqual(101, pw_sf[1]._create_datetime)
