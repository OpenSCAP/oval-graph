import tree.ovalNode
import os
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

def treeWithBadValueOfOperator():
    Tree = tree.ovalNode.ovalNode(1, "operator", 'nad')
    

def treeWithBadValueOfValue():
    Tree = tree.ovalNode.ovalNode(1, "value", 'and')

def treeWithBadType():
    Tree = tree.ovalNode.ovalNode(1, "auto", 'and')

# normal trees
#and tree
def test_ANDTreeTrue():
    Tree = tree.ovalNode.ovalNode(1, 'operator', 'and', [
        tree.ovalNode.ovalNode(2, 'value', "true"),
        tree.ovalNode.ovalNode(3, 'value', "true"),
         tree.ovalNode.ovalNode(4, 'value', "notappl")
    ]
    )

    dictOfTree = {'node_id': 1, 'type': 'operator', 'value': 'and',
                  'child': [
                      {'node_id': 2, 'type': 'value', 'value': "true", 'child': None},
                      {'node_id': 3, 'type': 'value', 'value': "true", 'child': None},
                      {'node_id': 4, 'type': 'value', 'value': "notappl", 'child': None}
                  ]
                  }

    any_test_treeEvaluation(Tree, "true")
    any_test_renderTree(Tree)
    any_test_treeToDictOfTree(Tree, dictOfTree)
    find_any_node(Tree, 1)
    any_test_dictToTree(dictOfTree)


def test_ANDTreeFalse():
    Tree = tree.ovalNode.ovalNode(1, 'operator', 'and', [
        tree.ovalNode.ovalNode(2, 'value', "false"),
        tree.ovalNode.ovalNode(3, 'value', "false"),

        tree.ovalNode.ovalNode(4, 'value', "true"),
        tree.ovalNode.ovalNode(5, 'value', "error"),
        tree.ovalNode.ovalNode(6, 'value', "unknown"),
        tree.ovalNode.ovalNode(7, 'value', "noteval"),
        tree.ovalNode.ovalNode(8, 'value', "notappl")       
    ]
    )

    dictOfTree = {'node_id': 1, 'type': 'operator', 'value': 'and',
                  'child': [
                      {'node_id': 2, 'type': 'value', 'value': "false", 'child': None},
                      {'node_id': 3, 'type': 'value', 'value': "false", 'child': None},
                      
                      {'node_id': 4, 'type': 'value', 'value': "true", 'child': None},
                      {'node_id': 5, 'type': 'value', 'value': "error", 'child': None},
                      {'node_id': 6, 'type': 'value', 'value': "unknown", 'child': None},
                      {'node_id': 7, 'type': 'value', 'value': "noteval", 'child': None},
                      {'node_id': 8, 'type': 'value', 'value': "notappl", 'child': None}
                  ]
                  }

    any_test_treeEvaluation(Tree, "false")
    any_test_renderTree(Tree)
    any_test_treeToDictOfTree(Tree, dictOfTree)
    find_any_node(Tree, 1)
    any_test_dictToTree(dictOfTree)


def test_ANDTreeError():
    Tree = tree.ovalNode.ovalNode(1, 'operator', 'and', [
        tree.ovalNode.ovalNode(2, 'value', "error"),
        tree.ovalNode.ovalNode(3, 'value', "error"),
        
        tree.ovalNode.ovalNode(4, 'value', "true"),
        tree.ovalNode.ovalNode(5, 'value', "unknown"),
        tree.ovalNode.ovalNode(6, 'value', "noteval"),
        tree.ovalNode.ovalNode(7, 'value', "notappl"),           tree.ovalNode.ovalNode(8, 'value', "error")
    ]
    )

    dictOfTree = {'node_id': 1, 'type': 'operator', 'value': 'and',
                  'child': [
                      {'node_id': 2, 'type': 'value', 'value': "error", 'child': None},
                      {'node_id': 3, 'type': 'value', 'value': "error", 'child': None},

                      {'node_id': 4, 'type': 'value', 'value': "true", 'child': None},
                      {'node_id': 5, 'type': 'value', 'value': "unknown", 'child': None},
                      {'node_id': 6, 'type': 'value', 'value': "noteval", 'child': None},
                      {'node_id': 7, 'type': 'value', 'value': "notappl", 'child': None},
                      {'node_id': 8, 'type': 'value', 'value': "error", 'child': None},
                  ]
                  }

    any_test_treeEvaluation(Tree, "error")
    any_test_renderTree(Tree)
    any_test_treeToDictOfTree(Tree, dictOfTree)
    find_any_node(Tree, 1)
    any_test_dictToTree(dictOfTree)


