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
checked_data = fs.getvalue('checked_options')
# -----------

# checked_data = request.form['checked_options']
# print checked_data
d = md.read_data(filename=sql_path, filter_label_str=checked_data)
result = json.dumps(d)
# -----------
# boiler plate
# -----------
sys.stdout.write(result)
sys.stdout.write("\n")
sys.stdout.close()
