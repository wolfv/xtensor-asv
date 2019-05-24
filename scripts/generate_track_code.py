import json
import types
import sys
import os

result_file = sys.argv[1]
gen_dir = sys.argv[2]

with open(result_file, "r") as fi:
	benchmarks = json.load(fi)

header =  f"""
import json
with open('{result_file}', 'r') as fi:
	j_dict = json.load(fi)

def extract_result(result_name):
	for b in j_dict['benchmarks']:
		if b['name'] == result_name:
			return b['real_time']
	return 0
"""

temp = """
def {fname}():
	return extract_result('{result_name}')
"""

def normalize_funcname(fname):
	for c in ['/', '<', ':', '>', ',', ' ']:
		fname = fname.replace(c, '_')
	return fname

with open(os.path.join(gen_dir, "track_code_gen.py"), "w") as fo:
	fo.write(header)

	for b in benchmarks["benchmarks"]:
		fname = "track_" + normalize_funcname(b['name'])
		fo.write(temp.format(fname=fname, result_name=b['name']))
