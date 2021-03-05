import uuid

from .oval_node import OvalNode


class Builder:
    @staticmethod
    def _definition_dict_to_node(dict_of_definition):
        children = []
        for child in dict_of_definition['node']:
            if 'operator' in child:
                children.append(
                    Builder._definition_dict_to_node(child))
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
            node_id=Builder._get_id_defintion(dict_of_definition),
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
    def dict_of_rule_to_oval_tree(rule):
        dict_of_definition = rule['definition']
        dict_of_definition['node']['definition_id'] = rule['definition_id']
        return OvalNode(
            node_id=rule['rule_id'],
            node_type='operator',
            value='and',
            negation=False,
            comment=dict_of_definition['comment'],
            tag='Rule',
            children=[
                Builder._definition_dict_to_node(
                    dict_of_definition['node'])],
        )

    @staticmethod
    def dict_to_oval_tree(dict_of_tree):
        if dict_of_tree['child'] is None:
            return OvalNode(
                node_id=dict_of_tree['node_id'],
                node_type=dict_of_tree['type'],
                value=dict_of_tree['value'],
                negation=dict_of_tree['negation'],
                comment=dict_of_tree['comment'],
                tag=dict_of_tree['tag'],
                test_result_details=dict_of_tree['test_result_details']
            )
        return OvalNode(
            node_id=dict_of_tree['node_id'],
            node_type=dict_of_tree['type'],
            value=dict_of_tree['value'],
            negation=dict_of_tree['negation'],
            comment=dict_of_tree['comment'],
            tag=dict_of_tree['tag'],
            test_result_details=dict_of_tree['test_result_details'],
            children=[Builder.dict_to_oval_tree(i) for i in dict_of_tree['child']]
        )
