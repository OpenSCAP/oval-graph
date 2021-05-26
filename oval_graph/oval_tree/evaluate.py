"""
    Function for evaluate OVAL operators.
"""


def oval_operator_and(result):
    """The AND operator produces a true result if every argument is true. If one or more arguments
       are false, the result of the AND is false. If one or more of the arguments are unknown, and
       if none of the arguments are false, then the AND operator produces a result of unknown.

    Args:
            result (dict): Dictionary storing occurrence of given values

    Returns:
            str. return values::

                true
                false
                error
                unknown
                noteval
    """
    out_result = None
    eval_eq_zero = eq_zero(result, 'false_cnt')
    eval_greater_zero = greater_zero(result, 'true_cnt')
    if eval_eq_zero and eval_greater_zero and error_unknown_noteval_eq_zero(result):
        out_result = 'true'
    elif greater_zero(result, 'false_cnt'):
        out_result = 'false'
    else:
        out_result = error_unknown_noteval_for_operators_and_or(result, 'and')
    return out_result


def oval_operator_one(result):
    """The ONE operator produces a true result if one and only one argument is true. If there are
       more than argument is true (or if there are no true arguments), the result of the ONE
       is false. If one or more of the arguments are unknown, then the ONE operator produces
       a result of unknown.

    Args:
            result (dict): Dictionary storing occurrence of given values

    Returns:
            str. return values::

                true
                false
                error
                unknown
                noteval
    """
    out_result = None
    if one_is_true(result):
        out_result = 'true'
    elif one_is_false(result):
        out_result = 'false'
    elif one_is_error(result):
        out_result = 'error'
    elif one_is_unknown(result):
        out_result = 'unknown'
    elif one_is_noteval(result):
        out_result = 'noteval'
    return out_result


def oval_operator_or(result):
    """The OR operator produces a true result if one or more arguments is true. If every argument
       is false, the result of the OR is false. If one or more of the arguments are unknown and
       if none of arguments are true, then the OR operator produces a result of unknown.

    Args:
            result (dict): Dictionary storing occurrence of given values

    Returns:
            str. return values::

                true
                false
                error
                unknown
                noteval
    """
    out_result = None
    eval_eq_zero = eq_zero(result, 'true_cnt')
    eval_greater_zero = greater_zero(result, 'false_cnt')
    if greater_zero(result, 'true_cnt'):
        out_result = 'true'
    elif eval_eq_zero and eval_greater_zero and error_unknown_noteval_eq_zero(result):
        out_result = 'false'
    else:
        out_result = error_unknown_noteval_for_operators_and_or(result, 'or')
    return out_result


def oval_operator_xor(result):
    """XOR is defined to be true if an odd number of its arguments are true, and false otherwise.
       If any of the arguments are unknown, then the XOR operator produces a result of unknown.

    Args:
            result (dict): Dictionary storing occurrence of given values

    Returns:
            str. return values::

                true
                false
                error
                unknown
                noteval
    """
    out_result = None
    eval_error_cnt = eq_zero(result, 'error_cnt')
    eval_unknown_cnt = eq_zero(result, 'unknown_cnt')
    if (result['true_cnt'] % 2) == 1 and eq_zero_unknown_noteval_notappl(result):
        out_result = 'true'
    elif (result['true_cnt'] % 2) == 0 and eq_zero_unknown_noteval_notappl(result):
        out_result = 'false'
    elif greater_zero(result, 'error_cnt'):
        out_result = 'error'
    elif eq_zero(result, 'error_cnt') and greater_zero(result, 'unknown_cnt'):
        out_result = 'unknown'
    elif eval_error_cnt and eval_unknown_cnt and greater_zero(result, 'noteval_cnt'):
        out_result = 'noteval'
    return out_result


def error_unknown_noteval_for_operators_and_or(result, operator):
    """Evaluates if the result match the values for error, unknown, noteval.

    Args:
            result (dict): Dictionary storing occurrence of given values
            operator (str): Specifies for which operator is used

    Returns:
            str or None. return values::

                error
                unknown
                notappl
    """
    out_result = None
    value_for_check = 'false_cnt' if operator == 'and' else 'true_cnt'
    if eq_zero(result, value_for_check) and greater_zero(result, 'error_cnt'):
        out_result = 'error'
    elif eq_zero(result, value_for_check) and error_unknown_eq_zero(result):
        out_result = 'unknown'
    elif eq_zero(result, value_for_check) and error_unknown_eq_noteval_greater_zero(result):
        out_result = 'noteval'
    return out_result


def eq_zero(result, cnt):
    return result[cnt] == 0


def eq_zero_duo(result, cnt0, cnt1):
    return result[cnt0] == 0 and result[cnt1] == 0


def greater_zero(result, cnt):
    return result[cnt] > 0


def eq_or_greater_zero(result, cnt):
    return result[cnt] >= 0


def eq_or_greater_zero_duo(result, cnt0, cnt1):
    return result[cnt0] >= 0 and result[cnt1] >= 0


def smaller_than_two(result, cnt):
    return result[cnt] < 2


