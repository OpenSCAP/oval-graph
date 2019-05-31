#import xml.etree.ElementTree as ET
from lxml import etree as ET
tree = ET.parse('data/ssg-fedora-ds-arf.xml')
#tree = ET.parse('ssg-fedora-ds-xccdf.results.xml')
root = tree.getroot()
"""
for i in root:
    print(i)
"""
#get rules             
rules = root.findall('.//{http://checklists.nist.gov/xccdf/1.2}Rule')

print('...')

#get results
testResults = root.find('.//{http://checklists.nist.gov/xccdf/1.2}TestResult')
#print(testResults)
ruleResults = testResults.findall('.//{http://checklists.nist.gov/xccdf/1.2}rule-result')


"""
check = root.find('.//{http://scap.nist.gov/schema/asset-reporting-format/1.1}reports')
for i in check:
    print(i)
    for j in i:
        print(j)
        for x in j:
            print(x)
"""

oval_def = root.findall('.//{http://oval.mitre.org/XMLSchema/oval-definitions-5}definition')
"""
for i in oval_def:
    print(i)
    for j in i.findall('.//{http://oval.mitre.org/XMLSchema/oval-definitions-5}criteria'):
        print(j)
"""

print("...")
oval = root.find('.//{http://oval.mitre.org/XMLSchema/oval-results-5}oval_results')
"""
for i in oval:
    print(i)
"""
"""
rule-result idref="xccdf_org.ssgproject.content_rule_package_abrt_removed" time="2019-05-27T15:05:45" severity="medium" weight="1.000000">
            <result>fail</result>
            <check system="http://oval.mitre.org/XMLSchema/oval-definitions-5">
              <check-content-ref name="oval:ssg-package_abrt_removed:def:1" href="#oval0"/>
            </check>
          </rule-result>


"""



#print result
for ruleResult in ruleResults:
    for res in ruleResult:
        if res.text=="fail" or res.text=="pass":
            #print (ruleResult.get('idref'))
            for res in ruleResult:
                for r in res:
                    if r.get('href')=='#oval0':
                        print(r.get('name'))
                #print(res.text)
            #print rule for result 
            """
            for rule in rules:
                if rule.get("id")==ruleResult.get('idref'):
                    for item in rule:
                        if item.tag!="{http://checklists.nist.gov/xccdf/1.2}reference":
                            if item.tag != "{http://checklists.nist.gov/xccdf/1.2}platform":
                                print(item.text)
                                #add how fix it
            """

def get_used_def(root):
    testResults = root.find('.//{http://checklists.nist.gov/xccdf/1.2}TestResult')
    ruleResults = testResults.findall('.//{http://checklists.nist.gov/xccdf/1.2}rule-result')
    out = []
    for ruleResult in ruleResults:
        for res in ruleResult:
            if res.text=="fail" or res.text=="pass":
                out.append(ruleResult.get('idref'))
    return out