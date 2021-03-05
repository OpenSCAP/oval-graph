"""
    This file contains a class for creating OVAL graph from ARF XML source
"""

import os
import sys

from lxml import etree as ET

from ._xml_parser_oval_scan_definitions import _XmlParserScanDefinitions
from .exceptions import NotChecked
from .oval_tree.builder import Builder

ns = {
    'XMLSchema': 'http://oval.mitre.org/XMLSchema/oval-results-5',
    'xccdf': 'http://checklists.nist.gov/xccdf/1.2',
    'arf': 'http://scap.nist.gov/schema/asset-reporting-format/1.1',
    'oval-definitions': 'http://oval.mitre.org/XMLSchema/oval-definitions-5',
    'scap': 'http://scap.nist.gov/schema/scap/source/1.2',
    'oval-characteristics': 'http://oval.mitre.org/XMLSchema/oval-system-characteristics-5',
}


class XmlParser:
    def __init__(self, src):
        self.src = src
        self.tree = ET.parse(self.src)
        self.root = self.tree.getroot()
        if not self.validate(
                'schemas/arf/1.1/asset-reporting-format_1.1.0.xsd'):
            CRED = '\033[91m'
            CEND = '\033[0m'
            print(
                CRED +
                "Warning: This file is not valid arf report." +
                CEND,
                file=sys.stderr)
        try:
            self.used_rules = self._get_used_rules()
            self.report_data = self._get_report_data(
                list(self.used_rules.values())[0]['href'])
            self.notselected_rules = self._get_notselected_rules()
            self.definitions = self._get_definitions()
            self.oval_definitions = self._get_oval_definitions()
            self.scan_definitions = _XmlParserScanDefinitions(
                self.definitions, self.oval_definitions, self.report_data).get_scan()
        except BaseException:
            raise ValueError(
                'This file "{}" is not arf report file or there are no results'.format(
                    self.src))

    def get_src(self, src):
        _dir = os.path.dirname(os.path.realpath(__file__))
        FIXTURE_DIR = os.path.join(_dir, src)
        return str(FIXTURE_DIR)

    def validate(self, xsd_path):
        xsd_path = self.get_src(xsd_path)
        xmlschema_doc = ET.parse(xsd_path)
        xmlschema = ET.XMLSchema(xmlschema_doc)

        xml_doc = self.tree
        result = xmlschema.validate(xml_doc)

        return result

    def _get_used_rules(self):
        rulesResults = self.root.findall(
            './/xccdf:TestResult/xccdf:rule-result', ns)
        rules = {}
        for ruleResult in rulesResults:
            result = ruleResult.find('.//xccdf:result', ns)
            if result.text != "notselected":
                check_content_ref = ruleResult.find(
                    './/xccdf:check/xccdf:check-content-ref', ns)
                message = ruleResult.find(
                    './/xccdf:message', ns)
                rule_dict = {}
                if check_content_ref is not None:
                    rule_dict['id_def'] = check_content_ref.attrib.get('name')
                    rule_dict['href'] = check_content_ref.attrib.get('href')
                    rule_dict['result'] = result.text
                    if message is not None:
                        rule_dict['message'] = message.text
                    rules[ruleResult.get('idref')] = rule_dict
        return rules

    def _get_report_data(self, href):
        report_data = None
        reports = self.root.find('.//arf:reports', ns)
        for report in reports:
            if "#" + str(report.get("id")) == href:
                report_data = report
        return report_data

    def _get_notselected_rules(self):
        rulesResults = self.root.findall(
            './/xccdf:TestResult/xccdf:rule-result', ns)
        rules = []
        for ruleResult in rulesResults:
            result = ruleResult.find('.//xccdf:result', ns)
            if result.text == "notselected":
                rules.append(ruleResult.get('idref'))
        return rules

    def _get_definitions(self):
        data = self.report_data.find(
            ('.//XMLSchema:oval_results/XMLSchema:results/'
             'XMLSchema:system/XMLSchema:definitions'), ns)
        return data

    def _get_oval_definitions(self):
        return self.root.find(
            './/arf:report-requests/arf:report-request/'
            'arf:content/scap:data-stream-collection/'
            'scap:component/oval-definitions:oval_definitions/'
            'oval-definitions:definitions', ns)

    def _get_definition_of_rule(self, rule_id):
        if rule_id in self.used_rules:
            rule_info = self.used_rules[rule_id]
            if rule_info['id_def'] is None:
                raise NotChecked(
                    '"{}" is {}: {}'.format(
                        rule_id,
                        rule_info['result'],
                        rule_info['message']))
            return dict(rule_id=rule_id,
                        definition_id=rule_info['id_def'],
                        definition=self.scan_definitions[rule_info['id_def']])
        elif rule_id in self.notselected_rules:
            raise ValueError(
                'Rule "{}" was not selected, so there are no results.'
                .format(rule_id))
        else:
            raise ValueError('404 rule "{}" not found!'.format(rule_id))

    def get_oval_tree(self, rule_id):
        return Builder.dict_of_rule_to_oval_tree(
            self._get_definition_of_rule(rule_id))
