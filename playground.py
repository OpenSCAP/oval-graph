import operator

def evaluateTree(tree):
    operator, tests = list(tree.items())[0]
    operators = {
        u"or": any,
        u"and": all,
    }
    evaluator = operators[operator]
    return evaluator(evaluateTree(i) if type(i) is dict else i for i in tests)

print(evaluateTree({"and": [True,True,True,{"or": [True,True,True,False]}]}))

######################################################################################
class Tree(object):
    def __init__(self, name='root', children=None):
        self.name = name
        self.children = []
        if children is not None:
            for child in children:
                self.add_child(child)
    
    def __repr__(self):
        return self.name

    def add_child(self, node):
        if self.name == "or" or self.name=="and":
            assert isinstance(node, Tree)
            self.children.append(node)
        else:
            print("err- True or False have not child!")
    def evaluateTree(self):
        operator = self.name
        tests = self.children
        operators = {
            u"or": any,
            u"and": all,
        }
        evaluator = operators[operator]
        return evaluator(i.evaluateTree() if type(i.name) is not bool else i.name for i in tests)

#   and
#   /|\
#  t t or
#     / \
#    f   t

t = Tree('and', [
                 Tree(True),
                 Tree(False),
                 Tree('or', [
                             Tree(False),
                             Tree(True)
                            ]
                     )
                ]
        )
print(t.evaluateTree())

print("Dict To img")

import pydot

menu = {'dinner':
            {'chicken':'good',
             'beef':'average',
             'vegetarian':{
                   'tofu':'good',
                   'salad':{
                            'caeser':'bad',
                            'italian':'average'}
                   },
             'pork':'bad'}
        }

menu={'and':{
            'True': [], 
            'False': [], 
            'or': {
                'False1': [],
                'True1': []
            }
            }
            }
    

def draw(parent_name, child_name):
    edge = pydot.Edge(parent_name, child_name)
    graph.add_edge(edge)

def visit(node, parent=None):
    for k,v in node.items():
        print(k,v)
        if isinstance(v, dict):
            # We start with the root node whose parent is None
            # we don't want to graph the None node
            if parent:
                draw(parent, k)
            visit(v, k)
        else:
            draw(parent, k)
            # drawing the label using a distinct name
            #draw(k, k+'_'+str(v))

graph = pydot.Dot(graph_type='graph')
visit(menu)
graph.write_png('./example1_graph.png')



import sys
import networkx as nx
import matplotlib.pyplot as plt

G = nx.Graph()
G.add_node('A')
G.add_node('B')
G.add_node('C')
G.add_node('D')
G.add_edge('A','B',weight=1)
G.add_edge('C','B',weight=1)
G.add_edge('B','D',weight=30)

limits=plt.axis('off') 
colors=range(20)
nx.draw_spring(G, nodelist=sorted(G.nodes()), font_size=16, width=2,
               node_size=[1000, 1000, 2000, 3000],
               node_color=["#A0CBE2", "#A0CBE2", "#FF0000", "#FFFF00"],with_labels=True)
plt.savefig("./test.png",dpi=300)