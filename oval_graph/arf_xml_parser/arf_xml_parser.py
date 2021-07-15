"""
    This file contains a class for creating OVAL graph from ARF XML source
"""

import sys
from pathlib import Path

from lxml import etree as ET

from ..exceptions import NotTestedRule
from ..oval_tree.builder import Builder
from ._oval_scan_definitions import _OVALScanDefinitions
from .global_namespaces import namespaces

LOCAL_DATA_DIR = Path(__file__).parent.parent / "schemas"


class ARFXMLParser:
    def __init__(self, src):
        self.src = src
        self.tree = ET.parse(self.src)
        self.root = self.tree.getroot()
        self.arf_schemas_path = 'arf/1.1/asset-reporting-format_1.1.0.xsd'
        if not self.validate(self.arf_schemas_path):
            start_red_color = '\033[91m'
            end_red_color = '\033[0m'
            message = "{}Warning: This file is not valid arf report.{}".format(
                start_red_color, end_red_color)
            print(message, file=sys.stderr)
        try:
            self.used_rules, self.not_tested_rules = self._get_rules_in_profile()
            self.report_data_href = list(self.used_rules.values())[0]['href']
            self.report_data = self._get_report_data(self.report_data_href)
            self.definitions = self._get_definitions()
            self.oval_definitions = self._get_oval_definitions()
            self.scan_definitions = _OVALScanDefinitions(
                self.definitions, self.oval_definitions, self.report_data).get_scan()
        except BaseException as error:
            raise ValueError(
                'This file "{}" is not arf report file or there are no results'.format(
                    self.src)) from error

    def validate(self, xsd_path):
        xsd_path = str(LOCAL_DATA_DIR / xsd_path)
        xmlschema_doc = ET.parse(xsd_path)
        xmlschema = ET.XMLSchema(xmlschema_doc)
        return xmlschema.validate(self.tree)

    @staticmethod
    def _get_rule_dict(rule_result, result, id_def, check_content_ref):
        message = rule_result.find('.//xccdf:message', namespaces)
        rule_dict = {}
        rule_dict['id_def'] = id_def
        rule_dict['href'] = check_content_ref.attrib.get('href')
        rule_dict['result'] = result.text
        if message is not None:
            rule_dict['message'] = message.text
        return rule_dict

    def _get_rules_in_profile(self):
        rules_results = self.root.findall(
            './/xccdf:TestResult/xccdf:rule-result', namespaces)
        rules = {}
        not_tested_rules = {}
        for rule_result in rules_results:
            result = rule_result.find('.//xccdf:result', namespaces)
            check_content_ref = rule_result.find(
                './/xccdf:check/xccdf:check-content-ref', namespaces)
            if check_content_ref is not None:
                id_ = rule_result.get('idref')
                id_def = check_content_ref.attrib.get('name')
                if id_def is not None:
                    rules[id_] = self._get_rule_dict(
                        rule_result, result, id_def, check_content_ref)
                    continue
            not_tested_rules[rule_result.get('idref')] = result.text
        return (rules, not_tested_rules)

    def _get_report_data(self, href):
        report_data = None
        reports = self.root.find('.//arf:reports', namespaces)
        for report in reports:
            if "#" + str(report.get("id")) == href:
                report_data = report
        return report_data

    def _get_definitions(self):
        return self.report_data.find(
            ('.//XMLSchema:oval_results/XMLSchema:results/'
             'XMLSchema:system/XMLSchema:definitions'), namespaces)

    def _get_oval_definitions(self):
        return self.root.find(
            './/arf:report-requests/arf:report-request/'
            'arf:content/scap:data-stream-collection/'
            'scap:component/oval-definitions:oval_definitions/'
            'oval-definitions:definitions', namespaces)

    def _get_definition_of_rule(self, rule_id):
        if rule_id in self.used_rules:
            rule_info = self.used_rules[rule_id]
            return dict(rule_id=rule_id,
                        definition_id=rule_info['id_def'],
                        definition=self.scan_definitions[rule_info['id_def']])

        if rule_id in self.not_tested_rules:
            raise NotTestedRule(
                'Rule "{}" is {}, so there are no results.'
                .format(rule_id, self.not_tested_rules[rule_id]))
        raise ValueError('404 rule "{}" not found!'.format(rule_id))

    def get_oval_tree(self, rule_id):
        return Builder.dict_of_rule_to_oval_tree(
            self._get_definition_of_rule(rule_id))
