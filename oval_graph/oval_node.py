'''
    Modules form my lib and for create ID
'''
import uuid

import oval_graph.evaluate


'''
    This module contains methods and classes for
    constructing and controlling an oval tree.
'''


class OvalNode():
    '''
    The OvalNode object is one node of oval_graph.

    Args:
        node_id (str|int): identifies node
        input_node_type (str): type of node (value or operator)
        input_value (str): value of node
        input_negation (bool): value indicating whether the node is negated or not
        comment (str): text about node
        tag (str): tag specifies if the node represents OVAL test, OVAL definition or XCCDF rule
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
            tag,
            children=None
    ):
        self.comment = comment
        self.node_id = node_id
        self.negation = self.validate_negation(input_negation)
        self.node_type = self.validate_type(input_node_type)
        self.value = self.validate_type_and_value(input_value)
        self.children = []
        self.validate_children(children)
        self.tag = tag
        if children:
            for child in children:
                self.add_child(child)

    def validate_negation(self, input_negation):
        if not isinstance(input_negation, bool):
            raise ValueError("err- negation is bool (only True or False)")
        return input_negation

    def validate_type(self, input_node_type):
        node_type = input_node_type.lower()
        if node_type != "value" and node_type != "operator":
            raise ValueError("err- unknown type")
        return node_type

    def validate_type_and_value(self, input_value):
        value = input_value.lower()

        allowed_values = [
            "true",
            "false",
            "error",
            "unknown",
            "noteval",
            "notappl"]
        allowed_operators = ["or", "and", "one", "xor"]

        if self.node_type == "value":
            if value not in allowed_values:
                raise ValueError("err- unknown value")

        if self.node_type == "operator":
            if value not in allowed_operators:
                raise ValueError("err- unknown operator")
        return value

    def validate_children(self, children):
        if children is None and self.node_type == "operator":
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
        if oval_graph.evaluate.is_notapp_result(result):
            out_result = "notappl"
        else:
            if self.value == "or":
                out_result = oval_graph.evaluate.oval_operator_or(result)
            elif self.value == "and":
                out_result = oval_graph.evaluate.oval_operator_and(result)
            elif self.value == "one":
                out_result = oval_graph.evaluate.oval_operator_one(result)
            elif self.value == "xor":
                out_result = oval_graph.evaluate.oval_operator_xor(result)

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
                'tag': self.tag,
                'child': None
            }
        return {
            'node_id': self.node_id,
            'type': self.node_type,
            'value': self.value,
            'negation': self.negation,
            'comment': self.comment,
            'tag': self.tag,
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


def restore_dict_to_tree(dict_of_tree):
    if dict_of_tree["child"] is None:
        return OvalNode(
            dict_of_tree["node_id"],
            dict_of_tree["type"],
            dict_of_tree["value"],
            dict_of_tree["negation"],
            dict_of_tree["tag"],
            dict_of_tree['comment'])
    return OvalNode(
        dict_of_tree["node_id"],
        dict_of_tree["type"],
        dict_of_tree["value"],
        dict_of_tree["negation"],
        dict_of_tree['comment'],
        dict_of_tree["tag"],
        [restore_dict_to_tree(i) for i in dict_of_tree["child"]])
