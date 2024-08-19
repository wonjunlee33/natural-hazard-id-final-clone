#!/usr/bin/env python

import os
import argparse
import subprocess
import json

script_dir = os.path.dirname(os.path.realpath(__file__))

os.chdir(f"{script_dir}/..")

parser = argparse.ArgumentParser(description="Execute coverage command")

parser.add_argument("--value", action="store_true", help="print coverage value and exit")

args = parser.parse_args()


if args.value:

    subprocess.run(
        "coverage run --branch -m nose2 test_python",
        shell=True,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    subprocess.run(
        [
            "coverage",
            "json",
            "--omit=API/*",
        ],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )

    with open("coverage.json", "r") as coverage_file:
        coverage_data = json.load(coverage_file)

        percent_covered = coverage_data["totals"]["percent_covered_display"]

    print(percent_covered)

else:
    subprocess.run("coverage run --branch -m nose2 test_python", shell=True)
    subprocess.run(
        "coverage html --omit=API/*",
        shell=True,
    )
    subprocess.run("cd htmlcov/ && python -m http.server", shell=True)
