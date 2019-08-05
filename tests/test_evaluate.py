import graph.oval_graph
import tests.any_test_help


# AND operator


def test_ANDTreeTrue():
    Tree = graph.oval_graph.OvalNode(1, 'operator', 'and', [
        graph.oval_graph.OvalNode(2, 'value', "true"),
        graph.oval_graph.OvalNode(3, 'value', "true"),
        graph.oval_graph.OvalNode(4, 'value', "notappl")
    ]
    )

    tests.any_test_help.any_test_treeEvaluation(Tree, "true")


def test_ANDTreeFalse():
    Tree = graph.oval_graph.OvalNode(1, 'operator', 'and', [
        graph.oval_graph.OvalNode(2, 'value', "false"),
        graph.oval_graph.OvalNode(3, 'value', "false"),

        graph.oval_graph.OvalNode(4, 'value', "true"),
        graph.oval_graph.OvalNode(5, 'value', "error"),
        graph.oval_graph.OvalNode(6, 'value', "unknown"),
        graph.oval_graph.OvalNode(7, 'value', "noteval"),
        graph.oval_graph.OvalNode(8, 'value', "notappl")
    ]
    )

    tests.any_test_help.any_test_treeEvaluation(Tree, "false")


def test_ANDTreeError():
    Tree = graph.oval_graph.OvalNode(1, 'operator', 'and', [
        graph.oval_graph.OvalNode(2, 'value', "error"),
        graph.oval_graph.OvalNode(3, 'value', "error"),
        graph.oval_graph.OvalNode(4, 'value', "true"),
        graph.oval_graph.OvalNode(5, 'value', "unknown"),
        graph.oval_graph.OvalNode(6, 'value', "noteval"),
        graph.oval_graph.OvalNode(7, 'value', "notappl"),
        graph.oval_graph.OvalNode(8, 'value', "error")
    ])

    tests.any_test_help.any_test_treeEvaluation(Tree, "error")


def test_ANDTreeUnknown():
    Tree = graph.oval_graph.OvalNode(1, 'operator', 'and', [
        graph.oval_graph.OvalNode(2, 'value', "unknown"),
        graph.oval_graph.OvalNode(3, 'value', "unknown"),
        graph.oval_graph.OvalNode(4, 'value', "true"),
        graph.oval_graph.OvalNode(5, 'value', "unknown"),
        graph.oval_graph.OvalNode(6, 'value', "noteval"),
        graph.oval_graph.OvalNode(7, 'value', "notappl"),
        graph.oval_graph.OvalNode(8, 'value', "notappl")
    ]
    )

    tests.any_test_help.any_test_treeEvaluation(Tree, "unknown")


def test_ANDTreeNoteval():
    Tree = graph.oval_graph.OvalNode(1, 'operator', 'and', [
        graph.oval_graph.OvalNode(2, 'value', "noteval"),
        graph.oval_graph.OvalNode(3, 'value', "noteval"),
        graph.oval_graph.OvalNode(4, 'value', "true"),
        graph.oval_graph.OvalNode(5, 'value', "true"),
        graph.oval_graph.OvalNode(6, 'value', "noteval"),
        graph.oval_graph.OvalNode(7, 'value', "notappl"),
        graph.oval_graph.OvalNode(8, 'value', "notappl")
    ]
    )

    tests.any_test_help.any_test_treeEvaluation(Tree, "noteval")


def test_ANDTreeNotappl():
    Tree = graph.oval_graph.OvalNode(1, 'operator', 'and', [
        graph.oval_graph.OvalNode(2, 'value', "notappl"),
        graph.oval_graph.OvalNode(3, 'value', "notappl"),
        graph.oval_graph.OvalNode(4, 'value', "notappl")
    ]
    )

    tests.any_test_help.any_test_treeEvaluation(Tree, "notappl")

# ONE operator


def test_ONETreeTrue():
    Tree = graph.oval_graph.OvalNode(1, 'operator', 'one', [
        graph.oval_graph.OvalNode(2, 'value', "true"),
        graph.oval_graph.OvalNode(3, 'value', "false"),
        graph.oval_graph.OvalNode(4, 'value', "notappl"),
        graph.oval_graph.OvalNode(5, 'value', "false")
    ]
    )

    tests.any_test_help.any_test_treeEvaluation(Tree, "true")


