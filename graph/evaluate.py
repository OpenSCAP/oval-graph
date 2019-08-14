"""
    Function for evaluate oval operators.
"""


def oval_operator_and(result):
    """
        The AND operator produces a true result if every argument is true. If one or more arguments
        are false, the result of the AND is false. If one or more of the arguments are unknown, and
        if none of the arguments are false, then the AND operator produces a result of unknown.
    """
    out_result = None
    if eq_zero(result, 'false_cnt')\
            and greater_zero(result, 'true_cnt')\
            and error_unknown_noteval_eq_zero(result):
        out_result = 'true'
    elif greater_zero(result, 'false_cnt'):
        out_result = 'false'
    else:
        out_result = error_unknown_noteval_for_operators_and_or(result, 'and')
    return out_result


def oval_operator_one(result):
    """
        The ONE operator produces a true result if one and only one argument is true. If there are
        more than argument is true (or if there are no true arguments), the result of the ONE
        is false. If one or more of the arguments are unknown, then the ONE operator produces
        a result of unknown.
    """
    out_result = None
    if one_is_true(result):
        out_result = 'true'
    elif one_is_false(result) or one_is_false1(result):
        out_result = 'false'
    elif one_is_error(result):
        out_result = 'error'
    elif one_is_unknown(result):
        out_result = 'unknown'
    elif one_is_noteval(result):
        out_result = 'noteval'
    else:
        out_result = None
    return out_result


def oval_operator_or(result):
    """
        The OR operator produces a true result if one or more arguments is true. If every argument
        is false, the result of the OR is false. If one or more of the arguments are unknown and
        if none of arguments are true, then the OR operator produces a result of unknown.
    """
    out_result = None
    if greater_zero(result, 'true_cnt'):
        out_result = 'true'
    elif eq_zero(result, 'true_cnt')\
            and greater_zero(result, 'false_cnt')\
            and error_unknown_noteval_eq_zero(result):
        out_result = 'false'
    else:
        out_result = error_unknown_noteval_for_operators_and_or(result, 'or')
    return out_result


def oval_operator_xor(result):
    """
        XOR is defined to be true if an odd number of its arguments are true, and false otherwise.
        If any of the arguments are unknown, then the XOR operator produces a result of unknown.
    """
    out_result = None
    if (result['true_cnt'] % 2) == 1\
            and eq_zero_unknown_noteval_notappl(result):
        out_result = 'true'
    elif (result['true_cnt'] % 2) == 0\
            and eq_zero_unknown_noteval_notappl(result):
        out_result = 'false'
    elif greater_zero(result, 'error_cnt'):
        out_result = 'error'
    elif eq_zero(result, 'error_cnt')\
            and greater_zero(result, 'unknown_cnt'):
        out_result = 'unknown'
    elif eq_zero(result, 'error_cnt')\
            and eq_zero(result, 'unknown_cnt')\
            and greater_zero(result, 'noteval_cnt'):
        out_result = 'noteval'
    else:
        out_result = None
    return out_result


def error_unknown_noteval_for_operators_and_or(result, operator):
    out_result = None
    if and_or_eq_zero(operator, result)\
            and greater_zero(result, 'error_cnt'):
        out_result = 'error'
    elif and_or_eq_zero(operator, result)\
            and error_unknown_eq_zero(result):
        out_result = 'unknown'
    elif and_or_eq_zero(operator, result)\
            and error_unknown_eq_noteval_greater_zero(result):
        out_result = 'noteval'
    else:
        out_result = None
    return out_result


def and_or_eq_zero(operator, result):
    if operator == 'and':
        return eq_zero(result, 'false_cnt')
    if operator == 'or':
        return eq_zero(result, 'true_cnt')
    return None


def eq_zero(result, cnt):
    if result[cnt] == 0:
        return True
    return False


def eq_zero_duo(result, cnt0, cnt1):
    if result[cnt0] == 0 and result[cnt1] == 0:
        return True
    return False


def greater_zero(result, cnt):
    if result[cnt] > 0:
        return True
    return False


def eq_or_greater_zero(result, cnt):
    if result[cnt] >= 0:
        return True
    return False


def eq_or_greater_zero_duo(result, cnt0, cnt1):
    if result[cnt0] >= 0 and result[cnt1] >= 0:
        return True
    return False


def smaller_than_two(result, cnt):
    if result[cnt] < 2:
        return True
    return False


def one_is_noteval(result):
    if smaller_than_two(result, 'true_cnt')\
            and eq_or_greater_zero_duo(result, 'false_cnt', 'notappl_cnt')\
            and eq_zero_duo(result, 'error_cnt', 'unknown_cnt')\
            and greater_zero(result, 'noteval_cnt'):
        return True
    return False


def one_is_unknown(result):
    if smaller_than_two(result, 'true_cnt')\
            and eq_or_greater_zero(result, 'false_cnt')\
            and eq_zero(result, 'error_cnt')\
            and result['unknown_cnt'] >= 1\
            and eq_or_greater_zero_duo(result, 'noteval_cnt', 'notappl_cnt'):
        return True
    return False


def one_is_error(result):
    if smaller_than_two(result, 'true_cnt')\
            and eq_or_greater_zero(result, 'false_cnt')\
            and greater_zero(result, 'error_cnt')\
            and eq_or_greater_zero_unknown_noteval_notappl(result):
        return True
    return False


def one_is_false(result):
    if eq_zero(result, 'true_cnt')\
            and eq_or_greater_zero(result, 'false_cnt')\
            and error_unknown_noteval_eq_zero(result)\
            and result['notappl_cnt'] >= 0:
        return True
    return False


def one_is_false1(result):
    if result['true_cnt'] >= 2\
            and eq_or_greater_zero_duo(result, 'false_cnt', 'error_cnt')\
            and eq_or_greater_zero_unknown_noteval_notappl(result):
        return True
    return False


def one_is_true(result):
    if result['true_cnt'] == 1\
            and eq_or_greater_zero_duo(result, 'false_cnt', 'notappl_cnt')\
            and error_unknown_noteval_eq_zero(result):
        return True
    return False


def eq_or_greater_zero_unknown_noteval_notappl(result):
    if eq_or_greater_zero(result, 'unknown_cnt')\
            and eq_or_greater_zero(result, 'noteval_cnt')\
            and eq_or_greater_zero(result, 'notappl_cnt'):
        return True
    return False


def eq_zero_unknown_noteval_notappl(result):
    if eq_zero(result, 'error_cnt')\
            and eq_zero(result, 'unknown_cnt')\
            and eq_zero(result, 'noteval_cnt'):
        return True
    return False


def error_unknown_noteval_eq_zero(result):
    if eq_zero(result, 'error_cnt')\
            and eq_zero(result, 'unknown_cnt')\
            and eq_zero(result, 'noteval_cnt'):
        return True
    return False


def error_unknown_eq_noteval_greater_zero(result):
    if eq_zero(result, 'error_cnt')\
            and eq_zero(result, 'unknown_cnt')\
            and greater_zero(result, 'noteval_cnt'):
        return True
    return False


def error_unknown_eq_zero(result):
    if eq_zero(result, 'error_cnt')\
            and greater_zero(result, 'unknown_cnt'):
        return True
    return False


def is_notapp_result(result):
    if (result['notappl_cnt'] > 0
            and eq_zero(result, 'false_cnt')
            and error_unknown_noteval_eq_zero(result)
            and eq_zero(result, 'true_cnt')):
        return True
    return False
