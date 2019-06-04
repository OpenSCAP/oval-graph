import tree.oval_tree
import pytest
import os
import py


global results_counts
results_counts = {
    'true_cnt': -1,
    'false_cnt': -1,
    'error_cnt': -1,
    'unknown_cnt': -1,
    'noteval_cnt': -1,
    'notappl_cnt': -1
}


def test_bad_tree():
    with pytest.raises(ValueError) as e:
        badTree()
    assert str(
        e.value) == 'err- true, false, error, unknown. noteval, notappl have not child!'

    with pytest.raises(ValueError) as e:
        treeOnlyAnd()
    assert str(e.value) == 'err- OR, XOR, ONE, AND have child!'

    with pytest.raises(ValueError) as e:
        treeOnlyOr()
    assert str(e.value) == 'err- OR, XOR, ONE, AND have child!'

    with pytest.raises(ValueError) as e:
        treeWithBadType()
    assert str(e.value) == 'err- unknown type'

    with pytest.raises(ValueError) as e:
        treeWithBadValueOfOperator()
    assert str(e.value) == 'err- unknown operator'

    with pytest.raises(ValueError) as e:
        treeWithBadValueOfValue()
    assert str(e.value) == 'err- unknown value'


# degenered trees

def badTree():
    """
         t
         |
        and
         |
         t
    """
    t = tree.oval_tree.OvalNode(
        1, "value", "true", [
            tree.oval_tree.OvalNode(
                2, "operator", "and", [
                    tree.oval_tree.OvalNode(
                        3, "value", "true")])])
    return


def treeOnlyOr():
    """
        or
    """
    Tree = tree.oval_tree.OvalNode(1, "operator", 'or')
    return


def treeOnlyAnd():
    """
        and
    """
    Tree = tree.oval_tree.OvalNode(1, "operator", 'and')
    return


def treeWithBadValueOfOperator():
    Tree = tree.oval_tree.OvalNode(1, "operator", 'nad')
    return


def treeWithBadValueOfValue():
    Tree = tree.oval_tree.OvalNode(1, "value", 'and')
    return


def treeWithBadType():
    Tree = tree.oval_tree.OvalNode(1, "auto", 'and')
    return

# normal trees


def test_UPPERCASETree():
    t = tree.oval_tree.OvalNode(
        1, "OPERATOR", "AND", [
            tree.oval_tree.OvalNode(
                2, "VALUE", "TRUE",), tree.oval_tree.OvalNode(
                3, "VALUE", "NOTAPPL")])

# AND operator


def test_ANDTreeTrue():
    Tree = tree.oval_tree.OvalNode(1, 'operator', 'and', [
        tree.oval_tree.OvalNode(2, 'value', "true"),
        tree.oval_tree.OvalNode(3, 'value', "true"),
        tree.oval_tree.OvalNode(4, 'value', "notappl")
    ]
    )

    any_test_treeEvaluation(Tree, "true")


def test_ANDTreeFalse():
    Tree = tree.oval_tree.OvalNode(1, 'operator', 'and', [
        tree.oval_tree.OvalNode(2, 'value', "false"),
        tree.oval_tree.OvalNode(3, 'value', "false"),

        tree.oval_tree.OvalNode(4, 'value', "true"),
        tree.oval_tree.OvalNode(5, 'value', "error"),
        tree.oval_tree.OvalNode(6, 'value', "unknown"),
        tree.oval_tree.OvalNode(7, 'value', "noteval"),
        tree.oval_tree.OvalNode(8, 'value', "notappl")
    ]
    )

    any_test_treeEvaluation(Tree, "false")


def test_ANDTreeError():
    Tree = tree.oval_tree.OvalNode(1, 'operator', 'and', [
                tree.oval_tree.OvalNode(2, 'value', "error"),
                tree.oval_tree.OvalNode(3, 'value', "error"),
                tree.oval_tree.OvalNode(4, 'value', "true"),
                tree.oval_tree.OvalNode(5, 'value', "unknown"),
                tree.oval_tree.OvalNode(6, 'value', "noteval"),
                tree.oval_tree.OvalNode(7, 'value', "notappl"),
                tree.oval_tree.OvalNode(8, 'value', "error")
                ])

    any_test_treeEvaluation(Tree, "error")


