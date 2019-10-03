# OVAL visualization as graph
[![Scrutinizer Code Quality](https://scrutinizer-ci.com/g/OpenSCAP/OVAL-visualization-as-graph/badges/quality-score.png?b=master)](https://scrutinizer-ci.com/g/OpenSCAP/OVAL-visualization-as-graph/?branch=master) [![Code Coverage](https://scrutinizer-ci.com/g/OpenSCAP/OVAL-visualization-as-graph/badges/coverage.png?b=master)](https://scrutinizer-ci.com/g/OpenSCAP/OVAL-visualization-as-graph/?branch=master) [![Build Status](https://scrutinizer-ci.com/g/OpenSCAP/OVAL-visualization-as-graph/badges/build.png?b=master)](https://scrutinizer-ci.com/g/OpenSCAP/OVAL-visualization-as-graph/build-status/master) [![Code Intelligence Status](https://scrutinizer-ci.com/g/OpenSCAP/OVAL-visualization-as-graph/badges/code-intelligence.svg?b=master)](https://scrutinizer-ci.com/code-intelligence)

Understanding result in the blink of an eye

### Usage
```
Command:
    python3 run.py ARF-file.xml id-rule
Example:
    python3 run.py data/ssg-fedora-ds-arf.xml xccdf_org.ssgproject.content_rule_disable_host_auth
```
* *ARF-file.xml* -  ARF xml report from OpenSCAP scan. 
* *id-rule*  - Rule ID to be visualized. A part from the full rule ID a part of the ID or a regular expression can be used. If brackets are used in the regular expression the regular expression must be quoted.

It opens web browser with graph. Default is Firefox. If Firefox not installed it opens default web browser in OS.  
![demo-screenshot](https://raw.githubusercontent.com/OpenSCAP/OVAL-visualization-as-graph/master/demo-screenshot.png "demo-screenshot")
* ### Minimal requirements:
  * **python3**
  * lxml

* ### Recommended requirements:
  * include minimal requirements
  * PyInquirer **(If installation of PyInquirer fails, try to install _python3-devel.x86_64_ and retry the installation.)**
