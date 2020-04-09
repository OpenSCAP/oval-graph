import re
import uuid

from .oval_node import OvalNode


class Converter():
    def __init__(self, tree):
        self.VALUE_TO_BOOTSTRAP_COLOR = {
            "true": "text-success",
            "false": "text-danger",
            "error": "text-dark",
            "unknown": "text-dark",
            "noteval": "text-dark",
            "notappl": "text-dark"
        }

        self.BOOTSTRAP_COLOR_TO_LABEL_COLOR = {
            "text-success": "label-success",
            "text-danger": "label-danger",
            "text-dark": "label-default"
        }

        self.VALUE_TO_ICON = {
            "true": "glyphicon glyphicon-ok text-success",
            "false": "glyphicon glyphicon-remove text-danger",
            "error": "glyphicon glyphicon-question-sign text-dark",
            "unknown": "glyphicon glyphicon-question-sign text-dark",
            "noteval": "glyphicon glyphicon-question-sign text-dark",
            "notappl": "glyphicon glyphicon-question-sign text-dark"
        }

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
            color=self.VALUE_TO_BOOTSTRAP_COLOR[values['test_value']],
            icon=self.VALUE_TO_ICON[values['negation_color']],
        )

    def get_comment(self):
        if self.tree.comment is not None:
            return str(self.tree.comment)
        return ""

    def get_tag(self):
        if self.tree.tag is not None:
            return str(self.tree.tag)
        return ""

    def to_JsTree_dict(self, hide_passing_tests=False):
        icons = self._get_node_icon()
        label = self._get_label()
        if self.tree.test_result_details:
            self.tree.test_result_details['result'] = (
                ' <span class="label {color_tag}">{result}</span>'
                .format(
                    color_tag=self.BOOTSTRAP_COLOR_TO_LABEL_COLOR[icons['color']],
                    result=self.result,
                ))
        out = {'text':
               '{negation} <strong><span class="{icon}">{label}</span></strong>'
               ' <span class="label {color_tag}">{tag}</span>'
               ' <span class="label {color_tag}">{result}</span>'
               ' <i>{comment}</i>'
               .format(negation=str(
                   label['negation'] if label['negation'] else ""),
                   icon=icons['color'],
                   label=label['str'],
                   color_tag=self.BOOTSTRAP_COLOR_TO_LABEL_COLOR[icons['color']],
                   tag=self.get_tag(),
                   result=self._get_not_negate_result(),
                   comment=self.get_comment()),
               "icon": icons['icon'],
               "state": {"opened": self._show_node(hide_passing_tests)},
               "info": self.tree.test_result_details,
               }
        if self.tree.children:
            out['children'] = [Converter(child).to_JsTree_dict(
                hide_passing_tests) for child in self.tree.children]
        return out

    def _get_not_negate_result(self):
        if self.tree.negation and self.tree.node_type == 'operator' and self.is_bool(
                self.result):
            return self.negate_bool(self.result)
        return self.result

    def _show_node(self, hide_passing_tests):
        return not(self.result == 'true' and hide_passing_tests)

    def _get_node_style(self):
        value = self._get_not_negate_result()
        out_color = None
        if self.tree.negation and self.is_bool(value):
            out_color = self.negate_bool(value)
        else:
            out_color = value
        return dict(
            negation_color=out_color,
            test_value=value,
        )

    def get_negation_character(self, value):
        return ('<strong><span class="' +
                self.VALUE_TO_BOOTSTRAP_COLOR[value] +
                '">NOT</strong></span>')

    def _get_label(self):
        out = dict(negation=None, str="")
        if self.tree.node_type == 'value':
            out['negation'] = self._get_negation_for_label_of_value()
            out['str'] = re.sub(
                '(oval:ssg-test_|oval:ssg-)|(:def:1|:tst:1)', '', str(self.tree.node_id))
        else:
            if str(self.tree.node_id).startswith('xccdf_org'):
                out['str'] = re.sub(
                    '(xccdf_org.ssgproject.content_)', '', str(
                        self.tree.node_id))
            else:
                out['negation'] = self._get_negation_for_label_of_operator()
                out['str'] = (self.tree.value).upper()
        return out

    def _get_negation_for_label_of_value(self):
        if self.tree.negation and self.is_bool(self.tree.value):
            return self.get_negation_character(
                self.negate_bool(self.tree.value))

    def _get_negation_for_label_of_operator(self):
        if self.tree.negation and self.is_bool(self.result):
            return self.get_negation_character(self.result)

    def negate_bool(self, value):
        values = {
            "true": "false",
            "false": "true",
        }
        return values[str(value)]

    def is_bool(self, value):
        return value == "true" or value == "false"
