#!/bin/bash

kernprof -l -o profile.lprof main.py --model ../../models/replit-code-v1-3b-q4_0.bin --temperature=0.1 --n_batch=128 --n_gpu_layers 100 --prompt="$(cat main.py | head -n 20)"
python -m line_profiler profile.lprof > profile.txt
rm profile.lprof
cat profile.txt
# rm profile.txt