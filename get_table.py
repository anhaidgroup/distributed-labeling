#!/home/slamphear/miniconda2/bin/python
import cgi
import sys
import model as md
import json
import os
import ConfigParser

config = ConfigParser.RawConfigParser()
config.read('distributed-labeling.cfg')
sqlite_db_path = config.get('Data', 'sqlite_db_path')
if sqlite_db_path.startswith('/'):
	sql_path = sqlite_db_path
else:
	sql_path = os.path.join(os.path.dirname(__file__), sqlite_db_path)

# -----------
# boiler plate
# -----------
fs = cgi.FieldStorage()
sys.stdout.write("Content-Type: application/json")
sys.stdout.write("\n")
sys.stdout.write("\n")
# -----------

d = md.read_data(filename=sql_path)
sys.stderr.write(json.dumps(d, indent=1))
result = json.dumps(d, indent=1)

# -----------
# boiler plate
# -----------
sys.stdout.write(result)
sys.stdout.write("\n")
sys.stdout.close()