def test_ANDTreeUnknown():
    Tree = tree.oval_tree.OvalNode(1, 'operator', 'and', [
                tree.oval_tree.OvalNode(2, 'value', "unknown"),
                tree.oval_tree.OvalNode(3, 'value', "unknown"),
                tree.oval_tree.OvalNode(4, 'value', "true"),
                tree.oval_tree.OvalNode(5, 'value', "unknown"),
                tree.oval_tree.OvalNode(6, 'value', "noteval"),
                tree.oval_tree.OvalNode(7, 'value', "notappl"),
                tree.oval_tree.OvalNode(8, 'value', "notappl")
                ]
                )

    any_test_treeEvaluation(Tree, "unknown")


def test_ANDTreeNoteval():
    Tree = tree.oval_tree.OvalNode(1, 'operator', 'and', [
                tree.oval_tree.OvalNode(2, 'value', "noteval"),
                tree.oval_tree.OvalNode(3, 'value', "noteval"),
                tree.oval_tree.OvalNode(4, 'value', "true"),
                tree.oval_tree.OvalNode(5, 'value', "true"),
                tree.oval_tree.OvalNode(6, 'value', "noteval"),
                tree.oval_tree.OvalNode(7, 'value', "notappl"),
                tree.oval_tree.OvalNode(8, 'value', "notappl")
                ]
                )

    any_test_treeEvaluation(Tree, "noteval")


def test_ANDTreeNotappl():
    Tree = tree.oval_tree.OvalNode(1, 'operator', 'and', [
        tree.oval_tree.OvalNode(2, 'value', "notappl"),
        tree.oval_tree.OvalNode(3, 'value', "notappl"),
        tree.oval_tree.OvalNode(4, 'value', "notappl")
    ]
    )

    any_test_treeEvaluation(Tree, "notappl")

# ONE operator


def test_ONETreeTrue():
    Tree = tree.oval_tree.OvalNode(1, 'operator', 'one', [
        tree.oval_tree.OvalNode(2, 'value', "true"),
        tree.oval_tree.OvalNode(3, 'value', "false"),
        tree.oval_tree.OvalNode(4, 'value', "notappl"),
        tree.oval_tree.OvalNode(5, 'value', "false")
    ]
    )

    any_test_treeEvaluation(Tree, "true")


def test_ONETreeFalse():
    Tree = tree.oval_tree.OvalNode(1, 'operator', 'one', [
        tree.oval_tree.OvalNode(2, 'value', "true"),
        tree.oval_tree.OvalNode(3, 'value', "true"),

        tree.oval_tree.OvalNode(4, 'value', "false"),
        tree.oval_tree.OvalNode(5, 'value', "error"),
        tree.oval_tree.OvalNode(6, 'value', "unknown"),
        tree.oval_tree.OvalNode(7, 'value', "noteval"),
        tree.oval_tree.OvalNode(8, 'value', "notappl")
    ]
    )

    any_test_treeEvaluation(Tree, "false")


def test_ONETreeFalse1():
    Tree = tree.oval_tree.OvalNode(1, 'operator', 'one', [
        tree.oval_tree.OvalNode(2, 'value', "false"),
        tree.oval_tree.OvalNode(3, 'value', "false"),
        tree.oval_tree.OvalNode(4, 'value', "notappl")
    ]
    )

    any_test_treeEvaluation(Tree, "false")


def test_ONETreeError():
    Tree = tree.oval_tree.OvalNode(1, 'operator', 'one', [
                tree.oval_tree.OvalNode(2, 'value', "error"),
                tree.oval_tree.OvalNode(3, 'value', "error"),
                tree.oval_tree.OvalNode(4, 'value', "true"),
                tree.oval_tree.OvalNode(5, 'value', "unknown"),
                tree.oval_tree.OvalNode(6, 'value', "noteval"),
                tree.oval_tree.OvalNode(7, 'value', "notappl"),
                tree.oval_tree.OvalNode(8, 'value', "false")
                ]
                )

    any_test_treeEvaluation(Tree, "error")