def test_ONETreeFalse():
    Tree = graph.oval_graph.OvalNode(1, 'operator', 'one', [
        graph.oval_graph.OvalNode(2, 'value', "true"),
        graph.oval_graph.OvalNode(3, 'value', "true"),

        graph.oval_graph.OvalNode(4, 'value', "false"),
        graph.oval_graph.OvalNode(5, 'value', "error"),
        graph.oval_graph.OvalNode(6, 'value', "unknown"),
        graph.oval_graph.OvalNode(7, 'value', "noteval"),
        graph.oval_graph.OvalNode(8, 'value', "notappl")
    ]
    )

    tests.any_test_help.any_test_treeEvaluation(Tree, "false")


def test_ONETreeFalse1():
    Tree = graph.oval_graph.OvalNode(1, 'operator', 'one', [
        graph.oval_graph.OvalNode(2, 'value', "false"),
        graph.oval_graph.OvalNode(3, 'value', "false"),
        graph.oval_graph.OvalNode(4, 'value', "notappl")
    ]
    )

    tests.any_test_help.any_test_treeEvaluation(Tree, "false")


def test_ONETreeError():
    Tree = graph.oval_graph.OvalNode(1, 'operator', 'one', [
        graph.oval_graph.OvalNode(2, 'value', "error"),
        graph.oval_graph.OvalNode(3, 'value', "error"),
        graph.oval_graph.OvalNode(4, 'value', "true"),
        graph.oval_graph.OvalNode(5, 'value', "unknown"),
        graph.oval_graph.OvalNode(6, 'value', "noteval"),
        graph.oval_graph.OvalNode(7, 'value', "notappl"),
        graph.oval_graph.OvalNode(8, 'value', "false")
    ]
    )

    tests.any_test_help.any_test_treeEvaluation(Tree, "error")


def test_ONETreeUnknown():
    Tree = graph.oval_graph.OvalNode(1, 'operator', 'one', [
        graph.oval_graph.OvalNode(2, 'value', "unknown"),
        graph.oval_graph.OvalNode(3, 'value', "unknown"),
        graph.oval_graph.OvalNode(4, 'value', "true"),
        graph.oval_graph.OvalNode(5, 'value', "unknown"),
        graph.oval_graph.OvalNode(6, 'value', "noteval"),
        graph.oval_graph.OvalNode(7, 'value', "notappl"),
        graph.oval_graph.OvalNode(8, 'value', "false")
    ])

    tests.any_test_help.any_test_treeEvaluation(Tree, "unknown")


def test_ONETreeNoteval():
    Tree = graph.oval_graph.OvalNode(1, 'operator', 'one', [
        graph.oval_graph.OvalNode(2, 'value', "noteval"),
        graph.oval_graph.OvalNode(3, 'value', "noteval"),
        graph.oval_graph.OvalNode(4, 'value', "true"),
        graph.oval_graph.OvalNode(5, 'value', "false"),
        graph.oval_graph.OvalNode(6, 'value', "noteval"),
        graph.oval_graph.OvalNode(7, 'value', "notappl"),
        graph.oval_graph.OvalNode(8, 'value', "notappl")
    ]
    )

    tests.any_test_help.any_test_treeEvaluation(Tree, "noteval")


def test_ONETreeNotappl():
    Tree = graph.oval_graph.OvalNode(1, 'operator', 'one', [
        graph.oval_graph.OvalNode(2, 'value', "notappl"),
        graph.oval_graph.OvalNode(3, 'value', "notappl"),
        graph.oval_graph.OvalNode(4, 'value', "notappl")
    ]
    )

    tests.any_test_help.any_test_treeEvaluation(Tree, "notappl")

# OR operator


def test_ORTreeTrue():
    Tree = graph.oval_graph.OvalNode(1, 'operator', 'or', [
        graph.oval_graph.OvalNode(2, 'value', "true"),
        graph.oval_graph.OvalNode(3, 'value', "false"),

        graph.oval_graph.OvalNode(4, 'value', "true"),
        graph.oval_graph.OvalNode(5, 'value', "error"),
        graph.oval_graph.OvalNode(6, 'value', "unknown"),
        graph.oval_graph.OvalNode(7, 'value', "noteval"),
        graph.oval_graph.OvalNode(8, 'value', "notappl")
    ]
    )

    tests.any_test_help.any_test_treeEvaluation(Tree, "true")


