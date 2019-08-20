import graph.client


def get_client():
    return graph.client.client(['data/ssg-fedora-ds-arf.xml', 'rule'])


def test_client():
    client = get_client()
    assert client.source_filename == 'data/ssg-fedora-ds-arf.xml'
    assert client.rule_name == 'rule'


def test_search_rules_id():
    client = get_client()
    assert len(client.search_rules_id()) == 184
