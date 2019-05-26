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
                and noteval_eq_zero(result)\
                and false_eq_zero(result)\
                and error_eq_zero(result)\
                and unknown_eq_zero(result)\
                and true_eq_zero(result):
            return "notappl"
        else:
            if self.value == "or":
                return oval_operator_or(result)
            elif self.value == "and":
                return oval_operator_and(result)
            elif self.value == "one":
                return oval_operator_one(result)
            elif self.value == "xor":
                return oval_operator_xor(result)

    def treeToDict(self):
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
            'child': [child.treeToDict() for child in self.children]
        }


def dictToTree(dictOfTree):
    if dictOfTree["child"] is None:
        return OvalNode(
            dictOfTree["node_id"],
            dictOfTree["type"],
            dictOfTree["value"])
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


def oval_operator_and(result):
    out_result = None
    if true_greater_zero(result)\
            and false_eq_zero(result)\
            and error_unknown_noteval_eq_zero(result):
        out_result = 'true'
    elif false_greater_zero(result):
        out_result = 'false'
    elif false_eq_zero(result)\
            and error_greater_zero(result):
        out_result = 'error'
    elif false_eq_zero(result)\
            and error_unknown_eq_zero(result):
        out_result = 'unknown'
    elif false_eq_zero(result)\
            and error_unknown_eq_noteval_greater_zero(result):
        out_result = 'noteval'
    else:
        out_result = None
    return out_result


def oval_operator_one(result):
    out_result = None
    if result['true_cnt'] == 1\
            and result['false_cnt'] >= 0\
            and error_eq_zero(result)\
            and unknown_eq_zero(result)\
            and noteval_eq_zero(result)\
            and result['notappl_cnt'] >= 0:
        out_result = 'true'
    elif result['true_cnt'] >= 2\
            and result['false_cnt'] >= 0\
            and result['error_cnt'] >= 0\
            and result['unknown_cnt'] >= 0\
            and result['noteval_cnt'] >= 0\
            and result['notappl_cnt'] >= 0:
        out_result = 'false'
    elif true_eq_zero(result)\
            and result['false_cnt'] >= 0\
            and error_eq_zero(result)\
            and unknown_eq_zero(result)\
            and noteval_eq_zero(result)\
            and result['notappl_cnt'] >= 0:
        out_result = 'false'
    elif result['true_cnt'] < 2\
            and result['false_cnt'] >= 0\
            and error_greater_zero(result)\
            and result['unknown_cnt'] >= 0\
            and result['noteval_cnt'] >= 0\
            and result['notappl_cnt'] >= 0:
        out_result = 'error'
    elif result['true_cnt'] < 2\
            and result['false_cnt'] >= 0\
            and error_eq_zero(result)\
            and result['unknown_cnt'] >= 1\
            and result['noteval_cnt'] >= 0\
            and result['notappl_cnt'] >= 0:
        out_result = 'unknown'
    elif result['true_cnt'] < 2\
            and result['false_cnt'] >= 0\
            and error_eq_zero(result)\
            and unknown_eq_zero(result)\
            and noteval_greater_zero(result)\
            and result['notappl_cnt'] >= 0:
        out_result = 'noteval'
    else:
        out_result = None
    return out_result


def oval_operator_or(result):
    out_result = None
    if true_greater_zero(result):
        out_result = 'true'
    elif true_eq_zero(result)\
            and false_greater_zero(result)\
            and error_unknown_noteval_eq_zero(result):
        out_result = 'false'
    elif true_eq_zero(result)\
            and error_greater_zero(result):
        out_result = 'error'
    elif true_eq_zero(result)\
            and error_unknown_eq_zero(result):
        out_result = 'unknown'
    elif true_eq_zero(result)\
            and error_unknown_eq_noteval_greater_zero(result):
        out_result = 'noteval'
    else:
        out_result = None
    return out_result


def oval_operator_xor(result):
    out_result = None
    if (result['true_cnt'] % 2) == 1\
            and error_eq_zero(result)\
            and unknown_eq_zero(result)\
            and noteval_eq_zero(result):
        out_result = 'true'
    elif (result['true_cnt'] % 2) == 0\
            and error_eq_zero(result)\
            and unknown_eq_zero(result)\
            and noteval_eq_zero(result):
        out_result = 'false'
    elif error_greater_zero(result):
        out_result = 'error'
    elif error_eq_zero(result)\
            and unknown_greater_zero(result):
        out_result = 'unknown'
    elif error_eq_zero(result)\
            and unknown_eq_zero(result)\
            and noteval_greater_zero(result):
        out_result = 'noteval'
    else:
        out_result = None
    return out_result


def noteval_eq_zero(result):
    if result['noteval_cnt'] == 0:
        return True
    return False


def false_eq_zero(result):
    if result['false_cnt'] == 0:
        return True
    return False


def error_eq_zero(result):
    if result['error_cnt'] == 0:
        return True
    return False


def unknown_eq_zero(result):
    if result['unknown_cnt'] == 0:
        return True
    return False


def true_eq_zero(result):
    if result['true_cnt'] == 0:
        return True
    return False


def true_greater_zero(result):
    if result['true_cnt'] > 0:
        return True
    return False


def false_greater_zero(result):
    if result['false_cnt'] > 0:
        return True
    return False


def error_greater_zero(result):
    if result['error_cnt'] > 0:
        return True
    return False


def unknown_greater_zero(result):
    if result['unknown_cnt'] > 0:
        return True
    return False


def noteval_greater_zero(result):
    if result['noteval_cnt'] > 0:
        return True
    return False


def error_unknown_noteval_eq_zero(result):
    if error_eq_zero(result)\
            and unknown_eq_zero(result)\
            and noteval_eq_zero(result):
        return True
    return False


def error_unknown_eq_noteval_greater_zero(result):
    if error_eq_zero(result)\
            and unknown_eq_zero(result)\
            and noteval_greater_zero(result):
        return True
    return False


def error_unknown_eq_zero(result):
    if error_eq_zero(result)\
            and unknown_greater_zero(result):
        return True
    return False
