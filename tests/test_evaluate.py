import pytest

import tests.any_test_help
from oval_graph.oval_tree.oval_result import OvalResult

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


@pytest.fixture
def oval_result():
    results_counts = {
        "number_of_true": -1,
        "number_of_false": -1,
        "number_of_error": -1,
        "number_of_unknown": -1,
        "number_of_noteval": -1,
        "number_of_notappl": -1
    }
    return OvalResult(**results_counts)


@pytest.fixture
def oval_result1():
    results_counts = {
        "number_of_true": 3,
        "number_of_false": 3,
        "number_of_error": 3,
        "number_of_unknown": 0,
        "number_of_noteval": -1,
        "number_of_notappl": 3
    }
    return OvalResult(**results_counts)


def test_bad_results_counts_for_operator_and(oval_result):
    assert oval_result.eval_operator_and() is None


def test_bad_results_counts_for_operator_one(oval_result):
    assert oval_result.eval_operator_one() is None


def test_bad_results_counts_for_operator_or(oval_result):
    assert oval_result.eval_operator_or() is None


def test_bad_results_counts_for_operator_xor(oval_result):
    assert oval_result.eval_operator_xor() is None


def test_false_eq_or_greater_zero_unknown_noteval_notappl(oval_result1):
    assert not oval_result1._unknown_noteval_notappl_ge_zero()


def test_false_error_unknown_eq_noteval_greater_zero(oval_result):
    assert not oval_result._error_unknown_eq_zero_and_noteval_ge_one()
