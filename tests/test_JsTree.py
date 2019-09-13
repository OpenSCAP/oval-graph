import tests.any_test_help
import graph.oval_graph


def test_create_node_dict_for_JsTree_0():
    src = 'test_JsTree_data/JsTree_data_0.json'
    Tree = tests.any_test_help.get_simple_tree()
    tests.any_test_help.any_test_create_node_dict_for_JsTree(Tree, src)


def test_create_node_dict_for_JsTree_1():
    src = 'test_JsTree_data/JsTree_data_1.json'

    Tree = graph.oval_graph.OvalNode(1, 'operator', 'and', False, None, [
        graph.oval_graph.OvalNode(2, 'value', "true", False, None)
    ]
    )

    tests.any_test_help.any_test_create_node_dict_for_JsTree(Tree, src)


def test_create_node_dict_for_JsTree_2():
    src = 'test_JsTree_data/JsTree_data_2.json'

    Tree = graph.oval_graph.OvalNode(1, 'operator', 'and', False, None, [
        graph.oval_graph.OvalNode(2, 'value', "noteval", False, None)
    ]
    )

    tests.any_test_help.any_test_create_node_dict_for_JsTree(Tree, src)


def test_create_node_dict_for_JsTree_3():
    src = 'test_JsTree_data/JsTree_data_3.json'

    Tree = graph.oval_graph.OvalNode(1, 'value', 'false', False, None)

    tests.any_test_help.any_test_create_node_dict_for_JsTree(Tree, src)


def test_create_node_dict_for_JsTree_4():
    src = 'test_JsTree_data/JsTree_data_4.json'

    Tree = graph.oval_graph.OvalNode(1, 'value', 'true', False, None)

    tests.any_test_help.any_test_create_node_dict_for_JsTree(Tree, src)


def test_create_node_dict_for_JsTree_5():
    src = 'test_JsTree_data/JsTree_data_5.json'

    Tree = graph.oval_graph.OvalNode(1, 'value', 'error', False, None)

    tests.any_test_help.any_test_create_node_dict_for_JsTree(Tree, src)


def test_create_node_with_negation_dict_for_JsTree():
    src = 'test_JsTree_data/JsTree_data_negated_0.json'

    Tree = graph.oval_graph.OvalNode(1, 'operator', 'and', True, None, [
        graph.oval_graph.OvalNode(2, 'value', "false", False, None)
    ]
    )

    tests.any_test_help.any_test_create_node_dict_for_JsTree(Tree, src)


def test_create_node_with_negation_dict_for_JsTree1():
    src = 'test_JsTree_data/JsTree_data_negated_1.json'

    Tree = graph.oval_graph.OvalNode(1, 'operator', 'and', True, None, [
        graph.oval_graph.OvalNode(2, 'value', "true", False, None)
    ]
    )

    tests.any_test_help.any_test_create_node_dict_for_JsTree(Tree, src)


def test_create_node_with_negation_dict_for_JsTree2():
    src = 'test_JsTree_data/JsTree_data_negated_2.json'

    Tree = graph.oval_graph.OvalNode(1, 'operator', 'and', False, None, [
        graph.oval_graph.OvalNode(2, 'value', "true", True, None)
    ]
    )

    tests.any_test_help.any_test_create_node_dict_for_JsTree(
        Tree.children[0], src)


def test_create_node_with_negation_dict_for_JsTree3():
    src = 'test_JsTree_data/JsTree_data_negated_3.json'

    Tree = graph.oval_graph.OvalNode(1, 'operator', 'and', False, None, [
        graph.oval_graph.OvalNode(2, 'value', "false", True, None)
    ]
    )

    tests.any_test_help.any_test_create_node_dict_for_JsTree(
        Tree.children[0], src)


def test_transformation_tree_to_Json_for_JsTree_0():
    test_data_src = 'test_data/JsTree_json0.json'
    src = 'test_data/ssg-fedora-ds-arf.xml'
    rule_id = 'xccdf_org.ssgproject.content_rule_accounts_passwords_pam_faillock_deny'

    tests.any_test_help.any_test_transformation_tree_to_Json_for_JsTree(
        src, test_data_src, rule_id)


def test_transformation_tree_to_Json_for_JsTree_with_duplicated_test():
    test_data_src = 'test_data/JsTree_json1.json'
    src = 'test_data/ssg-fedora-ds-arf.xml'
    rule_id = 'xccdf_org.ssgproject.content_rule_disable_host_auth'

    tests.any_test_help.any_test_transformation_tree_to_Json_for_JsTree(
        src, test_data_src, rule_id)
