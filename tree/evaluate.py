"""
    Function for evaluate oval operators.
"""

def oval_operator_and(result):
    out_result = None
    if false_eq_zero(result)\
            and true_greater_zero(result)\
            and error_unknown_noteval_eq_zero(result):
        out_result = 'true'
    elif false_greater_zero(result):
        out_result = 'false'
    elif false_eq_zero(result)\
            and error_greater_zero(result):
        out_result = 'error'
    elif false_eq_zero(result)\
            and error_unknown_eq_zero(result):
        out_result = 'unknown'
    elif false_eq_zero(result)\
            and error_unknown_eq_noteval_greater_zero(result):
        out_result = 'noteval'
    else:
        out_result = None
    return out_result

def oval_operator_one(result):
    out_result = None
    if result['true_cnt'] == 1\
            and result['false_cnt'] >= 0\
            and error_eq_zero(result)\
            and unknown_eq_zero(result)\
            and noteval_eq_zero(result)\
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
    out_result = None
    if true_greater_zero(result):
        out_result = 'true'
    elif true_eq_zero(result)\
            and false_greater_zero(result)\
            and error_unknown_noteval_eq_zero(result):
        out_result = 'false'
    elif true_eq_zero(result)\
            and error_greater_zero(result):
        out_result = 'error'
    elif true_eq_zero(result)\
            and error_unknown_eq_zero(result):
        out_result = 'unknown'
    elif true_eq_zero(result)\
            and error_unknown_eq_noteval_greater_zero(result):
        out_result = 'noteval'
    else:
        out_result = None
    return out_result

def oval_operator_xor(result):
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