def test_ONETreeUnknown():
    Tree = tree.oval_tree.OvalNode(1, 'operator', 'one', [
                tree.oval_tree.OvalNode(2, 'value', "unknown"),
                tree.oval_tree.OvalNode(3, 'value', "unknown"),
                tree.oval_tree.OvalNode(4, 'value', "true"),
                tree.oval_tree.OvalNode(5, 'value', "unknown"),
                tree.oval_tree.OvalNode(6, 'value', "noteval"),
                tree.oval_tree.OvalNode(7, 'value', "notappl"),
                tree.oval_tree.OvalNode(8, 'value', "false")
                ])

    any_test_treeEvaluation(Tree, "unknown")


def test_ONETreeNoteval():
    Tree = tree.oval_tree.OvalNode(1, 'operator', 'one', [
                tree.oval_tree.OvalNode(2, 'value', "noteval"),
                tree.oval_tree.OvalNode(3, 'value', "noteval"),
                tree.oval_tree.OvalNode(4, 'value', "true"),
                tree.oval_tree.OvalNode(5, 'value', "false"),
                tree.oval_tree.OvalNode(6, 'value', "noteval"),
                tree.oval_tree.OvalNode(7, 'value', "notappl"),
                tree.oval_tree.OvalNode(8, 'value', "notappl")
                ]
                )

    any_test_treeEvaluation(Tree, "noteval")


def test_ONETreeNotappl():
    Tree = tree.oval_tree.OvalNode(1, 'operator', 'one', [
        tree.oval_tree.OvalNode(2, 'value', "notappl"),
        tree.oval_tree.OvalNode(3, 'value', "notappl"),
        tree.oval_tree.OvalNode(4, 'value', "notappl")
    ]
    )

    any_test_treeEvaluation(Tree, "notappl")

# OR operator


def test_ORTreeTrue():
    Tree = tree.oval_tree.OvalNode(1, 'operator', 'or', [
        tree.oval_tree.OvalNode(2, 'value', "true"),
        tree.oval_tree.OvalNode(3, 'value', "false"),

        tree.oval_tree.OvalNode(4, 'value', "true"),
        tree.oval_tree.OvalNode(5, 'value', "error"),
        tree.oval_tree.OvalNode(6, 'value', "unknown"),
        tree.oval_tree.OvalNode(7, 'value', "noteval"),
        tree.oval_tree.OvalNode(8, 'value', "notappl")
    ]
    )

    any_test_treeEvaluation(Tree, "true")


def test_ORTreeFalse():
    Tree = tree.oval_tree.OvalNode(1, 'operator', 'or', [
        tree.oval_tree.OvalNode(2, 'value', "false"),
        tree.oval_tree.OvalNode(3, 'value', "false"),
        tree.oval_tree.OvalNode(4, 'value', "notappl")
    ]
    )

    any_test_treeEvaluation(Tree, "false")


def test_ORTreeError():
    Tree = tree.oval_tree.OvalNode(1, 'operator', 'or', [
                tree.oval_tree.OvalNode(2, 'value', "error"),
                tree.oval_tree.OvalNode(3, 'value', "error"),
                tree.oval_tree.OvalNode(4, 'value', "false"),
                tree.oval_tree.OvalNode(5, 'value', "unknown"),
                tree.oval_tree.OvalNode(6, 'value', "noteval"),
                tree.oval_tree.OvalNode(7, 'value', "notappl"),
                tree.oval_tree.OvalNode(8, 'value', "error")
                ]
                )

    any_test_treeEvaluation(Tree, "error")


def test_ORTreeUnknown():
    Tree = tree.oval_tree.OvalNode(1, 'operator', 'or', [
                tree.oval_tree.OvalNode(2, 'value', "unknown"),
                tree.oval_tree.OvalNode(3, 'value', "unknown"),
                tree.oval_tree.OvalNode(4, 'value', "false"),
                tree.oval_tree.OvalNode(5, 'value', "unknown"),
                tree.oval_tree.OvalNode(6, 'value', "noteval"),
                tree.oval_tree.OvalNode(7, 'value', "notappl"),
                tree.oval_tree.OvalNode(8, 'value', "notappl")
                ]
                )

    any_test_treeEvaluation(Tree, "unknown")


