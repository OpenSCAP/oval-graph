import tree.oval_tree
import xml.etree.ElementTree as ET

tree = ET.parse('data/ssg-fedora-ds-xccdf.results.xml')
root = tree.getroot()

print(root.tag)

for TestResult in root.findall("./{http://checklists.nist.gov/xccdf/1.2}TestResult"):
    for result in TestResult.findall("./{http://checklists.nist.gov/xccdf/1.2}rule-result"):
        print(result.attrib)
        for value in result.findall("./{http://checklists.nist.gov/xccdf/1.2}result"):
            print(value.text)


"""
for child in root:
    #print(child.tag, child.attrib)
    if child.tag=="{http://checklists.nist.gov/xccdf/1.2}TestResult":
        TestResult=child

print('...........................................................')
for child in TestResult:
    if child.tag=="{http://checklists.nist.gov/xccdf/1.2}rule-result":
        print(child.tag, child.attrib)
        for child1 in child:
            print(child1.tag, child1.attrib, child1.text)

"""