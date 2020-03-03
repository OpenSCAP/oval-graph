from oval_graph.oval_node import OvalNode
import oval_graph.evaluate
import tests.any_test_help


# AND operator


def test_ANDTreeTrue():
    tests.any_test_help.any_test_treeEvaluation(
        None, "true", 'ANDTreeTrue.json')


def test_ANDTreeFalse():
    tests.any_test_help.any_test_treeEvaluation(
        None, "false", 'ANDTreeFalse.json')


def test_ANDTreeError():
    tests.any_test_help.any_test_treeEvaluation(
        None, "error", 'ANDTreeError.json')


def test_ANDTreeUnknown():
    tests.any_test_help.any_test_treeEvaluation(
        None, "unknown", 'ANDTreeUnknown.json')


def test_ANDTreeNoteval():
    tests.any_test_help.any_test_treeEvaluation(
        None, "noteval", 'ANDTreeNoteval.json')


def test_ANDTreeNotappl():
    tests.any_test_help.any_test_treeEvaluation(
        None, "notappl", 'ANDTreeNotappl.json')

# ONE operator


def test_ONETreeTrue():
    tests.any_test_help.any_test_treeEvaluation(
        None, "true", 'ONETreeTrue.json')


def test_ONETreeFalse():
    tests.any_test_help.any_test_treeEvaluation(
        None, "false", 'ONETreeFalse.json')


def test_ONETreeFalse1():
    tests.any_test_help.any_test_treeEvaluation(
        None, "false", 'ONETreeFalse1.json')


def test_ONETreeError():
    tests.any_test_help.any_test_treeEvaluation(
        None, "error", 'ONETreeError.json')


def test_ONETreeUnknown():
    tests.any_test_help.any_test_treeEvaluation(
        None, "unknown", 'ONETreeUnknown.json')


def test_ONETreeNoteval():
    tests.any_test_help.any_test_treeEvaluation(
        None, "noteval", 'ONETreeNoteval.json')


def test_ONETreeNotappl():
    tests.any_test_help.any_test_treeEvaluation(
        None, "notappl", 'ONETreeNotappl.json')

# OR operator


def test_ORTreeTrue():
    tests.any_test_help.any_test_treeEvaluation(
        None, "true", 'ORTreeTrue.json')


def test_ORTreeFalse():
    tests.any_test_help.any_test_treeEvaluation(
        None, "false", 'ORTreeFalse.json')


def test_ORTreeError():
    tests.any_test_help.any_test_treeEvaluation(
        None, "error", 'ORTreeError.json')


def test_ORTreeUnknown():
    tests.any_test_help.any_test_treeEvaluation(
        None, "unknown", 'ORTreeUnknown.json')


def test_ORTreeNoteval():
    tests.any_test_help.any_test_treeEvaluation(
        None, "noteval", 'ORTreeNoteval.json')


def test_ORTreeNotappl():
    tests.any_test_help.any_test_treeEvaluation(
        None, "notappl", 'ORTreeNotappl.json')

# XOR operator


def test_XORTreeTrue():
    tests.any_test_help.any_test_treeEvaluation(
        None, "true", 'XORTreeTrue.json')


def test_XORTreeFalse():
    tests.any_test_help.any_test_treeEvaluation(
        None, "false", 'XORTreeFalse.json')


def test_XORTreeError():
    tests.any_test_help.any_test_treeEvaluation(
        None, "error", 'XORTreeError.json')


def test_XORTreeUnknown():
    tests.any_test_help.any_test_treeEvaluation(
        None, "unknown", 'XORTreeUnknown.json')


def test_XORTreeNoteval():
    tests.any_test_help.any_test_treeEvaluation(
        None, "noteval", 'XORTreeNoteval.json')


def test_XORTreeNotappl():
    tests.any_test_help.any_test_treeEvaluation(
        None, "notappl", 'XORTreeNotappl.json')


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


def test_bad_results_counts_for_operator_and():
    assert oval_graph.evaluate.oval_operator_and(results_counts) is None


def test_bad_results_counts_for_operator_one():
    assert oval_graph.evaluate.oval_operator_one(results_counts) is None


def test_bad_results_counts_for_operator_or():
    assert oval_graph.evaluate.oval_operator_or(results_counts) is None


def test_bad_results_counts_for_operator_xor():
    assert oval_graph.evaluate.oval_operator_xor(results_counts) is None


def test_false_noteval_greater_zero():
    assert not oval_graph.evaluate.greater_zero(results_counts, 'noteval_cnt')


def test_false_smaller_then_two():
    assert not oval_graph.evaluate.smaller_than_two(
        results_counts1, 'true_cnt')


def test_false_eq_zero_duo():
    assert not oval_graph.evaluate.eq_zero_duo(
        results_counts, 'noteval_cnt', 'error_cnt')


def test_false_eq_or_greater_zero_unknown_noteval_notappl():
    assert not oval_graph.evaluate.eq_or_greater_zero_unknown_noteval_notappl(
        results_counts1)


def test_false_error_unknown_eq_noteval_greater_zero():
    assert not oval_graph.evaluate.error_unknown_eq_noteval_greater_zero(
        results_counts)
