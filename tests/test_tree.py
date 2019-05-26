import tree.oval_tree
import pytest


def test_bad_tree():
    with pytest.raises(ValueError) as e:
        badTree()
    assert str(
        e.value) == 'err- true, false, error, unknown. noteval, notappl have not child!'

    with pytest.raises(ValueError) as e:
        treeOnlyAnd()
    assert str(e.value) == 'err- OR, XOR, ONE, AND have child!'

    with pytest.raises(ValueError) as e:
        treeOnlyOr()
    assert str(e.value) == 'err- OR, XOR, ONE, AND have child!'

    with pytest.raises(ValueError) as e:
        treeWithBadType()
    assert str(e.value) == 'err- unknown type'

    with pytest.raises(ValueError) as e:
        treeWithBadValueOfOperator()
    assert str(e.value) == 'err- unknown operator'

    with pytest.raises(ValueError) as e:
        treeWithBadValueOfValue()
    assert str(e.value) == 'err- unknown value'


# degenered trees

def badTree():
    """
         t
         |
        and
         |
         t
    """
    t = tree.oval_tree.OvalNode(
        1, "value", "true", [
            tree.oval_tree.OvalNode(
                2, "operator", "and", [
                    tree.oval_tree.OvalNode(
                        3, "value", "true")])])
    return


def treeOnlyOr():
    """
        or
    """
    Tree = tree.oval_tree.OvalNode(1, "operator", 'or')
    return


def treeOnlyAnd():
    """
        and
    """
    Tree = tree.oval_tree.OvalNode(1, "operator", 'and')
    return


def treeWithBadValueOfOperator():
    Tree = tree.oval_tree.OvalNode(1, "operator", 'nad')
    return


def treeWithBadValueOfValue():
    Tree = tree.oval_tree.OvalNode(1, "value", 'and')
    return


def treeWithBadType():
    Tree = tree.oval_tree.OvalNode(1, "auto", 'and')
    return

# normal trees


def test_UPPERCASETree():
    t = tree.oval_tree.OvalNode(
        1, "OPERATOR", "AND", [
            tree.oval_tree.OvalNode(
                2, "VALUE", "TRUE",), tree.oval_tree.OvalNode(
                3, "VALUE", "NOTAPPL")])

# AND operator


def test_ANDTreeTrue():
    Tree = tree.oval_tree.OvalNode(1, 'operator', 'and', [
        tree.oval_tree.OvalNode(2, 'value', "true"),
        tree.oval_tree.OvalNode(3, 'value', "true"),
        tree.oval_tree.OvalNode(4, 'value', "notappl")
    ]
    )

    any_test_treeEvaluation(Tree, "true")


def test_ANDTreeFalse():
    Tree = tree.oval_tree.OvalNode(1, 'operator', 'and', [
        tree.oval_tree.OvalNode(2, 'value', "false"),
        tree.oval_tree.OvalNode(3, 'value', "false"),

        tree.oval_tree.OvalNode(4, 'value', "true"),
        tree.oval_tree.OvalNode(5, 'value', "error"),
        tree.oval_tree.OvalNode(6, 'value', "unknown"),
        tree.oval_tree.OvalNode(7, 'value', "noteval"),
        tree.oval_tree.OvalNode(8, 'value', "notappl")
    ]
    )

    any_test_treeEvaluation(Tree, "false")


def test_ANDTreeError():
    Tree = tree.oval_tree.OvalNode(
        1, 'operator', 'and', [
            tree.oval_tree.OvalNode(
                2, 'value', "error"), tree.oval_tree.OvalNode(
                3, 'value', "error"), tree.oval_tree.OvalNode(
                    4, 'value', "true"), tree.oval_tree.OvalNode(
                        5, 'value', "unknown"), tree.oval_tree.OvalNode(
                            6, 'value', "noteval"), tree.oval_tree.OvalNode(
                                7, 'value', "notappl"), tree.oval_tree.OvalNode(
                                    8, 'value', "error")])

    any_test_treeEvaluation(Tree, "error")


