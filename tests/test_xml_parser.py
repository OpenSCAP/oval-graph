import tests.any_test_help
import oval_graph.oval_graph
import os
import py
import pytest
import json


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


def test_get_def_id_by_rule_id():
    src = 'test_data/ssg-fedora-ds-arf.xml'
    parser = oval_graph.xml_parser.xml_parser(tests.any_test_help.get_src(src))

    with pytest.raises(Exception, match="err- 404 rule not found!"):
        assert parser.get_def_id_by_rule_id('hello')


def test_get_def_id_by_notselected_rule_id():
    src = 'test_data/ssg-fedora-ds-arf.xml'

    parser = tests.any_test_help.get_parser(src)
    rule_id = 'xccdf_org.ssgproject.content_rule_ntpd_specify_remote_server'

    with pytest.raises(Exception, match="not selected"):
        assert parser.get_def_id_by_rule_id(rule_id)


def test_str_to_bool():
    src = 'test_data/ssg-fedora-ds-arf.xml'
    parser = tests.any_test_help.get_parser(src)

    assert parser._str_to_bool('true')
    assert not parser._str_to_bool('false')
    with pytest.raises(Exception, match="err- negation is not bool"):
        assert parser._str_to_bool('error')


def test_use_bat_report_file():
    src = (
        'test_data/xccdf_org.ssgproject.'
        'content_rule_sssd_ssh_known_hosts_timeout-comment.'
        'fail.sh-xccdf_org.ssgproject.content_profile_ospp-results-initial.xml')

    with pytest.raises(Exception, match=r"arf\b|ARF\b"):
        assert tests.any_test_help.get_parser(src)


def test_get_rule_dict():
    src = 'test_data/ssg-fedora-ds-arf.xml'
    parser = oval_graph.xml_parser.xml_parser(tests.any_test_help.get_src(src))
    rule_dict = parser.get_rule_dict(
        'xccdf_org.ssgproject.content_rule_dconf_gnome_session_idle_user_locks')
    src = 'test_data/rule_dict.json'
    with open(tests.any_test_help.get_src(src), 'r') as f:
        data = json.load(f)
    assert data == rule_dict
