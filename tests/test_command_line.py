import os
import tempfile
import glob
import pexpect
import uuid
import re
from readchar import key


import tests.any_test_help

tmp = tempfile.gettempdir()


def create_env_with_installed_lxml():
    exit_status = os.system(
        'virtualenv -p python3 ' +
        tmp +
        '/testEnvironmentLxml')
    assert exit_status == 0
    exit_status = os.system(tmp + '/testEnvironmentLxml/bin/pip3 install lxml')
    assert exit_status == 0


def test_prepare_envs():
    create_env_with_installed_lxml()


def test_entrypoint_help():
    exit_status = os.system(
        'python3 -m oval_graph.command_line -h')
    assert exit_status == 0


def test_entrypoint_run():
    out = os.popen(
        ('python3 -m oval_graph.command_line --off-web-browser'
         ' tests/test_data/ssg-fedora-ds-arf.xml xccdf_org.ssgproject.'
         'content_rule_package_abrt_removed')).read()
    result = tests.any_test_help.any_get_tested_file(
        os.path.join(tmp, out.split("\n")[-2], 'data.js'))
    referenc_result = tests.any_test_help.any_get_tested_file(
        'test_data/referenc_result_data_tree.js')
    assert result == referenc_result


def test_entrypoint_run_choice_rule():
    random_dir = str(uuid.uuid4())
    src = os.path.join(tmp, random_dir)
    sut = pexpect.spawn(
        r'python3 -m oval_graph.command_line --out ' +
        src +
        r' --off-web-browser tests/test_data/ssg-fedora-ds-arf.xml "_package_\w+_removed"')
    sut.expect(r'\w+', timeout=1)
    sut.send(key.SPACE)
    sut.send(key.ENTER)
    sut.expect(
        r'graph-of-xccdf_org.ssgproject.content_rule_package_abrt_removed_\w+')
    for name in os.listdir(src):
        result = tests.any_test_help.any_get_tested_file(
            os.path.join(src, name, 'data.js'))
        referenc_result = tests.any_test_help.any_get_tested_file(
            'test_data/referenc_result_data_tree.js')
        assert result == referenc_result


def test_entrypoint_run_choice_two_rule():
    random_dir = str(uuid.uuid4())
    src = os.path.join(tmp, random_dir)
    sut = pexpect.spawn(
        r'python3 -m oval_graph.command_line --out ' +
        src +
        r' --off-web-browser tests/test_data/ssg-fedora-ds-arf.xml "_package_\w+_removed"')
    sut.expect(r'\w+', timeout=1)
    sut.send(key.SPACE)
    sut.send(key.DOWN)
    sut.send(key.SPACE)
    sut.send(key.ENTER)
    sut.expect(
        r'raph-of-xccdf_org.ssgproject.content_rule_package_sendmail_removed_\w+')
    for name in os.listdir(src):
        result = tests.any_test_help.any_get_tested_file(
            os.path.join(src, name, 'data.js'))
        referenc_result = tests.any_test_help.any_get_tested_file(os.path.join(
            'test_data', re.sub(
                r'_\d\d-\d\d-\d\d\d\d_\d\d:\d\d:\d\d',
                '',
                str(name)) + '.js'))
        assert result == referenc_result


def test_run_with_more_then_one_rule():
    out = os.popen(
        ('python3 -m oval_graph.command_line --off-web-browser'
         r' tests/test_data/ssg-fedora-ds-arf.xml "_package_\w+_removed"')).read()
    assert out == (
        '\n[?] = The Rules IDs = (move - UP and DOWN arrows, select - SPACE or LEFT an...: \n'
        ' > o xccdf_org.ssgproject.content_rule_package_abrt_removed\n'
        '   o xccdf_org.ssgproject.content_rule_package_sendmail_removed\n\n')


def test_run_with_more_then_one_rule_if_not_installed_inquirer():
    out = os.popen(
        tmp +
        '/testEnvironmentLxml/bin/python3 -m oval_graph.command_line --off-web-browser'
        r' tests/test_data/ssg-fedora-ds-arf.xml "_package_\w+_removed"').read()
    assert out == (
        "== The Rule IDs ==\n"
        "xccdf_org.ssgproject.content_rule_package_abrt_removed\\b\n"
        "xccdf_org.ssgproject.content_rule_package_sendmail_removed\\b\n"
        "You haven't got installed inquirer lib. Please copy id rule with you"
        " want use and put it in command\n")


def test_run_with_more_then_one_rule_with_option_show_fail_rules():
    out = os.popen(
        ('python3 -m oval_graph.command_line '
         '--off-web-browser --show-fail-rules'
         r' tests/test_data/ssg-fedora-ds-arf.xml "_package_\w+_removed"')).read()
    print(repr(out))
    assert out == (
        '\n[?] = The Rules IDs = (move - UP and DOWN arrows, select - SPACE or LEFT an...: \n'
        ' > o xccdf_org.ssgproject.content_rule_package_abrt_removed\n\n')


def test_run_with_more_then_one_rule_if_not_installed_inquirer_with_option_show_fail_rules():
    out = os.popen(
        (tmp + '/testEnvironmentLxml/bin/python3 -m oval_graph.command_line --off-web-browser '
         r'--show-fail-rules tests/test_data/ssg-fedora-ds-arf.xml "_package_\w+_removed"')).read()
    print(repr(out))
    assert out == (
        "== The Rule IDs ==\n"
        "xccdf_org.ssgproject.content_rule_package_abrt_removed\\b\n"
        "You haven't got installed inquirer lib. Please copy id rule with you"
        " want use and put it in command\n")


