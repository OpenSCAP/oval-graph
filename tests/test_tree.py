import tree.ovalNode
import os
import pytest

def test_bad_tree():
    with pytest.raises(ValueError) as e:
        bad_tree()
    assert str(e.value) == 'err- true, false, error, unknown. noteval, notappl have not child!' 

    with pytest.raises(ValueError) as e:
        treeOnlyAnd()
    assert str(e.value) == 'err- OR, XOR, ONE, AND have child!' 

    with pytest.raises(ValueError) as e:
        treeOnlyOr()
    assert str(e.value) == 'err- OR, XOR, ONE, AND have child!' 

#degenered trees 
def bad_tree():
    """
         t
         |
        and
         |
         t
    """
    t = tree.ovalNode.ovalNode(1,"true",[tree.ovalNode.ovalNode(2,"and",[tree.ovalNode.ovalNode(3,"true")])])
    
def treeOnlyOr():
    """
        or
    """
    Tree = tree.ovalNode.ovalNode(1,'or')

def treeOnlyAnd():
    """
        and
    """
    Tree = tree.ovalNode.ovalNode(1,'and')

#normal trees
def test_treeAndFalse():
    """
        and
         |
         f
    """
    Tree = tree.ovalNode.ovalNode(1,'and', [
                 tree.ovalNode.ovalNode(2,"false")
                ]
        )
    
    dictOfTree={'node_id': 1,'value': 'and',
            'child': [
                {'node_id': 2,'value': "false", 'child': None }
            ]
        }

    any_test_treeEvaluation(Tree, "false")
    any_test_renderTree(Tree)
    any_test_treeTodictOfTree(Tree,dictOfTree)
    find_any_node(Tree,1)

def test_treeAllFalse():
    """
        and
        /|\
       f f or
          / \
         f   f
    """
    Tree = tree.ovalNode.ovalNode(1,'and', [
                 tree.ovalNode.ovalNode(2,"false"),
                 tree.ovalNode.ovalNode(3,"false"),
                 tree.ovalNode.ovalNode(4,'or', [
                             tree.ovalNode.ovalNode(5,"false"),
                             tree.ovalNode.ovalNode(6,"false")
                            ]
                     )
                ]
        )
    
    dictOfTree={'node_id': 1,'value': 'and',
            'child': [
                {'node_id': 2,'value': "false", 'child': None}, 
                {'node_id': 3,'value': "false", 'child': None}, 
                {'node_id': 4,'value': 'or', 'child': [
                                {'node_id': 5,'value': "false", 'child': None},
                                {'node_id': 6,'value': "false", 'child': None}
                            ]
                }
            ]
        }

    any_test_treeEvaluation(Tree, "false")
    any_test_renderTree(Tree)
    any_test_treeTodictOfTree(Tree,dictOfTree)
    find_any_node(Tree,5)

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
    Tree = tree.ovalNode.ovalNode(1,'and', [
                 tree.ovalNode.ovalNode(2,"error"),
                 tree.ovalNode.ovalNode(3,"xor",[tree.ovalNode.ovalNode(4,'error'),                                                   tree.ovalNode.ovalNode(5,'one',[
                                                    tree.ovalNode.ovalNode(6,'error'),
                                                    tree.ovalNode.ovalNode(7,'error'),
                                                    tree.ovalNode.ovalNode(8,'error')]),
                                                 tree.ovalNode.ovalNode(9,'error')]),
                 tree.ovalNode.ovalNode(10,'or', [
                             tree.ovalNode.ovalNode(11,"error"),
                             tree.ovalNode.ovalNode(12,"error")
                            ]
                     )
                ]
        )
    
    dictOfTree={'node_id': 1,'value': 'and',
            'child': [
                {'node_id': 2,'value': "error", 'child': None}, 
                {'node_id': 3,'value': "xor", 'child': [
                        {'node_id': 4,'value': "error", 'child': None},
                        {'node_id': 5,'value': "one", 'child': [
                                {'node_id': 6,'value': "error", 'child': None},
                                {'node_id': 7,'value': "error", 'child': None},
                                {'node_id': 8,'value': "error", 'child': None}
                                ]},
                        {'node_id': 9,'value': "error", 'child': None}]}, 
                {'node_id': 10,'value': 'or', 'child': [
                                {'node_id': 11,'value': "error", 'child': None},
                                {'node_id': 12,'value': "error", 'child': None}
                            ]
                }
            ]
        }

    any_test_treeEvaluation(Tree, "error")
    any_test_renderTree(Tree)
    any_test_treeTodictOfTree(Tree,dictOfTree)
    find_any_node(Tree,5)