def test_ANDTreeUnknown():
    Tree = tree.ovalNode.ovalNode(1, 'operator', 'and', [
        tree.ovalNode.ovalNode(2, 'value', "unknown"),
        tree.ovalNode.ovalNode(3, 'value', "unknown"),
        
        tree.ovalNode.ovalNode(4, 'value', "true"),
        tree.ovalNode.ovalNode(5, 'value', "unknown"),
        tree.ovalNode.ovalNode(6, 'value', "noteval"),
        tree.ovalNode.ovalNode(7, 'value', "notappl"),           tree.ovalNode.ovalNode(8, 'value', "notappl")
    ]
    )

    dictOfTree = {'node_id': 1, 'type': 'operator', 'value': 'and',
                  'child': [
                      {'node_id': 2, 'type': 'value', 'value': "unknown", 'child': None},
                      {'node_id': 3, 'type': 'value', 'value': "unknown", 'child': None},

                      {'node_id': 4, 'type': 'value', 'value': "true", 'child': None},
                      {'node_id': 5, 'type': 'value', 'value': "unknown", 'child': None},
                      {'node_id': 6, 'type': 'value', 'value': "noteval", 'child': None},
                      {'node_id': 7, 'type': 'value', 'value': "notappl", 'child': None},
                      {'node_id': 8, 'type': 'value', 'value': "notappl", 'child': None},
                  ]
                  }

    any_test_treeEvaluation(Tree, "unknown")
    any_test_renderTree(Tree)
    any_test_treeToDictOfTree(Tree, dictOfTree)
    find_any_node(Tree, 1)
    any_test_dictToTree(dictOfTree)

def test_ANDTreeNoteval():
    Tree = tree.ovalNode.ovalNode(1, 'operator', 'and', [
        tree.ovalNode.ovalNode(2, 'value', "noteval"),
        tree.ovalNode.ovalNode(3, 'value', "noteval"),
        
        tree.ovalNode.ovalNode(4, 'value', "true"),
        tree.ovalNode.ovalNode(5, 'value', "true"),
        tree.ovalNode.ovalNode(6, 'value', "noteval"),
        tree.ovalNode.ovalNode(7, 'value', "notappl"),           tree.ovalNode.ovalNode(8, 'value', "notappl")
    ]
    )

    dictOfTree = {'node_id': 1, 'type': 'operator', 'value': 'and',
                  'child': [
                      {'node_id': 2, 'type': 'value', 'value': "noteval", 'child': None},
                      {'node_id': 3, 'type': 'value', 'value': "noteval", 'child': None},

                      {'node_id': 4, 'type': 'value', 'value': "true", 'child': None},
                      {'node_id': 5, 'type': 'value', 'value': "true", 'child': None},
                      {'node_id': 6, 'type': 'value', 'value': "noteval", 'child': None},
                      {'node_id': 7, 'type': 'value', 'value': "notappl", 'child': None},
                      {'node_id': 8, 'type': 'value', 'value': "notappl", 'child': None},
                  ]
                  }

    any_test_treeEvaluation(Tree, "noteval")
    any_test_renderTree(Tree)
    any_test_treeToDictOfTree(Tree, dictOfTree)
    find_any_node(Tree, 1)
    any_test_dictToTree(dictOfTree)

def test_ANDTreeNotappl():
    Tree = tree.ovalNode.ovalNode(1, 'operator', 'and', [
        tree.ovalNode.ovalNode(2, 'value', "notappl"),
        tree.ovalNode.ovalNode(3, 'value', "notappl"),
         tree.ovalNode.ovalNode(4, 'value', "notappl")
    ]
    )

    dictOfTree = {'node_id': 1, 'type': 'operator', 'value': 'and',
                  'child': [
                      {'node_id': 2, 'type': 'value', 'value': "notappl", 'child': None},
                      {'node_id': 3, 'type': 'value', 'value': "notappl", 'child': None},
                      {'node_id': 4, 'type': 'value', 'value': "notappl", 'child': None}
                  ]
                  }

    any_test_treeEvaluation(Tree, "notappl")
    any_test_renderTree(Tree)
    any_test_treeToDictOfTree(Tree, dictOfTree)
    find_any_node(Tree, 1)
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
    any_test_treeToDictOfTree(Tree, dictOfTree)
    find_any_node(Tree, 5)
    any_test_dictToTree(dictOfTree)

###################################################

def any_test_treeToDictOfTree(tree, dictOfTree):
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
