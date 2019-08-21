import graph.client
import pytest
import tests.any_test_help
def get_client(src,rule):
    return graph.client.client([src,rule])


def test_client():
    src='test_data/ssg-fedora-ds-arf.xml'
    rule='rule'
    client = get_client(tests.any_test_help.get_src(src), rule)
    assert client.source_filename == tests.any_test_help.get_src(src)
    assert client.rule_name == rule


def test_search_rules_id():
    src='test_data/ssg-fedora-ds-arf.xml'
    part_of_id_rule='xccdf_org.ssgproject.'
    client = get_client(tests.any_test_help.get_src(src), part_of_id_rule)
    assert len(client.search_rules_id()) == 184


def test_find_doest_exist_rule():
    rule='random_rule_which_doest_exist'
    src='test_data/ssg-fedora-ds-arf.xml'
    client = get_client(tests.any_test_help.get_src(src), rule)
    with pytest.raises(Exception, match="err- 404 rule not found!"):
        assert client.search_rules_id()


def test_find_not_selected_rule():
    rule='xccdf_org.ssgproject.content_rule_ntpd_specify_remote_server'
    src='test_data/ssg-fedora-ds-arf.xml'
    client = get_client(tests.any_test_help.get_src(src), rule)
    with pytest.raises(Exception, match=rule):
        assert client.search_rules_id()


def test_search_rules_id():
    src='test_data/ssg-fedora-ds-arf.xml'
    regex=r'(_package_)\w+(_removed)'
    client = get_client(tests.any_test_help.get_src(src), regex)
    assert len(client.search_rules_id()) == 2

def test_get_questions():
    src='test_data/ssg-fedora-ds-arf.xml'
    regex=r'(_package_)\w+(_removed)'
    client = get_client(tests.any_test_help.get_src(src), regex)
    import pprint
    pprint.pprint(client.get_questions())
    assert client.get_questions()[0]['choices'][1]['name']=='xccdf_org.ssgproject.content_rule_package_abrt_removed'
    assert client.get_questions()[0]['choices'][2]['name']=='xccdf_org.ssgproject.content_rule_package_sendmail_removed'
