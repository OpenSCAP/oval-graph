import re

from .oval_node import OvalNode

VALUE_TO_BOOTSTRAP_COLOR = {
    "true": "text-success",
    "false": "text-danger",
    "error": "text-dark",
    "unknown": "text-dark",
    "noteval": "text-dark",
    "notappl": "text-dark"
}

BOOTSTRAP_COLOR_TO_LABEL_COLOR = {
    "text-success": "label-success",
    "text-danger": "label-danger",
    "text-dark": "label-default"
}

VALUE_TO_ICON = {
    "true": "glyphicon glyphicon-ok text-success",
    "false": "glyphicon glyphicon-remove text-danger",
    "error": "glyphicon glyphicon-question-sign text-dark",
    "unknown": "glyphicon glyphicon-question-sign text-dark",
    "noteval": "glyphicon glyphicon-question-sign text-dark",
    "notappl": "glyphicon glyphicon-question-sign text-dark"
}


class Converter():
    """The Converter object converts OVAL tree to dict according JSON
       for graphic representation with JsTree.

    Attributes:
        tree (OvalNode): OVAL tree
        result (str): result of node
    """

    def __init__(self, tree):
        if isinstance(tree, OvalNode):
            self.tree = tree
            self.result = self.tree.evaluate_tree()
            if self.tree.node_type == 'value':
                self.result = self.tree.value
        else:
            raise ValueError(
                'This converter can process only trees created from OvalNodes.')

    def _get_node_icon(self):
        values = self._get_node_style()
        return dict(
            color=VALUE_TO_BOOTSTRAP_COLOR[values['test_value']],
            icon=VALUE_TO_ICON[values['negation_color']],
        )

    def _get_comment(self):
        if self.tree.comment is not None:
            return str(self.tree.comment)
        return ""

    def _get_tag(self):
        if self.tree.tag is not None:
            return str(self.tree.tag)
        return ""

    def _get_not_negate_result(self):
        if self.tree.negation and self.tree.node_type == 'operator' and self._is_bool(
                self.result):
            return self._negate_bool(self.result)
        return self.result

    def _show_node(self, hide_passing_tests):
        return not(self.result == 'true' and hide_passing_tests)

    def _get_node_style(self):
        value = self._get_not_negate_result()
        out_color = None
        if self.tree.negation and self._is_bool(value):
            out_color = self._negate_bool(value)
        else:
            out_color = value
        return dict(
            negation_color=out_color,
            test_value=value,
        )

    @staticmethod
    def _get_negation_character(value):
        return (
            '<strong>'
            '<span class="' + VALUE_TO_BOOTSTRAP_COLOR[value] + '">NOT</strong>'
            '</span>'
        )

    def _get_label(self):
        out = dict(negation=None, str="")
        if self.tree.node_type == 'value':
            out['negation'] = self._get_negation_label()
            out['str'] = re.sub(
                '(oval:ssg-test_|oval:ssg-)|(:def:1|:tst:1)', '', str(self.tree.node_id))
        else:
            if str(self.tree.node_id).startswith('xccdf_org'):
                out['str'] = re.sub(
                    '(xccdf_org.ssgproject.content_)', '', str(
                        self.tree.node_id))
            else:
                out['negation'] = self._get_negation_label()
                out['str'] = (self.tree.value).upper()
        return out

    def _get_negation_label(self):
        if self.tree.negation and self._is_bool(self.tree.value):
            return self._get_negation_character(self._negate_bool(self.tree.value))
        if self.tree.negation and self._is_bool(self.result):
            return self._get_negation_character(self.result)
        return None

    @staticmethod
    def _negate_bool(value):
        values = {
            "true": "false",
            "false": "true",
        }
        return values[str(value)]

    @staticmethod
    def _is_bool(value):
        return value in ("true", "false")

    def to_js_tree_dict(self, hide_passing_tests=False):
        """Converts the OVAL tree to dict according JSON
           for graphic representation with JsTree.

        Args:
            hide_passing_tests (bool): bool switch witch enable hiding passing tests

        Returns:
            dict. Dictionary representing OVAL tree
        """
        icons = self._get_node_icon()
        label = self._get_label()
        if self.tree.test_result_details:
            self.tree.test_result_details['result'] = (
                ' <span class="label {color_tag}">{result}</span>'
                .format(
                    color_tag=BOOTSTRAP_COLOR_TO_LABEL_COLOR[icons['color']],
                    result=self.result,
                ))
        out = {'text':
               '{negation} <strong><span class="{icon}">{label}</span></strong>'
               ' <span class="label {color_tag}">{tag}</span>'
               ' <span class="label {color_tag}">{result}</span>'
               ' <i>{comment}</i>'
               .format(
                   negation=str(label['negation'] if label['negation'] else ""),
                   icon=icons['color'],
                   label=label['str'],
                   color_tag=BOOTSTRAP_COLOR_TO_LABEL_COLOR[icons['color']],
                   tag=self._get_tag(),
                   result=self._get_not_negate_result(),
                   comment=self._get_comment()),
               "icon": icons['icon'],
               "state": {"opened": self._show_node(hide_passing_tests)},
               "info": self.tree.test_result_details,
               }
        if self.tree.children:
            out['children'] = [Converter(child).to_js_tree_dict(
                hide_passing_tests) for child in self.tree.children]
        return out

    def to_dict(self):
        node = self.tree
        if not node.children:
            return {
                'node_id': node.node_id,
                'type': node.node_type,
                'value': node.value,
                'negation': node.negation,
                'comment': node.comment,
                'tag': node.tag,
                'test_result_details': node.test_result_details,
                'child': None
            }
        return {
            'node_id': node.node_id,
            'type': node.node_type,
            'value': node.value,
            'negation': node.negation,
            'comment': node.comment,
            'tag': node.tag,
            'test_result_details': node.test_result_details,
            'child': [Converter(child).to_dict() for child in node.children]
        }