def test_ORTreeNoteval():
    Tree = tree.oval_tree.OvalNode(1, 'operator', 'or', [
                tree.oval_tree.OvalNode(2, 'value', "noteval"),
                tree.oval_tree.OvalNode(3, 'value', "noteval"),
                tree.oval_tree.OvalNode(4, 'value', "false"),
                tree.oval_tree.OvalNode(5, 'value', "false"),
                tree.oval_tree.OvalNode(6, 'value', "noteval"),
                tree.oval_tree.OvalNode(7, 'value', "notappl"),
                tree.oval_tree.OvalNode(8, 'value', "notappl")
                ]
                )

    any_test_treeEvaluation(Tree, "noteval")


def test_ORTreeNotappl():
    Tree = tree.oval_tree.OvalNode(1, 'operator', 'or', [
        tree.oval_tree.OvalNode(2, 'value', "notappl"),
        tree.oval_tree.OvalNode(3, 'value', "notappl"),
        tree.oval_tree.OvalNode(4, 'value', "notappl")
    ]
    )

    any_test_treeEvaluation(Tree, "notappl")

# XOR operator


def test_XORTreeTrue():
    Tree = tree.oval_tree.OvalNode(1, 'operator', 'xor', [
        tree.oval_tree.OvalNode(2, 'value', "true"),
        tree.oval_tree.OvalNode(3, 'value', "false"),

        tree.oval_tree.OvalNode(4, 'value', "false"),
        tree.oval_tree.OvalNode(5, 'value', "false"),
        tree.oval_tree.OvalNode(6, 'value', "true"),
        tree.oval_tree.OvalNode(7, 'value', "true"),
        tree.oval_tree.OvalNode(8, 'value', "notappl")
    ]
    )

    any_test_treeEvaluation(Tree, "true")


def test_XORTreeFalse():
    Tree = tree.oval_tree.OvalNode(1, 'operator', 'xor', [
        tree.oval_tree.OvalNode(2, 'value', "true"),
        tree.oval_tree.OvalNode(3, 'value', "false"),

        tree.oval_tree.OvalNode(4, 'value', "false"),
        tree.oval_tree.OvalNode(5, 'value', "true"),
        tree.oval_tree.OvalNode(6, 'value', "true"),
        tree.oval_tree.OvalNode(7, 'value', "true"),
        tree.oval_tree.OvalNode(8, 'value', "notappl")
    ]
    )

    any_test_treeEvaluation(Tree, "false")


def test_XORTreeError():
    Tree = tree.oval_tree.OvalNode(1, 'operator', 'xor', [
                tree.oval_tree.OvalNode(2, 'value', "error"),
                tree.oval_tree.OvalNode(3, 'value', "error"),
                tree.oval_tree.OvalNode(4, 'value', "true"),
                tree.oval_tree.OvalNode(5, 'value', "unknown"),
                tree.oval_tree.OvalNode(6, 'value', "noteval"),
                tree.oval_tree.OvalNode(7, 'value', "notappl"),
                tree.oval_tree.OvalNode(8, 'value', "false")
                ]
                )

    any_test_treeEvaluation(Tree, "error")


def test_xORTreeUnknown():
    Tree = tree.oval_tree.OvalNode(1, 'operator', 'xor', [
                tree.oval_tree.OvalNode(2, 'value', "unknown"),
                tree.oval_tree.OvalNode(3, 'value', "unknown"),
                tree.oval_tree.OvalNode(4, 'value', "true"),
                tree.oval_tree.OvalNode(5, 'value', "unknown"),
                tree.oval_tree.OvalNode(6, 'value', "noteval"),
                tree.oval_tree.OvalNode(7, 'value', "notappl"),
                tree.oval_tree.OvalNode(8, 'value', "notappl")
                ]
                )

    any_test_treeEvaluation(Tree, "unknown")


