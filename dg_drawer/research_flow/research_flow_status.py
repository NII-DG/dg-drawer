
from typing import List
import json

class SubFlowStatus():
    def __init__(self, id:str, name:str, data_dir, link:str, parent_ids:List[str], create_datetime:int) -> None:
        self._id = id
        self._name = name
        self._data_dir = data_dir
        self._link = link
        self._parent_ids = parent_ids
        self._create_datetime = create_datetime


class PhaseStatus():

    def __init__(self, seq_number:int, name:str, sub_flow_data: List[SubFlowStatus]) -> None:
        self._seq_number = seq_number
        self._name = name
        self._sub_flow_data = sub_flow_data

    def update_name(self, name:str):
        self._name = name

class ResearchFlowStatus():


    @classmethod
    def load_from_json(cls, json_path:str)->List[PhaseStatus]:
        """Load a research flow status file (JSON) to obtain an instance

        Args:
            json_path (str): [Research flow status file path]

        Returns:
            List[PhaseStatus]: [Research Flow Status Instance]
        """

        with open(json_path, 'r') as f:
            loaded_json = json.load(f)

        ## TODO : check property : key and type

        ## get phase status list from ['research_flow_pahse_data']
        phase_list = loaded_json['research_flow_pahse_data']

        research_flow_status = []
        for phase in phase_list:
            sub_flow_data = []
            for sub_flow in phase['sub_flow_data']:
                sfs = SubFlowStatus(
                        id=sub_flow['id'],
                        name=sub_flow['name'],
                        data_dir=sub_flow['data_dir'],
                        link=sub_flow['link'],
                        parent_ids=sub_flow['parent_ids'],
                        create_datetime=sub_flow['create_datetime']
                    )
                sub_flow_data.append(sfs)
            ps = PhaseStatus(phase['seq_number'], phase['name'], sub_flow_data)
            research_flow_status.append(ps)

        sorted_research_flow_status = sorted(research_flow_status, key=lambda x : x._seq_number)
        return sorted_research_flow_status
