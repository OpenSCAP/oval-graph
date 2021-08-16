TEST_ARF_XML_PATH = 'tests_oval_graph/global_test_data/ssg-fedora-ds-arf.xml'

COMMAND_START = ['python3',
                 '-m',
                 'oval_graph.command_line',
                 ]

COMMAND_END = [TEST_ARF_XML_PATH,
               'xccdf_org.ssgproject.content_rule_package_abrt_removed',
               ]

ARF_TO_GRAPH = [*COMMAND_START,
                'arf-to-graph',
                '-o', '.',
                *COMMAND_END,
                ]

ARF_TO_JSON = [*COMMAND_START,
               'arf-to-json',
               *COMMAND_END,
               ]

BAD_JSON_TO_GRAPH = [*COMMAND_START,
                     'json-to-graph',
                     TEST_ARF_XML_PATH,
                     '.'
                     ]

START_OF_JSON_TO_GRAPH_COMMAND = [*COMMAND_START,
                                  'json-to-graph',
                                  ]