def test_XORTreeNoteval():
    Tree = tree.oval_tree.OvalNode(1, 'operator', 'xor', [
                tree.oval_tree.OvalNode(2, 'value', "noteval"),
                tree.oval_tree.OvalNode(3, 'value', "noteval"),
                tree.oval_tree.OvalNode(4, 'value', "true"),
                tree.oval_tree.OvalNode(5, 'value', "true"),
                tree.oval_tree.OvalNode(6, 'value', "noteval"),
                tree.oval_tree.OvalNode(7, 'value', "notappl"),
                tree.oval_tree.OvalNode(8, 'value', "notappl")
                ]
                )

    any_test_treeEvaluation(Tree, "noteval")


def test_XORTreeNotappl():
    Tree = tree.oval_tree.OvalNode(1, 'operator', 'xor', [
        tree.oval_tree.OvalNode(2, 'value', "notappl"),
        tree.oval_tree.OvalNode(3, 'value', "notappl"),
        tree.oval_tree.OvalNode(4, 'value', "notappl")
    ]
    )

    any_test_treeEvaluation(Tree, "notappl")


def test_bigOvalTree():
    Tree = tree.oval_tree.OvalNode(1, 'operator', 'and', [
                tree.oval_tree.OvalNode(2, 'value', "false"),
                tree.oval_tree.OvalNode(3, 'operator', "xor", [
                            tree.oval_tree.OvalNode(4, 'value', 'true'),
                            tree.oval_tree.OvalNode(5, 'operator', 'one', [
                                        tree.oval_tree.OvalNode(6, 'value', 'noteval'),
                                        tree.oval_tree.OvalNode(7, 'value', 'true'), 
                                        tree.oval_tree.OvalNode(8, 'value', 'notappl')
                                        ]
                                        ),
                            tree.oval_tree.OvalNode(9, 'value', 'error')
                            ]
                            ),
                tree.oval_tree.OvalNode(10, 'operator', 'or', [
                                        tree.oval_tree.OvalNode(11, 'value', "unknown"),
                                        tree.oval_tree.OvalNode(12, 'value', "true")
                                        ]
                                        )
                ]
                )

    dict_of_tree = {'node_id': 1, 'type': 'operator', 'value': 'and',
                    'child': [
                        {'node_id': 2, 'type': 'value', 'value': "false", 'child': None},
                        {'node_id': 3, 'type': 'operator', 'value': "xor", 'child': [
                            {'node_id': 4, 'type': 'value', 'value': "true", 'child': None},
                            {'node_id': 5, 'type': 'operator', 'value': "one", 'child': [
                                {'node_id': 6, 'type': 'value', 'value': "noteval", 'child': None},
                                {'node_id': 7, 'type': 'value', 'value': "true", 'child': None},
                                {'node_id': 8, 'type': 'value', 'value': "notappl", 'child': None}
                            ]},
                            {'node_id': 9, 'type': 'value', 'value': "error", 'child': None}]},
                        {'node_id': 10, 'type': 'operator', 'value': 'or', 'child': [
                            {'node_id': 11, 'type': 'value', 'value': "unknown", 'child': None},
                            {'node_id': 12, 'type': 'value', 'value': "true", 'child': None}
                        ]
                        }
                    ]
                    }

    any_test_treeEvaluation(Tree, "false")
    any_test_tree_to_dict_of_tree(Tree, dict_of_tree)
    find_any_node(Tree, 5)
    any_test_dict_to_tree(dict_of_tree)

###################################################


def any_test_tree_to_dict_of_tree(tree, dict_of_tree):
    assert tree.tree_to_dict() == dict_of_tree


def find_any_node(Tree, node_id):
    findTree = Tree.find_node_with_ID(node_id)
    assert findTree.node_id == node_id


def any_test_treeEvaluation(tree, expect):
    assert tree.evaluate_tree() == expect


def any_test_dict_to_tree(dict_of_tree):
    treedict_of_tree = tree.oval_tree.dict_to_tree(dict_of_tree)
    assert treedict_of_tree.tree_to_dict() == dict_of_tree


