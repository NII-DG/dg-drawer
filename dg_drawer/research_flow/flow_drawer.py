import math
from typing import List
from copy import deepcopy
import uuid

from dg_drawer.research_flow.component.node import Node, DummyNode
from dg_drawer.research_flow.component.line import Line
from dg_drawer.research_flow.component.frame import Frame
from dg_drawer.research_flow.enums.color import ColorType
from dg_drawer.research_flow.research_flow_status import PhaseStatus, SubFlowStatus


class FlowDrawer():
    """FlowDrawer class

    This class manipulates the drawing of Research Flow Status images (SVG).
    """

    def __init__(self, research_flow_status:List[PhaseStatus], whole_max_width:int=900, header_height:int=100, top_margin:int=50, bottom_margin:int=50, between_node_vertical_length:int=100 ) -> None:
        """FlowDrawer constructor

        Args:
            research_flow_status (List[PhaseStatus]): [Research Flow Status Instance]

            whole_max_width (int, optional): [Maximum width of Research Flow History Image]. Defaults to 900.

            header_height (int, optional): [Header height in Research Flow History Image]. Defaults to 100.

            top_margin (int, optional): [Distance of the node from the highest horizontal edge in the body part of the Research Flow History Image.]. Defaults to 50.

            bottom_margin (int, optional): [Distance of the node from the lowest horizontal edge in the body part of the Research Flow History Image]. Defaults to 50.

            between_node_vertical_length (int, optional): [Distance between vertical nodes]. Defaults to 100.
        """

        self._research_flow_status = research_flow_status
        self._whole_max_width = whole_max_width
        self._header_height = header_height
        self._top_margin = top_margin
        self._bottom_margin = bottom_margin
        self._between_node_vertical_length = between_node_vertical_length

    def pack_svg_tag(self, frame:str, line:str, node:str, node_label:str,  height:int, width:int)->str:
        """Package three SVG data (frame, line, node, node label) into an SVG tag

        Args:
            frame (str): [frame SVG data]

            line (str): [line SVG data]

            node (str): [node SVG data]

            node_label (str): [node label SVG data]

            height (int): [SVG data height]

        Returns:
            str: [SVG data]
        """
        return f'<svg width="{width}" height="{height}">{frame}{line}{node}{node_label}</svg>'

    def get_nodes(self, sub_flow_list:List[SubFlowStatus])->List[Node]:
        """Create a node list from phase data.
        Args:
            phase_unit_data (dict): [single phase data]

        Returns:
            list[Node]: [node list]
        """

        nodes = []
        for sub_flow in sub_flow_list:

            node = Node(
                id=sub_flow._id,
                parent_ids=sub_flow._parent_ids,
                node_name=sub_flow._name,
                create_datetime=sub_flow._create_datetime,
                href=sub_flow._link,
            )
            nodes.append(node)
        return nodes

    def set_node_location(self, nodes:List[Node], color_index:int, node_x:int, node_r:int=10)->List[Node]:
        """Set the coordinates in the SGV to each node in the node list.

        Args:
            nodes (list[Node]): [node list]
            color_index (int): [color index of the node being drawn.]
            node_x (int): [X-coordinate at which the node is located]
            node_r (int, optional): [node radius]. Defaults to 10.

        Returns:
            list[Node]: [Updated node list.]
        """

        # Calculate the initial Y-coordinate.
        start_y = self._header_height + self._top_margin

        positioned_nodes = []
        for node in nodes:
            # Set Y-coordinate
            node.cy = start_y
            # Set X-coordinate
            node.cx = node_x
            # Set radius
            node.cr = node_r

            if type(node) is DummyNode:
                node.fill = 'none'
                node._stroke = 'none'
                node._stroke_width = 0
            else:
                # Set color
                node.fill = ColorType.get_phase_node_by_index(color_index)

            positioned_nodes.append(node)
                # Update of initial X-coordinates
            start_y += self._between_node_vertical_length

        return positioned_nodes

    def calculate_body_height(self, nodes_each_phase:List[List[Node]])->int:
        """Calculate the height of the body part of the research flow history image.

        This method calculates the height from the number of nodes in the phase with the highest number of nodes in each phase

        Args:
            nodes_each_phase (list[list[Node]]): [Group of node data divided by phase]

        Returns:
            int: [height of the body part of the research flow history image.]
        """

        # Compare the number of nodes held between each phase to obtain the maximum number of nodes
        max_node_num = 0
        for nodes in nodes_each_phase:
            node_num = len(nodes)
            if node_num > max_node_num:
                max_node_num = node_num
            else:
                continue
        # Calculate and return the height of the body part
        return (self._top_margin + ((max_node_num-1) * 100) + self._bottom_margin)



    def draw(self)->str:
        """Drawing research flow history as SVG data

        Returns:
            str: [research flow history as SVG data]
        """
        research_flow_status = self._research_flow_status

        # Calculation of the number of phases
        phase_num = len(research_flow_status)

        # Calculation of phase width (rounding down to the nearest whole number)
        phase_width = math.floor(self._whole_max_width / phase_num)

        # Calculation of horizontal node spacing length
        between_node_horizontal_length = math.floor(self._whole_max_width / phase_num)



        # Organize research flow history data
        ## Obtain a list of node information per phase
        nodes_each_phase = []
        for phase_status in research_flow_status:
            nodes_each_phase.append(self.get_nodes(phase_status._sub_flow_data))

        # fill dumpy node
        filled_nodes_each_phase = self.fill_dummy_nodes_each_phase(nodes_each_phase)

        ## Sort the list of node information by phase
        sorted_nodes_each_phase = self.sort_nodes_each_phase(filled_nodes_each_phase)

        ## TODO : Rearrange the list of node information per phase

        # Add drawing position information to the node information for each phase.
        positioned_nodes_each_phase = []
        ## Calculate initial X-coordinates.
        start_x = math.floor(self._whole_max_width / phase_num / 2)

        for index, nodes in enumerate(sorted_nodes_each_phase):
            positioned_nodes_each_phase.append(self.set_node_location(nodes=nodes, node_x=start_x, color_index=index))
            ## Update initial X-coordinates
            start_x += between_node_horizontal_length

        # Calculate the height of the body part.
        body_height =  self.calculate_body_height(positioned_nodes_each_phase)

        # Building SVG data.

        ## Obtain SVG data for the frame (header + body)
        frame = Frame(phase_list=research_flow_status, phase_width=phase_width, header_height=self._header_height, body_height=body_height)
        frame_svg = frame.generate_frame()

        ## Obtain SVG data for inter-node lines
        line_svg = Line.generate_svg_lines(positioned_nodes_each_phase)

        ## Obtain the SVG data of a node.
        node_svg = ''
        node_label = ''
        for nodes in positioned_nodes_each_phase:
            for node in nodes:
                node_svg = node_svg + node.generate_svg_component()
                node_label = node_label + node.get_lable_svg_component()

        # Calculate the height of the entire SVG data.
        svg_height = body_height + self._header_height

        # Mature and return as SVG data
        return self.pack_svg_tag(frame=frame_svg, line=line_svg, node=node_svg, node_label=node_label, height=svg_height, width=(phase_width*phase_num))

    def fill_dummy_nodes_each_phase(self, nodes_each_phase:List[List[Node]])->List[List[Node]]:
        # ノード間が隣接するフェーズではなく2つ以上空いている場合は、ダミーノードを埋める。
        phase_num = len(nodes_each_phase)

        copy_nodes_each_phase = deepcopy(nodes_each_phase)

        for index in range(phase_num-1, 0, -1): # 後ろのフェーズから処理する
            nodes = nodes_each_phase[index]
            nodes_in_pre_phase = nodes_each_phase[index-1]
            for node in nodes:
                no_exist_ids = self.exist_nodes_in_phase_by_ids(nodes_in_pre_phase, node.parent_ids)
                if len(no_exist_ids)<=0:
                    continue # 標的Nodeの親IDの全てが前のフェーズに含まれている。
                else:
                    # 標的Nodeの親IDの内、少なくとも１以上が２つ前のフェーズに含まれる
                    # ２つ前のフェーズにある親ノードを特定する。
                    parant_ids_stock_last_edit_node = []
                    for no_exist_id in no_exist_ids:
                        parent_pahse_index, parent_node = self.get_pahse_index_and_node_with_node_id(nodes_each_phase, index-2, no_exist_id)

                        if index == -1 or parent_node is None:
                            raise Exception(f'Not Found Parent Nodes [start_last_index] : {index-2}, [no_exist_id] : {no_exist_id}')

                        diff_index_num = index - parent_pahse_index # フェーズの差
                        addition_datetime = math.floor((node.create_datetime - parent_node.create_datetime) / diff_index_num) # 加算ようUnixTime

                        tmp_node = None
                        for edit_index in range(parent_pahse_index+1, index+1, 1):
                            if tmp_node is None:
                                add_id = f'dummy:{uuid.uuid4()}'
                                add_node = DummyNode(
                                                id=add_id,
                                                parent_ids=[parent_node.id],
                                                create_datetime=parent_node.create_datetime + addition_datetime,
                                                node_name=''
                                            )
                                tmp_node = add_node
                                if (edit_index+1) == index:
                                    parant_ids_stock_last_edit_node.append(add_id)
                            elif tmp_node is not None and edit_index < index:
                                add_id = f'dummy:{uuid.uuid4()}'
                                add_node = DummyNode(
                                                id=add_id,
                                                parent_ids=[tmp_node.id],
                                                create_datetime=tmp_node.create_datetime + addition_datetime,
                                                node_name=''
                                            )
                                tmp_node = add_node
                                if (edit_index+1) == index:
                                    parant_ids_stock_last_edit_node.append(add_id)
                            else:
                                add_node_parent_ids = []
                                add_node_parent_ids.extend(parant_ids_stock_last_edit_node)

                                # for parent_id in node.parent_ids:
                                #     add_node_parent_ids.append(parent_id)
                                # for remove_id in no_exist_ids:
                                #     add_node_parent_ids.remove(remove_id)

                                add_node_parent_ids.extend(list(set(node.parent_ids) ^ set(no_exist_ids)))

                                add_node = Node(
                                                id=node.id,
                                                parent_ids=add_node_parent_ids,
                                                create_datetime=node.create_datetime,
                                                node_name=node.node_name,
                                                href=node.href
                                            )

                            for copy_node in copy_nodes_each_phase[edit_index]:
                                if copy_node.id == add_node.id:
                                    copy_nodes_each_phase[edit_index].remove(copy_node)
                            copy_nodes_each_phase[edit_index].append(add_node)
        return copy_nodes_each_phase

    def get_pahse_index_and_node_with_node_id(self, nodes_each_phase:List[List[Node]], start_last_index:int, id):
        for index in range(start_last_index, -1, -1):
            nodes = nodes_each_phase[index]
            for node in nodes:
                if node.id == id:
                    return index, node
        return -1, None


    def exist_nodes_in_phase_by_ids(self, nodes: List[Node], ids:List[str])->List[str]:
        ids_num = len(ids)
        exist_count = 0
        exist_ids = []
        for id in ids:
            for node in nodes:
                if node.id == id:
                    exist_count += 1
                    exist_ids.append(id)

        if ids_num == exist_count:
            return []
        else:
            diff_ids = set(ids) ^ set(exist_ids)
            return list(diff_ids)

    def sort_nodes_each_phase(self, nodes_each_phase:List[List[Node]])->List[List[Node]]:
        """Sort_nodes_each_phase all nodes in the research flow history

        Args:
            nodes_each_phase (list[list[Node]]): [Data before sorting]

        Returns:
            list[list[Node]]: [Data after sorting]
        """
        sorted_nodes_each_phaselist = []

        for index, nodes in enumerate(nodes_each_phase):
            if index == 0 or (len(nodes_each_phase[0])==1 and index==1):

                # The most recent phase is sorted in ascending order of node ID.
                sorted_nodes = self.sort_nodes_by_createdatetime(nodes)
                sorted_nodes_each_phaselist.append(sorted_nodes)
            else:
                sorted_nodes = []
                # Reorder the node data by looking at the parent ID list according to the order of the previous phase.
                ## Obtain the node data list (sorted) from the previous phase.
                pre_phase_nodes = sorted_nodes_each_phaselist[index-1]
                sorted_nodes = self.sort_nodes_by_pre_phase_nodes(pre_phase_nodes, nodes)
                sorted_nodes_each_phaselist.append(sorted_nodes)
        return sorted_nodes_each_phaselist


    def sort_nodes_by_createdatetime(self, nodes:List[Node])->List[Node]:
        return sorted(nodes, key=lambda x: x.create_datetime)


    def sort_nodes_by_pre_phase_nodes(self, pre_phase_nodes:List[Node], target_nodes:List[Node])->List[Node]:
        """Reorder the node data by looking at the parent ID list according to the order of the previous phase.
        Args:
            pre_phase_nodes (list[Node]): [Comparison node list]
            target_nodes (list[Node]): [Sorted target node list]

        Returns:
            list[Node]: [Data after sorting]
        """
        sorted_nodes = []

        grouped_node = [] # グループNodeリスト
        for pre_phase_node in pre_phase_nodes:
            pre_phase_node_id = pre_phase_node.id # 前フェーズのNodeID
            grouping_node = []
            for target_node in target_nodes:
                if pre_phase_node_id in target_node.parent_ids and not self.is_contain_id_in_grouped_node(grouped_node, target_node.id):
                    # 前フェーズのIDが次のフェーズ親IDリストに含まれ、かつグループNodeリストに既にターゲットNodeが含まれいない場合追加
                    grouping_node.append(target_node)
            grouped_node.append(grouping_node)

        for nodes in grouped_node:
            sorted_nodes.extend(self.sort_nodes_by_createdatetime(nodes))

        return sorted_nodes

    def is_contain_id_in_grouped_node(self, grouped_node:List[List[Node]], target_id)->bool:
        for nodes in grouped_node:
            for node in nodes:
                if node.id == target_id:
                    return True
        return False


    # TODO : リサーチフロ－来歴図における各ノードの配置を綺麗するためのメソッドを開発する（2023/8/25 時点で優先度：低）
    # def rearrange_nodes_each_phase(self, nodes_each_phase:list[list[Node]])->list[list[Node]]:

    #     pre_rearranged_nodes_each_phase = list[list[Node]]()

    #     # インデックスリスト（降順）を生成する
    #     phase_index_list = list[int]()
    #     for index in  range((len(nodes_each_phase)-1), -1, -1):
    #         phase_index_list.append(index)

    #     pre_rearranged_nodes_each_phase.append(nodes_each_phase[len(nodes_each_phase)-1])

    #     for phase_index in phase_index_list[1:]:
    #         # [3,2,1,0]
    #         print(phase_index)
    #         new_nodes = list[Node]()
    #         nodes = nodes_each_phase[phase_index]
    #         for node in nodes:
    #             new_nodes.append(node)
    #             node_id = node.id
    #             parent_ids = sorted(node.parent_ids)
    #             if len(parent_ids)>0:
    #                 priority_parent_id = parent_ids[0]
    #                 dummy_parent_ids = [priority_parent_id]
    #             else:
    #                 dummy_parent_ids = []
    #             child_node_num = self.get_child_node_num_by_id(node_id, nodes_each_phase[phase_index+1])
    #             new_nodes.extend(self.generate_dummy_nodes(child_node_num-1, dummy_parent_ids))

    #         pre_rearranged_nodes_each_phase.append(new_nodes)

    #     rearranged_nodes_each_phase = list[list[Node]]()
    #     for phase_index in phase_index_list:
    #         rearranged_nodes_each_phase.append(pre_rearranged_nodes_each_phase[phase_index])
    #     return rearranged_nodes_each_phase

    # def get_child_node_num_by_id(self, target_node_id:int, nodes:List[Node])->int:
    #     child_node_num = 0

    #     for node in nodes:
    #         parent_ids = sorted(node.parent_ids)
    #         priority_parent_id = parent_ids[0]
    #         if priority_parent_id == target_node_id:
    #             child_node_num += 1

    #     return child_node_num

    # def generate_dummy_nodes(self, node_num:int, parent_ids:List[int])->List[Node]:
    #     dummy_nodes = []
    #     for i in range(node_num):
    #         dummy_nodes.append(Node(
    #             id=-1,
    #             parent_ids=parent_ids,
    #             start_time=0,
    #             node_name='',
    #             status='',
    #             stroke_width=0
    #         ))
    #     return dummy_nodes
