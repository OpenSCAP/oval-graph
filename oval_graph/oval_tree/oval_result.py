from typing import NamedTuple


class OvalResult(NamedTuple):
    number_of_true: int = 0
    number_of_false: int = 0
    number_of_error: int = 0
    number_of_unknown: int = 0
    number_of_noteval: int = 0
    number_of_notappl: int = 0

    def eval_operator_and(self):
        """
        The AND operator produces a true result if every argument is true. If one or more arguments
        are false, the result of the AND is false. If one or more of the arguments are unknown, and
        if none of the arguments are false, then the AND operator produces a result of unknown.

        Returns:
                str. return values::

                    true
                    false
                    error
                    unknown
                    noteval
        """
        out_result = None
        false_eq_zero = self.number_of_false == 0
        true_gt_zero = self.number_of_true > 0
        if true_gt_zero and false_eq_zero and self._error_unknown_noteval_eq_zero():
            out_result = 'true'
        elif self.number_of_false >= 1:
            out_result = 'false'
        else:
            out_result = self._eval_error_unknown_noteval_for_operators_and_or('and')
        return out_result

    def eval_operator_one(self):
        """
        The ONE operator produces a true result if one and only one argument is true. If there are
        more than argument is true (or if there are no true arguments), the result of the ONE
        is false. If one or more of the arguments are unknown, then the ONE operator produces
        a result of unknown.

        Returns:
            str. return values::

                true
                false
                error
                unknown
                noteval
        """
        out_result = None
        if self._one_is_true():
            out_result = 'true'
        elif self._one_is_false():
            out_result = 'false'
        elif self._one_is_error():
            out_result = 'error'
        elif self._one_is_unknown():
            out_result = 'unknown'
        elif self._one_is_noteval():
            out_result = 'noteval'
        return out_result

    def _one_is_noteval(self):
        """Evaluates if the result match noteval for one operator.

        Returns:
                bool.
        """
        true_lt_two = self.number_of_true < 2

        false_ge_zero = self.number_of_false >= 0
        notappl_ge_zero = self.number_of_notappl >= 0

        noteval_ge_one = self.number_of_noteval >= 1

        error_eq_zero = self.number_of_error == 0
        unknown_eq_zero = self.number_of_unknown == 0

        false_notappl_ge_zero = false_ge_zero and notappl_ge_zero
        error_unknown_eq_zero = error_eq_zero and unknown_eq_zero
        return true_lt_two and false_notappl_ge_zero and noteval_ge_one and error_unknown_eq_zero

    def _one_is_unknown(self):
        """Evaluates if the result match unknown for one operator.

        Returns:
                bool.
        """
        true_lt_two = self.number_of_true < 2

        false_ge_zero = self.number_of_false >= 0
        notappl_ge_zero = self.number_of_notappl >= 0
        noteval_ge_zero = self.number_of_noteval >= 0

        error_eq_zero = self.number_of_error == 0

        unknown_ge_one = self.number_of_unknown >= 1

        false_notappl_noteval_ge_zero = false_ge_zero and notappl_ge_zero and noteval_ge_zero
        return true_lt_two and false_notappl_noteval_ge_zero and error_eq_zero and unknown_ge_one

    def _one_is_error(self):
        """Evaluates if the result match unknown for one operator.

        Returns:
                bool.
        """
        true_lt_two = self.number_of_true < 2

        false_ge_zero = self.number_of_false >= 0

        error_ge_one = self.number_of_error >= 1

        unknown_noteval_notappl_ge_zero = self._unknown_noteval_notappl_ge_zero()
        return true_lt_two and false_ge_zero and error_ge_one and unknown_noteval_notappl_ge_zero

    def _one_is_false(self):
        """
        Evaluates if the result match false for one operator.
        Operator ONE has two cases of false state.

        Returns:
                bool.
        """
        # The first case for false
        true_ge_two = self.number_of_true >= 2
        false_ge_zero = self.number_of_false >= 0
        error_ge_zero = self.number_of_error >= 0
        unknown_noteval_notappl_ge_zero = self._unknown_noteval_notappl_ge_zero()

        false_error_ge_zero = false_ge_zero and error_ge_zero

        first_case = true_ge_two and false_error_ge_zero and unknown_noteval_notappl_ge_zero

        # The second case for false
        true_eq_zero = self.number_of_true == 0
        false_ge_one = self.number_of_false >= 1
        notappl_ge_zero = self.number_of_notappl >= 0
        error_unknown_noteval_eq_zero = self._error_unknown_noteval_eq_zero()

        true_error_unknown_noteval_eq_zero = true_eq_zero and error_unknown_noteval_eq_zero

        second_case = true_error_unknown_noteval_eq_zero and false_ge_one and notappl_ge_zero

        return first_case or second_case

    def _one_is_true(self):
        """
        Evaluates if the result match true for one operator.

        Returns:
                bool.
        """
        true_eq_one = self.number_of_true == 1
        false_ge_zero = self.number_of_false >= 0
        notappl_ge_zero = self.number_of_notappl >= 0
        error_unknown_noteval_eq_zero = self._error_unknown_noteval_eq_zero()

        false_notappl_ge_zero = false_ge_zero and notappl_ge_zero
        return true_eq_one and error_unknown_noteval_eq_zero and false_notappl_ge_zero

    def eval_operator_or(self):
        """
        The OR operator produces a true result if one or more arguments is true. If every argument
        is false, the result of the OR is false. If one or more of the arguments are unknown and
        if none of arguments are true, then the OR operator produces a result of unknown.

        Returns:
            str. return values::

                true
                false
                error
                unknown
                noteval
        """
        out_result = None
        true_eq_zero = self.number_of_true == 0
        false_ge_one = self.number_of_false >= 1
        if self.number_of_true >= 1:
            out_result = 'true'
        elif true_eq_zero and false_ge_one and self._error_unknown_noteval_eq_zero():
            out_result = 'false'
        else:
            out_result = self._eval_error_unknown_noteval_for_operators_and_or('or')
        return out_result

    def eval_operator_xor(self):
        """
        XOR is defined to be true if an odd number of its arguments are true, and false otherwise.
        If any of the arguments are unknown, then the XOR operator produces a result of unknown.

        Returns:
            str. return values::

                true
                false
                error
                unknown
                noteval
        """
        out_result = None
        error_eq_zero = self.number_of_error == 0
        unknown_eq_zero = self.number_of_unknown == 0
        is_number_of_true_even = (self.number_of_true % 2) == 0
        if not is_number_of_true_even and self._error_unknown_noteval_eq_zero():
            out_result = 'true'
        elif is_number_of_true_even and self._error_unknown_noteval_eq_zero():
            out_result = 'false'
        elif self.number_of_error >= 1:
            out_result = 'error'
        elif error_eq_zero and self.number_of_unknown >= 1:
            out_result = 'unknown'
        elif error_eq_zero and unknown_eq_zero and self.number_of_noteval >= 1:
            out_result = 'noteval'
        return out_result

    def _eval_error_unknown_noteval_for_operators_and_or(self, operator):
        """
        Evaluates if the operator result match the values for error, unknown, noteval.

        Args:
            operator (str): Specifies for which operator is used

        Returns:
            str or None. return values::

                error
                unknown
                noteval
        """
        out_result = None
        bool_eq_zero = self.number_of_false == 0 if operator == 'and' else self.number_of_true == 0
        if bool_eq_zero and self.number_of_error >= 1:
            out_result = 'error'
        elif bool_eq_zero and self.number_of_error == 0 and self.number_of_unknown >= 1:
            out_result = 'unknown'
        elif bool_eq_zero and self._error_unknown_eq_zero_and_noteval_ge_one():
            out_result = 'noteval'
        return out_result

    def _error_unknown_noteval_eq_zero(self):
        error_eq_zero = self.number_of_error == 0
        unknown_eq_zero = self.number_of_unknown == 0
        noteval_eq_zero = self.number_of_noteval == 0
        return error_eq_zero and unknown_eq_zero and noteval_eq_zero

    def _error_unknown_eq_zero_and_noteval_ge_one(self):
        error_eq_zero = self.number_of_error == 0
        unknown_eq_zero = self.number_of_unknown == 0
        noteval_ge_one = self.number_of_noteval >= 1
        return error_eq_zero and unknown_eq_zero and noteval_ge_one

    def _unknown_noteval_notappl_ge_zero(self):
        unknown_ge_zero = self.number_of_unknown >= 0
        noteval_ge_zero = self.number_of_noteval >= 0
        notappl_ge_zero = self.number_of_notappl >= 0
        return unknown_ge_zero and notappl_ge_zero and noteval_ge_zero

    def is_notapp_result(self):
        """
        Evaluates if the counts of values in the result matches the notapp result.

        Returns:
            bool.
        """
        notappl_gt_zero = self.number_of_notappl > 0
        false_eq_zero = self.number_of_false == 0
        true_eq_zero = self.number_of_true == 0
        error_unknown_noteval_eq_zero = self._error_unknown_noteval_eq_zero()

        true_false_eq_zero = false_eq_zero and true_eq_zero
        return notappl_gt_zero and true_false_eq_zero and error_unknown_noteval_eq_zero
