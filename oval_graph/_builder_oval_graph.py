import uuid

from .oval_node import OvalNode

# rework this (use static metodes)


class _BuilderOvalGraph:
    def __init__(self):
        pass

    def _definition_dict_to_node(self, dict_of_definition):
        children = []
        for child in dict_of_definition['node']:
            if 'operator' in child and 'id':
                children.append(self._definition_dict_to_node(child))
            else:
                children.append(
                    OvalNode(
                        node_id=child['value_id'],
                        node_type='value',
                        value=child['value'],
                        negation=child['negate'],
                        comment=child['comment'],
                        tag=child['tag'],
                        test_result_details=child['test_result_details'],
                    ))

        if 'id' in dict_of_definition:
            children[0].node_id = dict_of_definition['id']
            return children[0]
        else:
            return OvalNode(
                node_id=str(uuid.uuid4()),
                node_type='operator',
                value=dict_of_definition['operator'],
                negation=dict_of_definition['negate'],
                comment=dict_of_definition['comment'],
                tag=dict_of_definition['tag'],
                children=children,
            )

    def get_oval_graph_from_dict_of_rule(self, rule):
        dict_of_definition = rule['definition']
        return OvalNode(
            node_id=rule['rule_id'],
            node_type='operator',
            value='and',
            negation=False,
            comment=dict_of_definition['comment'],
            tag="Rule",
            children=[self._definition_dict_to_node(dict_of_definition)],
        )
