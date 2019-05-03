import operator


class operatorTree(object):
    def __init__(self, node_id, value='root', children=None):
        self.node_id = node_id
        allowedValues = ["or", "and", "one", "xor", "true", "false", "error", "unknown", "noteval", "notappl"]
        value.lower()
        if value in allowedValues:
            self.value = value
        else:
            raise ValueError("err- unknown value: ", value)
        self.children = []
        if children is not None:
            for child in children:
                self.add_child(child)
        else:
            if self.value == "or" or self.value == "and" or self.value == "one" or self.value == "xor":
                raise ValueError('err- OR, XOR, ONE, AND have child!')

    def __repr__(self):
        return self.value

    def add_child(self, node):
        if self.value == "or" or self.value == "and" or self.value == "one" or self.value == "xor":
            assert isinstance(node, operatorTree)
            self.children.append(node)
        else:
            self.children = None
            raise ValueError("err- True or False have not child!")

    def evaluateTree(self):
        operators = {
            "or": any,
            "and": all,
        }
        evaluator = operators[self.value]
        return evaluator(
            i.evaluateTree() if type(i.value)is not bool else i.value
            for i in self.children)

    def treeToDict(self):
        if not self.children:
            return {'node_id': self.node_id,
                    'value': self.value,
                    'child': None
                    }
        else:
            return {'node_id': self.node_id,
                    'value': self.value,
                    'child': [child.treeToDict() for child in self.children]
                    }

    def renderTree(self, img=None):
        return True


def dictToTree(dictOfTree):
    if dictOfTree["child"] is None:
        return operatorTree(dictOfTree["node_id"], dictOfTree["value"])
    else:
        return operatorTree(
                    dictOfTree["node_id"],
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


result = {
    'true_cnt': 1,
    'false_cnt': 1,
    'error_cnt': 1,
    'unknown_cnt': 1,
    'noteval_cnt': 1,
    'notappl_cnt': 1
}


def counter(node):
    result = {
        'true_cnt': 0,
        'false_cnt': 0,
        'error_cnt': 0,
        'unknown_cnt': 0,
        'noteval_cnt': 0,
        'notappl_cnt': 0
    }

    for child in node.children:
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
            raise ValueError("err- unknown value:", child.value)


def OVAL_OPERATOR_AND(result):
    if result['true_cnt'] > 0 and result['false_cnt'] == 0 and result['error_cnt'] == 0 and result['unknown_cnt'] == 0 and result['noteval_cnt'] == 0:
        outResult = 'OVAL_RESULT_TRUE'
    elif result['false_cnt'] > 0:
        outResult = 'OVAL_RESULT_FALSE'
    elif result['false_cnt'] == 0 and result['error_cnt'] > 0:
        outResult = 'OVAL_RESULT_ERROR'
    elif result['false_cnt'] == 0 and result['error_cnt'] == 0 and result['unknown_cnt'] > 0:
        outResult = 'OVAL_RESULT_UNKNOWN'
    elif result['false_cnt'] == 0 and result['error_cnt'] == 0 and result['unknown_cnt'] == 0 and result['noteval_cnt'] > 0:
        outResult = 'OVAL_RESULT_NOT_EVALUATED'
    return outResult


def OVAL_OPERATOR_ONE(result):
    if result['true_cnt'] == 1 and result['false_cnt'] >= 0 and result['error_cnt'] == 0 and result['unknown_cnt'] == 0 and result['noteval_cnt'] == 0 and result['notappl_cnt'] >= 0:
        outResult = 'OVAL_RESULT_TRUE'
    elif result['true_cnt'] >= 2 and result['false_cnt'] >= 0 and result['error_cnt'] >= 0 and result['unknown_cnt'] >= 0 and result['noteval_cnt'] >= 0 and result['notappl_cnt'] >= 0:
        outResult = 'OVAL_RESULT_FALSE'
    elif result['true_cnt'] == 0 and result['false_cnt'] >= 0 and result['error_cnt'] == 0 and result['unknown_cnt'] == 0 and result['noteval_cnt'] == 0 and result['notappl_cnt'] >= 0:
        outResult = 'OVAL_RESULT_FALSE'
    elif result['true_cnt'] < 2 and result['false_cnt'] >= 0 and result['error_cnt'] > 0 and result['unknown_cnt'] >= 0 and result['noteval_cnt'] >= 0 and result['notappl_cnt'] >= 0:
        outResult = 'OVAL_RESULT_ERROR'
    elif result['true_cnt'] < 2 and result['false_cnt'] >= 0 and result['error_cnt'] == 0 and result['unknown_cnt'] >= 1 and result['noteval_cnt'] >= 0 and result['notappl_cnt'] >= 0:
        outResult = 'OVAL_RESULT_UNKNOWN'
    elif result['true_cnt'] < 2 and result['false_cnt'] >= 0 and result['error_cnt'] == 0 and result['unknown_cnt'] == 0 and result['noteval_cnt'] > 0 and result['notappl_cnt'] >= 0:
        outResult = 'OVAL_RESULT_NOT_EVALUATED'
    return outResult


def OVAL_OPERATOR_OR(result):
    if result['true_cnt'] > 0:
        outResult = 'OVAL_RESULT_TRUE'
    elif result['true_cnt'] == 0 and result['false_cnt'] > 0 and result['error_cnt'] == 0 and result['unknown_cnt'] == 0 and result['noteval_cnt'] == 0:
        outResult = 'OVAL_RESULT_FALSE'
    elif result['true_cnt'] == 0 and result['error_cnt'] > 0:
        outResult = 'OVAL_RESULT_ERROR'
    elif result['true_cnt'] == 0 and result['error_cnt'] == 0 and result['unknown_cnt'] > 0:
        outResult = 'OVAL_RESULT_UNKNOWN'
    elif result['true_cnt'] == 0 and result['error_cnt'] == 0 and result['unknown_cnt'] == 0 and result['noteval_cnt'] > 0:
        outResult = 'OVAL_RESULT_NOT_EVALUATED'
    return outResult


def OVAL_OPERATOR_XOR(result):
    if (result['true_cnt'] % 2) == 1 and result['error_cnt'] == 0 and result['unknown_cnt'] == 0 and result['noteval_cnt'] == 0:
        outResult = 'OVAL_RESULT_TRUE'
    elif (result['true_cnt'] % 2) == 0 and result['error_cnt'] == 0 and result['unknown_cnt'] == 0 and result['noteval_cnt'] == 0:
        outResult = 'OVAL_RESULT_FALSE'
    elif result['error_cnt'] > 0:
        outResult = 'OVAL_RESULT_ERROR'
    elif result['error_cnt'] == 0 and result['unknown_cnt'] > 0:
        outResult = 'OVAL_RESULT_UNKNOWN'
    elif result['error_cnt'] == 0 and result['unknown_cnt'] == 0 and result['noteval_cnt'] > 0:
        outResult = 'OVAL_RESULT_NOT_EVALUATED'
    return outResult
