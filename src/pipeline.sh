#!/usr/bin/env bash

set -euo pipefail

echo "extracting hot question test_cases"
#time ./test_cases.py

echo "extracting faulty submissions for the questions"
#time ./sources.py

echo "running submissions to fill coverage data"
for question_path in "./result/"/*; do
    if [ -d "$question_path" ]; then
        question=$(basename "$question_path")
        echo "question: ${question}"
        time ./run.py "${question}"
        echo "generating graphs"
        ./graph1-generator.py "${question}"
        ./graph2-generator.py "${question}"
        #./graph3-generator.py "${question}"
    fi
done