def test_ORTreeFalse():
    Tree = graph.oval_graph.OvalNode(1, 'operator', 'or', [
        graph.oval_graph.OvalNode(2, 'value', "false"),
        graph.oval_graph.OvalNode(3, 'value', "false"),
        graph.oval_graph.OvalNode(4, 'value', "notappl")
    ]
    )

    tests.any_test_help.any_test_treeEvaluation(Tree, "false")


def test_ORTreeError():
    Tree = graph.oval_graph.OvalNode(1, 'operator', 'or', [
        graph.oval_graph.OvalNode(2, 'value', "error"),
        graph.oval_graph.OvalNode(3, 'value', "error"),
        graph.oval_graph.OvalNode(4, 'value', "false"),
        graph.oval_graph.OvalNode(5, 'value', "unknown"),
        graph.oval_graph.OvalNode(6, 'value', "noteval"),
        graph.oval_graph.OvalNode(7, 'value', "notappl"),
        graph.oval_graph.OvalNode(8, 'value', "error")
    ]
    )

    tests.any_test_help.any_test_treeEvaluation(Tree, "error")


def test_ORTreeUnknown():
    Tree = graph.oval_graph.OvalNode(1, 'operator', 'or', [
        graph.oval_graph.OvalNode(2, 'value', "unknown"),
        graph.oval_graph.OvalNode(3, 'value', "unknown"),
        graph.oval_graph.OvalNode(4, 'value', "false"),
        graph.oval_graph.OvalNode(5, 'value', "unknown"),
        graph.oval_graph.OvalNode(6, 'value', "noteval"),
        graph.oval_graph.OvalNode(7, 'value', "notappl"),
        graph.oval_graph.OvalNode(8, 'value', "notappl")
    ]
    )

    tests.any_test_help.any_test_treeEvaluation(Tree, "unknown")


def test_ORTreeNoteval():
    Tree = graph.oval_graph.OvalNode(1, 'operator', 'or', [
        graph.oval_graph.OvalNode(2, 'value', "noteval"),
        graph.oval_graph.OvalNode(3, 'value', "noteval"),
        graph.oval_graph.OvalNode(4, 'value', "false"),
        graph.oval_graph.OvalNode(5, 'value', "false"),
        graph.oval_graph.OvalNode(6, 'value', "noteval"),
        graph.oval_graph.OvalNode(7, 'value', "notappl"),
        graph.oval_graph.OvalNode(8, 'value', "notappl")
    ]
    )

    tests.any_test_help.any_test_treeEvaluation(Tree, "noteval")


def test_ORTreeNotappl():
    Tree = graph.oval_graph.OvalNode(1, 'operator', 'or', [
        graph.oval_graph.OvalNode(2, 'value', "notappl"),
        graph.oval_graph.OvalNode(3, 'value', "notappl"),
        graph.oval_graph.OvalNode(4, 'value', "notappl")
    ]
    )

    tests.any_test_help.any_test_treeEvaluation(Tree, "notappl")

# XOR operator


def test_XORTreeTrue():
    Tree = graph.oval_graph.OvalNode(1, 'operator', 'xor', [
        graph.oval_graph.OvalNode(2, 'value', "true"),
        graph.oval_graph.OvalNode(3, 'value', "false"),

        graph.oval_graph.OvalNode(4, 'value', "false"),
        graph.oval_graph.OvalNode(5, 'value', "false"),
        graph.oval_graph.OvalNode(6, 'value', "true"),
        graph.oval_graph.OvalNode(7, 'value', "true"),
        graph.oval_graph.OvalNode(8, 'value', "notappl")
    ]
    )

    tests.any_test_help.any_test_treeEvaluation(Tree, "true")


def test_XORTreeFalse():
    Tree = graph.oval_graph.OvalNode(1, 'operator', 'xor', [
        graph.oval_graph.OvalNode(2, 'value', "true"),
        graph.oval_graph.OvalNode(3, 'value', "false"),

        graph.oval_graph.OvalNode(4, 'value', "false"),
        graph.oval_graph.OvalNode(5, 'value', "true"),
        graph.oval_graph.OvalNode(6, 'value', "true"),
        graph.oval_graph.OvalNode(7, 'value', "true"),
        graph.oval_graph.OvalNode(8, 'value', "notappl")
    ]
    )

    tests.any_test_help.any_test_treeEvaluation(Tree, "false")