def test_treeRepr():
    """
        and
         |
         f
    """
    Tree = tree.oval_tree.OvalNode(1, 'operator', 'and', [
        tree.oval_tree.OvalNode(2, 'value', "false")
    ]
    )
    assert str(Tree) == "and"


def test_add_to_tree():
    """
        and
         |
         f
    """

    dict_of_tree = {'node_id': 1,
                    'type': 'operator',
                    'value': 'and',
                    'child': [{'node_id': 2,
                               'type': 'value',
                               'value': "false",
                               'child': None},
                              {'node_id': 3,
                               'type': 'value',
                               'value': "true",
                               'child': None},
                              ]}

    Tree = tree.oval_tree.OvalNode(1, 'operator', 'and', [
        tree.oval_tree.OvalNode(2, 'value', "false")
    ]
    )
    Tree1 = tree.oval_tree.OvalNode(3, 'value', "true")
    Tree.add_to_tree(1, Tree1)
    assert Tree.tree_to_dict() == dict_of_tree


def test_ChangeValueTree():
    """
        and
        /|\
       t t or
          / \
         f   t
    """
    Tree = tree.oval_tree.OvalNode(1, 'operator', 'and', [
        tree.oval_tree.OvalNode(2, 'value', "true"),
        tree.oval_tree.OvalNode(3, 'value', "false"),
        tree.oval_tree.OvalNode(4, 'operator', 'or', [
            tree.oval_tree.OvalNode(5, 'value', "false"),
            tree.oval_tree.OvalNode(6, 'value', "true")
        ]
        )
    ]
    )

    Tree.change_tree_value(3, "true")
    any_test_treeEvaluation(Tree, "true")


def test_bad_operator_input_and():
    Tree = tree.oval_tree.OvalNode(0, 'value', "true")
    assert Tree._oval_operator_and(results_counts) is None


def test_bad_operator_input_one():
    Tree = tree.oval_tree.OvalNode(0, 'value', "true")
    assert Tree._oval_operator_one(results_counts) is None


def test_bad_operator_input_or():
    Tree = tree.oval_tree.OvalNode(0, 'value', "true")
    assert Tree._oval_operator_or(results_counts) is None


def test_bad_operator_input_xor():
    Tree = tree.oval_tree.OvalNode(0, 'value', "true")
    assert Tree._oval_operator_xor(results_counts) is None


def test_false_noteval_greater_zero():
    Tree = tree.oval_tree.OvalNode(0, 'value', "true")
    assert Tree._noteval_greater_zero(results_counts) == False


def test_false_error_unknown_eq_noteval_greater_zero():
    Tree = tree.oval_tree.OvalNode(0, 'value', "true")
    assert Tree._error_unknown_eq_noteval_greater_zero(results_counts) == False


def any_test_parsing_and_evaluate_scan_rule(src, rule_id, result):
    _dir = os.path.dirname(os.path.realpath(__file__))
    FIXTURE_DIR = py.path.local(_dir) / src

    oval_trees_array = tree.oval_tree.xml_to_tree(str(FIXTURE_DIR))
    for oval_tree in oval_trees_array:
        if oval_tree.node_id == rule_id:
            any_test_treeEvaluation(oval_tree, result)


def test_parsing_full_can_XML_and_evaluate():
    src = 'test_data/ssg-fedora-ds-arf.xml'
    rule_id = 'xccdf_org.ssgproject.content_rule_accounts_passwords_pam_faillock_deny'
    result = 'false'

    any_test_parsing_and_evaluate_scan_rule(src, rule_id, result)


def test_parsing_and_evaluate_scan_with_extend_def():
    src = 'test_data/ssg-fedora-ds-arf-scan-with-extend-definitions.xml'
    rule_id = 'xccdf_org.ssgproject.content_rule_sysctl_net_ipv6_conf_all_disable_ipv6'
    result = 'false'

    any_test_parsing_and_evaluate_scan_rule(src, rule_id, result)