def test_UltimateTree():
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
    Tree = tree.ovalNode.ovalNode(1,'and', [
                 tree.ovalNode.ovalNode(2,"false"),
                 tree.ovalNode.ovalNode(3,"xor",[tree.ovalNode.ovalNode(4,'true'),                                                   tree.ovalNode.ovalNode(5,'one',[
                                                    tree.ovalNode.ovalNode(6,'noteval'),
                                                    tree.ovalNode.ovalNode(7,'true'),
                                                    tree.ovalNode.ovalNode(8,'notappl')]),
                                                 tree.ovalNode.ovalNode(9,'error')]),
                 tree.ovalNode.ovalNode(10,'or', [
                             tree.ovalNode.ovalNode(11,"unknown"),
                             tree.ovalNode.ovalNode(12,"true")
                            ]
                     )
                ]
        )
    
    dictOfTree={'node_id': 1,'value': 'and',
            'child': [
                {'node_id': 2,'value': "false", 'child': None}, 
                {'node_id': 3,'value': "xor", 'child': [
                        {'node_id': 4,'value': "true", 'child': None},
                        {'node_id': 5,'value': "one", 'child': [
                                {'node_id': 6,'value': "noteval", 'child': None},
                                {'node_id': 7,'value': "true", 'child': None},
                                {'node_id': 8,'value': "notappl", 'child': None}
                                ]},
                        {'node_id': 9,'value': "error", 'child': None}]}, 
                {'node_id': 10,'value': 'or', 'child': [
                                {'node_id': 11,'value': "unknown", 'child': None},
                                {'node_id': 12,'value': "true", 'child': None}
                            ]
                }
            ]
        }

    any_test_treeEvaluation(Tree, "false")
    any_test_renderTree(Tree)
    any_test_treeTodictOfTree(Tree,dictOfTree)
    find_any_node(Tree,5)

def test_treenode_ideal():
    """
        and
        /|\
       t t or
          / \
         f   t
    """
    Tree = tree.ovalNode.ovalNode(1,'and', [
                 tree.ovalNode.ovalNode(2,"true"),
                 tree.ovalNode.ovalNode(3,"false"),
                 tree.ovalNode.ovalNode(4,'or', [
                             tree.ovalNode.ovalNode(5,"false"),
                             tree.ovalNode.ovalNode(6,"true")
                            ]
                     )
                ]
        )
    
    dictOfTree={'node_id': 1,'value': 'and',
            'child': [
                {'node_id': 2,'value': "true", 'child': None}, 
                {'node_id': 3,'value': "false", 'child': None}, 
                {'node_id': 4,'value': 'or', 'child': [
                                {'node_id': 5,'value': "false", 'child': None},
                                {'node_id': 6,'value': "true", 'child': None}
                            ]
                }
            ]
        }

    any_test_treeEvaluation(Tree, "false")
    any_test_renderTree(Tree)
    any_test_treeTodictOfTree(Tree,dictOfTree)
    find_any_node(Tree,6)
###################################################

def any_test_treeTodictOfTree(tree,dictOfTree):
    assert tree.treeToDict() == dictOfTree

def find_any_node(Tree,node_id):
    findTree=tree.ovalNode.findNodeWithID(Tree, node_id)
    assert  findTree.node_id == node_id

def any_test_renderTree(tree,img =None):
    assert tree.renderTree(img)

def any_test_treeEvaluation(tree,expect):
    assert tree.evaluateTree() == expect

def test_dictToTree():
    """
        and
        /|\
       t t or
          / \
         f   t
    """
    Tree = tree.ovalNode.ovalNode(1,'and', [
                 tree.ovalNode.ovalNode(2,"true"),
                 tree.ovalNode.ovalNode(3,"false"),
                 tree.ovalNode.ovalNode(4,'or', [
                             tree.ovalNode.ovalNode(5,"false"),
                             tree.ovalNode.ovalNode(6,"true")
                            ]
                     )
                ]
        )

    dictOfTree={'node_id': 1,'value': 'and',
            'child': [
                {'node_id': 2,'value': "true", 'child': None}, 
                {'node_id': 3,'value': "false", 'child': None}, 
                {'node_id': 4,'value': 'or', 'child': [
                                {'node_id': 5,'value': "false", 'child': None},
                                {'node_id': 6,'value': "true", 'child': None}
                            ]
                }
            ]
        }

    treedictOfTree = tree.ovalNode.dictToTree(dictOfTree)
    #Je to ok?
    assert treedictOfTree.treeToDict() == dictOfTree

def test_treeRepr():
    """
        and
         |
         f
    """
    Tree = tree.ovalNode.ovalNode(1,'and', [
                 tree.ovalNode.ovalNode(2,"false")
                ]
        )
    assert str(Tree) == "and"


def test_addToTree():
    """
        and
         |
         f
    """

    dictOfTree={'node_id': 1,'value': 'and',
            'child': [
                {'node_id': 2,'value': "false", 'child': None}, 
                {'node_id': 3,'value': "true", 'child': None}, 
            ]
        }

    Tree = tree.ovalNode.ovalNode(1,'and', [
                 tree.ovalNode.ovalNode(2,"false")
                ]
        )
    Tree1=tree.ovalNode.ovalNode(3,"true")
    tree.ovalNode.addToTree(Tree,1,Tree1)
    assert Tree.treeToDict()==dictOfTree    

def test_ChangeValueTree():
    """
        and
        /|\
       t t or
          / \
         f   t
    """
    Tree = tree.ovalNode.ovalNode(1,'and', [
                 tree.ovalNode.ovalNode(2,"true"),
                 tree.ovalNode.ovalNode(3,"false"),
                 tree.ovalNode.ovalNode(4,'or', [
                             tree.ovalNode.ovalNode(5,"false"),
                             tree.ovalNode.ovalNode(6,"true")
                            ]
                     )
                ]
        )
    
    tree.ovalNode.ChangeTreeValue(Tree,3,"true")
    any_test_treeEvaluation(Tree, "true")
