#!/home/slamphear/miniconda2/bin/python
import cgi
import sys
import model as md
import json
import datetime
import os
import logging
import ConfigParser

#logging.basicConfig(filename='log-mur.txt',
#                            filemode='a',
#                            format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
#                            datefmt='%H:%M:%S',
#                            level=logging.DEBUG)

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
label_info = fs.getvalue('checked_options')
#sys.stderr.write(label_info)
#logging.info('Checked labels:\n\n')
#logging.info(label_info)
#label_info = '3131870_520759_115954_5,3462725_521363_486565_0,3774864_522419_38011_0,5134833_522366_176506_0,5332488_527595_264187_0,5495790_531401_300105_0,6881391_523123_411421_0'
# -----------

md.save_data(label_info)
t = datetime.datetime.now().strftime("%I:%M%p on %B %d, %Y")
#t = "Time"
#result = json.dumps({'status': 'OK', 'Time': t})
result = json.dumps({'status': 'OK', 'Time': t}, indent=1)
#result = json.dumps({})
#d = {}
#d['status'] = 'OK'
#d['Time'] = t
#result = {}
#result['foo'] = d
#l = md.get_summary()
#result = json.dumps(d, indent=1)
#result = json.dumps(l, indent=1)
#result = json.dumps(result, indent=1)
# -----------
# boiler plate
# -----------
#sys.stdout.write('{}')
sys.stdout.write(json.dumps(result, indent=1))
sys.stdout.write("\n")
sys.stdout.close()
