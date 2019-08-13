"""
Playgrounds are scripts where i testing and preparing new things and  new futures.

regex
"""

import re
str='xccdf_org.ssgproject.content_rule_audit_rules_login_events'
str1='oval:ssg-audit_rules_login_events:def:1'
str2='oval:ssg-test_arle_faillock_auditctl:tst:1'
str3='1'
strs=[str1,str2,str,str3]
for string in strs:
    print(re.sub('(oval:ssg-test_|oval:ssg-)|(:def:1|:tst:1)|(xccdf_org.ssgproject.content_)', '', string))
    