def test_XORTreeError():
    Tree = graph.oval_graph.OvalNode(1, 'operator', 'xor', [
        graph.oval_graph.OvalNode(2, 'value', "error"),
        graph.oval_graph.OvalNode(3, 'value', "error"),
        graph.oval_graph.OvalNode(4, 'value', "true"),
        graph.oval_graph.OvalNode(5, 'value', "unknown"),
        graph.oval_graph.OvalNode(6, 'value', "noteval"),
        graph.oval_graph.OvalNode(7, 'value', "notappl"),
        graph.oval_graph.OvalNode(8, 'value', "false")
    ]
    )

    tests.any_test_help.any_test_treeEvaluation(Tree, "error")


def test_xORTreeUnknown():
    Tree = graph.oval_graph.OvalNode(1, 'operator', 'xor', [
        graph.oval_graph.OvalNode(2, 'value', "unknown"),
        graph.oval_graph.OvalNode(3, 'value', "unknown"),
        graph.oval_graph.OvalNode(4, 'value', "true"),
        graph.oval_graph.OvalNode(5, 'value', "unknown"),
        graph.oval_graph.OvalNode(6, 'value', "noteval"),
        graph.oval_graph.OvalNode(7, 'value', "notappl"),
        graph.oval_graph.OvalNode(8, 'value', "notappl")
    ]
    )

    tests.any_test_help.any_test_treeEvaluation(Tree, "unknown")


def test_XORTreeNoteval():
    Tree = graph.oval_graph.OvalNode(1, 'operator', 'xor', [
        graph.oval_graph.OvalNode(2, 'value', "noteval"),
        graph.oval_graph.OvalNode(3, 'value', "noteval"),
        graph.oval_graph.OvalNode(4, 'value', "true"),
        graph.oval_graph.OvalNode(5, 'value', "true"),
        graph.oval_graph.OvalNode(6, 'value', "noteval"),
        graph.oval_graph.OvalNode(7, 'value', "notappl"),
        graph.oval_graph.OvalNode(8, 'value', "notappl")
    ]
    )

    tests.any_test_help.any_test_treeEvaluation(Tree, "noteval")


def test_XORTreeNotappl():
    Tree = graph.oval_graph.OvalNode(1, 'operator', 'xor', [
        graph.oval_graph.OvalNode(2, 'value', "notappl"),
        graph.oval_graph.OvalNode(3, 'value', "notappl"),
        graph.oval_graph.OvalNode(4, 'value', "notappl")
    ]
    )

    tests.any_test_help.any_test_treeEvaluation(Tree, "notappl")

results_counts = {
    'true_cnt': -1,
    'false_cnt': -1,
    'error_cnt': -1,
    'unknown_cnt': -1,
    'noteval_cnt': -1,
    'notappl_cnt': -1
}

results_counts1 = {
    'true_cnt': 3,
    'false_cnt': 3,
    'error_cnt': 3,
    'unknown_cnt': 0,
    'noteval_cnt': -1,
    'notappl_cnt': 3
}

def test_and_or_eq_zero():
    assert graph.evaluate.and_or_eq_zero('and', results_counts) == False
    assert graph.evaluate.and_or_eq_zero('or', results_counts) == False
    assert graph.evaluate.and_or_eq_zero('xor', results_counts) is None

def test_bad_results_counts_for_operator_and():
    assert graph.evaluate.oval_operator_and(results_counts) is None


def test_bad_results_counts_for_operator_one():
    assert graph.evaluate.oval_operator_one(results_counts) is None


def test_bad_results_counts_for_operator_or():
    assert graph.evaluate.oval_operator_or(results_counts) is None


def test_bad_results_counts_for_operator_xor():
    assert graph.evaluate.oval_operator_xor(results_counts) is None


def test_false_noteval_greater_zero():
    assert graph.evaluate.greater_zero(results_counts, 'noteval_cnt') == False


def test_false_smaller_then_two():
    assert graph.evaluate.smaller_than_two(
        results_counts1, 'true_cnt') == False


def test_false_eq_or_greater_zero_unknown_noteval_notappl():
    assert graph.evaluate.eq_or_greater_zero_unknown_noteval_notappl(
        results_counts1) == False


def test_false_error_unknown_eq_noteval_greater_zero():
    assert graph.evaluate.error_unknown_eq_noteval_greater_zero(
        results_counts) == False
