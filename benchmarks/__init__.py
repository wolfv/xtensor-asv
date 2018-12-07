# Build extension ... 

import subprocess
import os
import glob

def build_extension():
	curdir = os.path.abspath(os.path.dirname(__file__))
	exepath = os.path.join(curdir, "cpp/build_extension.sh")
	cppsourcepath = os.path.join(curdir, "cpp/")
	subprocess.run([exepath, cppsourcepath])

	compiled_so = glob.glob(os.path.join(cppsourcepath, "build/*.so"))

	print(compiled_so)
	subprocess.run(["cp", compiled_so[0], curdir])



build_extension()