from ._xml_parser_comments import _XmlParserComments
from ._xml_parser_test_info import _XmlParserTestInfo


class _XmlParserScanDefinitions:
    def __init__(self, definitions, oval_definitions, report_data):
        self.definitions = definitions
        self.comments_parser = _XmlParserComments(oval_definitions)
        self.test_info_parser = _XmlParserTestInfo(report_data)

    def get_scan(self):
        scan = dict(definitions={})
        for definition in self.definitions:
            graph = self._build_graph(definition)
            scan['definitions'][graph['id']] = graph
        self.comments_parser.insert_comments(scan)
        return self._fill_extend_definition(scan)

    def _build_graph(self, tree_data):
        graph = dict(
            id=tree_data.get('definition_id'),
            node=[],
        )
        for tree in tree_data:
            graph['node'].append(self._build_node(tree, "Definition"))
        return graph

    def _get_negate_status(self, node):
        str_to_bool = {
            'true': True,
            'false': False,
        }
        negate_status = False
        if node.get('negate') is not None:
            negate_status = str_to_bool[node.get('negate')]
        return negate_status

    def _build_node(self, tree, tag):
        node = dict(
            operator=tree.get('operator'),
            negate=self._get_negate_status(tree),
            result=tree.get('result'),
            comment=None,
            tag=tag,
            node=[],
        )
        for child in tree:
            if child.get('operator') is not None:
                node['node'].append(self._build_node(child, "Criteria"))
            else:
                negate_status = self._get_negate_status(child)
                result_of_node = child.get('result')
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

    def _fill_extend_definition(self, scan):
        out = dict(definitions=[])
        definitions = scan['definitions']
        for definition in definitions:
            nodes = []
            for value in definitions[definition]['node']:
                nodes.append(self._fill_extend_definition_help(value, scan))
            out['definitions'].append(
                dict(
                    id=definitions[definition]['id'],
                    comment=definitions[definition]['comment'],
                    node=nodes,
                ))
        return out

    def _fill_extend_definition_help(self, value, scan):
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
                out['node'].append(self._fill_extend_definition_help(child, scan))
            elif 'extend_definition' in child:
                out['node'].append(
                    self._find_definition_by_id(
                        scan,
                        child['extend_definition'],
                        child['negate'],
                        child['comment'],
                        child['tag'],
                    ))
            else:
                out['node'].append(child)
        return out

    def _find_definition_by_id(self, scan, id_, negate_status, comment, tag):
        if id_ in scan['definitions']:
            scan['definitions'][id_]['node'][0]['negate'] = negate_status
            scan['definitions'][id_]['node'][0]['comment'] = comment
            scan['definitions'][id_]['node'][0]['tag'] = tag
            return self._fill_extend_definition_help(scan['definitions'][id_]['node'][0], scan)