def test_ANDTreeUnknown():
    Tree = tree.oval_tree.OvalNode(
        1, 'operator', 'and', [
            tree.oval_tree.OvalNode(
                2, 'value', "unknown"), tree.oval_tree.OvalNode(
                3, 'value', "unknown"), tree.oval_tree.OvalNode(
                    4, 'value', "true"), tree.oval_tree.OvalNode(
                        5, 'value', "unknown"), tree.oval_tree.OvalNode(
                            6, 'value', "noteval"), tree.oval_tree.OvalNode(
                                7, 'value', "notappl"), tree.oval_tree.OvalNode(
                                    8, 'value', "notappl")])

    any_test_treeEvaluation(Tree, "unknown")


def test_ANDTreeNoteval():
    Tree = tree.oval_tree.OvalNode(
        1, 'operator', 'and', [
            tree.oval_tree.OvalNode(
                2, 'value', "noteval"), tree.oval_tree.OvalNode(
                3, 'value', "noteval"), tree.oval_tree.OvalNode(
                    4, 'value', "true"), tree.oval_tree.OvalNode(
                        5, 'value', "true"), tree.oval_tree.OvalNode(
                            6, 'value', "noteval"), tree.oval_tree.OvalNode(
                                7, 'value', "notappl"), tree.oval_tree.OvalNode(
                                    8, 'value', "notappl")])

    any_test_treeEvaluation(Tree, "noteval")


def test_ANDTreeNotappl():
    Tree = tree.oval_tree.OvalNode(1, 'operator', 'and', [
        tree.oval_tree.OvalNode(2, 'value', "notappl"),
        tree.oval_tree.OvalNode(3, 'value', "notappl"),
        tree.oval_tree.OvalNode(4, 'value', "notappl")
    ]
    )

    any_test_treeEvaluation(Tree, "notappl")

# ONE operator


def test_ONETreeTrue():
    Tree = tree.oval_tree.OvalNode(1, 'operator', 'one', [
        tree.oval_tree.OvalNode(2, 'value', "true"),
        tree.oval_tree.OvalNode(3, 'value', "false"),
        tree.oval_tree.OvalNode(4, 'value', "notappl"),
        tree.oval_tree.OvalNode(5, 'value', "false")
    ]
    )

    any_test_treeEvaluation(Tree, "true")


def test_ONETreeFalse():
    Tree = tree.oval_tree.OvalNode(1, 'operator', 'one', [
        tree.oval_tree.OvalNode(2, 'value', "true"),
        tree.oval_tree.OvalNode(3, 'value', "true"),

        tree.oval_tree.OvalNode(4, 'value', "false"),
        tree.oval_tree.OvalNode(5, 'value', "error"),
        tree.oval_tree.OvalNode(6, 'value', "unknown"),
        tree.oval_tree.OvalNode(7, 'value', "noteval"),
        tree.oval_tree.OvalNode(8, 'value', "notappl")
    ]
    )

    any_test_treeEvaluation(Tree, "false")


def test_ONETreeFalse1():
    Tree = tree.oval_tree.OvalNode(1, 'operator', 'one', [
        tree.oval_tree.OvalNode(2, 'value', "false"),
        tree.oval_tree.OvalNode(3, 'value', "false"),
        tree.oval_tree.OvalNode(4, 'value', "notappl")
    ]
    )

    any_test_treeEvaluation(Tree, "false")


def test_ONETreeError():
    Tree = tree.oval_tree.OvalNode(
        1, 'operator', 'one', [
            tree.oval_tree.OvalNode(
                2, 'value', "error"), tree.oval_tree.OvalNode(
                3, 'value', "error"), tree.oval_tree.OvalNode(
                    4, 'value', "true"), tree.oval_tree.OvalNode(
                        5, 'value', "unknown"), tree.oval_tree.OvalNode(
                            6, 'value', "noteval"), tree.oval_tree.OvalNode(
                                7, 'value', "notappl"), tree.oval_tree.OvalNode(
                                    8, 'value', "false")])

    any_test_treeEvaluation(Tree, "error")


