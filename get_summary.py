#!/home/slamphear/miniconda2/bin/python
import cgi
import sys
import model as md
import json

# -----------
# boiler plate
# -----------
fs = cgi.FieldStorage()
sys.stdout.write("Content-Type: application/json")
sys.stdout.write("\n")
sys.stdout.write("\n")
# -----------

l = md.get_summary()
result = json.dumps(l, indent=1)
# -----------
# boiler plate
# -----------
sys.stdout.write(result)
sys.stdout.write("\n")
sys.stdout.close()