def test_parsing_and_evaluate_scan_with_pasing_rule():
    src = 'test_data/ssg-fedora-ds-arf-passing-scan.xml'
    rule_id = 'xccdf_org.ssgproject.content_rule_service_debug-shell_disabled'
    result = 'true'

    any_test_parsing_and_evaluate_scan_rule(src, rule_id, result)


def test_parsing_and_evaluate_scan_with_fail_rule():
    src = 'test_data/ssg-fedora-ds-arf-scan-fail.xml'
    rule_id = 'xccdf_org.ssgproject.content_rule_mount_option_dev_shm_noexec'
    result = 'false'

    any_test_parsing_and_evaluate_scan_rule(src, rule_id, result)


def test_parsing_and_evaluate_scan_with_rule_with_XOR():
    src = 'test_data/ssg-fedora-ds-arf-scan-with-xor.xml'
    rule_id = 'xccdf_org.ssgproject.content_rule_mount_option_nosuid_removable_partitions'
    result = 'true'

    any_test_parsing_and_evaluate_scan_rule(src, rule_id, result)


def test_parsing_and_evaluate_scan_with_11_rules():
    src = 'test_data/ssg-fedora-ds-arf-scan-with-11-rules.xml'
    rule_id = 'xccdf_org.ssgproject.content_rule_mount_option_tmp_nosuid'
    result = 'true'

    any_test_parsing_and_evaluate_scan_rule(src, rule_id, result)


