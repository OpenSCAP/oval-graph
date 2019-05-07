import tree.ovalNode
import os
import pytest


def test_bad_tree():
    with pytest.raises(ValueError) as e:
        bad_tree()
    assert str(
        e.value) == 'err- true, false, error, unknown. noteval, notappl have not child!'

    with pytest.raises(ValueError) as e:
        treeOnlyAnd()
    assert str(e.value) == 'err- OR, XOR, ONE, AND have child!'

    with pytest.raises(ValueError) as e:
        treeOnlyOr()
    assert str(e.value) == 'err- OR, XOR, ONE, AND have child!'

# degenered trees


def bad_tree():
    """
         t
         |
        and
         |
         t
    """
    t = tree.ovalNode.ovalNode(
        1, "value", "true", [
            tree.ovalNode.ovalNode(
                2, "operator", "and", [
                    tree.ovalNode.ovalNode(
                        3, "value", "true")])])


def treeOnlyOr():
    """
        or
    """
    Tree = tree.ovalNode.ovalNode(1, "operator", 'or')


def treeOnlyAnd():
    """
        and
    """
    Tree = tree.ovalNode.ovalNode(1, "operator", 'and')

# normal trees


def test_treeAndFalse():
    """
        and
         |
         f
    """
    Tree = tree.ovalNode.ovalNode(1, "operator", 'and', [
        tree.ovalNode.ovalNode(2, "value", "false")
    ]
    )

    dictOfTree = {'node_id': 1, 'type': 'operator', 'value': 'and', 'child': [
        {'node_id': 2, 'type': 'value', 'value': "false", 'child': None}]}

    any_test_treeEvaluation(Tree, "false")
    any_test_renderTree(Tree)
    any_test_treeTodictOfTree(Tree, dictOfTree)
    find_any_node(Tree, 1)
    any_test_dictToTree(dictOfTree)


def test_treeAllFalse():
    """
        and
        /|\
       f f or
          / \
         f   f
    """
    Tree = tree.ovalNode.ovalNode(1, 'operator', 'and', [
        tree.ovalNode.ovalNode(2, 'value', "false"),
        tree.ovalNode.ovalNode(3, 'value', "false"),
        tree.ovalNode.ovalNode(4, 'operator', 'or', [
            tree.ovalNode.ovalNode(5, 'value', "false"),
            tree.ovalNode.ovalNode(6, 'value', "false")
        ]
        )
    ]
    )

    dictOfTree = {'node_id': 1, 'type': 'operator', 'value': 'and',
                  'child': [
                      {'node_id': 2, 'type': 'value', 'value': "false", 'child': None},
                      {'node_id': 3, 'type': 'value', 'value': "false", 'child': None},
                      {'node_id': 4, 'type': 'operator', 'value': 'or', 'child': [
                          {'node_id': 5, 'type': 'value', 'value': "false", 'child': None},
                          {'node_id': 6, 'type': 'value', 'value': "false", 'child': None}
                      ]
                      }
                  ]
                  }

    any_test_treeEvaluation(Tree, "false")
    any_test_renderTree(Tree)
    any_test_treeTodictOfTree(Tree, dictOfTree)
    find_any_node(Tree, 5)
    any_test_dictToTree(dictOfTree)


def test_allErrorTree():
    """
        and
      /  |\
    and  f or
          / \
         f   f

         "or",
            "and",
            "one",
            "xor",
            "true",
            "false",
            "error",
            "unknown",
            "noteval",
            "notappl"
    """
    Tree = tree.ovalNode.ovalNode(
        1, 'operator', 'and', [
            tree.ovalNode.ovalNode(
                2, 'value', "error"), tree.ovalNode.ovalNode(
                3, 'operator', "xor", [
                    tree.ovalNode.ovalNode(
                        4, 'value', 'error'), tree.ovalNode.ovalNode(
                            5, 'operator', 'one', [
                                tree.ovalNode.ovalNode(
                                    6, 'value', 'error'), tree.ovalNode.ovalNode(
                                        7, 'value', 'error'), tree.ovalNode.ovalNode(
                                            8, 'value', 'error')]), tree.ovalNode.ovalNode(
                                                9, 'value', 'error')]), tree.ovalNode.ovalNode(
                                                    10, 'operator', 'or', [
                                                        tree.ovalNode.ovalNode(
                                                            11, 'value', "error"), tree.ovalNode.ovalNode(
                                                                12, 'value', "error")])])

    dictOfTree = {'node_id': 1, 'type': 'operator', 'value': 'and',
                  'child': [
                      {'node_id': 2, 'type': 'value', 'value': "error", 'child': None},
                      {'node_id': 3, 'type': 'operator', 'value': "xor", 'child': [
                          {'node_id': 4, 'type': 'value', 'value': "error", 'child': None},
                          {'node_id': 5, 'type': 'operator', 'value': "one", 'child': [
                              {'node_id': 6, 'type': 'value', 'value': "error", 'child': None},
                              {'node_id': 7, 'type': 'value', 'value': "error", 'child': None},
                              {'node_id': 8, 'type': 'value', 'value': "error", 'child': None}
                          ]},
                          {'node_id': 9, 'type': 'value', 'value': "error", 'child': None}]},
                      {'node_id': 10, 'type': 'operator', 'value': 'or', 'child': [
                          {'node_id': 11, 'type': 'value', 'value': "error", 'child': None},
                          {'node_id': 12, 'type': 'value', 'value': "error", 'child': None}
                      ]
                      }
                  ]
                  }

    any_test_treeEvaluation(Tree, "error")
    any_test_renderTree(Tree)
    any_test_treeTodictOfTree(Tree, dictOfTree)
    find_any_node(Tree, 5)
    any_test_dictToTree(dictOfTree)


