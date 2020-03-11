import uuid

from .oval_node import OvalNode


class _BuilderOvalGraph:

    @staticmethod
    def _definition_dict_to_node(dict_of_definition):
        children = []
        for child in dict_of_definition['node']:
            if 'operator' in child:
                children.append(
                    _BuilderOvalGraph._definition_dict_to_node(child))
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

        return OvalNode(
            node_id=_BuilderOvalGraph._get_id_defintion(dict_of_definition),
            node_type='operator',
            value=dict_of_definition['operator'],
            negation=dict_of_definition['negate'],
            comment=dict_of_definition['comment'],
            tag=dict_of_definition['tag'],
            children=children,
        )

    @staticmethod
    def _get_id_defintion(dict_of_definition):
        if 'definition_id' in dict_of_definition:
            return dict_of_definition['definition_id']
        return str(uuid.uuid4())

    @staticmethod
    def get_oval_graph_from_dict_of_rule(rule):
        dict_of_definition = rule['definition']
        dict_of_definition['node']['definition_id'] = rule['definition_id']
        return OvalNode(
            node_id=rule['rule_id'],
            node_type='operator',
            value='and',
            negation=False,
            comment=dict_of_definition['comment'],
            tag="Rule",
            children=[
                _BuilderOvalGraph._definition_dict_to_node(
                    dict_of_definition['node'])],
        )
