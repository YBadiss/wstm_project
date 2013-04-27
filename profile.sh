#!/bin/sh

# Use runsnakerun to open profiles: http://www.vrplumber.com/programming/runsnakerun/pip or play with "python -m pstats profiles/file.profile"
filename=$(date +"%Y-%m-%d-%H-%M-%S")
echo "=> Profiling to profiles/$filename.profile"
python -m cProfile -o profiles/$filename.profile -s tottime be_smart.py
echo "sort time\nstats 15" | python -m pstats profiles/$filename.profile
