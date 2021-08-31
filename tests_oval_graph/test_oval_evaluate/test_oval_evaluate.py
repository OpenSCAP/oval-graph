import json
from pathlib import Path

import pytest

from oval_graph.oval_tree.builder import Builder
from oval_graph.oval_tree.oval_result import OvalResult

BAD_RESULT_COUNTS = {
    "number_of_true": -1,
    "number_of_false": -1,
    "number_of_error": -1,
    "number_of_unknown": -1,
    "number_of_noteval": -1,
    "number_of_notappl": -1
}


RESULT_COUNTS_1 = {
    "number_of_true": 3,
    "number_of_false": 3,
    "number_of_error": 3,
    "number_of_unknown": 0,
    "number_of_noteval": -1,
    "number_of_notappl": 3
}


def get_path_to_data_source(data_source):
    directory = ''
    if data_source.startswith('AND'):
        directory = 'and'
    elif data_source.startswith('OR'):
        directory = 'or'
    elif data_source.startswith('XOR'):
        directory = 'xor'
    elif data_source.startswith('ONE'):
        directory = 'one'
    else:
        directory = 'NONE'

    return Path(__file__).parent / 'test_data' / directory / data_source


@pytest.mark.parametrize("data_source, expected_result", [
    ('ANDTreeTrue.json', "true"),
    ('ANDTreeFalse.json', 'false'),
    ('ANDTreeError.json', "error"),
    ('ANDTreeUnknown.json', "unknown"),
    ('ANDTreeNoteval.json', "noteval"),
    ("ANDTreeNotappl.json", 'notappl'),

    ('ONETreeTrue.json', "true"),
    ('ONETreeFalse.json', 'false'),
    ('ONETreeFalse1.json', 'false'),
    ('ONETreeError.json', "error"),
    ('ONETreeUnknown.json', "unknown"),
    ('ONETreeNoteval.json', "noteval"),
    ("ONETreeNotappl.json", 'notappl'),

    ('ORTreeTrue.json', "true"),
    ('ORTreeFalse.json', 'false'),
    ('ORTreeError.json', "error"),
    ('ORTreeUnknown.json', "unknown"),
    ('ORTreeNoteval.json', "noteval"),
    ("ORTreeNotappl.json", 'notappl'),

    ('XORTreeTrue.json', "true"),
    ('XORTreeFalse.json', 'false'),
    ('XORTreeError.json', "error"),
    ('XORTreeUnknown.json', "unknown"),
    ('XORTreeNoteval.json', "noteval"),
    ("XORTreeNotappl.json", 'notappl'),
])
def test_evaluation_of_oval_tree(data_source, expected_result):
    path = get_path_to_data_source(data_source)
    data = dict()
    with open(path, "r") as file_:
        data = json.load(file_)
    oval_tree = Builder.dict_to_oval_tree(data)
    assert oval_tree.evaluate_tree() == expected_result


@pytest.mark.parametrize("eval_function, result", [
    (OvalResult(**BAD_RESULT_COUNTS).eval_operator_and, None),
    (OvalResult(**BAD_RESULT_COUNTS).eval_operator_one, None),
    (OvalResult(**BAD_RESULT_COUNTS).eval_operator_or, None),
    (OvalResult(**BAD_RESULT_COUNTS).eval_operator_xor, None),
    (OvalResult(**RESULT_COUNTS_1).eval_operator_and, 'false'),
    (OvalResult(**RESULT_COUNTS_1).eval_operator_one, None),
    (OvalResult(**RESULT_COUNTS_1).eval_operator_or, 'true'),
    (OvalResult(**RESULT_COUNTS_1).eval_operator_xor, 'error'),
])
def test_evaluate_oval_result(eval_function, result):
    assert eval_function() is result