def test_transformation_tree_to_Json_for_SigmaJs():
    test_data = {"nodes": [{"id": "xccdf_org.ssgproject.content_rule_accounts_passwords_pam_faillock_deny",
                            "label": "and",
                            "x": 0,
                            "y": 0,
                            "size": 3},
                           {"id": "oval:ssg-accounts_passwords_pam_faillock_deny:def:1",
                            "label": "and",
                            "x": 0,
                            "y": 1,
                            "size": 3},
                           {"id": "oval:ssg-test_accounts_passwords_pam_faillock_preauth_silent_system-auth:tst:1",
                            "label": "false",
                            "x": 2,
                            "y": 3,
                            "size": 3},
                           {"id": "oval:ssg-test_accounts_passwords_pam_faillock_account_phase_system-auth:tst:1",
                            "label": "false",
                            "x": 3,
                            "y": 3,
                            "size": 3},
                           {"id": "oval:ssg-test_accounts_passwords_pam_faillock_preauth_silent_password-auth:tst:1",
                            "label": "false",
                            "x": 4,
                            "y": 3,
                            "size": 3},
                           {"id": "oval:ssg-test_accounts_passwords_pam_faillock_account_phase_password-auth:tst:1",
                            "label": "false",
                            "x": 5,
                            "y": 3,
                            "size": 3},
                           {"id": "cd2670ff-ec6a-450d-a501-f13ccc53c442",
                            "label": "and",
                            "x": 6,
                            "y": 3,
                            "size": 3},
                           {"id": "94b8d8f8-25d5-4d91-80bb-4cb981c79018",
                            "label": "or",
                            "x": 8,
                            "y": 5,
                            "size": 3},
                           {"id": "oval:ssg-test_accounts_passwords_pam_faillock_numeric_default_check_system-auth:tst:1",
                            "label": "false",
                            "x": 10,
                            "y": 7,
                            "size": 3},
                           {"id": "oval:ssg-test_accounts_passwords_pam_faillock_authfail_deny_system-auth:tst:1",
                            "label": "false",
                            "x": 11,
                            "y": 7,
                            "size": 3},
                           {"id": "ddcfa90d-6b1f-4e93-9984-20cfec3f164c",
                            "label": "or",
                            "x": 9,
                            "y": 5,
                            "size": 3},
                           {"id": "oval:ssg-test_accounts_passwords_pam_faillock_numeric_default_check_password-auth:tst:1",
                            "label": "false",
                            "x": 11,
                            "y": 7,
                            "size": 3},
                           {"id": "oval:ssg-test_accounts_passwords_pam_faillock_authfail_deny_password-auth:tst:1",
                            "label": "false",
                            "x": 12,
                            "y": 7,
                            "size": 3}],
                 "edges": [{"id": "7c749b2b-cda0-47d3-af1c-4ae5896eb06e",
                            "source": "xccdf_org.ssgproject.content_rule_accounts_passwords_pam_faillock_deny",
                            "target": "oval:ssg-accounts_passwords_pam_faillock_deny:def:1"},
                           {"id": "ad1f0982-252f-4c8d-b89e-f3dacf95a384",
                            "source": "oval:ssg-accounts_passwords_pam_faillock_deny:def:1",
                            "target": "oval:ssg-test_accounts_passwords_pam_faillock_preauth_silent_system-auth:tst:1"},
                           {"id": "7011d766-f739-48d0-8e8b-225957586f2c",
                            "source": "oval:ssg-accounts_passwords_pam_faillock_deny:def:1",
                            "target": "oval:ssg-test_accounts_passwords_pam_faillock_account_phase_system-auth:tst:1"},
                           {"id": "03e3f2b0-5283-4800-8c46-ca23c19e1b3a",
                            "source": "oval:ssg-accounts_passwords_pam_faillock_deny:def:1",
                            "target": "oval:ssg-test_accounts_passwords_pam_faillock_preauth_silent_password-auth:tst:1"},
                           {"id": "951ce893-90f3-443a-a90f-89cf65c409b8",
                            "source": "oval:ssg-accounts_passwords_pam_faillock_deny:def:1",
                            "target": "oval:ssg-test_accounts_passwords_pam_faillock_account_phase_password-auth:tst:1"},
                           {"id": "e96dcac1-8a38-45be-9aad-968ca7fecec5",
                            "source": "oval:ssg-accounts_passwords_pam_faillock_deny:def:1",
                            "target": "cd2670ff-ec6a-450d-a501-f13ccc53c442"},
                           {"id": "aa32e847-b6a5-4566-b8f4-af19a90d14c9",
                            "source": "cd2670ff-ec6a-450d-a501-f13ccc53c442",
                            "target": "94b8d8f8-25d5-4d91-80bb-4cb981c79018"},
                           {"id": "4b918b29-b0af-454e-9ca3-b2df6e414e2d",
                            "source": "94b8d8f8-25d5-4d91-80bb-4cb981c79018",
                            "target": "oval:ssg-test_accounts_passwords_pam_faillock_numeric_default_check_system-auth:tst:1"},
                           {"id": "d662d791-c6ce-4921-bb47-4cf7cdef829d",
                            "source": "94b8d8f8-25d5-4d91-80bb-4cb981c79018",
                            "target": "oval:ssg-test_accounts_passwords_pam_faillock_authfail_deny_system-auth:tst:1"},
                           {"id": "e8fd65b3-7727-4008-8e10-3a70a336a07c",
                            "source": "cd2670ff-ec6a-450d-a501-f13ccc53c442",
                            "target": "ddcfa90d-6b1f-4e93-9984-20cfec3f164c"},
                           {"id": "a18808f4-f0e5-431b-ab85-72ebf265d3b3",
                            "source": "ddcfa90d-6b1f-4e93-9984-20cfec3f164c",
                            "target": "oval:ssg-test_accounts_passwords_pam_faillock_numeric_default_check_password-auth:tst:1"},
                           {"id": "c9c4a710-fc36-499b-9539-c5f9668179b1",
                            "source": "ddcfa90d-6b1f-4e93-9984-20cfec3f164c",
                            "target": "oval:ssg-test_accounts_passwords_pam_faillock_authfail_deny_password-auth:tst:1"}]}
    src = 'data/ssg-fedora-ds-arf.xml'
    rule_id = 'xccdf_org.ssgproject.content_rule_accounts_passwords_pam_faillock_deny'
    result = 'false'

    out = []
    test = []
    oval_trees_array = tree.oval_tree.xml_to_tree(src)
    for oval_tree in oval_trees_array:
        if oval_tree.node_id == rule_id:
            out_data = oval_tree.to_sigma_dict(0, 0)
            for node_out in out_data['nodes']:
                out.append(node_out['label'])
            for node_test in test_data['nodes']:
                test.append(node_test['label'])
    assert out == test
