import tree.operatorTree
import os

def test_tree():
    t = tree.operatorTree.operatorTree("and")
    t1 = tree.operatorTree.operatorTree(True)

    assert str(t) == "and"
    assert t1

def test_bad_tree():
    t = tree.operatorTree.operatorTree(True,[tree.operatorTree.operatorTree("and")])
    assert t.children == []
    assert t.name

def test_treeEvaluationAllFalse():
    """
        and
        /|\
       f f or
          / \
         f   f
    """
    Tree = tree.operatorTree.operatorTree('and', [
                 tree.operatorTree.operatorTree(False),
                 tree.operatorTree.operatorTree(False),
                 tree.operatorTree.operatorTree('or', [
                             tree.operatorTree.operatorTree(False),
                             tree.operatorTree.operatorTree(False)
                            ]
                     )
                ]
        )
    
    dict={'name': 'and',
            'child': [
                {'name': False, 'child': []}, 
                {'name': False, 'child': []}, 
                {'name': 'or', 'child': [
                                {'name': False, 'child': []},
                                {'name': False, 'child': []}
                            ]
                }
            ]
        }

    any_test_treeEvaluation(Tree, False)
    any_test_renderTree(Tree)
    any_test_treeToDict(Tree,dict)



def test_treeEvaluation():
    """
        and
        /|\
       t t or
          / \
         f   t
    """
    Tree = tree.operatorTree.operatorTree('and', [
                 tree.operatorTree.operatorTree(True),
                 tree.operatorTree.operatorTree(False),
                 tree.operatorTree.operatorTree('or', [
                             tree.operatorTree.operatorTree(False),
                             tree.operatorTree.operatorTree(True)
                            ]
                     )
                ]
        )
    
    dict={'name': 'and',
            'child': [
                {'name': True, 'child': []}, 
                {'name': False, 'child': []}, 
                {'name': 'or', 'child': [
                                {'name': False, 'child': []},
                                {'name': True, 'child': []}
                            ]
                }
            ]
        }

    any_test_treeEvaluation(Tree, False)
    any_test_renderTree(Tree)
    any_test_treeToDict(Tree,dict)

def any_test_treeToDict(tree,dict):
    assert tree.treeToDict() == dict

def any_test_renderTree(tree,img =None):
    assert tree.renderTree(img)

def any_test_treeEvaluation(tree,expect):
    assert tree.evaluateTree() == expect

def test_dictToTree():
    tree.operatorTree.dictToTree({"and": [True,True,True,{"or": [True,True,True,False]}]})
    tree.operatorTree.dictToTree({"and": [False]})