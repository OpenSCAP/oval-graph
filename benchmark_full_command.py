import os
import subprocess
import tempfile
import time
import uuid

print("Start process all rules")
src = os.path.join(tempfile.gettempdir(), str(uuid.uuid4()))

start_time_all_rules = time.time()

subprocess.check_call(['python3',
                       '-m',
                       'oval_graph.command_line',
                       'arf-to-graph',
                       '--all',
                       '-o',
                       src,
                       'tests/test_data/ssg-fedora-ds-arf.xml',
                       '.'
                       ])

print("--- %s seconds ---" % (time.time() - start_time_all_rules))
