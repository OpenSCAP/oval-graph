"""
    Function for evaluate oval operators.
"""


def oval_operator_and(result):
    """
        The AND operator produces a true result if every argument is true. If one or more arguments are false, the result of the AND is false. If one or more of the arguments are unknown, and if none of the arguments are false, then the AND operator produces a result of unknown.
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
    elif eq_zero(result, 'true_cnt')\
            and result['false_cnt'] >= 0\
            and eq_zero(result, 'error_cnt')\
            and eq_zero(result, 'unknown_cnt')\
            and eq_zero(result, 'noteval_cnt')\
            and result['notappl_cnt'] >= 0:
        out_result = 'false'
    elif result['true_cnt'] < 2\
            and result['false_cnt'] >= 0\
            and greater_zero(result, 'error_cnt')\
            and result['unknown_cnt'] >= 0\
            and result['noteval_cnt'] >= 0\
            and result['notappl_cnt'] >= 0:
        out_result = 'error'
    elif result['true_cnt'] < 2\
            and result['false_cnt'] >= 0\
            and eq_zero(result, 'error_cnt')\
            and result['unknown_cnt'] >= 1\
            and result['noteval_cnt'] >= 0\
            and result['notappl_cnt'] >= 0:
        out_result = 'unknown'
    elif result['true_cnt'] < 2\
            and result['false_cnt'] >= 0\
            and eq_zero(result, 'error_cnt')\
            and eq_zero(result, 'unknown_cnt')\
            and greater_zero(result, 'noteval_cnt')\
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
        XOR is defined to be true if an odd number of its arguments are true, and false otherwise. If any of the arguments are unknown, then the XOR operator produces a result of unknown.
    """
    out_result = None
    if (result['true_cnt'] % 2) == 1\
            and eq_zero(result, 'error_cnt')\
            and eq_zero(result, 'unknown_cnt')\
            and eq_zero(result, 'noteval_cnt'):
        out_result = 'true'
    elif (result['true_cnt'] % 2) == 0\
            and eq_zero(result, 'error_cnt')\
            and eq_zero(result, 'unknown_cnt')\
            and eq_zero(result, 'noteval_cnt'):
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

def greater_zero(result, cnt):
    if result[cnt] > 0:
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