def test_ONETreeUnknown():
    Tree = tree.oval_tree.OvalNode(
        1, 'operator', 'one', [
            tree.oval_tree.OvalNode(
                2, 'value', "unknown"), tree.oval_tree.OvalNode(
                3, 'value', "unknown"), tree.oval_tree.OvalNode(
                    4, 'value', "true"), tree.oval_tree.OvalNode(
                        5, 'value', "unknown"), tree.oval_tree.OvalNode(
                            6, 'value', "noteval"), tree.oval_tree.OvalNode(
                                7, 'value', "notappl"), tree.oval_tree.OvalNode(
                                    8, 'value', "false")])

    any_test_treeEvaluation(Tree, "unknown")


def test_ONETreeNoteval():
    Tree = tree.oval_tree.OvalNode(
        1, 'operator', 'one', [
            tree.oval_tree.OvalNode(
                2, 'value', "noteval"), tree.oval_tree.OvalNode(
                3, 'value', "noteval"), tree.oval_tree.OvalNode(
                    4, 'value', "true"), tree.oval_tree.OvalNode(
                        5, 'value', "false"), tree.oval_tree.OvalNode(
                            6, 'value', "noteval"), tree.oval_tree.OvalNode(
                                7, 'value', "notappl"), tree.oval_tree.OvalNode(
                                    8, 'value', "notappl")])

    any_test_treeEvaluation(Tree, "noteval")


def test_ONETreeNotappl():
    Tree = tree.oval_tree.OvalNode(1, 'operator', 'one', [
        tree.oval_tree.OvalNode(2, 'value', "notappl"),
        tree.oval_tree.OvalNode(3, 'value', "notappl"),
        tree.oval_tree.OvalNode(4, 'value', "notappl")
    ]
    )

    any_test_treeEvaluation(Tree, "notappl")

# OR operator


def test_ORTreeTrue():
    Tree = tree.oval_tree.OvalNode(1, 'operator', 'or', [
        tree.oval_tree.OvalNode(2, 'value', "true"),
        tree.oval_tree.OvalNode(3, 'value', "false"),

        tree.oval_tree.OvalNode(4, 'value', "true"),
        tree.oval_tree.OvalNode(5, 'value', "error"),
        tree.oval_tree.OvalNode(6, 'value', "unknown"),
        tree.oval_tree.OvalNode(7, 'value', "noteval"),
        tree.oval_tree.OvalNode(8, 'value', "notappl")
    ]
    )

    any_test_treeEvaluation(Tree, "true")


def test_ORTreeFalse():
    Tree = tree.oval_tree.OvalNode(1, 'operator', 'or', [
        tree.oval_tree.OvalNode(2, 'value', "false"),
        tree.oval_tree.OvalNode(3, 'value', "false"),
        tree.oval_tree.OvalNode(4, 'value', "notappl")
    ]
    )

    any_test_treeEvaluation(Tree, "false")


def test_ORTreeError():
    Tree = tree.oval_tree.OvalNode(
        1, 'operator', 'or', [
            tree.oval_tree.OvalNode(
                2, 'value', "error"), tree.oval_tree.OvalNode(
                3, 'value', "error"), tree.oval_tree.OvalNode(
                    4, 'value', "false"), tree.oval_tree.OvalNode(
                        5, 'value', "unknown"), tree.oval_tree.OvalNode(
                            6, 'value', "noteval"), tree.oval_tree.OvalNode(
                                7, 'value', "notappl"), tree.oval_tree.OvalNode(
                                    8, 'value', "error")])

    any_test_treeEvaluation(Tree, "error")


