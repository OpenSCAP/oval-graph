from .client import Client
from .converter import Converter
from ._builder_html_graph import BuilderHtmlGraph
from .xml_parser import XmlParser


class ArfToHtml(Client):
    def _set_attributes(self):
        self.all_in_one = self.arg.all_in_one
        self.all_rules = True if self.all_in_one else self.arg.all
        self.display_html = True if self.out is None else self.arg.display
        self.show_failed_rules = self.arg.show_failed_rules
        self.show_not_selected_rules = self.arg.show_not_selected_rules
        self.html_builder = BuilderHtmlGraph(self.parts, self.verbose, self.all_in_one)
        self.xml_parser = XmlParser(self.source_filename)

    def _get_message(self):
        MESSAGES = {
            'description': 'Client for visualization of SCAP rule evaluation results',
            'source_filename': 'ARF scan file',
        }
        return MESSAGES

    def create_dict_of_rule(self, rule_id):
        converter = Converter(self.xml_parser.get_oval_tree(rule_id))
        return converter.to_JsTree_dict(self.hide_passing_tests)

    def _put_to_dict_oval_trees(self, dict_oval_trees, rule):
        dict_oval_trees[rule] = self.create_dict_of_rule(rule)

    def _get_src_for_one_graph(self, rule):
        return self.get_save_src(rule + self.date)

    def prepare_parser(self):
        super().prepare_parser()
        self.prepare_args_when_output_is_html()
        self.prepare_args_when_user_can_list_in_rules()
