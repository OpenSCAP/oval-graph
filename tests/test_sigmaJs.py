import tests.any_test_help
import graph.oval_graph
import os
import py
import pytest


def test_create_node_dict_for_sigmaJs_0():
    out = {
        'color': '#ff0000',
        'id': 1,
        'label': 'and',
        'size': 3,
        'text': 'null',
        'url': 'null',
        'title': 1,
        'x': 0,
        'y': 0
    }
    Tree = tests.any_test_help.get_simple_tree()
    tests.any_test_help.any_test_create_node_dict_for_sigmaJs(Tree, out)


def test_create_node_dict_for_sigmaJs_1():
    out = {
        'color': '#00ff00',
        'id': 1,
        'label': 'and',
        'size': 3,
        'text': 'null',
        'url': 'null',
        'title': 1,
        'x': 0,
        'y': 0
    }
    Tree = graph.oval_graph.OvalNode(1, 'operator', 'and', [
        graph.oval_graph.OvalNode(2, 'value', "true")
    ]
    )

    tests.any_test_help.any_test_create_node_dict_for_sigmaJs(Tree, out)


def test_create_node_dict_for_sigmaJs_2():
    out = {
        'color': '#000000',
        'id': 1,
        'label': 'and',
        'size': 3,
        'text': 'null',
        'url': 'null',
        'title': '1 and',
        'x': 0,
        'y': 0
    }
    Tree = graph.oval_graph.OvalNode(1, 'operator', 'and', [
        graph.oval_graph.OvalNode(2, 'value', "noteval")
    ]
    )

    tests.any_test_help.any_test_create_node_dict_for_sigmaJs(Tree, out)


def test_create_node_dict_for_sigmaJs_3():
    out = {
        'color': '#ff0000',
        'id': 1,
        'label': '1',
        'size': 3,
        'text': 'null',
        'url': 'null',
        'title': 1,
        'x': 0,
        'y': 0
    }
    Tree = graph.oval_graph.OvalNode(1, 'value', 'false')

    tests.any_test_help.any_test_create_node_dict_for_sigmaJs(Tree, out)


def test_create_node_dict_for_sigmaJs_4():
    out = {
        'color': '#00ff00',
        'id': 1,
        'label': '1',
        'size': 3,
        'text': 'null',
        'url': 'null',
        'title': 1,
        'x': 0,
        'y': 0
    }
    Tree = graph.oval_graph.OvalNode(1, 'value', 'true')

    tests.any_test_help.any_test_create_node_dict_for_sigmaJs(Tree, out)


def test_create_node_dict_for_sigmaJs_5():
    out = {
        'color': '#000000',
        'id': 1,
        'label': '1',
        'size': 3,
        'text': 'null',
        'url': 'null',
        'title': '1 error',
        'x': 0,
        'y': 0
    }
    Tree = graph.oval_graph.OvalNode(1, 'value', 'error')

    tests.any_test_help.any_test_create_node_dict_for_sigmaJs(Tree, out)


def test_create_edge_dict_for_sigmaJs():
    out = {
        'id': 'random_ID',
        'source': 1,
        'target': 2,
        'color': '#000000'
    }

    target_node = {
        'color': '#000000',
        'id': 2,
        'label': 'error',
        'size': 3,
        'text': 'null',
        'url': 'null',
        'title': '1 error',
        'x': 0,
        'y': 0
    }

    assert tests.any_test_help.get_simple_tree()._create_edge(
        1, 2, target_node)['source'] == out['source']
    assert tests.any_test_help.get_simple_tree()._create_edge(
        1, 2, target_node)['target'] == out['target']
    assert tests.any_test_help.get_simple_tree()._create_edge(
        1, 2, target_node)['color'] == out['color']


def test_create_array_of_ids_form_tree():
    array = tests.any_test_help.get_simple_tree().create_list_of_id()
    assert array == [1, 2, 3, 4, 5, 6]


def test_parsing_full_can_XML_and_evaluate():
    src = 'test_data/ssg-fedora-ds-arf.xml'
    rule_id = 'xccdf_org.ssgproject.content_rule_accounts_passwords_pam_faillock_deny'
    result = 'false'

    tests.any_test_help.any_test_parsing_and_evaluate_scan_rule(
        src, rule_id, result)


def test_parsing_and_evaluate_scan_with_extend_def():
    src = 'test_data/ssg-fedora-ds-arf-scan-with-extend-definitions.xml'
    rule_id = 'xccdf_org.ssgproject.content_rule_sysctl_net_ipv6_conf_all_disable_ipv6'
    result = 'false'

    tests.any_test_help.any_test_parsing_and_evaluate_scan_rule(
        src, rule_id, result)


def test_parsing_and_evaluate_scan_with_pasing_rule():
    src = 'test_data/ssg-fedora-ds-arf-passing-scan.xml'
    rule_id = 'xccdf_org.ssgproject.content_rule_service_debug-shell_disabled'
    result = 'true'

    tests.any_test_help.any_test_parsing_and_evaluate_scan_rule(
        src, rule_id, result)


def test_parsing_and_evaluate_scan_with_fail_rule():
    src = 'test_data/ssg-fedora-ds-arf-scan-fail.xml'
    rule_id = 'xccdf_org.ssgproject.content_rule_mount_option_dev_shm_noexec'
    result = 'false'

    tests.any_test_help.any_test_parsing_and_evaluate_scan_rule(
        src, rule_id, result)


def test_parsing_and_evaluate_scan_with_rule_with_XOR():
    src = 'test_data/ssg-fedora-ds-arf-scan-with-xor.xml'
    rule_id = 'xccdf_org.ssgproject.content_rule_mount_option_nosuid_removable_partitions'
    result = 'true'

    tests.any_test_help.any_test_parsing_and_evaluate_scan_rule(
        src, rule_id, result)


def test_parsing_and_evaluate_scan_with_11_rules():
    src = 'test_data/ssg-fedora-ds-arf-scan-with-11-rules.xml'
    rule_id = 'xccdf_org.ssgproject.content_rule_mount_option_tmp_nosuid'
    result = 'true'

    tests.any_test_help.any_test_parsing_and_evaluate_scan_rule(
        src, rule_id, result)


def test_transformation_tree_to_Json_for_SigmaJs_0():
    test_data_src = 'test_data/sigmaJs_json0.json'
    src = 'data/ssg-fedora-ds-arf.xml'
    rule_id = 'xccdf_org.ssgproject.content_rule_accounts_passwords_pam_faillock_deny'

    tests.any_test_help.any_test_transformation_tree_to_Json_for_SigmaJs(
        src, test_data_src, rule_id)


def test_transformation_tree_to_Json_for_SigmaJs_with_duplicated_test():
    test_data_src = 'test_data/sigmaJs_json1.json'
    src = 'data/ssg-fedora-ds-arf.xml'
    rule_id = 'xccdf_org.ssgproject.content_rule_disable_host_auth'

    tests.any_test_help.any_test_transformation_tree_to_Json_for_SigmaJs(
        src, test_data_src, rule_id)


def test_get_def_id_by_rule_id():
    src = 'test_data/ssg-fedora-ds-arf.xml'
    _dir = os.path.dirname(os.path.realpath(__file__))
    FIXTURE_DIR = py.path.local(_dir) / src

    parser = graph.xml_parser.xml_parser(str(FIXTURE_DIR))

    with pytest.raises(ValueError) as e:
        parser.get_def_id_by_rule_id('hello')
    assert str(
        e.value) == 'err- 404 rule not found!'