def test_ORTreeUnknown():
    Tree = tree.oval_tree.OvalNode(
        1, 'operator', 'or', [
            tree.oval_tree.OvalNode(
                2, 'value', "unknown"), tree.oval_tree.OvalNode(
                3, 'value', "unknown"), tree.oval_tree.OvalNode(
                    4, 'value', "false"), tree.oval_tree.OvalNode(
                        5, 'value', "unknown"), tree.oval_tree.OvalNode(
                            6, 'value', "noteval"), tree.oval_tree.OvalNode(
                                7, 'value', "notappl"), tree.oval_tree.OvalNode(
                                    8, 'value', "notappl")])

    any_test_treeEvaluation(Tree, "unknown")


def test_ORTreeNoteval():
    Tree = tree.oval_tree.OvalNode(
        1, 'operator', 'or', [
            tree.oval_tree.OvalNode(
                2, 'value', "noteval"), tree.oval_tree.OvalNode(
                3, 'value', "noteval"), tree.oval_tree.OvalNode(
                    4, 'value', "false"), tree.oval_tree.OvalNode(
                        5, 'value', "false"), tree.oval_tree.OvalNode(
                            6, 'value', "noteval"), tree.oval_tree.OvalNode(
                                7, 'value', "notappl"), tree.oval_tree.OvalNode(
                                    8, 'value', "notappl")])

    any_test_treeEvaluation(Tree, "noteval")


def test_ORTreeNotappl():
    Tree = tree.oval_tree.OvalNode(1, 'operator', 'or', [
        tree.oval_tree.OvalNode(2, 'value', "notappl"),
        tree.oval_tree.OvalNode(3, 'value', "notappl"),
        tree.oval_tree.OvalNode(4, 'value', "notappl")
    ]
    )

    any_test_treeEvaluation(Tree, "notappl")

# XOR operator


def test_XORTreeTrue():
    Tree = tree.oval_tree.OvalNode(1, 'operator', 'xor', [
        tree.oval_tree.OvalNode(2, 'value', "true"),
        tree.oval_tree.OvalNode(3, 'value', "false"),

        tree.oval_tree.OvalNode(4, 'value', "false"),
        tree.oval_tree.OvalNode(5, 'value', "false"),
        tree.oval_tree.OvalNode(6, 'value', "true"),
        tree.oval_tree.OvalNode(7, 'value', "true"),
        tree.oval_tree.OvalNode(8, 'value', "notappl")
    ]
    )

    any_test_treeEvaluation(Tree, "true")


def test_XORTreeFalse():
    Tree = tree.oval_tree.OvalNode(1, 'operator', 'xor', [
        tree.oval_tree.OvalNode(2, 'value', "true"),
        tree.oval_tree.OvalNode(3, 'value', "false"),

        tree.oval_tree.OvalNode(4, 'value', "false"),
        tree.oval_tree.OvalNode(5, 'value', "true"),
        tree.oval_tree.OvalNode(6, 'value', "true"),
        tree.oval_tree.OvalNode(7, 'value', "true"),
        tree.oval_tree.OvalNode(8, 'value', "notappl")
    ]
    )

    any_test_treeEvaluation(Tree, "false")


def test_XORTreeError():
    Tree = tree.oval_tree.OvalNode(
        1, 'operator', 'xor', [
            tree.oval_tree.OvalNode(
                2, 'value', "error"), tree.oval_tree.OvalNode(
                3, 'value', "error"), tree.oval_tree.OvalNode(
                    4, 'value', "true"), tree.oval_tree.OvalNode(
                        5, 'value', "unknown"), tree.oval_tree.OvalNode(
                            6, 'value', "noteval"), tree.oval_tree.OvalNode(
                                7, 'value', "notappl"), tree.oval_tree.OvalNode(
                                    8, 'value', "false")])

    any_test_treeEvaluation(Tree, "error")


def test_xORTreeUnknown():
    Tree = tree.oval_tree.OvalNode(
        1, 'operator', 'xor', [
            tree.oval_tree.OvalNode(
                2, 'value', "unknown"), tree.oval_tree.OvalNode(
                3, 'value', "unknown"), tree.oval_tree.OvalNode(
                    4, 'value', "true"), tree.oval_tree.OvalNode(
                        5, 'value', "unknown"), tree.oval_tree.OvalNode(
                            6, 'value', "noteval"), tree.oval_tree.OvalNode(
                                7, 'value', "notappl"), tree.oval_tree.OvalNode(
                                    8, 'value', "notappl")])

    any_test_treeEvaluation(Tree, "unknown")


