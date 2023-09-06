import math
from dg_drawer.research_flow.component.node import Node
from dg_drawer.research_flow.component.line import Line
from dg_drawer.research_flow.component.frame import Frame
from dg_drawer.research_flow.enums.color import ColorType
from typing import List

class FlowDrawer():
    """FlowDrawer class

    This class manipulates the drawing of research flow history images (SVG).
    """

    def __init__(self, raw_data:dict, whole_max_width:int=900, header_height:int=100, top_margin:int=50, bottom_margin:int=50, between_node_vertical_length:int=100 ) -> None:
        """FlowDrawer constructor

        Args:
            raw_data (dict): [Original data for research flow history]

            whole_max_width (int, optional): [Maximum width of Research Flow History Image]. Defaults to 900.

            header_height (int, optional): [Header height in Research Flow History Image]. Defaults to 100.

            top_margin (int, optional): [Distance of the node from the highest horizontal edge in the body part of the Research Flow History Image.]. Defaults to 50.

            bottom_margin (int, optional): [Distance of the node from the lowest horizontal edge in the body part of the Research Flow History Image]. Defaults to 50.

            between_node_vertical_length (int, optional): [Distance between vertical nodes]. Defaults to 100.
        """

        self._phase_data = raw_data['phase_data']
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

    def get_nodes(self, phase_unit_data:dict)->List[Node]:
        """Create a node list from phase data.
        Args:
            phase_unit_data (dict): [single phase data]

        Returns:
            list[Node]: [node list]
        """
        raw_nodes = phase_unit_data['nodes']
        nodes = list[Node]()
        for raw_node in raw_nodes:
            status = raw_node['status']
            if status == 'complete':
                stroke = 'black'
                stroke_width = 1
            else:
                stroke = 'red'
                stroke_width = 2

            node = Node(
                id=raw_node['node_id'],
                parent_ids=sorted(raw_node['parent_ids']),
                node_name=raw_node['node_name'],
                start_time=raw_node['start_time'],
                status=raw_node['status'],
                href=raw_node['link'],
                stroke=stroke,
                stroke_width=stroke_width,
            )
            nodes.append(node)
        return nodes


    def sort_phase_data_by_seq_number(self, data_list:List)->List:
        """Sort phase data in ascending sequence number order.

        Args:
            data_list (list): [phase data list]

        Returns:
            list: [sorted phase data list]
        """

        sorted_list = sorted(data_list, key=lambda x: x.get('seq_number', float('inf')))
        return sorted_list

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

        positioned_nodes = List[Node]()
        for node in nodes:
            # Set Y-coordinate
            node.cy = start_y
            # Set X-coordinate
            node.cx = node_x
            # Set radius
            node.cr = node_r
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
        phase_data = self.sort_phase_data_by_seq_number(self._phase_data)

        # Calculation of the number of phases
        phase_num = len(phase_data)

        # Calculation of phase width (rounding down to the nearest whole number)
        phase_width = math.floor(self._whole_max_width / phase_num)

        # Calculation of horizontal node spacing length
        between_node_horizontal_length = math.floor(self._whole_max_width / phase_num)



        # Organize research flow history data
        ## Obtain a list of node information per phase
        nodes_each_phase = list[list[Node]]()
        for phase_unit_data in phase_data:
            nodes_each_phase.append(self.get_nodes(phase_unit_data))

        ## Sort the list of node information by phase
        sorted_nodes_each_phase = self.sort_nodes_each_phase(nodes_each_phase)

        ## TODO : Rearrange the list of node information per phase

        # Add drawing position information to the node information for each phase.
        positioned_nodes_each_phase = list[list[Node]]()
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
        frame = Frame(phase_data=phase_data, phase_width=phase_width, header_height=self._header_height, body_height=body_height)
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

    def sort_nodes_each_phase(self, nodes_each_phase:List[List[Node]])->List[List[Node]]:
        """Sort_nodes_each_phase all nodes in the research flow history

        Args:
            nodes_each_phase (list[list[Node]]): [Data before sorting]

        Returns:
            list[list[Node]]: [Data after sorting]
        """
        # Rearrange the node data within each phase, taking into account the order of the node data within the previous phase.
        # Assuming that the phase order of nodes_each_phase is in ascending order

        sorted_nodes_each_phaselist = list[list[Node]]()

        for index, nodes in enumerate(nodes_each_phase):
            if index == 0:
                # The most recent phase is sorted in ascending order of node ID.
                sorted_nodes = self.sort_nodes_by_id(nodes)
                sorted_nodes_each_phaselist.append(sorted_nodes)
            else:
                sorted_nodes = list[Node]()
                # Reorder the node data by looking at the parent ID list according to the order of the previous phase.
                ## Obtain the node data list (sorted) from the previous phase.
                pre_phase_nodes = sorted_nodes_each_phaselist[index-1]
                sorted_nodes = self.sort_nodes_by_pre_phase_nodes(pre_phase_nodes, nodes)
                sorted_nodes_each_phaselist.append(sorted_nodes)
        return sorted_nodes_each_phaselist



    def sort_nodes_by_id(self, nodes:List[Node])->List[Node]:
        """Sort the node list in ascending order by node ID

        Args:
            nodes (list[Node]): [Data before sorting]

        Returns:
            list[Node]: [Data after sorting]
        """
        return sorted(nodes, key=lambda x: x.id)

    def sort_nodes_by_pre_phase_nodes(self, pre_phase_nodes:List[Node], target_nodes:List[Node])->List[Node]:
        """Reorder the node data by looking at the parent ID list according to the order of the previous phase.
        Args:
            pre_phase_nodes (list[Node]): [Comparison node list]
            target_nodes (list[Node]): [Sorted target node list]

        Returns:
            list[Node]: [Data after sorting]
        """
        sorted_nodes = list[Node]()
        # 前フェーズの並び従って、ノードデータの親IDリストを見て並び替える。
        for pre_phase_node in pre_phase_nodes:
            pre_phase_node_id = pre_phase_node.id
            for target_node in target_nodes:
                target_node_parent_ids = sorted(target_node.parent_ids)
                if pre_phase_node_id == target_node_parent_ids[0]:
                    sorted_nodes.append(target_node)
        return sorted_nodes

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

    def get_child_node_num_by_id(self, target_node_id:int, nodes:List[Node])->int:
        child_node_num = 0

        for node in nodes:
            parent_ids = sorted(node.parent_ids)
            priority_parent_id = parent_ids[0]
            if priority_parent_id == target_node_id:
                child_node_num += 1

        return child_node_num

    def generate_dummy_nodes(self, node_num:int, parent_ids:List[int])->List[Node]:
        dummy_nodes = list[Node]()
        for i in range(node_num):
            dummy_nodes.append(Node(
                id=-1,
                parent_ids=parent_ids,
                start_time=0,
                node_name='',
                status='',
                stroke_width=0
            ))
        return dummy_nodes
