# oval-graph

[![Scrutinizer Code Quality](https://scrutinizer-ci.com/g/OpenSCAP/oval-graph/badges/quality-score.png?b=master)](https://scrutinizer-ci.com/g/OpenSCAP/oval-graph/?branch=master) [![Code Coverage](https://scrutinizer-ci.com/g/OpenSCAP/oval-graph/badges/coverage.png?b=master)](https://scrutinizer-ci.com/g/OpenSCAP/oval-graph/?branch=master) [![Build Status](https://scrutinizer-ci.com/g/OpenSCAP/oval-graph/badges/build.png?b=master)](https://scrutinizer-ci.com/g/OpenSCAP/OVAL-visualization-as-graph/build-status/master) [![Code Intelligence Status](https://scrutinizer-ci.com/g/OpenSCAP/oval-graph/badges/code-intelligence.svg?b=master)](https://scrutinizer-ci.com/code-intelligence) [![Total alerts](https://img.shields.io/lgtm/alerts/g/OpenSCAP/oval-graph.svg?logo=lgtm&logoWidth=18)](https://lgtm.com/projects/g/OpenSCAP/oval-graph/alerts/) [![Language grade: Python](https://img.shields.io/lgtm/grade/python/g/OpenSCAP/oval-graph.svg?logo=lgtm&logoWidth=18)](https://lgtm.com/projects/g/OpenSCAP/oval-graph/context:python) [![Language grade: JavaScript](https://img.shields.io/lgtm/grade/javascript/g/OpenSCAP/oval-graph.svg?logo=lgtm&logoWidth=18)](https://lgtm.com/projects/g/OpenSCAP/oval-graph/context:javascript)

_Understanding result in the blink of an eye_

This tool generates an [OVAL](https://oval.cisecurity.org/) result in the form of a tree graph from an ARF xml report from an OpenSCAP scan.

## Installation

**[Learn how to install tool in the Guide.](https://github.com/OpenSCAP/oval-graph/blob/master/docs/GUIDE.md#installation)**

## Example usage

> More usage examples are in user [Guide](https://github.com/OpenSCAP/oval-graph/blob/master/docs/GUIDE.md#usage-examples)

This commands consumes the rule name or regular expression of rule name and the ARF file, which is one of possible standardized format for results of SCAP-compliant scanners. You can read about generating ARF report files using OpenSCAP in the OpenSCAP User [Manual](https://github.com/OpenSCAP/openscap/blob/maint-1.3/docs/manual/manual.adoc). Or you can use test arf files from repository `/tests/test_data`.  

```bash
arf-to-graph scan-data/ssg-fedora-ds-arf.xml xccdf_org.ssgproject.content_rule_audit_rules_unsuccessful_file_modification_creat
```

This command generates a graph and saves file named  `graph-of-<rule_id>-<date>.html` (The date the graph was created.) in the working directory. Then, it opens the generated file in your web browser. _Default web browser is Firefox. If Firefox is not installed, the default web browser in OS is used._

![demo-screenshot](https://raw.githubusercontent.com/OpenSCAP/oval-graph/master/docs/demo-screenshot.png "demo-screenshot")

## Execute the test suite

**[Learn how to execute the test suite in the Guide.](https://github.com/OpenSCAP/oval-graph/blob/master/docs/GUIDE.md#execute-the-test-suite)**
