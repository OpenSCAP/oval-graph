from pathlib import Path

import pytest

from oval_graph.arf_xml_parser.arf_xml_parser import ARFXMLParser
from oval_graph.oval_tree.converter import Converter

from .get_tree import GetTree


@pytest.mark.parametrize("tree_getter, json_src", [
    (GetTree.simple_tree, 'test_data/test_JsTree_data/JsTree_data_0.json'),
    (GetTree.tree_true, 'test_data/test_JsTree_data/JsTree_data_1.json'),
    (GetTree.tree_noteval, 'test_data/test_JsTree_data/JsTree_data_2.json'),
    (GetTree.tree_false_one_node, 'test_data/test_JsTree_data/JsTree_data_3.json'),
    (GetTree.tree_true_one_node, 'test_data/test_JsTree_data/JsTree_data_4.json'),
    (GetTree.tree_error_one_node, 'test_data/test_JsTree_data/JsTree_data_5.json'),
    (GetTree.negated_operator_node_false, 'test_data/test_JsTree_data/JsTree_data_negated_0.json'),
    (GetTree.negated_operator_node_true, 'test_data/test_JsTree_data/JsTree_data_negated_1.json'),
    (GetTree.negated_value_node_true, 'test_data/test_JsTree_data/JsTree_data_negated_2.json'),
    (GetTree.negated_value_node_false, 'test_data/test_JsTree_data/JsTree_data_negated_3.json'),
])
def test_create_node_dict_for_js_tree(tree_getter, json_src):
    data = GetTree.json_of_tree(json_src)
    oval_tree = tree_getter()
    assert Converter(oval_tree).to_js_tree_dict() == data


@pytest.mark.parametrize("src, test_data_src, rule_id", [
    (
        'global_test_data/ssg-fedora-ds-arf.xml',
        'test_data/JsTree_json1.json',
        'xccdf_org.ssgproject.content_rule_disable_host_auth',
    ),
    (
        'global_test_data/ssg-fedora-ds-arf.xml',
        'test_data/JsTree_json0.json',
        'xccdf_org.ssgproject.content_rule_accounts_passwords_pam_faillock_deny',
    ),
])
def test_transformation_xml_rule_to_json_for_js_tree(
        src, test_data_src, rule_id):
    test_data = GetTree.json_of_tree(test_data_src)

    patch_to_xml = str(Path(__file__).parent.parent / src)

    parser = ARFXMLParser(patch_to_xml)
    oval_tree = parser.get_oval_tree(rule_id)

    assert oval_tree.node_id == rule_id
    out_data = Converter(oval_tree).to_js_tree_dict()
    assert out_data == test_data
