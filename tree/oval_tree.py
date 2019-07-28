'''
    Module for create ID
'''
import uuid
import collections

'''
    Modules form my lib
'''
import tree.evaluate
import tree.xml_parser

'''
    This module contains methods and classes for
    constructing and controlling an oval tree.
'''


class OvalNode(object):
    '''
    The OvalNode object is one node of oval tree.

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

    def __init__(self, node_id, input_node_type, input_value, children=None):
        self.node_id = node_id
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

    def evaluate_tree(self):
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
                result['true_cnt'] += 1
            elif child.value == 'false':
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

        if result['notappl_cnt'] > 0\
                and tree.evaluate.noteval_eq_zero(result)\
                and tree.evaluate.false_eq_zero(result)\
                and tree.evaluate.error_eq_zero(result)\
                and tree.evaluate.unknown_eq_zero(result)\
                and tree.evaluate.true_eq_zero(result):
            return "notappl"
        else:
            if self.value == "or":
                return tree.evaluate.oval_operator_or(result)
            elif self.value == "and":
                return tree.evaluate.oval_operator_and(result)
            elif self.value == "one":
                return tree.evaluate.oval_operator_one(result)
            elif self.value == "xor":
                return tree.evaluate.oval_operator_xor(result)

    def save_tree_to_dict(self):
        if not self.children:
            return {
                'node_id': self.node_id,
                'type': self.node_type,
                'value': self.value,
                'child': None
            }
        return {
            'node_id': self.node_id,
            'type': self.node_type,
            'value': self.value,
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

    def _create_node(self, x, y):
        #print(self.evaluate_tree(),self.value)
        if self.value == 'true':
            return {
                'id': self.node_id,
                'label': self.value,
                'url': 'null',
                'text': 'null',
                'title': self.node_id,
                "x": x,
                "y": y,
                "size": 3,
                "color": '#00ff00'
            }
        elif self.value == 'false':
            return {
                'id': self.node_id,
                'label': self.value,
                'url': 'null',
                'text': 'null',
                'title': self.node_id,
                "x": x,
                "y": y,
                "size": 3,
                "color": '#ff0000'
            }
        else:
            if self.evaluate_tree() == 'true':
                return {
                    'id': self.node_id,
                    'label': self.value,
                    'url': 'null',
                    'text': 'null',
                    'title': self.node_id,
                    "x": x,
                    "y": y,
                    "size": 3,
                    "color": '#00ff00'
                }
            elif self.evaluate_tree() == 'false':
                return {
                    'id': self.node_id,
                    'label': self.value,
                    'url': 'null',
                    'text': 'null',
                    'title': self.node_id,
                    "x": x,
                    "y": y,
                    "size": 3,
                    "color": '#ff0000'
                }
            else:
                return {
                    'id': self.node_id,
                    'label': self.value,
                    'url': 'null',
                    'text': 'null',
                    'title': str(self.node_id) + ' ' + self.value,
                    "x": x,
                    "y": y,
                    "size": 3,
                    "color": '#000000'
                }

    def _create_edge(self, id_source, id_target):
        return {
            "id": str(uuid.uuid4()),
            "source": id_source,
            "target": id_target
        }

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
            preprocessed_graph_data['edges'].append(
                node._create_edge(self.node_id, node.node_id))
            x_row = x_row + 1
            if node.children is not None:
                preprocessed_graph_data = node._help_to_sigma_dict(
                    x_row + 1, y_row + 1, preprocessed_graph_data)
        return self._fix_graph(preprocessed_graph_data)

    # TODO - create center graph
    def center_graph(self, out):
        return out

    def to_sigma_dict(self, x, y):
        return self.center_graph(
            self._remove_Duplication(
                self._help_to_sigma_dict(
                    x, y)))


def restore_dict_to_tree(dict_of_tree):
    if dict_of_tree["child"] is None:
        return OvalNode(
            dict_of_tree["node_id"],
            dict_of_tree["type"],
            dict_of_tree["value"])
    return OvalNode(
        dict_of_tree["node_id"],
        dict_of_tree["type"],
        dict_of_tree["value"],
        [restore_dict_to_tree(i) for i in dict_of_tree["child"]])

# Function for transfer XML to OVAL_TREE


def xml_to_tree(xml_src):
    data = tree.xml_parser.parse_data_to_dict(
        tree.xml_parser.get_data_form_xml(xml_src), tree.xml_parser.get_used_rules(xml_src))
    out = []
    for rule in data['rules']:
        out.append(tree.xml_parser.xml_dict_of_rule_to_node(rule))
    return out