def test_XORTreeNoteval():
    Tree = tree.oval_tree.OvalNode(
        1, 'operator', 'xor', [
            tree.oval_tree.OvalNode(
                2, 'value', "noteval"), tree.oval_tree.OvalNode(
                3, 'value', "noteval"), tree.oval_tree.OvalNode(
                    4, 'value', "true"), tree.oval_tree.OvalNode(
                        5, 'value', "true"), tree.oval_tree.OvalNode(
                            6, 'value', "noteval"), tree.oval_tree.OvalNode(
                                7, 'value', "notappl"), tree.oval_tree.OvalNode(
                                    8, 'value', "notappl")])

    any_test_treeEvaluation(Tree, "noteval")


def test_XORTreeNotappl():
    Tree = tree.oval_tree.OvalNode(1, 'operator', 'xor', [
        tree.oval_tree.OvalNode(2, 'value', "notappl"),
        tree.oval_tree.OvalNode(3, 'value', "notappl"),
        tree.oval_tree.OvalNode(4, 'value', "notappl")
    ]
    )

    any_test_treeEvaluation(Tree, "notappl")


def test_bigOvalTree():
    Tree = tree.oval_tree.OvalNode(
        1, 'operator', 'and', [
            tree.oval_tree.OvalNode(
                2, 'value', "false"), tree.oval_tree.OvalNode(
                3, 'operator', "xor", [
                    tree.oval_tree.OvalNode(
                        4, 'value', 'true'), tree.oval_tree.OvalNode(
                            5, 'operator', 'one', [
                                tree.oval_tree.OvalNode(
                                    6, 'value', 'noteval'), tree.oval_tree.OvalNode(
                                        7, 'value', 'true'), tree.oval_tree.OvalNode(
                                            8, 'value', 'notappl')]), tree.oval_tree.OvalNode(
                                                9, 'value', 'error')]), tree.oval_tree.OvalNode(
                                                    10, 'operator', 'or', [
                                                        tree.oval_tree.OvalNode(
                                                            11, 'value', "unknown"), tree.oval_tree.OvalNode(
                                                                12, 'value', "true")])])

    dictOfTree = {'node_id': 1, 'type': 'operator', 'value': 'and',
                  'child': [
                      {'node_id': 2, 'type': 'value', 'value': "false", 'child': None},
                      {'node_id': 3, 'type': 'operator', 'value': "xor", 'child': [
                          {'node_id': 4, 'type': 'value', 'value': "true", 'child': None},
                          {'node_id': 5, 'type': 'operator', 'value': "one", 'child': [
                              {'node_id': 6, 'type': 'value', 'value': "noteval", 'child': None},
                              {'node_id': 7, 'type': 'value', 'value': "true", 'child': None},
                              {'node_id': 8, 'type': 'value', 'value': "notappl", 'child': None}
                          ]},
                          {'node_id': 9, 'type': 'value', 'value': "error", 'child': None}]},
                      {'node_id': 10, 'type': 'operator', 'value': 'or', 'child': [
                          {'node_id': 11, 'type': 'value', 'value': "unknown", 'child': None},
                          {'node_id': 12, 'type': 'value', 'value': "true", 'child': None}
                      ]
                      }
                  ]
                  }

    any_test_treeEvaluation(Tree, "false")
    any_test_treeToDictOfTree(Tree, dictOfTree)
    find_any_node(Tree, 5)
    any_test_dictToTree(dictOfTree)

###################################################


def any_test_treeToDictOfTree(tree, dictOfTree):
    assert tree.treeToDict() == dictOfTree


def find_any_node(Tree, node_id):
    findTree = tree.oval_tree.findNodeWithID(Tree, node_id)
    assert findTree.node_id == node_id


