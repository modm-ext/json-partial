#!/usr/bin/env python3
import os
import sys
import json
import shutil
import subprocess
from pathlib import Path
import urllib.request

source_paths = [
    "LICENSE.MIT",
    "single_include/**/*",
]

with urllib.request.urlopen("https://api.github.com/repos/nlohmann/json/releases/latest") as response:
   tag = json.loads(response.read())["tag_name"]

# clone the repository
if "--fast" not in sys.argv:
    print("Cloning NLOHMANN JSON repository at tag {}...".format(tag))
    shutil.rmtree("nlohmann_json_src", ignore_errors=True)
    subprocess.run("git clone --depth=1 --branch {} ".format(tag) +
                   "https://github.com/nlohmann/json.git  nlohmann_json_src", shell=True)

# remove the sources in this repo
shutil.rmtree("single_include", ignore_errors=True)

print("Copying nlohmann/json sources...")
for pattern in source_paths:
    for path in Path("nlohmann_json_src").glob(pattern):
        if not path.is_file(): continue
        dest = path.relative_to("nlohmann_json_src")
        dest.parent.mkdir(parents=True, exist_ok=True)
        print(dest)
        # Copy, normalize newline and remove trailing whitespace
        with path.open("r", newline=None, encoding="utf-8", errors="replace") as rfile, \
                           dest.open("w", encoding="utf-8") as wfile:
            wfile.writelines(l.rstrip()+"\n" for l in rfile.readlines())


subprocess.run("git add LICENSE.MIT single_include", shell=True)
if subprocess.call("git diff-index --quiet HEAD --", shell=True):
    subprocess.run('git commit -m "Update nlohmann/json to {}"'.format(tag), shell=True)
