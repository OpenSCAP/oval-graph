import graph.oval_graph

tree = graph.oval_graph.OvalNode(1,'operator','and',False,[
    graph.oval_graph.OvalNode(2,'value','false',False),
    graph.oval_graph.OvalNode(3,'value','true',False)])


print(tree.evaluate_tree())
print(graph.oval_graph.restore_dict_to_tree(tree.save_tree_to_dict()).evaluate_tree())