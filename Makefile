PYTHON ?= python

.PHONY: run test

run:
    $(PYTHON) -m src.main $(ARGS)

test:
    $(PYTHON) -m unittest discover -s tests -t .
