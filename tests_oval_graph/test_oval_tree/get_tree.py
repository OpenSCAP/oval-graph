import json
from pathlib import Path

from oval_graph.oval_tree.oval_node import OvalNode


class GetTree():

    @staticmethod
    def simple_tree():
        return OvalNode(
            node_id=1,
            node_type='operator',
            value='and',
            children=[
                OvalNode(
                    node_id=2,
                    node_type='value',
                    value='true',
                ),
                OvalNode(
                    node_id=3,
                    node_type='value',
                    value='false',
                ),
                OvalNode(
                    node_id=4,
                    node_type='operator',
                    value='or',
                    children=[
                        OvalNode(
                            node_id=5,
                            node_type='value',
                            value='false',
                        ),
                        OvalNode(
                            node_id=6,
                            node_type='value',
                            value="true",
                        ),
                    ]
                )
            ]
        )

    @staticmethod
    def tree_true():
        return OvalNode(
            node_id=1,
            node_type='operator',
            value='and',
            children=[
                OvalNode(
                    node_id=2,
                    node_type='value',
                    value='true',
                )
            ]
        )

    @staticmethod
    def tree_false():
        return OvalNode(
            node_id=1,
            node_type='operator',
            value='and',
            children=[
                OvalNode(
                    node_id=2,
                    node_type='value',
                    value="false",
                ),
            ]
        )

    @staticmethod
    def tree_noteval():
        return OvalNode(
            node_id=1,
            node_type='operator',
            value='and',
            children=[
                OvalNode(
                    node_id=2,
                    node_type='value',
                    value='noteval',
                )
            ]
        )

    @staticmethod
    def tree_false_one_node():
        return OvalNode(
            node_id=1,
            node_type='value',
            value='false',
        )

    @staticmethod
    def tree_true_one_node():
        return OvalNode(
            node_id=1,
            node_type='value',
            value='true',
        )

    @staticmethod
    def tree_error_one_node():
        return OvalNode(
            node_id=1,
            node_type='value',
            value='error',
        )

    @staticmethod
    def negated_operator_node_false():
        return OvalNode(
            node_id=1,
            node_type='operator',
            value='and',
            negation=True,
            children=[
                OvalNode(
                    node_id=2,
                    node_type='value',
                    value='false',
                )
            ]
        )

    @staticmethod
    def negated_operator_node_true():
        return OvalNode(
            node_id=1,
            node_type='operator',
            value='and',
            negation=True,
            children=[
                OvalNode(
                    node_id=2,
                    node_type='value',
                    value='true',
                )
            ]
        )

    @staticmethod
    def negate_value_node_false():
        return OvalNode(
            node_id=1,
            node_type='operator',
            value='and',
            children=[
                OvalNode(
                    node_id=2,
                    node_type='value',
                    value="false",
                    negation=True,
                ),
            ]
        )

    @staticmethod
    def negate_value_node_true():
        return OvalNode(
            node_id=1,
            node_type='operator',
            value='and',
            children=[
                OvalNode(
                    node_id=2,
                    node_type='value',
                    value="true",
                    negation=True,
                ),
            ]
        )

    @staticmethod
    def negated_value_node_true():
        return OvalNode(
            node_id=2,
            node_type='value',
            value='true',
            negation=True,
        )

    @staticmethod
    def negated_value_node_false():
        return OvalNode(
            node_id=2,
            node_type='value',
            value='false',
            negation=True,
        )

    @staticmethod
    def uppercase_tree():
        return OvalNode(
            node_id=1,
            node_type="OPERATOR",
            value="AND",
            children=[
                OvalNode(
                    node_id=2,
                    node_type="VALUE",
                    value="TRUE",
                ),
                OvalNode(
                    node_id=3,
                    node_type="VALUE",
                    value="NOTAPPL",
                ),
            ]
        )

    @staticmethod
    def big_oval_tree():
        return OvalNode(
            node_id=1,
            node_type='operator',
            value='and',
            children=[
                OvalNode(
                    node_id=2,
                    node_type='value',
                    value="false",
                ),
                OvalNode(
                    node_id=3,
                    node_type='operator',
                    value="xor",
                    children=[
                        OvalNode(
                            node_id=4,
                            node_type='value',
                            value='true',
                        ),
                        OvalNode(
                            node_id=5,
                            node_type='operator',
                            value='one',
                            children=[
                                OvalNode(
                                    node_id=6,
                                    node_type='value',
                                    value='noteval',
                                ),
                                OvalNode(
                                    node_id=7,
                                    node_type='value',
                                    value='true',
                                ),
                                OvalNode(
                                    node_id=8,
                                    node_type='value',
                                    value='notappl',
                                ),
                            ]
                        ),
                        OvalNode(
                            node_id=9,
                            node_type='value',
                            value='error',
                        ),
                    ]
                ),
                OvalNode(
                    node_id=10,
                    node_type='operator',
                    value='or',
                    children=[
                        OvalNode(
                            node_id=11,
                            node_type='value',
                            value="unknown",
                        ),
                        OvalNode(
                            node_id=12,
                            node_type='value',
                            value="true",
                        ),
                    ]
                ),
            ]
        )

    # Degenered trees
    @staticmethod
    def bad_tree():
        """
            t
            |
            and
            |
            t
        """
        return OvalNode(
            node_id=1,
            node_type="value",
            value="true",
            children=[
                OvalNode(
                    node_id=2,
                    node_type="operator",
                    value="and",
                    children=[
                        OvalNode(
                            node_id=3,
                            node_type="value",
                            value="true",
                        ),
                    ]
                ),
            ]
        )

    @staticmethod
    def tree_only_or():
        """
            or
        """
        return OvalNode(
            node_id=1,
            node_type="operator",
            value='or',
        )

    @staticmethod
    def tree_only_and():
        """
            and
        """
        return OvalNode(
            node_id=1,
            node_type="operator",
            value='and',
        )

    @staticmethod
    def tree_with_bad_value_of_operator():
        return OvalNode(
            node_id=1,
            node_type="operator",
            value='nad',
        )

    @staticmethod
    def tree_with_bad_value_of_value():
        return OvalNode(
            node_id=1,
            node_type="value",
            value='and',
        )

    @staticmethod
    def tree_with_bad_type():
        return OvalNode(
            node_id=1,
            node_type="car",
            value='and',
        )

    @staticmethod
    def tree_with_bad_value_of_negation():
        return OvalNode(
            node_id=1,
            node_type="operator",
            value="true",
            children=[
                OvalNode(
                    node_id=2,
                    node_type="value",
                    value='true',
                    negation="random_string",
                )
            ]
        )

    @staticmethod
    def json_of_tree(src):
        path = Path(__file__).parent / src
        with open(path, 'r') as file_:
            return json.load(file_)
