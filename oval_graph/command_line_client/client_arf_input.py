from ..arf_xml_parser.arf_xml_parser import ARFXMLParser
from .client import Client


class ClientArfInput(Client):
    def __init__(self, args):
        super().__init__(args)
        self.show_failed_rules = self.arg.show_failed_rules
        self.show_not_selected_rules = self.arg.show_not_selected_rules
        self.arf_xml_parser = ARFXMLParser(self.source_filename)

    def _get_not_selected_rules(self):
        rules = []
        for rule, result in self.arf_xml_parser.not_tested_rules.items():
            if result == 'notselected':
                rules.append(rule)
        return rules

    def _get_rows_of_unselected_rules(self):
        out = []
        out.append('== The not selected rule IDs ==')
        for rule in self._get_wanted_rules(
                self._get_not_selected_rules()):
            out.append(rule + '(Not selected)')
        return out

    def get_only_fail_rule(self, rules):
        return list(
            filter(
                lambda rule: self.arf_xml_parser.used_rules[rule]['result'] == 'fail',
                rules))

    def search_rules_id(self):
        return self._check_rules_id(
            self._get_wanted_rules(
                self.arf_xml_parser.used_rules.keys()),
            self._get_wanted_rules(
                self._get_not_selected_rules()))
