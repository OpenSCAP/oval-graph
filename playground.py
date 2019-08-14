"""
Playgrounds are scripts where i testing and preparing new things and  new futures.

negation
"""

import graph.oval_graph
import graph.xml_parser
import json

tree = graph.oval_graph.OvalNode(1, 'operator', 'and', False, [
    graph.oval_graph.OvalNode(2, 'value', 'false', False),
    graph.oval_graph.OvalNode(3, 'value', 'true', False)])


print(tree.evaluate_tree())
print(graph.oval_graph.restore_dict_to_tree(
    tree.save_tree_to_dict()).evaluate_tree())
parser = graph.xml_parser.xml_parser('./data/ssg-fedora-ds-arf.xml')
dict = parser.get_rule_dict(
    'xccdf_org.ssgproject.content_rule_dconf_gnome_session_idle_user_locks')


oval_tree = graph.oval_graph.build_nodes_form_xml(
    './data/ssg-fedora-ds-arf.xml',
    'xccdf_org.ssgproject.content_rule_dconf_gnome_session_idle_user_locks')
with open('./data.json', "w+") as file:
    file.write(
        str(json.dumps(oval_tree.save_tree_to_dict(), sort_keys=False, indent=4)))
    file.write('\n\n')
    file.write(
        str(json.dumps(dict, sort_keys=False, indent=4)))
