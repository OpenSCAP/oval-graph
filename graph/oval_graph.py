'''
    Modules form my lib and for create ID
'''
import graph.xml_parser
import graph.evaluate
import uuid
import collections
import re

'''
    This module contains methods and classes for
    constructing and controlling an oval tree.
'''


class OvalNode():
    '''
    The OvalNode object is one node of oval graph.

    Args:
        node_id (str|int): identifies node
        input_node_type (str): type of node (value or operator)
        input_value (str): value of node
        children ([OvalNode]): array of children of node

    Attributes:
        node_id (str): id of node
        node_type (str): type node
        value (str): value of node for operator and,
        or, one etc... and for value true, false, error etc...
        children ([OvalNode]): children of node
    '''

    def __init__(
            self,
            node_id,
            input_node_type,
            input_value,
            input_negation,
            children=None):
        self.node_id = node_id
        if isinstance(input_negation, bool):
            self.negation = input_negation
        else:
            raise ValueError("err- negation si bool (only True or False)")
        value = input_value.lower()
        node_type = input_node_type.lower()
        if node_type == "value" or node_type == "operator":
            self.node_type = node_type
        else:
            raise ValueError("err- unknown type")
        allowed_operators = [
            "or",
            "and",
            "one",
            "xor"]
        allowed_values = [
            "true",
            "false",
            "error",
            "unknown",
            "noteval",
            "notappl"]
        if self.node_type == "value":
            if value in allowed_values:
                self.value = value
            else:
                raise ValueError("err- unknown value")
        if self.node_type == "operator":
            if value in allowed_operators:
                self.value = value
            else:
                raise ValueError("err- unknown operator")
        self.children = []
        if children is not None:
            for child in children:
                self.add_child(child)
        else:
            if self.node_type == "operator":
                raise ValueError('err- OR, XOR, ONE, AND have child!')

    def __repr__(self):
        return self.value

    def add_child(self, node):
        if self.node_type == "operator":
            assert isinstance(node, OvalNode)
            self.children.append(node)
        else:
            self.children = None
            raise ValueError(
                "err- true, false, error, unknown. noteval, notappl have not child!")

    def _get_result_counts(self):
        result = {
            'true_cnt': 0,
            'false_cnt': 0,
            'error_cnt': 0,
            'unknown_cnt': 0,
            'noteval_cnt': 0,
            'notappl_cnt': 0
        }

        for child in self.children:
            if child.value == 'true':
                if child.negation:
                    result['false_cnt'] += 1
                else:
                    result['true_cnt'] += 1
            elif child.value == 'false':
                if child.negation:
                    result['true_cnt'] += 1
                else:
                    result['false_cnt'] += 1
            elif child.value == 'error':
                result['error_cnt'] += 1
            elif child.value == 'unknown':
                result['unknown_cnt'] += 1
            elif child.value == 'noteval':
                result['noteval_cnt'] += 1
            elif child.value == 'notappl':
                result['notappl_cnt'] += 1
            else:
                if self.node_type == "operator":
                    result[child.evaluate_tree() + "_cnt"] += 1
        return result

    def evaluate_tree(self):
        result = self._get_result_counts()
        out_result = None
        if graph.evaluate.is_notapp_result(result):
            out_result = "notappl"
        else:
            if self.value == "or":
                out_result = graph.evaluate.oval_operator_or(result)
            elif self.value == "and":
                out_result = graph.evaluate.oval_operator_and(result)
            elif self.value == "one":
                out_result = graph.evaluate.oval_operator_one(result)
            elif self.value == "xor":
                out_result = graph.evaluate.oval_operator_xor(result)

        if out_result == 'true' and self.negation:
            out_result = 'false'
        elif out_result == 'false' and self.negation:
            out_result = 'true'

        return out_result

    def save_tree_to_dict(self):
        if not self.children:
            return {
                'node_id': self.node_id,
                'type': self.node_type,
                'value': self.value,
                'negation': self.negation,
                'child': None
            }
        return {
            'node_id': self.node_id,
            'type': self.node_type,
            'value': self.value,
            'negation': self.negation,
            'child': [child.save_tree_to_dict() for child in self.children]
        }

    def find_node_with_ID(self, node_id):
        if self.node_id == node_id:
            return self
        else:
            for child in self.children:
                if child.node_id == node_id:
                    return child
            for child in self.children:
                if child.children != []:
                    return child.find_node_with_ID(node_id)

    def add_to_tree(self, node_id, newNode):
        self.find_node_with_ID(node_id).add_child(newNode)

    def change_tree_value(self, node_id, value):
        self.find_node_with_ID(node_id).value = value

    # Methods for interpreting oval tree with SigmaJS

    def _get_label(self):
        if self.node_type == 'value':
            return re.sub(
                '(oval:ssg-test_|oval:ssg-)|(:def:1|:tst:1)', '', str(self.node_id))
        else:
            if str(self.node_id).startswith('xccdf_org'):
                return re.sub(
                    '(xccdf_org.ssgproject.content_)', '', str(
                        self.node_id))
            return self.value

    def _is_negated_boolean(self, boolean, value):
        if value == boolean and self.negation:
            return True
        return False

    def _get_node_colors(self):
        value = self.evaluate_tree()
        borderValue = None
        if value is None:
            if self._is_negated_boolean('true', self.value):
                borderValue = 'false'
            elif self._is_negated_boolean('false', self.value):
                borderValue = 'true'
            else:
                borderValue = self.value
            borderValue, value = self.value, borderValue
        else:
            if self._is_negated_boolean('true', value):
                borderValue = 'false'
            elif self._is_negated_boolean('false', value):
                borderValue = 'true'
            else:
                borderValue = value
        VALUE_TO_COLOR = {
            "true": "#00ff00",
            "false": "#ff0000",
            "error": "#000000",
            "unknown": "#000000",
            "noteval": "#000000",
            "notappl": "#000000"
        }
        return dict(
            color=VALUE_TO_COLOR[value],
            borderColor=VALUE_TO_COLOR[borderValue])

    def _get_node_title(self):
        value = self.evaluate_tree()
        if value is None:
            value = self.value
        if value == 'true' or value == 'false':
            return self.node_id
        return str(self.node_id) + ' ' + self.value

    def _create_node(self, x, y):
        # print(self.evaluate_tree(),self.value)
        colors = self._get_node_colors()
        return {
            'id': self.node_id,
            'label': self._get_label(),
            'url': 'null',
            'text': 'null',
            'title': self._get_node_title(),
            "x": x,
            "y": y,
            "size": 3,
            "color": colors['color'],
            "type": "circle",
            "borderColor": colors['borderColor']}

    def _create_edge(self, id_source, id_target, target_node):
        return {
            "id": str(uuid.uuid4()),
            "source": id_source,
            "target": id_target,
            "color": self._get_color_edge(target_node)
        }

    def _get_color_edge(self, target_node):
        return target_node['color']

    def create_list_of_id(self, array_of_ids=None):
        if array_of_ids is None:
            array_of_ids = []
            array_of_ids.append(self.node_id)
        for child in self.children:
            if child.node_type != "operator":
                array_of_ids.append(child.node_id)
            else:
                array_of_ids.append(child.node_id)
                child.create_list_of_id(array_of_ids)
        return array_of_ids

    def _remove_Duplication(self, graph_data):
        array_of_ids = self.create_list_of_id()
        out = dict(nodes=[], edges=graph_data['edges'])
        duplicate_ids = [item for item, count in collections.Counter(
            array_of_ids).items() if count > 1]

        for node in graph_data['nodes']:
            if node['id'] not in duplicate_ids:
                out['nodes'].append(node)

        for id in duplicate_ids:
            for node in graph_data['nodes']:
                if node['id'] == id:
                    out['nodes'].append(node)
                    break
        return out

    def _fix_graph(self, preprocessed_graph_data):
        for node in preprocessed_graph_data['nodes']:
            for node1 in preprocessed_graph_data['nodes']:
                if node['x'] == node1['x'] and node['y'] == node1['y']:
                    node['x'] = node['x'] - 1
        return preprocessed_graph_data

    def _help_to_sigma_dict(self, x, y, preprocessed_graph_data=None):
        if preprocessed_graph_data is None:
            preprocessed_graph_data = dict(nodes=[], edges=[])
            preprocessed_graph_data['nodes'].append(self._create_node(x, y))
        y_row = y + 1
        x_row = x
        for node in self.children:
            preprocessed_graph_data['nodes'].append(
                node._create_node(x_row, y_row))
            preprocessed_graph_data['edges'].append(node._create_edge(
                self.node_id, node.node_id, preprocessed_graph_data['nodes'][-1]))
            x_row = x_row + 1
            if node.children is not None:
                preprocessed_graph_data = node._help_to_sigma_dict(
                    x_row + 1, y_row + 1, preprocessed_graph_data)
        return self._fix_graph(preprocessed_graph_data)

    def _count_max_y(self, out):
        max_y = 0

        for node in out['nodes']:
            if max_y < node['y']:
                max_y = node['y']
        return max_y

    def _create_nodes_in_rows(self, rows):
        nodes_in_rows = dict()

        for i in range(rows + 1):
            nodes_in_rows[i] = []
        return nodes_in_rows

    def _push_nodes_to_nodes_in_row(self, out, nodes_in_rows):
        for node in out['nodes']:
            nodes_in_rows[node['y']].append(node)

    def _remove_empty_rows(self, nodes_in_rows, max_y):
        for row in range(max_y + 1):
            if not nodes_in_rows[row]:
                del nodes_in_rows[row]

    def _move_rows(self, nodes_in_rows):
        count = 0
        nodes_in_rows1 = dict()

        for row in nodes_in_rows:
            nodes_in_rows1[count] = nodes_in_rows[row]
            for node in nodes_in_rows1[count]:
                node['y'] = count
            count += 1
        return nodes_in_rows1

    def _create_positions(self, nodes_in_rows):
        positions = []
        for row in nodes_in_rows:
            len_of_row = len(nodes_in_rows[row])
            if len_of_row > 1:
                if (len_of_row % 2) == 1:
                    len_of_row += 1

                for i in range((int(-(len_of_row / 2))) * 2,
                               (int(+(len_of_row / 2)) + 1) * 2, 2):
                    positions.append(i)

                if len_of_row == 2:
                    positions.remove(0)

                if len(nodes_in_rows[row]) < len(positions):
                    positions.pop()
                    if len(nodes_in_rows[row]) < len(positions):
                        positions.pop(0)

                count = 0

                for pos in positions:
                    nodes_in_rows[row][count]['x'] = pos
                    count += 1
                positions = []
            else:
                nodes_in_rows[row][0]['x'] = 0

        return positions

    def _convert_nodes_in_rows_to_nodes(self, nodes_in_rows):
        nodes = []
        for row in nodes_in_rows:
            for node in nodes_in_rows[row]:
                nodes.append(node)
        return nodes

    def _change_position(self, positions, nodes_in_rows):
        x = 0.6
        up_and_down = True
        down = False
        down_row = False
        save_x = 0
        continue_move = False

        for row in nodes_in_rows:
            for node in nodes_in_rows[row]:
                if (len(node['label']) > 6
                        and len(node['label']) < 40
                        or continue_move):
                    if up_and_down:
                        node['y'] = node['y'] + (0.6 * x)
                        up_and_down = False
                    else:
                        up_and_down = True
                    continue_move = True
                elif len(node['label']) > 30:
                    node['y'] = node['y'] + (0.6 * x)
                    x += 0.6
                    save_x = x
                    down = True
                else:
                    if down:
                        node['y'] = node['y'] + (0.6 * save_x)

                    if down_row:
                        node['y'] = node['y'] + (0.6 * save_x) - 0.7
            if down:
                down = False
                down_row = True
            continue_move = False
            x = 0.6

    def _sort(self, array):
        less = []
        equal = []
        greater = []

        if len(array) > 1:
            pivot = array[0]['x']
            for node in array:
                if node['x'] < pivot:
                    less.append(node)
                if node['x'] == pivot:
                    equal.append(node)
                if node['x'] > pivot:
                    greater.append(node)
            return self._sort(less) + equal + self._sort(greater)
        else:
            return array

    def _sort_nodes(self, nodes_in_rows):
        for row in nodes_in_rows:
            nodes_in_rows[row] = self._sort(nodes_in_rows[row])

    def _center_graph(self, out):
        max_y = self._count_max_y(out)
        nodes_in_rows = self._create_nodes_in_rows(max_y)
        self._push_nodes_to_nodes_in_row(out, nodes_in_rows)
        self._remove_empty_rows(nodes_in_rows, max_y)
        nodes_in_rows = self._move_rows(nodes_in_rows)
        self._sort_nodes(nodes_in_rows)
        positions = self._create_positions(nodes_in_rows)
        self._change_position(positions, nodes_in_rows)
        out['nodes'] = self._convert_nodes_in_rows_to_nodes(nodes_in_rows)
        return out

    def to_sigma_dict(self, x, y):
        return self._center_graph(
            self._remove_Duplication(
                self._help_to_sigma_dict(
                    x, y)))


def build_nodes_form_xml(xml_src, rule_id):
    parser = graph.xml_parser.xml_parser(xml_src)
    return parser.get_oval_graph(rule_id)


def restore_dict_to_tree(dict_of_tree):
    if dict_of_tree["child"] is None:
        return OvalNode(
            dict_of_tree["node_id"],
            dict_of_tree["type"],
            dict_of_tree["value"],
            dict_of_tree["negation"])
    return OvalNode(
        dict_of_tree["node_id"],
        dict_of_tree["type"],
        dict_of_tree["value"],
        dict_of_tree["negation"],
        [restore_dict_to_tree(i) for i in dict_of_tree["child"]])
