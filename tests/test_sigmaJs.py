import tests.any_test_help
import graph.oval_graph
import os
import py
import pytest
import json


def test_create_node_dict_for_sigmaJs_0():
    out = {
        'type': 'circle',
        'borderColor': '#ff0000',
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
        'type': 'circle',
        'borderColor': '#00ff00',
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
    Tree = graph.oval_graph.OvalNode(1, 'operator', 'and', False, [
        graph.oval_graph.OvalNode(2, 'value', "true", False)
    ]
    )

    tests.any_test_help.any_test_create_node_dict_for_sigmaJs(Tree, out)


def test_create_node_dict_for_sigmaJs_2():
    out = {
        'type': 'circle',
        'borderColor': '#000000',
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
    Tree = graph.oval_graph.OvalNode(1, 'operator', 'and', False, [
        graph.oval_graph.OvalNode(2, 'value', "noteval", False)
    ]
    )

    tests.any_test_help.any_test_create_node_dict_for_sigmaJs(Tree, out)


def test_create_node_dict_for_sigmaJs_3():
    out = {
        'type': 'circle',
        'borderColor': '#ff0000',
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
    Tree = graph.oval_graph.OvalNode(1, 'value', 'false', False)

    tests.any_test_help.any_test_create_node_dict_for_sigmaJs(Tree, out)


def test_create_node_dict_for_sigmaJs_4():
    out = {
        'type': 'circle',
        'borderColor': '#00ff00',
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
    Tree = graph.oval_graph.OvalNode(1, 'value', 'true', False)

    tests.any_test_help.any_test_create_node_dict_for_sigmaJs(Tree, out)


def test_create_node_dict_for_sigmaJs_5():
    out = {
        'type': 'circle',
        'borderColor': '#000000',
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
    Tree = graph.oval_graph.OvalNode(1, 'value', 'error', False)

    tests.any_test_help.any_test_create_node_dict_for_sigmaJs(Tree, out)


def test_create_node_with_negation_dict_for_sigmaJs():
    out = {
        'type': 'circle',
        'borderColor': '#ff0000',
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
    Tree = graph.oval_graph.OvalNode(1, 'operator', 'and', True, [
        graph.oval_graph.OvalNode(2, 'value', "false", False)
    ]
    )

    tests.any_test_help.any_test_create_node_dict_for_sigmaJs(Tree, out)


def test_create_node_with_negation_dict_for_sigmaJs1():
    out = {
        'type': 'circle',
        'borderColor': '#00ff00',
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
    Tree = graph.oval_graph.OvalNode(1, 'operator', 'and', True, [
        graph.oval_graph.OvalNode(2, 'value', "true", False)
    ]
    )

    tests.any_test_help.any_test_create_node_dict_for_sigmaJs(Tree, out)


def test_create_node_with_negation_dict_for_sigmaJs2():
    out = {
        'type': 'circle',
        'borderColor': '#00ff00',
        'color': '#ff0000',
        'id': 2,
        'label': '2',
        'size': 3,
        'text': 'null',
        'url': 'null',
        'title': 2,
        'x': 0,
        'y': 0
    }
    Tree = graph.oval_graph.OvalNode(1, 'operator', 'and', False, [
        graph.oval_graph.OvalNode(2, 'value', "true", True)
    ]
    )

    tests.any_test_help.any_test_create_node_dict_for_sigmaJs(
        Tree.children[0], out)


def test_create_node_with_negation_dict_for_sigmaJs3():
    out = {
        'type': 'circle',
        'borderColor': '#ff0000',
        'color': '#00ff00',
        'id': 2,
        'label': '2',
        'size': 3,
        'text': 'null',
        'url': 'null',
        'title': 2,
        'x': 0,
        'y': 0
    }
    Tree = graph.oval_graph.OvalNode(1, 'operator', 'and', False, [
        graph.oval_graph.OvalNode(2, 'value', "false", True)
    ]
    )

    tests.any_test_help.any_test_create_node_dict_for_sigmaJs(
        Tree.children[0], out)


def test_create_edge_dict_for_sigmaJs():
    out = {
        'id': 'random_ID',
        'source': 1,
        'target': 2,
        'color': '#000000'
    }

    target_node = {
        'type': 'circle',
        'borderColor': '#000000',
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


def test_parsing_full_scan_XML_and_evaluate():
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


def test_parsing_and_evaluate_scan_0():
    src = 'test_data/ssg-fedora-ds-arf.xml'
    rule_id = 'xccdf_org.ssgproject.content_rule_audit_rules_file_deletion_events_rmdir'
    result = 'false'

    tests.any_test_help.any_test_parsing_and_evaluate_scan_rule(
        src, rule_id, result)


def test_parsing_and_evaluate_scan_1():
    src = 'test_data/ssg-fedora-ds-arf-scan-with-negated-extend-definitions.xml'
    rule_id = 'xccdf_org.ssgproject.content_rule_install_PAE_kernel_on_x86-32'
    result = 'true'

    tests.any_test_help.any_test_parsing_and_evaluate_scan_rule(
        src, rule_id, result)


def test_parsing_and_evaluate_scan_1():
    src = 'test_data/ssg-fedora-ds-arf.xml'
    rule_id = 'xccdf_org.ssgproject.content_rule_sssd_offline_cred_expiration'
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

    with pytest.raises(Exception, match="err- 404 rule not found!"):
        assert parser.get_def_id_by_rule_id('hello')


def test_get_def_id_by_notselected_rule_id():
    src = 'test_data/ssg-fedora-ds-arf.xml'

    parser = tests.any_test_help.get_parser(src)
    rule_id = 'xccdf_org.ssgproject.content_rule_ntpd_specify_remote_server'

    with pytest.raises(Exception, match="err- rule \"{}\" was not selected, so there are no results.".format(rule_id)):
        assert parser.get_def_id_by_rule_id(rule_id)


def test_str_to_bool():
    src = 'test_data/ssg-fedora-ds-arf.xml'
    parser = tests.any_test_help.get_parser(src)

    assert parser._str_to_bool('true')
    assert not parser._str_to_bool('false')
    with pytest.raises(Exception, match="err- negation is not bool"):
        assert parser._str_to_bool('error')


def test_use_bat_report_file():
    src = ('test_data/xccdf_org.ssgproject.content_rule_sssd_' +
           'ssh_known_hosts_timeout-comment.fail.sh-xccdf_or' +
           'g.ssgproject.content_profile_ospp-results-initial.xml')

    with pytest.raises(Exception, match="err- This is not arf report file."):
        assert tests.any_test_help.get_parser(src)


def test_get_rule_dict():
    src = 'test_data/ssg-fedora-ds-arf.xml'
    _dir = os.path.dirname(os.path.realpath(__file__))
    FIXTURE_DIR = py.path.local(_dir) / src
    parser = graph.xml_parser.xml_parser(str(FIXTURE_DIR))
    dict = parser.get_rule_dict(
        'xccdf_org.ssgproject.content_rule_dconf_gnome_session_idle_user_locks')
    src = 'test_data/rule_dict.json'
    _dir = os.path.dirname(os.path.realpath(__file__))
    FIXTURE_DIR = py.path.local(_dir) / src
    with open(str(FIXTURE_DIR), 'r') as f:
        data = json.load(f)
    assert data == dict
