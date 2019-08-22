import graph.client
import pytest
import tests.any_test_help
import re
import json


def get_client(src, rule):
    return graph.client.client([tests.any_test_help.get_src(src), rule])


def test_client():
    src = 'test_data/ssg-fedora-ds-arf.xml'
    rule = 'rule'
    client = get_client(src, rule)
    assert client.source_filename == tests.any_test_help.get_src(src)
    assert client.rule_name == rule


def test_search_rules_id():
    src = 'test_data/ssg-fedora-ds-arf.xml'
    part_of_id_rule = 'xccdf_org.ssgproject.'
    client = get_client(src, part_of_id_rule)
    assert len(client.search_rules_id()) == 184


def test_find_doest_exist_rule():
    rule = 'random_rule_which_doest_exist'
    src = 'test_data/ssg-fedora-ds-arf.xml'
    client = get_client(src, rule)
    with pytest.raises(Exception, match="err- 404 rule not found!"):
        assert client.search_rules_id()


def test_find_not_selected_rule():
    rule = 'xccdf_org.ssgproject.content_rule_ntpd_specify_remote_server'
    src = 'test_data/ssg-fedora-ds-arf.xml'
    client = get_client(src, rule)
    with pytest.raises(Exception, match=rule):
        assert client.search_rules_id()


def test_search_rules_with_regex():
    src = 'test_data/ssg-fedora-ds-arf.xml'
    regex = r'_package_\w+_removed'
    client = get_client(src, regex)
    assert len(client.search_rules_id()) == 2


def test_get_questions():
    src = 'test_data/ssg-fedora-ds-arf.xml'
    regex = r'_package_\w+_removed'
    client = get_client(src, regex)
    out = client.get_questions()
    assert out[0]['choices'][1]['name'] == 'xccdf_org.ssgproject.content_rule_package_abrt_removed'
    assert out[0]['choices'][2]['name'] == 'xccdf_org.ssgproject.content_rule_package_sendmail_removed'


def test_get_wanted_not_selected_rules():
    src = 'test_data/ssg-fedora-ds-arf.xml'
    regex = r'_package_\w+_removed'
    client = get_client(src, regex)

    out = [
        {'id_rule': 'xccdf_org.ssgproject.content_rule_package_nis_removed'},
        {'id_rule': 'xccdf_org.ssgproject.content_rule_package_ntpdate_removed'},
        {'id_rule': 'xccdf_org.ssgproject.content_rule_package_telnetd_removed'},
        {'id_rule': 'xccdf_org.ssgproject.content_rule_package_gdm_removed'},
        {'id_rule': 'xccdf_org.ssgproject.content_rule_package_setroubleshoot_removed'},
        {'id_rule': 'xccdf_org.ssgproject.content_rule_package_mcstrans_removed'}]

    assert out == client._get_wanted_not_selected_rules()


def test_get_wanted_rules():
    src = 'test_data/ssg-fedora-ds-arf.xml'
    regex = r'_package_\w+_removed'
    client = get_client(src, regex)

    out = [
        {'href': '#oval0',
         'id_def': 'oval:ssg-package_abrt_removed:def:1',
         'id_rule': 'xccdf_org.ssgproject.content_rule_package_abrt_removed',
         'result': 'fail'},
        {'href': '#oval0',
         'id_def': 'oval:ssg-package_sendmail_removed:def:1',
         'id_rule': 'xccdf_org.ssgproject.content_rule_package_sendmail_removed',
         'result': 'pass'}]

    assert out == client._get_wanted_rules()


def test_search_non_existent_rule():
    src = 'test_data/ssg-fedora-ds-arf.xml'
    non_existent_rule = 'non-existent_rule'
    with pytest.raises(Exception, match="err- 404 rule not found!"):
        assert get_client(src, non_existent_rule).search_rules_id()


def test_search_not_selected_rule():
    src = 'test_data/ssg-fedora-ds-arf.xml'
    non_existent_rule = 'xccdf_org.ssgproject.content_rule_package_nis_removed'
    with pytest.raises(Exception, match=non_existent_rule):
        assert get_client(src, non_existent_rule).search_rules_id()


def test_prepare_graph():
    src = 'test_data/ssg-fedora-ds-arf.xml'
    rule = 'xccdf_org.ssgproject.content_rule_package_abrt_removed'
    client = get_client(src, rule)
    rules = {'rules': [rule]}
    client.prepare_graphs(rules)
    result = load_tested_file('../html_interpreter/data.js')
    referenc_result = load_tested_file('test_data/referenc_result_data.js')
    assert result == referenc_result


def load_tested_file(src):
    with open(tests.any_test_help.get_src(src), 'r') as f:
        data = f.readlines()
    out = []
    edge = False
    for row in data:
        if row == '    "edges": [\n':
            print('wow')
            edge = True
        if not edge:
            out.append(row)
    return out


def try_expection_for_prepare_graph(src, rule, err):
    client = get_client(src, rule)
    rules = {'rules': [rule]}
    with pytest.raises(Exception, match=err):
        assert client.prepare_graphs(rules)


def test_prepare_graph_with_non_existent_rule():
    src = 'test_data/ssg-fedora-ds-arf.xml'
    rule = 'non-existent_rule'
    try_expection_for_prepare_graph(src, rule, '404')


def test_prepare_graph_with_not_selected_rule():
    src = 'test_data/ssg-fedora-ds-arf.xml'
    rule = 'xccdf_org.ssgproject.content_rule_package_nis_removed'
    try_expection_for_prepare_graph(src, rule, 'not selected')