def any_test_treeEvaluation(tree, expect):
    assert tree.evaluateTree() == expect


def any_test_dictToTree(dictOfTree):
    treedictOfTree = tree.oval_tree.dictToTree(dictOfTree)
    assert treedictOfTree.treeToDict() == dictOfTree


def test_treeRepr():
    """
        and
         |
         f
    """
    Tree = tree.oval_tree.OvalNode(1, 'operator', 'and', [
        tree.oval_tree.OvalNode(2, 'value', "false")
    ]
    )
    assert str(Tree) == "and"


def test_addToTree():
    """
        and
         |
         f
    """

    dictOfTree = {'node_id': 1, 'type': 'operator', 'value': 'and',
                  'child': [
                      {'node_id': 2, 'type': 'value', 'value': "false", 'child': None},
                      {'node_id': 3, 'type': 'value', 'value': "true", 'child': None},
                  ]
                  }

    Tree = tree.oval_tree.OvalNode(1, 'operator', 'and', [
        tree.oval_tree.OvalNode(2, 'value', "false")
    ]
    )
    Tree1 = tree.oval_tree.OvalNode(3, 'value', "true")
    tree.oval_tree.addToTree(Tree, 1, Tree1)
    assert Tree.treeToDict() == dictOfTree


def test_ChangeValueTree():
    """
        and
        /|\
       t t or
          / \
         f   t
    """
    Tree = tree.oval_tree.OvalNode(1, 'operator', 'and', [
        tree.oval_tree.OvalNode(2, 'value', "true"),
        tree.oval_tree.OvalNode(3, 'value', "false"),
        tree.oval_tree.OvalNode(4, 'operator', 'or', [
            tree.oval_tree.OvalNode(5, 'value', "false"),
            tree.oval_tree.OvalNode(6, 'value', "true")
        ]
        )
    ]
    )

    tree.oval_tree.ChangeTreeValue(Tree, 3, "true")
    any_test_treeEvaluation(Tree, "true")


def test_bad_operator_input_and():
    result = {
        'true_cnt': -1,
        'false_cnt': -1,
        'error_cnt': -1,
        'unknown_cnt': -1,
        'noteval_cnt': -1,
        'notappl_cnt': -1
    }
    assert tree.oval_tree.oval_operator_and(result) is None


def test_bad_operator_input_one():
    result = {
        'true_cnt': -1,
        'false_cnt': -1,
        'error_cnt': -1,
        'unknown_cnt': -1,
        'noteval_cnt': -1,
        'notappl_cnt': -1
    }
    assert tree.oval_tree.oval_operator_one(result) is None


def test_bad_operator_input_or():
    result = {
        'true_cnt': -1,
        'false_cnt': -1,
        'error_cnt': -1,
        'unknown_cnt': -1,
        'noteval_cnt': -1,
        'notappl_cnt': -1
    }
    assert tree.oval_tree.oval_operator_or(result) is None


def test_bad_operator_input_xor():
    result = {
        'true_cnt': -1,
        'false_cnt': -1,
        'error_cnt': -1,
        'unknown_cnt': -1,
        'noteval_cnt': -1,
        'notappl_cnt': -1
    }
    assert tree.oval_tree.oval_operator_xor(result) is None


def test_false_noteval_greater_zero():
    result = {
        'true_cnt': -1,
        'false_cnt': -1,
        'error_cnt': -1,
        'unknown_cnt': -1,
        'noteval_cnt': -1,
        'notappl_cnt': -1
    }
    assert tree.oval_tree.noteval_greater_zero(result) == False

def test_false_error_unknown_eq_zero_noteval_greater_zero():
    result = {
        'true_cnt': -1,
        'false_cnt': -1,
        'error_cnt': -1,
        'unknown_cnt': -1,
        'noteval_cnt': -1,
        'notappl_cnt': -1
    }
    assert tree.oval_tree.error_unknown_eq_noteval_greater_zero(result) == False
