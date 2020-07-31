# OVAL visualization as graph

Understanding result in the blink of an eye

[![Scrutinizer Code Quality](https://scrutinizer-ci.com/g/OpenSCAP/OVAL-visualization-as-graph/badges/quality-score.png?b=master)](https://scrutinizer-ci.com/g/OpenSCAP/OVAL-visualization-as-graph/?branch=master) [![Code Coverage](https://scrutinizer-ci.com/g/OpenSCAP/OVAL-visualization-as-graph/badges/coverage.png?b=master)](https://scrutinizer-ci.com/g/OpenSCAP/OVAL-visualization-as-graph/?branch=master) [![Build Status](https://scrutinizer-ci.com/g/OpenSCAP/OVAL-visualization-as-graph/badges/build.png?b=master)](https://scrutinizer-ci.com/g/OpenSCAP/OVAL-visualization-as-graph/build-status/master) [![Code Intelligence Status](https://scrutinizer-ci.com/g/OpenSCAP/OVAL-visualization-as-graph/badges/code-intelligence.svg?b=master)](https://scrutinizer-ci.com/code-intelligence)

## Visualization of SCAP rule evaluation results

This tool generates a tree graph from ARF xml report from OpenSCAP scan.

## Installation

**[Learn how to install tool in the Guide.](docs/GUIDE.md#Installation)**

## Example usage

> More usage examples are in user [Guide](./docs/GUIDE.md#Usage-Examples)

This commands consumes the rule name or regular expression of rule name and the ARF file, which is one of possible standardized format for results of SCAP-compliant scanners. You can read about generating ARF report files using OpenSCAP in the OpenSCAP User [Manual](https://github.com/OpenSCAP/openscap/blob/maint-1.3/docs/manual/manual.adoc). Or you can use test arf files from repository `/tests/test_data`.  

```bash
arf-to-graph scan-data/ssg-fedora-ds-arf.xml xccdf_org.ssgproject.content_rule_audit_rules_unsuccessful_file_modification_creat
```

This command generates a graph and saves file named  `graph-of-<rule_id>-<date>.html` (The date the graph was created.) in the working directory. Then, it opens the generated file in your web browser. _Default web browser is Firefox. If Firefox is not installed, the default web browser in OS is used._

![demo-screenshot](./docs/demo-screenshot.png "demo-screenshot")
