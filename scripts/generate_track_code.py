import json
import types
import sys
import os

result_file = sys.argv[1]
gen_dir = sys.argv[2]

with open(result_file, "r") as fi:
	benchmarks = json.load(fi)

temp = """
def {fname}():
	return {result}

"""

def normalize_funcname(fname):
	for c in ['/', '<', ':', '>', ',', ' ']:
		fname = fname.replace(c, '_')
	return fname

with open(os.path.join(gen_dir, "track_code_gen.py"), "w") as fo:
	for b in benchmarks["benchmarks"]:
		fname = "track_" + normalize_funcname(b['name'])
		fo.write(temp.format(fname=fname, result=b['real_time']))