def one_is_noteval(result):
    """Evaluates if the result match noteval for one operator.

    Args:
            result (dict): Dictionary storing occurrence of given values

    Returns:
            bool.
    """
    true_cnt = smaller_than_two(result, 'true_cnt')
    false_cnt_notappl_cnt = eq_or_greater_zero_duo(result, 'false_cnt', 'notappl_cnt')
    error_cnt_unknown_cnt = eq_zero_duo(result, 'error_cnt', 'unknown_cnt')
    noteval_cnt = greater_zero(result, 'noteval_cnt')
    return true_cnt and false_cnt_notappl_cnt and error_cnt_unknown_cnt and noteval_cnt


def one_is_unknown(result):
    """Evaluates if the result match unknown for one operator.

    Args:
            result (dict): Dictionary storing occurrence of given values

    Returns:
            bool.
    """
    true_cnt = smaller_than_two(result, 'true_cnt')
    false_cnt = eq_or_greater_zero(result, 'false_cnt')
    error_cnt = eq_zero(result, 'error_cnt')
    unknown_cnt = result['unknown_cnt'] >= 1
    noteval_cnt_notappl_cnt = eq_or_greater_zero_duo(result, 'noteval_cnt', 'notappl_cnt')
    return true_cnt and false_cnt and error_cnt and unknown_cnt and noteval_cnt_notappl_cnt


def one_is_error(result):
    """Evaluates if the result match unknown for one operator.

    Args:
            result (dict): Dictionary storing occurrence of given values

    Returns:
            bool.
    """
    true_cnt = smaller_than_two(result, 'true_cnt')
    false_cnt = eq_or_greater_zero(result, 'false_cnt')
    error_cnt = greater_zero(result, 'error_cnt')
    unknown_noteval_notappl = eq_or_greater_zero_unknown_noteval_notappl(result)
    return true_cnt and false_cnt and error_cnt and unknown_noteval_notappl


def one_is_false(result):
    """Evaluates if the result match false for one operator.
       Operator ONE has two cases of false state.

    Args:
            result (dict): Dictionary storing occurrence of given values

    Returns:
            bool.
    """
    # The first case for false
    true_cnt = eq_zero(result, 'true_cnt')
    false_cnt = eq_or_greater_zero(result, 'false_cnt')
    unknown_noteval_cnt = error_unknown_noteval_eq_zero(result)
    notappl_cnt = result['notappl_cnt'] >= 0

    first_case = true_cnt and false_cnt and unknown_noteval_cnt and notappl_cnt

    # The second case for false
    true_cnt = result['true_cnt'] >= 2
    false_error_cnt = eq_or_greater_zero_duo(result, 'false_cnt', 'error_cnt')
    unknown_noteval_notappl = eq_or_greater_zero_unknown_noteval_notappl(result)
    second_case = true_cnt and false_error_cnt and unknown_noteval_notappl

    return first_case or second_case


def one_is_true(result):
    """Evaluates if the result match true for one operator.

    Args:
            result (dict): Dictionary storing occurrence of given values

    Returns:
            bool.
    """
    true_cnt = result['true_cnt'] == 1
    false_notappl_cnt = eq_or_greater_zero_duo(result, 'false_cnt', 'notappl_cnt')
    unknown_noteval_cnt = error_unknown_noteval_eq_zero(result)
    return true_cnt and false_notappl_cnt and unknown_noteval_cnt


def eq_or_greater_zero_unknown_noteval_notappl(result):
    unknown_cnt = eq_or_greater_zero(result, 'unknown_cnt')
    noteval_cnt = eq_or_greater_zero(result, 'noteval_cnt')
    notappl_cnt = eq_or_greater_zero(result, 'notappl_cnt')
    return unknown_cnt and notappl_cnt and noteval_cnt


def eq_zero_unknown_noteval_notappl(result):
    error_cnt = eq_zero(result, 'error_cnt')
    unknown_cnt = eq_zero(result, 'unknown_cnt')
    noteval_cnt = eq_zero(result, 'noteval_cnt')
    return error_cnt and unknown_cnt and noteval_cnt


def error_unknown_noteval_eq_zero(result):
    error_cnt = eq_zero(result, 'error_cnt')
    unknown_cnt = eq_zero(result, 'unknown_cnt')
    noteval_cnt = eq_zero(result, 'noteval_cnt')
    return error_cnt and unknown_cnt and noteval_cnt


def error_unknown_eq_noteval_greater_zero(result):
    error_cnt = eq_zero(result, 'error_cnt')
    unknown_cnt = eq_zero(result, 'unknown_cnt')
    noteval_cnt = greater_zero(result, 'noteval_cnt')
    return error_cnt and unknown_cnt and noteval_cnt


def error_unknown_eq_zero(result):
    return eq_zero(result, 'error_cnt') and greater_zero(result, 'unknown_cnt')


def is_notapp_result(result):
    """Evaluates if the counts of values in
       the result matches the notapp result.

    Args:
            result (dict): Dictionary storing occurrence of given values

    Returns:
            bool.
     """
    notappl_cnt = result['notappl_cnt'] > 0
    false_cnt = eq_zero(result, 'false_cnt')
    unknown_noteval_cnt = error_unknown_noteval_eq_zero(result)
    true_cnt = eq_zero(result, 'true_cnt')
    return notappl_cnt and false_cnt and unknown_noteval_cnt and true_cnt
