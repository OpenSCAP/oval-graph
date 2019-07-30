"""
    Function for evaluate oval operators.
"""


def oval_operator_and(result):
    """
        The AND operator produces a true result if every argument is true. If one or more arguments are false, the result of the AND is false. If one or more of the arguments are unknown, and if none of the arguments are false, then the AND operator produces a result of unknown.
    """
    out_result = None
    if false_eq_zero(result)\
            and true_greater_zero(result)\
            and error_unknown_noteval_eq_zero(result):
        out_result = 'true'
    elif false_greater_zero(result):
        out_result = 'false'
    else:
        out_result = error_unknown_noteval_for_operators_and_or(result, 'and')
    return out_result


def oval_operator_one(result):
    """
        The ONE operator produces a true result if one and only one argument is true. If there are more than argument is true (or if there are no true arguments), the result of the ONE is false. If one or more of the arguments are unknown, then the ONE operator produces a result of unknown.
    """
    out_result = None
    if result['true_cnt'] == 1\
            and result['false_cnt'] >= 0\
            and error_unknown_noteval_eq_zero(result)\
            and result['notappl_cnt'] >= 0:
        out_result = 'true'
    elif result['true_cnt'] >= 2\
            and result['false_cnt'] >= 0\
            and result['error_cnt'] >= 0\
            and result['unknown_cnt'] >= 0\
            and result['noteval_cnt'] >= 0\
            and result['notappl_cnt'] >= 0:
        out_result = 'false'
    elif true_eq_zero(result)\
            and result['false_cnt'] >= 0\
            and error_eq_zero(result)\
            and unknown_eq_zero(result)\
            and noteval_eq_zero(result)\
            and result['notappl_cnt'] >= 0:
        out_result = 'false'
    elif result['true_cnt'] < 2\
            and result['false_cnt'] >= 0\
            and error_greater_zero(result)\
            and result['unknown_cnt'] >= 0\
            and result['noteval_cnt'] >= 0\
            and result['notappl_cnt'] >= 0:
        out_result = 'error'
    elif result['true_cnt'] < 2\
            and result['false_cnt'] >= 0\
            and error_eq_zero(result)\
            and result['unknown_cnt'] >= 1\
            and result['noteval_cnt'] >= 0\
            and result['notappl_cnt'] >= 0:
        out_result = 'unknown'
    elif result['true_cnt'] < 2\
            and result['false_cnt'] >= 0\
            and error_eq_zero(result)\
            and unknown_eq_zero(result)\
            and noteval_greater_zero(result)\
            and result['notappl_cnt'] >= 0:
        out_result = 'noteval'
    else:
        out_result = None
    return out_result


def oval_operator_or(result):
    """
        The OR operator produces a true result if one or more arguments is true. If every argument is false, the result of the OR is false. If one or more of the arguments are unknown and if none of arguments are true, then the OR operator produces a result of unknown.
    """
    out_result = None
    if true_greater_zero(result):
        out_result = 'true'
    elif true_eq_zero(result)\
            and false_greater_zero(result)\
            and error_unknown_noteval_eq_zero(result):
        out_result = 'false'
    else:
        out_result = error_unknown_noteval_for_operators_and_or(result, 'or')
    return out_result


def oval_operator_xor(result):
    """
        XOR is defined to be true if an odd number of its arguments are true, and false otherwise. If any of the arguments are unknown, then the XOR operator produces a result of unknown.
    """
    out_result = None
    if (result['true_cnt'] % 2) == 1\
            and error_eq_zero(result)\
            and unknown_eq_zero(result)\
            and noteval_eq_zero(result):
        out_result = 'true'
    elif (result['true_cnt'] % 2) == 0\
            and error_eq_zero(result)\
            and unknown_eq_zero(result)\
            and noteval_eq_zero(result):
        out_result = 'false'
    elif error_greater_zero(result):
        out_result = 'error'
    elif error_eq_zero(result)\
            and unknown_greater_zero(result):
        out_result = 'unknown'
    elif error_eq_zero(result)\
            and unknown_eq_zero(result)\
            and noteval_greater_zero(result):
        out_result = 'noteval'
    else:
        out_result = None
    return out_result


def error_unknown_noteval_for_operators_and_or(result, operator):
    out_result = None
    if and_or_eq_zero(operator, result)\
            and error_greater_zero(result):
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
        return false_eq_zero(result)
    if operator == 'or':
        return true_eq_zero(result)
    return None


def noteval_eq_zero(result):
    if result['noteval_cnt'] == 0:
        return True
    return False


def false_eq_zero(result):
    if result['false_cnt'] == 0:
        return True
    return False


def error_eq_zero(result):
    if result['error_cnt'] == 0:
        return True
    return False


def unknown_eq_zero(result):
    if result['unknown_cnt'] == 0:
        return True
    return False


def true_eq_zero(result):
    if result['true_cnt'] == 0:
        return True
    return False


def true_greater_zero(result):
    if result['true_cnt'] > 0:
        return True
    return False


def false_greater_zero(result):
    if result['false_cnt'] > 0:
        return True
    return False


def error_greater_zero(result):
    if result['error_cnt'] > 0:
        return True
    return False


def unknown_greater_zero(result):
    if result['unknown_cnt'] > 0:
        return True
    return False


def noteval_greater_zero(result):
    if result['noteval_cnt'] > 0:
        return True
    return False


def error_unknown_noteval_eq_zero(result):
    if error_eq_zero(result)\
            and unknown_eq_zero(result)\
            and noteval_eq_zero(result):
        return True
    return False


def error_unknown_eq_noteval_greater_zero(result):
    if error_eq_zero(result)\
            and unknown_eq_zero(result)\
            and noteval_greater_zero(result):
        return True
    return False


def error_unknown_eq_zero(result):
    if error_eq_zero(result)\
            and unknown_greater_zero(result):
        return True
    return False
