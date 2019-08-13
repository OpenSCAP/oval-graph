"""
Playgrounds are scripts where i testing and preparing new things and  new futures.

test parser for negation
"""

import graph.xml_parser

parser = graph.xml_parser.xml_parser(
    'tests/test_data/ssg-fedora-ds-arf-scan-with-extend-definitions.xml')


# print(parser.get_data_form_xml('#oval0'))

rule_id = 'xccdf_org.ssgproject.content_rule_sysctl_net_ipv6_conf_all_disable_ipv6'
print(parser.parse_data_to_dict(rule_id))
