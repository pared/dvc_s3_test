#!/bin/bash

ulimit -n 48 

python -m cProfile -o profile_result code.py
