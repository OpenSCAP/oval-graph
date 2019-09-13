import tests.any_test_help
import graph.oval_graph
import graph.converter


def test_create_node_dict_for_sigmaJs_0():
    out = {
        'type': 'circle',
        'borderColor': '#ff0000',
        'color': '#ff0000',
        'id': 1,
        'label': 'AND',
        'size': 3,
        'text': None,
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
        'label': 'AND',
        'size': 3,
        'text': None,
        'url': 'null',
        'title': 1,
        'x': 0,
        'y': 0
    }
    Tree = graph.oval_graph.OvalNode(1, 'operator', 'and', False, None, [
        graph.oval_graph.OvalNode(2, 'value', "true", False, None)
    ]
    )

    tests.any_test_help.any_test_create_node_dict_for_sigmaJs(Tree, out)


def test_create_node_dict_for_sigmaJs_2():
    out = {
        'type': 'circle',
        'borderColor': '#000000',
        'color': '#000000',
        'id': 1,
        'label': 'AND',
        'size': 3,
        'text': None,
        'url': 'null',
        'title': '1 and',
        'x': 0,
        'y': 0
    }
    Tree = graph.oval_graph.OvalNode(1, 'operator', 'and', False, None, [
        graph.oval_graph.OvalNode(2, 'value', "noteval", False, None)
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
        'text': None,
        'url': 'null',
        'title': 1,
        'x': 0,
        'y': 0
    }
    Tree = graph.oval_graph.OvalNode(1, 'value', 'false', False, None)

    tests.any_test_help.any_test_create_node_dict_for_sigmaJs(Tree, out)


def test_create_node_dict_for_sigmaJs_4():
    out = {
        'type': 'circle',
        'borderColor': '#00ff00',
        'color': '#00ff00',
        'id': 1,
        'label': '1',
        'size': 3,
        'text': None,
        'url': 'null',
        'title': 1,
        'x': 0,
        'y': 0
    }
    Tree = graph.oval_graph.OvalNode(1, 'value', 'true', False, None)

    tests.any_test_help.any_test_create_node_dict_for_sigmaJs(Tree, out)


def test_create_node_dict_for_sigmaJs_5():
    out = {
        'type': 'circle',
        'borderColor': '#000000',
        'color': '#000000',
        'id': 1,
        'label': '1',
        'size': 3,
        'text': None,
        'url': 'null',
        'title': '1 error',
        'x': 0,
        'y': 0
    }
    Tree = graph.oval_graph.OvalNode(1, 'value', 'error', False, None)

    tests.any_test_help.any_test_create_node_dict_for_sigmaJs(Tree, out)


def test_create_node_with_negation_dict_for_sigmaJs():
    out = {
        'type': 'circle',
        'borderColor': '#00ff00',
        'color': '#ff0000',
        'id': 1,
        'label': 'AND',
        'size': 3,
        'text': None,
        'url': 'null',
        'title': 1,
        'x': 0,
        'y': 0
    }
    Tree = graph.oval_graph.OvalNode(1, 'operator', 'and', True, None, [
        graph.oval_graph.OvalNode(2, 'value', "false", False, None)
    ]
    )

    tests.any_test_help.any_test_create_node_dict_for_sigmaJs(Tree, out)


def test_create_node_with_negation_dict_for_sigmaJs1():
    out = {
        'type': 'circle',
        'borderColor': '#ff0000',
        'color': '#00ff00',
        'id': 1,
        'label': 'AND',
        'size': 3,
        'text': None,
        'url': 'null',
        'title': 1,
        'x': 0,
        'y': 0
    }
    Tree = graph.oval_graph.OvalNode(1, 'operator', 'and', True, None, [
        graph.oval_graph.OvalNode(2, 'value', "true", False, None)
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
        'text': None,
        'url': 'null',
        'title': 2,
        'x': 0,
        'y': 0
    }
    Tree = graph.oval_graph.OvalNode(1, 'operator', 'and', False, None, [
        graph.oval_graph.OvalNode(2, 'value', "true", True, None)
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
        'text': None,
        'url': 'null',
        'title': 2,
        'x': 0,
        'y': 0
    }
    Tree = graph.oval_graph.OvalNode(1, 'operator', 'and', False, None, [
        graph.oval_graph.OvalNode(2, 'value', "false", True, None)
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
        'text': None,
        'url': 'null',
        'title': '1 error',
        'x': 0,
        'y': 0
    }
    converter = tests.any_test_help.get_converter_simple_tree()
    assert converter._create_edge(1, 2, target_node)['source'] == out['source']
    assert converter._create_edge(1, 2, target_node)['target'] == out['target']
    assert converter._create_edge(1, 2, target_node)['color'] == out['color']


def test_create_array_of_ids_form_tree():
    array = tests.any_test_help.get_converter_simple_tree().create_list_of_id()
    assert array == [1, 2, 3, 4, 5, 6]


def test_transformation_tree_to_Json_for_SigmaJs_0():
    test_data_src = 'test_data/sigmaJs_json0.json'
    src = 'test_data/ssg-fedora-ds-arf.xml'
    rule_id = 'xccdf_org.ssgproject.content_rule_accounts_passwords_pam_faillock_deny'

    tests.any_test_help.any_test_transformation_tree_to_Json_for_SigmaJs(
        src, test_data_src, rule_id)


def test_transformation_tree_to_Json_for_SigmaJs_with_duplicated_test():
    test_data_src = 'test_data/sigmaJs_json1.json'
    src = 'test_data/ssg-fedora-ds-arf.xml'
    rule_id = 'xccdf_org.ssgproject.content_rule_disable_host_auth'

    tests.any_test_help.any_test_transformation_tree_to_Json_for_SigmaJs(
        src, test_data_src, rule_id)
