#!/usr/bin/env python3

import json
import sys

import networkx as nx
from run import get_last_file_number


def t_no(i):
    return f"test-{i}"


def l_no(i):
    return f"line-{i}"


def base_graph(problem_id):
    src = open(f"result/{problem_id}/sol.cpp", "r", encoding="UTF-8").read()
    src_lines = len(src.splitlines())

    faults = open(
        f"result/{problem_id}/sol_info.txt",
        "r",
        encoding="UTF-8",
    ).read() \
        .splitlines()[2] \
        .split(":")[1] \
        .strip() \
        .split(",")

    faults_set = set([int(f.strip(",")) for f in faults])

    G = nx.Graph()
    failed_tests = set()
    with open(f"./result/{problem_id}/failed.txt", "r", encoding="UTF-8") as f:
        for failure in f.read().splitlines():
            failed_tests.add(int(failure.strip()))

    for line_no in range(1, src_lines+4):
        line_node = l_no(line_no)
        assert line_no <= src_lines+4
        G.add_node(line_node,
                   line_no=line_no,
                   faulty=(line_no in faults_set),
                   failed=False,
                   )

    for test_no in range(1, get_last_file_number()+1):
        test_node = t_no(test_no)
        G.add_node(test_node,
                   **{
                       "line_no": 0,
                       "faulty": False,
                       "failed": (test_no in failed_tests)
                   }
                   )

    return f"type-0-{problem_id}", G


if __name__ == "__main__":
    problem_id = int(sys.argv[1])
    name, G = base_graph(problem_id)
    print(f"generated {name} with nodes:{len(G.nodes)} edges:{len(G.edges)}")
    nx.write_gml(G, f"./result/{problem_id}/{name}.gml")
