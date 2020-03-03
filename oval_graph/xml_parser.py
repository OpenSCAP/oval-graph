import sys
import os

from lxml import etree as ET

from ._xml_parser_oval_scan_definitions import _XmlParserScanDefinitions
from ._builder_oval_graph import _BuilderOvalGraph

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
        self.oval_graph_builder = _BuilderOvalGraph()

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
                self.used_rules[0]['href'])
            self.notselected_rules = self._get_notselected_rules()
            self.definitions = self._get_definitions()
            self.oval_definitions = self._get_oval_definitions()
            self.scan_definitions = _XmlParserScanDefinitions(
                self.definitions, self.oval_definitions, self.report_data).get_scan()
        except BaseException:
            raise ValueError("err- This is not arf report file.")

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
        rules = []
        for ruleResult in rulesResults:
            result = ruleResult.find('.//xccdf:result', ns)
            if result.text != "notselected":
                check_content_ref = ruleResult.find(
                    './/xccdf:check/xccdf:check-content-ref', ns)
                if check_content_ref is not None:
                    rules.append(dict(
                        id_rule=ruleResult.get('idref'),
                        id_def=check_content_ref.attrib.get('name'),
                        href=check_content_ref.attrib.get('href'),
                        result=result.text,
                    ))
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
                rules.append(dict(id_rule=ruleResult.get('idref')))
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
        for definition in self.scan_definitions['definitions']:
            if self.get_def_id_by_rule_id(rule_id) == definition['id']:
                return dict(rule_id=rule_id, definition=definition)

    def get_def_id_by_rule_id(self, rule_id):
        for rule in self.notselected_rules:
            if rule['id_rule'] == rule_id:
                raise ValueError(
                    'err- rule "{}" was not selected, so there are no results.'
                    .format(rule_id))
        for rule in self.used_rules:
            if rule['id_rule'] == rule_id:
                return rule['id_def']
        raise ValueError('err- 404 rule not found!')

    def get_oval_tree(self, rule_id=None):
        return self.oval_graph_builder.get_oval_graph_from_definition_dict_of_rule(
            self._get_definition_of_rule(rule_id))
