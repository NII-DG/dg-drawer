import math
import os
from dg_drawer.error.error import ArgError, JSONDataError
from dg_drawer.research_flow.component.node import Node
from dg_drawer.research_flow.component.line import Line
from dg_drawer.research_flow.component.frame import Frame
from dg_drawer.research_flow.enums.color import ColorType
import json

WHOLE_MAX_WIDTH = 900
HEADER_HEIGHT = 100
TOP_MARGIN = 50
BOTTOM_MARGIN = 50
BETWEEN_NODE_VERTICAL_LENGTH = 100



class FlowDrawer():

    def __init__(self, raw_json=None, json_path=None) -> None:
        '''
        コンストラクタ

        Param
        ------------------------------------------------------
        raw_json (dict) : フロー来歴データ（生データ）
        json_path (str): フロー来歴データJSONファイルのパス

        Note
        ------------------------------------------------------
        1. 引数 : raw_jsonとjson_pathはどちらか一方のみセットすることができる

        '''

        if raw_json is None and json_path is None:
            raise ArgError('Both arguments (raw_json and json_path) are not set')
        elif raw_json is not None and json_path is not None:
            raise ArgError('Only one of the arguments (raw_json and json_path) needs to be set')

        if raw_json is not None:
            if type(raw_json) is not dict:
                raise ArgError('The argument [raw_json] must be dictionary type')
            phase_data = raw_json['phase_data']
            if type(phase_data) is list:
                self._phase_data = phase_data
            else:
                raise JSONDataError('The phase_data\'s value of JSON data must be list type')

        elif json_path is not None:
            if type(json_path) is not str:
                raise ArgError('The argument [json_path] must be string type')

            if not os.path.isfile(json_path):
                raise ArgError(f'The file [{json_path}] does not exist.')

            raw_data = self.get_json_data(json_path)
            phase_data = raw_data['phase_data']
            if type(phase_data) is list:
                self._phase_data = phase_data
            else:
                raise JSONDataError('The phase_data\'s value of JSON data must be list type')

    def get_json_data(self, json_path):
        try:
            with open(json_path, mode='r') as f:
                return json.load(f)
        except Exception as e:
            raise ArgError(f'JSON file [{json_path}] is corrupt') from e

    def pack_svg_tag(self, frame:str, line:str, node:str, node_label:str,  height:int, width:int=WHOLE_MAX_WIDTH):
        return f'<svg width="{width}" height="{height}">{frame}{line}{node}{node_label}</svg>'

    def get_nodes(self, phase_unit_data)->list[Node]:
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

    def node_sort_key(self, node:Node):
        # idsリスト内の最も小さい数値を比較して並び替える関数
        if not node.parent_ids:  # idsが空の場合は無限大を返して後ろにくるようにする
            return (float('inf'), 0)
        return tuple(node.parent_ids)

    def sort_nodes(self, nodes:list[Node])->list[Node]:
        """各ノードの親IDリストの最も若い親IDを比較して並び替える

        Args:
            nodes (list[Node]): [並び替え対象ノードリスト]

        Returns:
            list[Node]: [並び替え後ノードリスト]
        """
        return sorted(nodes, key=self.node_sort_key)

    def sort_phase_data_by_seq_number(self, data_list:list):
        sorted_list = sorted(data_list, key=lambda x: x.get('seq_number', float('inf')))
        return sorted_list

    def set_node_location(self, nodes:list[Node], color_index:int, node_x:int, node_r:int=10)->list[Node]:
        # 初期Y座標
        start_y = HEADER_HEIGHT + TOP_MARGIN

        positioned_nodes = list[Node]()
        for node in nodes:
            # Y座標の設定
            node.cy = start_y
            # X座標の設定
            node.cx = node_x
            # 半径の設定
            node.cr = node_r
            # ノードカラーの設定
            node.fill = ColorType.get_phase_node_by_index(color_index)
            positioned_nodes.append(node)

            # 初期X座標の更新
            start_y += BETWEEN_NODE_VERTICAL_LENGTH

        return positioned_nodes

    def calculate_body_height(self, nodes_each_phase:list[list[Node]])->int:
        max_node_num = 0

        for nodes in nodes_each_phase:
            node_num = len(nodes)
            if node_num > max_node_num:
                max_node_num = node_num
            else:
                continue

        # ボディ部の高さ
        return (TOP_MARGIN + ((max_node_num-1) * 100) + BOTTOM_MARGIN)



    def draw(self):
        phase_data = self.sort_phase_data_by_seq_number(self._phase_data)

        # フェーズ数の算出
        phase_num = len(phase_data)

        # フェーズ幅の算出(少数点切り捨て)
        phase_width = math.floor(WHOLE_MAX_WIDTH / phase_num)

        # 水平ノード間隔長
        between_node_horizontal_length = math.floor(WHOLE_MAX_WIDTH / phase_num)



        # データの整理
        ## フェーズごとのノード情報リストの取得
        nodes_each_phase = list[list[Node]]()
        for phase_unit_data in phase_data:
            nodes_each_phase.append(self.get_nodes(phase_unit_data))

        ## フェーズごとのノード情報リストの並び替え
        sorted_nodes_each_phase = self.sort_nodes_each_phase(nodes_each_phase)

        ## TODO : フェーズごとのノード情報リストの再配列

        ## フェーズごとのノード情報に描画位置情報を追加する
        positioned_nodes_each_phase = list[list[Node]]()
        ## 初期X座標
        start_x = math.floor(WHOLE_MAX_WIDTH / phase_num / 2)
        for index, nodes in enumerate(sorted_nodes_each_phase):
            positioned_nodes_each_phase.append(self.set_node_location(nodes=nodes, node_x=start_x, color_index=index))
            ## 初期X座標を更新
            start_x += between_node_horizontal_length

        # ボディ部の高さを算出する
        body_height =  self.calculate_body_height(positioned_nodes_each_phase)

        # SVGデータの構築

        ## フレーム(ヘッダ+ボディ)の構築
        frame = Frame(phase_data=phase_data, phase_width=phase_width, header_height=HEADER_HEIGHT, body_height=body_height)
        frame_svg = frame.generate_frame()

        ## ノード間ラインの構築
        line_svg = Line.generate_svg_lines(positioned_nodes_each_phase)

        ## ノードの描画
        node_svg = ''
        node_label = ''
        for nodes in positioned_nodes_each_phase:
            for node in nodes:
                node_svg = node_svg + node.generate_svg_component()
                node_label = node_label + node.get_lable_svg_component()

        svg_height = body_height + HEADER_HEIGHT
        whole_svg = self.pack_svg_tag(frame=frame_svg, line=line_svg, node=node_svg, node_label=node_label, height=svg_height, width=(phase_width*phase_num))

        return whole_svg

    def sort_nodes_each_phase(self, nodes_each_phase:list[list[Node]])->list[list[Node]]:
        # 前フェーズ内のノードデータの並びを考慮して、各フェーズ内のノードデータを並び替える
        # nodes_each_phaseのフェーズ順序は昇順になっていることを前提とする

        sorted_nodes_each_phaselist = list[list[Node]]()

        for index, nodes in enumerate(nodes_each_phase):
            if index == 0:
                # 最前フェーズはノードID昇順にソートする
                sorted_nodes = self.sort_nodes_by_id(nodes)
                sorted_nodes_each_phaselist.append(sorted_nodes)
            else:
                sorted_nodes = list[Node]()
                # 前フェーズの並び従って、ノードデータの親IDリストを見て並び替える。
                ## 前フェーズのノードデータリスト(並び替え済み)を取得する。
                pre_phase_nodes = sorted_nodes_each_phaselist[index-1]
                sorted_nodes = self.sort_nodes_by_pre_phase_nodes(pre_phase_nodes, nodes)
                sorted_nodes_each_phaselist.append(sorted_nodes)
        return sorted_nodes_each_phaselist



    def sort_nodes_by_id(self, nodes:list[Node])->list[Node]:
        return sorted(nodes, key=lambda x: x.id)

    def sort_nodes_by_pre_phase_nodes(self, pre_phase_nodes:list[Node], target_nodes:list[Node])->list[Node]:
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

    def get_child_node_num_by_id(self, target_node_id:int, nodes:list[Node])->int:
        child_node_num = 0

        for node in nodes:
            parent_ids = sorted(node.parent_ids)
            priority_parent_id = parent_ids[0]
            if priority_parent_id == target_node_id:
                child_node_num += 1

        return child_node_num

    def generate_dummy_nodes(self, node_num:int, parent_ids:list[int])->list[Node]:
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
