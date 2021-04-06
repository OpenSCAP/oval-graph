ns = {
    'oval-definitions': 'http://oval.mitre.org/XMLSchema/oval-definitions-5',
}


class _XmlParserComments:
    def __init__(self, oval_definitions):
        self.oval_definitions = oval_definitions

    def _create_dict_form_criteria(self, criteria, description=None):
        comments = dict(
            operator=self._get_operator(criteria),
            comment=self._get_comment(criteria, description),
            node=[],
        )
        for criterion in criteria:
            if criterion.get('operator'):
                comments['node'].append(
                    self._create_dict_form_criteria(criterion))
            else:
                comments['node'].append(self._get_dict_with_comment(criterion))

        return comments

    def _get_dict_with_comment(self, criterion):
        out = dict(
            comment=self._get_comment(criterion),
        )
        if criterion.get('definition_ref'):
            out['extend_definition'] = criterion.get('definition_ref')
        else:
            out['value_id'] = criterion.get('test_ref')
        return out

    def _get_operator(self, criterion):
        operator = criterion.get('operator')
        return 'AND' if operator is None else operator

    def _get_comment(self, criterion, description=None):
        comment = criterion.get('comment')
        return description if comment is None else comment

    def _prepare_definition_comments(self):
        definitions = {}
        for definition in self.oval_definitions:
            comment_definition = dict(comment=None, node=[])
            title = definition.find(
                './/oval-definitions:metadata/oval-definitions:title', ns)
            description = definition.find(
                './/oval-definitions:metadata/oval-definitions:description', ns)
            comment_definition['comment'] = title.text
            criteria = definition.find('.//oval-definitions:criteria', ns)
            comment_definition['node'].append(
                self._create_dict_form_criteria(criteria, description.text))
            definitions[definition.get('id')] = comment_definition
        return definitions

    def _recursive_help_fill_comments(self, tree_of_comments, tree):
        for node, node_of_comment in zip(tree, tree_of_comments):
            node['comment'] = node_of_comment['comment']
            if 'operator' in node and node_of_comment.get('node'):
                self._recursive_help_fill_comments(
                    node_of_comment['node'], node['node'])

    def _fill_comment(self, comment_definition, tree_definition):
        tree_of_comments = comment_definition['node']
        tree = [tree_definition['node']]
        tree_definition['comment'] = comment_definition['comment']
        self._recursive_help_fill_comments(tree_of_comments, tree)

    def insert_comments(self, dict_of_definitions):
        comment_definitions = self._prepare_definition_comments()
        for id_definition, definition in dict_of_definitions.items():
            if id_definition in comment_definitions:
                self._fill_comment(
                    comment_definitions[id_definition], definition)