def test_run_with_more_then_one_rule_with_option_show_not_selected_rules():
    out = os.popen(
        ('python3 -m oval_graph.command_line --off-web-browser '
         '--show-not-selected-rules tests/test_data/ssg-fedora-ds-arf.xml'
         r' "_package_\w+_removed"')).read()
    print(repr(out))
    assert out == (
        '== The not selected rule IDs ==\n'
        'xccdf_org.ssgproject.content_rule_package_nis_removed(Not selected)\n'
        'xccdf_org.ssgproject.content_rule_package_ntpdate_removed(Not selected)\n'
        'xccdf_org.ssgproject.content_rule_package_telnetd_removed(Not selected)\n'
        'xccdf_org.ssgproject.content_rule_package_gdm_removed(Not selected)\n'
        'xccdf_org.ssgproject.content_rule_package_setroubleshoot_removed(Not selected)\n'
        'xccdf_org.ssgproject.content_rule_package_mcstrans_removed(Not selected)\n'
        '\n[?] = The Rules IDs = (move - UP and DOWN arrows, select - SPACE or LEFT an...: \n'
        ' > o xccdf_org.ssgproject.content_rule_package_abrt_removed\n'
        '   o xccdf_org.ssgproject.content_rule_package_sendmail_removed\n\n')


def test_run_if_not_installed_inquirer_with_option_show_not_selected_rules():
    out = os.popen(
        (tmp +
         '/testEnvironmentLxml/bin/python3 -m oval_graph.command_line --off-web-browser '
         '--show-not-selected-rules tests/test_data/ssg-fedora-ds-arf.xml '
         r'"_package_\w+_removed"')).read()
    print(repr(out))
    assert out == (
        "== The Rule IDs ==\n"
        "xccdf_org.ssgproject.content_rule_package_abrt_removed\\b\n"
        "xccdf_org.ssgproject.content_rule_package_sendmail_removed\\b\n"
        "== The not selected rule IDs ==\n"
        "xccdf_org.ssgproject.content_rule_package_nis_removed(Not selected)\n"
        "xccdf_org.ssgproject.content_rule_package_ntpdate_removed(Not selected)\n"
        "xccdf_org.ssgproject.content_rule_package_telnetd_removed(Not selected)\n"
        "xccdf_org.ssgproject.content_rule_package_gdm_removed(Not selected)\n"
        "xccdf_org.ssgproject.content_rule_package_setroubleshoot_removed(Not selected)\n"
        "xccdf_org.ssgproject.content_rule_package_mcstrans_removed(Not selected)\n"
        "You haven't got installed inquirer lib. Please copy id rule with you"
        " want use and put it in command\n")


def test_run_with_more_then_one_rule_with_option_show_not_selected_rules_and_show_fail_rules():
    out = os.popen(
        ('python3 -m oval_graph.command_line --off-web-browser '
         '--show-fail-rules --show-not-selected-rules tests/test_data/ssg-fedora-ds-arf.xml '
         r'"_package_\w+_removed"')).read()
    print(repr(out))
    assert out == (
        '== The not selected rule IDs ==\n'
        'xccdf_org.ssgproject.content_rule_package_nis_removed(Not selected)\n'
        'xccdf_org.ssgproject.content_rule_package_ntpdate_removed(Not selected)\n'
        'xccdf_org.ssgproject.content_rule_package_telnetd_removed(Not selected)\n'
        'xccdf_org.ssgproject.content_rule_package_gdm_removed(Not selected)\n'
        'xccdf_org.ssgproject.content_rule_package_setroubleshoot_removed(Not selected)\n'
        'xccdf_org.ssgproject.content_rule_package_mcstrans_removed(Not selected)\n'
        '\n[?] = The Rules IDs = (move - UP and DOWN arrows, select - SPACE or LEFT an...: \n'
        ' > o xccdf_org.ssgproject.content_rule_package_abrt_removed\n\n')


def test_run_if_not_installed_inquirer_with_option_show_not_selected_rules_and_show_fail_rules():
    out = os.popen(
        (tmp +
         r'/testEnvironmentLxml/bin/python3 -m oval_graph.command_line --off-web-browser'
         ' --show-fail-rules --show-not-selected-rules tests/test_data/ssg-fedora-ds-arf.xml '
         r'"_package_\w+_removed"')).read()
    print(repr(out))
    assert out == (
        "== The Rule IDs ==\n"
        "xccdf_org.ssgproject.content_rule_package_abrt_removed\\b\n"
        "== The not selected rule IDs ==\n"
        "xccdf_org.ssgproject.content_rule_package_nis_removed(Not selected)\n"
        "xccdf_org.ssgproject.content_rule_package_ntpdate_removed(Not selected)\n"
        "xccdf_org.ssgproject.content_rule_package_telnetd_removed(Not selected)\n"
        "xccdf_org.ssgproject.content_rule_package_gdm_removed(Not selected)\n"
        "xccdf_org.ssgproject.content_rule_package_setroubleshoot_removed(Not selected)\n"
        "xccdf_org.ssgproject.content_rule_package_mcstrans_removed(Not selected)\n"
        "You haven't got installed inquirer lib. Please copy id rule with you"
        " want use and put it in command\n")
