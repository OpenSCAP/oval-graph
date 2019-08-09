# OVAL visualization as graph
[![Scrutinizer Code Quality](https://scrutinizer-ci.com/g/OpenSCAP/OVAL-visualization-as-graph/badges/quality-score.png?b=codeStyle)](https://scrutinizer-ci.com/g/OpenSCAP/OVAL-visualization-as-graph/?branch=codeStyle) [![Code Coverage](https://scrutinizer-ci.com/g/OpenSCAP/OVAL-visualization-as-graph/badges/coverage.png?b=codeStyle)](https://scrutinizer-ci.com/g/OpenSCAP/OVAL-visualization-as-graph/?branch=codeStyle) [![Build Status](https://scrutinizer-ci.com/g/OpenSCAP/OVAL-visualization-as-graph/badges/build.png?b=codeStyle)](https://scrutinizer-ci.com/g/OpenSCAP/OVAL-visualization-as-graph/build-status/codeStyle) [![Code Intelligence Status](https://scrutinizer-ci.com/g/OpenSCAP/OVAL-visualization-as-graph/badges/code-intelligence.svg?b=codeStyle)](https://scrutinizer-ci.com/code-intelligence)

Understanding result in the blink of an eye

### How use?
```
Command:
    python3 run.py arf-file.xml id-rule
Example:
    python3 run.py data/ssg-fedora-ds-arf.xml xccdf_org.ssgproject.content_rule_disable_host_auth
```
## Requires:
  * **python3**
  * lxml
  * json
  * uuid
  * collections
  * argparse
  * webbrowser