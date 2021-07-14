from pathlib import Path

import pytest

from oval_graph.arf_xml_parser.arf_xml_parser import ARFXMLParser


def get_arf_report_path(src="global_test_data/ssg-fedora-ds-arf.xml"):
    return str(Path(__file__).parent.parent / src)


@pytest.mark.parametrize("rule_id, result", [
    (
        "xccdf_org.ssgproject.content_rule_accounts_passwords_pam_faillock_deny",
        "false",
    ),
    (
        "xccdf_org.ssgproject.content_rule_sshd_disable_gssapi_auth",
        "false",
    ),
    (
        "xccdf_org.ssgproject.content_rule_service_debug-shell_disabled",
        "true",
    ),
    (
        "xccdf_org.ssgproject.content_rule_mount_option_dev_shm_noexec",
        "false",
    ),
    (
        "xccdf_org.ssgproject.content_rule_audit_rules_unsuccessful_file_modification_creat",
        "false",
    ),
    (
        "xccdf_org.ssgproject.content_rule_audit_rules_file_deletion_events_rmdir",
        "false",
    ),
    (
        "xccdf_org.ssgproject.content_rule_require_singleuser_auth",
        "true",
    ),
])
def test_parsing_and_evaluate_scan_rule(rule_id, result):
    path = get_arf_report_path()

    parser = ARFXMLParser(path)
    oval_tree = parser.get_oval_tree(rule_id)
    assert oval_tree.evaluate_tree() == result


@pytest.mark.parametrize("rule_id, pattern", [
    ("hello", "404 rule \"hello\" not found!"),
    ("xccdf_org.ssgproject.content_rule_ntpd_specify_remote_server", "notselected"),
    ("xccdf_org.ssgproject.content_rule_configure_bind_crypto_policy", "notchecked"),
    ("xccdf_org.ssgproject.content_rule_ensure_gpgcheck_local_packages", "notapplicable"),
])
def test_parsing_bad_rule(rule_id, pattern):
    path = get_arf_report_path()
    parser = ARFXMLParser(path)

    with pytest.raises(Exception, match=pattern):
        assert parser.get_oval_tree(rule_id)


def test_use_bad_report_file():
    src = 'global_test_data/xccdf_org.ssgproject.content_profile_ospp-results-initial.xml'
    path = get_arf_report_path(src)
    with pytest.raises(Exception, match=r"arf\b|ARF\b"):
        assert ARFXMLParser(path)
