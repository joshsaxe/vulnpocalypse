# If the vulnpocalypse is the apocalypse, where are the agentic attacker hordes?  Rebuild every figure from the data tables.
#
#   make help          list the targets
#   make figures       draw all 13 figures, reusing the saved Chart 1 model fit              (about 2 minutes)
#   make all           refit the Chart 1 model first, then draw all 13 figures               (about 2 minutes)
#   make sensitivity   run the four robustness checks (each reruns the chart it checks)      (about 5 minutes)
#   make verify        check the numbers: results against the reference, typed numbers against the data,
#                      the bibliography against the tables, and every link in the Markdown files
#   make bibliography  rebuild docs/BIBLIOGRAPHY.md, docs/sources/ and data/sources.csv from the data tables
#
# Needs Python 3.12 or newer and `pip install -r requirements.txt` (exact versions: requirements-lock.txt); Linux or macOS
# (bash).  No network connection is used.  Set PY=/path/to/python to use another interpreter, JOBS=n to run n scripts at once.

SHELL       := /bin/bash
.SHELLFLAGS := -o pipefail -c

PY   ?= python3
JOBS ?= 2

.PHONY: help all figures sensitivity verify bibliography links clean

help:
	@sed -n '1,12p' Makefile | sed 's/^# \{0,1\}//'

all:
	$(PY) tools/run_all.py -j $(JOBS)

figures:
	$(PY) tools/run_all.py --figures -j $(JOBS)

sensitivity:
	$(PY) tools/run_all.py --only s01 s06 s07 s08 -j $(JOBS)

verify:
	$(PY) tools/verify_numbers.py
	$(PY) tools/check_inputs.py
	$(PY) tools/build_bibliography.py --check
	$(PY) tools/check_links.py

bibliography:
	$(PY) tools/build_bibliography.py

links:
	$(PY) tools/check_links.py

clean:
	find . -name __pycache__ -type d -prune -exec rm -rf {} +
