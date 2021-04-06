from ._xml_parser_comments import _XmlParserComments
from ._xml_parser_test_info import _XmlParserTestInfo


class _XmlParserScanDefinitions:
    def __init__(self, definitions, oval_definitions, report_data):
        self.definitions = definitions
        self.comments_parser = _XmlParserComments(oval_definitions)
        self.test_info_parser = _XmlParserTestInfo(report_data)

    def get_scan(self):
        dict_of_definitions = {}
        for definition in self.definitions:
            id_definition = definition.get('definition_id')
            dict_of_definitions[id_definition] = dict(
                commnet=None, node=self._build_node(
                    definition[0], "Definition", id_definition))
        self.comments_parser.insert_comments(dict_of_definitions)
        return self._fill_extend_definition(dict_of_definitions)

    def _get_negate_status(self, node):
        str_to_bool = {
            'true': True,
            'false': False,
        }
        negate_status = False
        if node.get('negate') is not None:
            negate_status = str_to_bool[node.get('negate')]
        return negate_status

    def _get_result(self, negate_status, tree):
        """
            This  method  removes  the  negation of
            the result. Because negation is already
            included in the result in ARF file.
        """
        result = tree.get('result')
        reverse_negate_value = {
            'true': 'false',
            'false': 'true',
        }
        if negate_status and result in ('true', 'false'):
            result = reverse_negate_value[result]
        return result

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
                negate_status = self._get_negate_status(child)
                result_of_node = self._get_result(negate_status, child)
                if child.get('definition_ref') is not None:
                    node['node'].append(
                        dict(
                            extend_definition=child.get('definition_ref'),
                            result=result_of_node,
                            negate=negate_status,
                            comment=None,
                            tag="Extend definition",
                        ))
                else:
                    node['node'].append(
                        dict(
                            value_id=child.get('test_ref'),
                            value=result_of_node,
                            negate=negate_status,
                            comment=None,
                            tag="Test",
                            test_result_details=self.test_info_parser.get_info_about_test(
                                child.get('test_ref')),
                        ))
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
                    self._find_definition_by_id(
                        dict_of_definitions,
                        child['extend_definition'],
                        child['negate'],
                        child['comment'],
                        child['tag'],
                    ))
            else:
                out['node'].append(child)
        return out

    def _find_definition_by_id(
            self,
            dict_of_definitions,
            id_,
            negate_status,
            comment,
            tag):
        if id_ in dict_of_definitions:
            dict_of_definitions[id_]['node']['negate'] = negate_status
            dict_of_definitions[id_]['node']['comment'] = comment
            dict_of_definitions[id_]['node']['tag'] = tag
            return self._fill_extend_definition_help(
                dict_of_definitions[id_]['node'], dict_of_definitions)
