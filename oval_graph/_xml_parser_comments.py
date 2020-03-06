ns = {
    'oval-definitions': 'http://oval.mitre.org/XMLSchema/oval-definitions-5',
}

# rework this (use static metodes)


class _XmlParserComments:
    def __init__(self, oval_definitions):
        self.oval_definitions = oval_definitions

    def _create_dict_form_criteria(self, criteria, description):
        comments = dict(
            operator='AND' if criteria.get('operator') is None else criteria.get('operator'),
            comment=description if criteria.get('comment') is None else criteria.get('comment'),
            node=[],
        )
        for criterion in criteria:
            if criterion.get('operator'):
                comments['node'].append(
                    self._create_dict_form_criteria(criterion, None))
            else:
                if criterion.get('definition_ref'):
                    comments['node'].append(
                        dict(
                            extend_definition=criterion.get('definition_ref'),
                            comment=criterion.get('comment'),
                        ))
                else:
                    comments['node'].append(
                        dict(
                            value_id=criterion.get('test_ref'),
                            comment=criterion.get('comment'),
                        ))
        return comments

    def _prepare_definition_comments(self):
        definitions = {}
        for definition in self.oval_definitions:
            comment_definition = dict(
                id=definition.get('id'), comment=None, node=[])
            title = definition.find(
                './/oval-definitions:metadata/oval-definitions:title', ns)
            description = definition.find(
                './/oval-definitions:metadata/oval-definitions:description', ns)
            comment_definition['comment'] = title.text
            criteria = definition.find('.//oval-definitions:criteria', ns)
            comment_definition['node'].append(
                self._create_dict_form_criteria(criteria, description.text))
            definitions[comment_definition['id']] = comment_definition
        return definitions

    def _recursive_help_fill_comments(self, comments, nodes):
        out = nodes
        out['comment'] = comments['comment']
        for node, comment in zip(out['node'], comments['node']):
            node['comment'] = comment['comment']
            if 'operator' in node:
                self._recursive_help_fill_comments(comment, node)

    def _fill_comment(self, comment_definition, data_definition):
        comments = comment_definition['node'][0]
        nodes = data_definition['node'][0]
        data_definition['comment'] = comment_definition['comment']
        self._recursive_help_fill_comments(comments, nodes)

    def insert_comments(self, data):
        comment_definitions = self._prepare_definition_comments()
        for data_definition in data['definitions']:
            if data_definition in comment_definitions:
                self._fill_comment(comment_definitions[data_definition], data['definitions'][data_definition])
