from ._comments import _Comments
from ._test_info import _TestInfo

STR_TO_BOOL = {'true': True, 'false': False}
STR_NEGATE_BOOL = {'true': 'false', 'false': 'true'}


class _OVALScanDefinitions:
    def __init__(self, definitions, oval_definitions, report_data):
        self.definitions = definitions
        self.comments_parser = _Comments(oval_definitions)
        self.test_info_parser = _TestInfo(report_data)

    def get_scan(self):
        dict_of_definitions = {}
        for definition in self.definitions:
            id_definition = definition.get('definition_id')
            dict_of_definitions[id_definition] = dict(
                commnet=None, node=self._build_node(
                    definition[0], "Definition", id_definition))
        self.comments_parser.insert_comments(dict_of_definitions)
        return self._fill_extend_definition(dict_of_definitions)

    @staticmethod
    def _get_negate_status(node):
        negate_status = False
        if node.get('negate') is not None:
            negate_status = STR_TO_BOOL[node.get('negate')]
        return negate_status

    @staticmethod
    def _get_result(negate_status, tree):
        """
            This  method  removes  the  negation of
            the result. Because negation is already
            included in the result in ARF file.
        """
        result = tree.get('result')
        if negate_status and result in ('true', 'false'):
            result = STR_NEGATE_BOOL[result]
        return result

    def _get_extend_definition_node(self, child):
        negate_status = self._get_negate_status(child)
        result_of_node = self._get_result(negate_status, child)
        return dict(
            extend_definition=child.get('definition_ref'),
            result=result_of_node,
            negate=negate_status,
            comment=None,
            tag="Extend definition",
        )

    def _get_test_node(self, child):
        negate_status = self._get_negate_status(child)
        result_of_node = self._get_result(negate_status, child)
        test_id = child.get('test_ref')
        return dict(
            value_id=test_id,
            value=result_of_node,
            negate=negate_status,
            comment=None,
            tag="Test",
            test_result_details=self.test_info_parser.get_info_about_test(test_id),
        )

    def _build_node(self, tree, tag, id_definition=None):
        negate_status = self._get_negate_status(tree)
        node = dict(
            id=id_definition,
            operator=tree.get('operator'),
            negate=negate_status,
            result=self._get_result(negate_status, tree),
            comment=None,
            tag=tag,
            node=[],
        )
        for child in tree:
            if child.get('operator') is not None:
                node['node'].append(self._build_node(child, "Criteria"))
            else:
                if child.get('definition_ref') is not None:
                    node['node'].append(self._get_extend_definition_node(child))
                else:
                    node['node'].append(self._get_test_node(child))
        return node

    def _fill_extend_definition(self, dict_of_definitions):
        out = {}
        for id_definition, definition in dict_of_definitions.items():
            out[id_definition] = dict(
                comment=definition['comment'],
                node=self._fill_extend_definition_help(
                    definition['node'],
                    dict_of_definitions))
        return out

    def _fill_extend_definition_help(self, value, dict_of_definitions):
        out = dict(
            operator=value['operator'],
            negate=value['negate'],
            result=value['result'],
            comment=value['comment'],
            tag=value['tag'],
            node=[],
        )
        for child in value['node']:
            if 'operator' in child:
                out['node'].append(
                    self._fill_extend_definition_help(
                        child, dict_of_definitions))
            elif 'extend_definition' in child:
                out['node'].append(
                    self._find_definition_by_id(dict_of_definitions, child))
            else:
                out['node'].append(child)
        return out

    def _find_definition_by_id(self, dict_of_definitions, child):
        id_ = child['extend_definition']
        if id_ in dict_of_definitions:
            dict_of_definitions[id_]['node']['negate'] = child['negate']
            dict_of_definitions[id_]['node']['comment'] = child['comment']
            dict_of_definitions[id_]['node']['tag'] = child['tag']
            return self._fill_extend_definition_help(
                dict_of_definitions[id_]['node'], dict_of_definitions)
        return None