def test_bigOvalTree():
    """
        and
      /  |\
    and  f or
          / \
         f   f

         "or",
            "and",
            "one",
            "xor",
            "true",
            "false",
            "error",
            "unknown",
            "noteval",
            "notappl"
    """
    Tree = tree.ovalNode.ovalNode(
        1, 'operator', 'and', [
            tree.ovalNode.ovalNode(
                2, 'value', "false"), tree.ovalNode.ovalNode(
                3, 'operator', "xor", [
                    tree.ovalNode.ovalNode(
                        4, 'value', 'true'), tree.ovalNode.ovalNode(
                            5, 'operator', 'one', [
                                tree.ovalNode.ovalNode(
                                    6, 'value', 'noteval'), tree.ovalNode.ovalNode(
                                        7, 'value', 'true'), tree.ovalNode.ovalNode(
                                            8, 'value', 'notappl')]), tree.ovalNode.ovalNode(
                                                9, 'value', 'error')]), tree.ovalNode.ovalNode(
                                                    10, 'operator', 'or', [
                                                        tree.ovalNode.ovalNode(
                                                            11, 'value', "unknown"), tree.ovalNode.ovalNode(
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
    any_test_renderTree(Tree)
    any_test_treeTodictOfTree(Tree, dictOfTree)
    find_any_node(Tree, 5)
    any_test_dictToTree(dictOfTree)


def test_idealTree():
    """
        and
        /|\
       t t or
          / \
         f   t
    """
    Tree = tree.ovalNode.ovalNode(1, 'operator', 'and', [
        tree.ovalNode.ovalNode(2, 'value', "true"),
        tree.ovalNode.ovalNode(3, 'value', "false"),
        tree.ovalNode.ovalNode(4, 'operator', 'or', [
            tree.ovalNode.ovalNode(5, 'value', "false"),
            tree.ovalNode.ovalNode(6, 'value', "true")
        ]
        )
    ]
    )

    dictOfTree = {'node_id': 1, 'type': 'operator', 'value': 'and',
                  'child': [
                      {'node_id': 2, 'type': 'value', 'value': "true", 'child': None},
                      {'node_id': 3, 'type': 'value', 'value': "false", 'child': None},
                      {'node_id': 4, 'type': 'operator', 'value': 'or', 'child': [
                          {'node_id': 5, 'type': 'value', 'value': "false", 'child': None},
                          {'node_id': 6, 'type': 'value', 'value': "true", 'child': None}
                      ]
                      }
                  ]
                  }

    any_test_treeEvaluation(Tree, "false")
    any_test_renderTree(Tree)
    any_test_treeTodictOfTree(Tree, dictOfTree)
    find_any_node(Tree, 6)
    any_test_dictToTree(dictOfTree)
###################################################


def any_test_treeTodictOfTree(tree, dictOfTree):
    assert tree.treeToDict() == dictOfTree


def find_any_node(Tree, node_id):
    findTree = tree.ovalNode.findNodeWithID(Tree, node_id)
    assert findTree.node_id == node_id


def any_test_renderTree(tree, img=None):
    assert tree.renderTree(img)


def any_test_treeEvaluation(tree, expect):
    assert tree.evaluateTree() == expect

def any_test_dictToTree(dictOfTree):
    treedictOfTree = tree.ovalNode.dictToTree(dictOfTree)
    # Je to ok?
    assert treedictOfTree.treeToDict() == dictOfTree

def test_treeRepr():
    """
        and
         |
         f
    """
    Tree = tree.ovalNode.ovalNode(1, 'operator', 'and', [
        tree.ovalNode.ovalNode(2, 'value', "false")
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

    Tree = tree.ovalNode.ovalNode(1, 'operator', 'and', [
        tree.ovalNode.ovalNode(2, 'value', "false")
    ]
    )
    Tree1 = tree.ovalNode.ovalNode(3, 'value', "true")
    tree.ovalNode.addToTree(Tree, 1, Tree1)
    assert Tree.treeToDict() == dictOfTree


def test_ChangeValueTree():
    """
        and
        /|\
       t t or
          / \
         f   t
    """
    Tree = tree.ovalNode.ovalNode(1, 'operator', 'and', [
        tree.ovalNode.ovalNode(2, 'value', "true"),
        tree.ovalNode.ovalNode(3, 'value', "false"),
        tree.ovalNode.ovalNode(4, 'operator', 'or', [
            tree.ovalNode.ovalNode(5, 'value', "false"),
            tree.ovalNode.ovalNode(6, 'value', "true")
        ]
        )
    ]
    )

    tree.ovalNode.ChangeTreeValue(Tree, 3, "true")
    any_test_treeEvaluation(Tree, "true")
