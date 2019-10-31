# OVAL visualization as graph
Understanding result in the blink of an eye

[![Scrutinizer Code Quality](https://scrutinizer-ci.com/g/OpenSCAP/OVAL-visualization-as-graph/badges/quality-score.png?b=master)](https://scrutinizer-ci.com/g/OpenSCAP/OVAL-visualization-as-graph/?branch=master) [![Code Coverage](https://scrutinizer-ci.com/g/OpenSCAP/OVAL-visualization-as-graph/badges/coverage.png?b=master)](https://scrutinizer-ci.com/g/OpenSCAP/OVAL-visualization-as-graph/?branch=master) [![Build Status](https://scrutinizer-ci.com/g/OpenSCAP/OVAL-visualization-as-graph/badges/build.png?b=master)](https://scrutinizer-ci.com/g/OpenSCAP/OVAL-visualization-as-graph/build-status/master) [![Code Intelligence Status](https://scrutinizer-ci.com/g/OpenSCAP/OVAL-visualization-as-graph/badges/code-intelligence.svg?b=master)](https://scrutinizer-ci.com/code-intelligence)

## Visualization of SCAP rule evaluation results
This tool generate tree graph from ARF xml report from OpenSCAP scan.
## Prerequisites
##### Minimal requirements
   - **python3**
   - [lxml](https://pypi.org/project/lxml/)
   
##### Recommended requirements
  * include minimal requirements
  * [inquirer](https://pypi.org/project/inquirer/)

### Installation

```bash
git clone https://github.com/OpenSCAP/OVAL-visualization-as-graph.git
cd OVAL-visualization-as-graph

# Install package with nice cli futures (recommended)
sudo pip3 install ".[niceCli]"

# Install package without futures (light version)
sudo pip3 install .
```
#### Example usage
```
arf-to-graph scan-results/ssg-fedora-ds-arf.xml xccdf_org.ssgproject.content_rule_disable_host_auth
```
It saves all necessary files to a directory named `rule_id` and `date`(The date the graph was created.) in `/tmp`. And default it opens web browser with graph. Default is Firefox. If Firefox not installed it opens default web browser in OS.  

It opens web browser with graph. Default is Firefox. If Firefox not installed it opens default web browser in OS.  
![demo-screenshot](https://raw.githubusercontent.com/OpenSCAP/OVAL-visualization-as-graph/master/demo-screenshot.png "demo-screenshot")
