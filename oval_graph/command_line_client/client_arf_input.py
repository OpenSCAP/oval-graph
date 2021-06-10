from ..arf_xml_parser.arf_xml_parser import ARFXMLParser
from ..exceptions import NotTestedRule
from .client import Client


class ClientArfInput(Client):
    def __init__(self, args):
        super().__init__(args)
        self.show_failed_rules = self.arg.show_failed_rules
        self.show_not_selected_rules = self.arg.show_not_selected_rules
        self.show_not_tested_rules = self.arg.show_not_tested_rules
        self.arf_xml_parser = None

    def load_file(self):
        self.arf_xml_parser = ARFXMLParser(self.source_filename)

    def _get_not_selected_rules(self):
        rules = []
        for rule, result in self.arf_xml_parser.not_tested_rules.items():
            if result == 'notselected':
                rules.append(rule)
        return rules

    def _get_rows_of_unselected_rules(self):
        out = []
        not_selected_rules = self._get_wanted_rules(self._get_not_selected_rules())
        maxlen = len(max(not_selected_rules, key=len))
        pattern = '{rule:' + str(maxlen) + '} (Not selected)'
        out.append('== The not selected rule IDs ==')
        for rule in not_selected_rules:
            out.append(pattern.format(rule=rule))
        return out

    def get_only_fail_rule(self, rules):
        return list(
            filter(
                lambda rule: self.arf_xml_parser.used_rules[rule]['result'] == 'fail',
                rules))

    def _get_rows_not_visualizable_rules(self):
        out = []
        out.append('== The not tested rule IDs ==')
        maxlen = len(max(self.arf_xml_parser.not_tested_rules.keys(), key=len))
        pattern = '{rule:' + str(maxlen) + '} {result}'
        for rule, result in self.arf_xml_parser.not_tested_rules.items():
            out.append(pattern.format(rule=rule, result=result))
        return out

    def get_matched_not_tested_rules(self):
        return self._get_wanted_rules(self.arf_xml_parser.not_tested_rules.keys())

    def search_rules_id(self):
        wanted_rules = self._get_wanted_rules(self.arf_xml_parser.used_rules.keys())
        not_tested_rule = self.get_matched_not_tested_rules()
        if not wanted_rules and not not_tested_rule:
            raise ValueError('404 rule "{}" not found!'.format(self.rule_name))
        if self.rule_name in not_tested_rule:
            raise NotTestedRule(
                'Rule "{}" is {}, so there are no results.'
                .format(self.rule_name, self.arf_xml_parser.not_tested_rules[self.rule_name]))
        return wanted_rules
