import json
import os

import pytest

from oval_graph.arf_xml_parser.arf_xml_parser import ARFXMLParser
from oval_graph.oval_tree.converter import Converter
from oval_graph.oval_tree.oval_node import OvalNode


def get_test_data_json(src):
    top_patch = os.path.dirname(os.path.realpath(__file__))
    patch = os.path.join(top_patch, src)
    with open(patch, 'r') as file_:
        return json.load(file_)


def get_simple_tree():
    return OvalNode(
        node_id=1,
        node_type='operator',
        value='and',
        children=[
            OvalNode(
                node_id=2,
                node_type='value',
                value='true',
            ),
            OvalNode(
                node_id=3,
                node_type='value',
                value='false',
            ),
            OvalNode(
                node_id=4,
                node_type='operator',
                value='or',
                children=[
                    OvalNode(
                        node_id=5,
                        node_type='value',
                        value='false',
                    ),
                    OvalNode(
                        node_id=6,
                        node_type='value',
                        value="true",
                    ),
                ]
            )
        ]
    )


def get_tree_true():
    return OvalNode(
        node_id=1,
        node_type='operator',
        value='and',
        children=[
            OvalNode(
                node_id=2,
                node_type='value',
                value='true',
            )
        ]
    )


def get_tree_noteval():
    return OvalNode(
        node_id=1,
        node_type='operator',
        value='and',
        children=[
            OvalNode(
                node_id=2,
                node_type='value',
                value='noteval',
            )
        ]
    )


def get_tree_false_one_node():
    return OvalNode(
        node_id=1,
        node_type='value',
        value='false',
    )


def get_tree_true_one_node():
    return OvalNode(
        node_id=1,
        node_type='value',
        value='true',
    )


def get_tree_error_one_node():
    return OvalNode(
        node_id=1,
        node_type='value',
        value='error',
    )


def get_negated_operator_node_false():
    return OvalNode(
        node_id=1,
        node_type='operator',
        value='and',
        negation=True,
        children=[
            OvalNode(
                node_id=2,
                node_type='value',
                value='false',
            )
        ]
    )


def get_negated_operator_node_true():
    return OvalNode(
        node_id=1,
        node_type='operator',
        value='and',
        negation=True,
        children=[
            OvalNode(
                node_id=2,
                node_type='value',
                value='true',
            )
        ]
    )


def get_negated_value_node_true():
    return OvalNode(
        node_id=2,
        node_type='value',
        value='true',
        negation=True,
    )


def get_negated_value_node_false():
    return OvalNode(
        node_id=2,
        node_type='value',
        value='false',
        negation=True,
    )


@pytest.mark.parametrize("tree_getter, json_src", [
    (get_simple_tree, 'test_data/test_JsTree_data/JsTree_data_0.json'),
    (get_tree_true, 'test_data/test_JsTree_data/JsTree_data_1.json'),
    (get_tree_noteval, 'test_data/test_JsTree_data/JsTree_data_2.json'),
    (get_tree_false_one_node, 'test_data/test_JsTree_data/JsTree_data_3.json'),
    (get_tree_true_one_node, 'test_data/test_JsTree_data/JsTree_data_4.json'),
    (get_tree_error_one_node, 'test_data/test_JsTree_data/JsTree_data_5.json'),
    (get_negated_operator_node_false, 'test_data/test_JsTree_data/JsTree_data_negated_0.json'),
    (get_negated_operator_node_true, 'test_data/test_JsTree_data/JsTree_data_negated_1.json'),
    (get_negated_value_node_true, 'test_data/test_JsTree_data/JsTree_data_negated_2.json'),
    (get_negated_value_node_false, 'test_data/test_JsTree_data/JsTree_data_negated_3.json'),
])
def test_create_node_dict_for_js_tree(tree_getter, json_src):
    data = get_test_data_json(json_src)
    oval_tree = tree_getter()
    assert Converter(oval_tree).to_js_tree_dict() == data


@pytest.mark.parametrize("src, test_data_src, rule_id", [
    (
        '../global_test_data/ssg-fedora-ds-arf.xml',
        'test_data/JsTree_json1.json',
        'xccdf_org.ssgproject.content_rule_disable_host_auth',
    ),
    (
        '../global_test_data/ssg-fedora-ds-arf.xml',
        'test_data/JsTree_json0.json',
        'xccdf_org.ssgproject.content_rule_accounts_passwords_pam_faillock_deny',
    ),
])
def test_transformation_xml_rule_to_json_for_js_tree(
        src, test_data_src, rule_id):
    test_data = get_test_data_json(test_data_src)

    top_patch = os.path.dirname(os.path.realpath(__file__))
    patch_to_xml = os.path.join(top_patch, src)

    parser = ARFXMLParser(patch_to_xml)
    oval_tree = parser.get_oval_tree(rule_id)

    assert oval_tree.node_id == rule_id
    out_data = Converter(oval_tree).to_js_tree_dict()
    assert out_data == test_data
