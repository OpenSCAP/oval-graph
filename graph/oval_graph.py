'''
    Modules form my lib and for create ID
'''
import graph.xml_parser
import graph.evaluate
import uuid


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
            comment,
            children=None):
        self.comment = comment
        self.node_id = node_id
        if isinstance(input_negation, bool):
            self.negation = input_negation
        else:
            raise ValueError("err- negation is bool (only True or False)")
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
                raise ValueError('err- Operator node has child!')

    def __repr__(self):
        return self.value

    def add_child(self, node):
        if self.node_type == "operator":
            assert isinstance(node, OvalNode)
            self.children.append(node)
        else:
            self.children = None
            raise ValueError(
                "err- Value node don't has any child!")

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
                'comment': self.comment,
                'child': None
            }
        return {
            'node_id': self.node_id,
            'type': self.node_type,
            'value': self.value,
            'negation': self.negation,
            'comment': self.comment,
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


def build_nodes_form_xml(xml_src, rule_id):
    parser = graph.xml_parser.xml_parser(xml_src)
    return parser.get_oval_graph(rule_id)


def restore_dict_to_tree(dict_of_tree):
    if dict_of_tree["child"] is None:
        return OvalNode(
            dict_of_tree["node_id"],
            dict_of_tree["type"],
            dict_of_tree["value"],
            dict_of_tree["negation"],
            dict_of_tree['comment'])
    return OvalNode(
        dict_of_tree["node_id"],
        dict_of_tree["type"],
        dict_of_tree["value"],
        dict_of_tree["negation"],
        dict_of_tree['comment'],
        [restore_dict_to_tree(i) for i in dict_of_tree["child"]])
