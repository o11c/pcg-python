#!/bin/sh
python3 -m coverage run --source=pcg_random -m pytest
python3 -m coverage html
python3 -m coverage report
