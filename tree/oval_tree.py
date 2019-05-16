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

    def evaluateTree(self):
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
                    result[child.evaluateTree() + "_cnt"] += 1

        if result['notappl_cnt'] > 0\
                and result['noteval_cnt'] == 0\
                and result['false_cnt'] == 0\
                and result['error_cnt'] == 0\
                and result['unknown_cnt'] == 0\
                and result['true_cnt'] == 0:
            return "notappl"

        if self.value == "or":
            return OVAL_OPERATOR_OR(result)
        elif self.value == "and":
            return OVAL_OPERATOR_AND(result)
        elif self.value == "one":
            return OVAL_OPERATOR_ONE(result)
        elif self.value == "xor":
            return OVAL_OPERATOR_XOR(result)

    def treeToDict(self):
        if not self.children:
            return {
                'node_id': self.node_id,
                'type': self.node_type,
                'value': self.value,
                'child': None
            }
        else:
            return {
                'node_id': self.node_id,
                'type': self.node_type,
                'value': self.value,
                'child': [child.treeToDict() for child in self.children]
            }


def dictToTree(dictOfTree):
    if dictOfTree["child"] is None:
        return OvalNode(
            dictOfTree["node_id"],
            dictOfTree["type"],
            dictOfTree["value"])
    else:
        return OvalNode(
            dictOfTree["node_id"],
            dictOfTree["type"],
            dictOfTree["value"],
            [dictToTree(i) for i in dictOfTree["child"]])


def findNodeWithID(tree, node_id):
    if tree.node_id == node_id:
        return tree
    else:
        for child in tree.children:
            if child.node_id == node_id:
                return child
        for child in tree.children:
            if child.children != []:
                return findNodeWithID(child, node_id)


def addToTree(tree, node_id, newNode):
    findNodeWithID(tree, node_id).add_child(newNode)


def ChangeTreeValue(tree, node_id, value):
    findNodeWithID(tree, node_id).value = value


def OVAL_OPERATOR_AND(result):
    out_result = None
    if result['true_cnt'] > 0\
            and result['false_cnt'] == 0\
            and result['error_cnt'] == 0\
            and result['unknown_cnt'] == 0\
            and result['noteval_cnt'] == 0:
        out_result = 'true'
    elif result['false_cnt'] > 0:
        out_result = 'false'
    elif result['false_cnt'] == 0\
            and result['error_cnt'] > 0:
        out_result = 'error'
    elif result['false_cnt'] == 0\
            and result['error_cnt'] == 0\
            and result['unknown_cnt'] > 0:
        out_result = 'unknown'
    elif result['false_cnt'] == 0\
            and result['error_cnt'] == 0\
            and result['unknown_cnt'] == 0\
            and result['noteval_cnt'] > 0:
        out_result = 'noteval'
    return out_result


def OVAL_OPERATOR_ONE(result):
    out_result = None
    if result['true_cnt'] == 1\
            and result['false_cnt'] >= 0\
            and result['error_cnt'] == 0\
            and result['unknown_cnt'] == 0\
            and result['noteval_cnt'] == 0\
            and result['notappl_cnt'] >= 0:
        out_result = 'true'
    elif result['true_cnt'] >= 2\
            and result['false_cnt'] >= 0\
            and result['error_cnt'] >= 0\
            and result['unknown_cnt'] >= 0\
            and result['noteval_cnt'] >= 0\
            and result['notappl_cnt'] >= 0:
        out_result = 'false'
    elif result['true_cnt'] == 0\
            and result['false_cnt'] >= 0\
            and result['error_cnt'] == 0\
            and result['unknown_cnt'] == 0\
            and result['noteval_cnt'] == 0\
            and result['notappl_cnt'] >= 0:
        out_result = 'false'
    elif result['true_cnt'] < 2\
            and result['false_cnt'] >= 0\
            and result['error_cnt'] > 0\
            and result['unknown_cnt'] >= 0\
            and result['noteval_cnt'] >= 0\
            and result['notappl_cnt'] >= 0:
        out_result = 'error'
    elif result['true_cnt'] < 2\
            and result['false_cnt'] >= 0\
            and result['error_cnt'] == 0\
            and result['unknown_cnt'] >= 1\
            and result['noteval_cnt'] >= 0\
            and result['notappl_cnt'] >= 0:
        out_result = 'unknown'
    elif result['true_cnt'] < 2\
            and result['false_cnt'] >= 0\
            and result['error_cnt'] == 0\
            and result['unknown_cnt'] == 0\
            and result['noteval_cnt'] > 0\
            and result['notappl_cnt'] >= 0:
        out_result = 'noteval'
    return out_result


def OVAL_OPERATOR_OR(result):
    out_result = None
    if result['true_cnt'] > 0:
        out_result = 'true'
    elif result['true_cnt'] == 0\
            and result['false_cnt'] > 0\
            and result['error_cnt'] == 0\
            and result['unknown_cnt'] == 0\
            and result['noteval_cnt'] == 0:
        out_result = 'false'
    elif result['true_cnt'] == 0\
            and result['error_cnt'] > 0:
        out_result = 'error'
    elif result['true_cnt'] == 0\
            and result['error_cnt'] == 0\
            and result['unknown_cnt'] > 0:
        out_result = 'unknown'
    elif result['true_cnt'] == 0\
            and result['error_cnt'] == 0\
            and result['unknown_cnt'] == 0\
            and result['noteval_cnt'] > 0:
        out_result = 'noteval'
    return out_result


def OVAL_OPERATOR_XOR(result):
    out_result = None
    if (result['true_cnt'] % 2) == 1\
            and result['error_cnt'] == 0\
            and result['unknown_cnt'] == 0\
            and result['noteval_cnt'] == 0:
        out_result = 'true'
    elif (result['true_cnt'] % 2) == 0\
            and result['error_cnt'] == 0\
            and result['unknown_cnt'] == 0\
            and result['noteval_cnt'] == 0:
        out_result = 'false'
    elif result['error_cnt'] > 0:
        out_result = 'error'
    elif result['error_cnt'] == 0\
            and result['unknown_cnt'] > 0:
        out_result = 'unknown'
    elif result['error_cnt'] == 0\
            and result['unknown_cnt'] == 0\
            and result['noteval_cnt'] > 0:
        out_result = 'noteval'
    return out_result
