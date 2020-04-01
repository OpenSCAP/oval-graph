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

    Attributes:
        node_id (str): id of node
        node_type (str): type node
        value (str): value of node for operator and, or, one etc... and for value true,
        false, error etc...
        negation (bool): value indicating whether the node is negated
        comment (str): some comment about node
        tag (str): tag specifies if the node represents OVAL test,
        OVAL definition or XCCDF rule
        test_result_details (dict|None): information about test
        children ([OvalNode]): children of node
    '''

    def __init__(self, **kwargs):
        """
        Note:
            This metode construct OvalNode and validate values of parameteres.

        Required args:
            node_id (str|int): identifies node
            node_type (str): type of node (value or operator)
            value (str): value of node

        Optional args:
            negation (bool): value indicating whether the node is negated (empty eq False)
            comment (str): text about node (empty eq None)
            tag (str): tag specifies if the node represents OVAL test,
            OVAL definition or XCCDF rule (empty eq None)
            test_result_details (dict|None): information about test (empty eq None)
            children ([OvalNode]): array of children of node (empty eq empty array)
        """
        try:
            self.node_id = kwargs['node_id']
            self.node_type = self._validate_type(kwargs['node_type'])
            self.value = self._validate_value(kwargs['value'])

            self._check_missing_children_for_operator(
                kwargs.get('children', None))
            self.negation = self._validate_negation(
                kwargs.get('negation', False))
        except KeyError:
            raise Exception("Missing required argument!")

        self.comment = kwargs.get('comment', None)
        self.tag = kwargs.get('tag', None)
        self.test_result_details = kwargs.get('test_result_details', None)

        input_children = kwargs.get('children', None)
        self.children = []
        if input_children:
            for child in input_children:
                self._add_child(child)

    def _validate_negation(self, input_negation):
        if not isinstance(input_negation, bool):
            raise TypeError("Wrong value of negation argument!")
        return input_negation

    def _validate_type(self, input_node_type):
        node_type = input_node_type.lower()
        if node_type not in ("value", "operator"):
            raise TypeError("Wrong value of node_type argument!")
        return node_type

    def _validate_value(self, input_value):
        value = input_value.lower()

        allowed_values = [
            "true",
            "false",
            "error",
            "unknown",
            "noteval",
            "notappl"]
        allowed_operators = ["or", "and", "one", "xor"]

        if self.node_type == "value" and value not in allowed_values:
            raise TypeError(
                "Wrong value of argument value for value node!")

        if self.node_type == "operator" and value not in allowed_operators:
            raise TypeError(
                "Wrong value of argument value for operator node!")

        return value

    def _check_missing_children_for_operator(self, children):
        if children is None and self.node_type == "operator":
            raise ValueError(
                "The operator node must have a child!")

    def __repr__(self):
        return self.value

    def _add_child(self, node):
        if self.node_type == "operator":
            assert isinstance(node, OvalNode)
            self.children.append(node)
        else:
            self.children = None
            raise ValueError(
                "The value node cannot contain any child!")

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
            if child.value == 'true' and not child.negation:
                result['true_cnt'] += 1
            elif child.value == 'true' and child.negation:
                result['false_cnt'] += 1
            elif child.value == 'false' and not child.negation:
                result['false_cnt'] += 1
            elif child.value == 'false' and child.negation:
                result['true_cnt'] += 1
            else:
                if child.node_type == "operator":
                    result[child.evaluate_tree() + "_cnt"] += 1
                else:
                    result[child.value + "_cnt"] += 1
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
                'test_result_details': self.test_result_details,
                'child': None
            }
        return {
            'node_id': self.node_id,
            'type': self.node_type,
            'value': self.value,
            'negation': self.negation,
            'comment': self.comment,
            'tag': self.tag,
            'test_result_details': self.test_result_details,
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
        self.find_node_with_ID(node_id)._add_child(newNode)

    def change_tree_value(self, node_id, value):
        self.find_node_with_ID(node_id).value = value


def restore_dict_to_tree(dict_of_tree):
    if dict_of_tree["child"] is None:
        return OvalNode(
            node_id=dict_of_tree["node_id"],
            node_type=dict_of_tree["type"],
            value=dict_of_tree["value"],
            negation=dict_of_tree["negation"],
            comment=dict_of_tree["comment"],
            tag=dict_of_tree["tag"],
            test_result_details=dict_of_tree["test_result_details"])
    return OvalNode(
        node_id=dict_of_tree["node_id"],
        node_type=dict_of_tree["type"],
        value=dict_of_tree["value"],
        negation=dict_of_tree["negation"],
        comment=dict_of_tree["comment"],
        tag=dict_of_tree["tag"],
        test_result_details=dict_of_tree["test_result_details"],
        children=[restore_dict_to_tree(i) for i in dict_of_tree["child"]])
