import tests.any_test_help
from oval_graph.oval_node import OvalNode


def test_create_node_dict_for_JsTree_0():
    src = 'test_data/test_JsTree_data/JsTree_data_0.json'
    tree = tests.any_test_help.get_simple_tree()
    tests.any_test_help.any_test_create_node_dict_for_JsTree(tree, src)


def test_create_node_dict_for_JsTree_1():
    src = 'test_data/test_JsTree_data/JsTree_data_1.json'

    tree = OvalNode(
        node_id=1,
        node_type='operator',
        value='and',
        children=[
            OvalNode(
                node_id=2,
                node_type='value',
                value='true',
            )
        ]
    )

    tests.any_test_help.any_test_create_node_dict_for_JsTree(tree, src)


def test_create_node_dict_for_JsTree_2():
    src = 'test_data/test_JsTree_data/JsTree_data_2.json'

    tree = OvalNode(
        node_id=1,
        node_type='operator',
        value='and',
        children=[
            OvalNode(
                node_id=2,
                node_type='value',
                value='noteval',
            )
        ]
    )

    tests.any_test_help.any_test_create_node_dict_for_JsTree(tree, src)


def test_create_node_dict_for_JsTree_3():
    src = 'test_data/test_JsTree_data/JsTree_data_3.json'

    tree = OvalNode(
        node_id=1,
        node_type='value',
        value='false',
    )
    tests.any_test_help.any_test_create_node_dict_for_JsTree(tree, src)


def test_create_node_dict_for_JsTree_4():
    src = 'test_data/test_JsTree_data/JsTree_data_4.json'

    tree = OvalNode(
        node_id=1,
        node_type='value',
        value='true',
    )

    tests.any_test_help.any_test_create_node_dict_for_JsTree(tree, src)


def test_create_node_dict_for_JsTree_5():
    src = 'test_data/test_JsTree_data/JsTree_data_5.json'

    tree = OvalNode(
        node_id=1,
        node_type='value',
        value='error',
    )

    tests.any_test_help.any_test_create_node_dict_for_JsTree(tree, src)


def test_create_node_with_negation_dict_for_JsTree():
    src = 'test_data/test_JsTree_data/JsTree_data_negated_0.json'

    tree = OvalNode(
        node_id=1,
        node_type='operator',
        value='and',
        negation=True,
        children=[
            OvalNode(
                node_id=2,
                node_type='value',
                value='false',
            )
        ]
    )

    tests.any_test_help.any_test_create_node_dict_for_JsTree(tree, src)


def test_create_node_with_negation_dict_for_JsTree1():
    src = 'test_data/test_JsTree_data/JsTree_data_negated_1.json'

    tree = OvalNode(
        node_id=1,
        node_type='operator',
        value='and',
        negation=True,
        children=[
            OvalNode(
                node_id=2,
                node_type='value',
                value='true',
            )
        ]
    )

    tests.any_test_help.any_test_create_node_dict_for_JsTree(tree, src)


def test_create_node_with_negation_dict_for_JsTree2():
    src = 'test_data/test_JsTree_data/JsTree_data_negated_2.json'

    tree = OvalNode(
        node_id=1,
        node_type='operator',
        value='and',
        children=[
            OvalNode(
                node_id=2,
                node_type='value',
                value='true',
                negation=True,
            )
        ]
    )

    tests.any_test_help.any_test_create_node_dict_for_JsTree(
        tree.children[0], src)


def test_create_node_with_negation_dict_for_JsTree3():
    src = 'test_data/test_JsTree_data/JsTree_data_negated_3.json'

    tree = OvalNode(
        node_id=1,
        node_type='operator',
        value='and',
        children=[
            OvalNode(
                node_id=2,
                node_type='value',
                value='false',
                negation=True,
            )
        ]
    )

    tests.any_test_help.any_test_create_node_dict_for_JsTree(
        tree.children[0], src)


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
