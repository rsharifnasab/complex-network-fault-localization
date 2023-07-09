#!/usr/bin/env python3

import json
import sys

import networkx as nx
from run import get_last_file_number
from commongraphgen import t_no, l_no, base_graph


PROBLEM_ID = 1111


def load_dataset():
    _, G = base_graph(PROBLEM_ID)

    src = open(f"result/{PROBLEM_ID}/sol.cpp", "r", encoding="UTF-8").read()
    src_lines = len(src.splitlines())

    for test_no in range(1, get_last_file_number(f"./result/{PROBLEM_ID}")+1):
        gcov_data = json.load(
            open(
                f"./result/{PROBLEM_ID}/coverages/gcov-{test_no}.json",
                "r",
                encoding="UTF-8"
            )
        )
        for line_data in gcov_data["lines"]:
            line_no = int(line_data["line_number"])
            line_node = l_no(line_no)
            test_node = t_no(test_no)

            assert line_no <= src_lines+2, f"line no out of file {line_no}"

            assert line_node in G.nodes, f"line node {line_node} not found in graph {G.nodes}"
            assert test_node in G.nodes, f"test node {test_node} not found in graph {G.nodes}"
            if (int(line_data["count"]) >= 1
                    # and G.nodes[test_node]["failed"]
                ):
                G.add_edge(test_node, line_node)

    return f"type-1-{PROBLEM_ID}", G


if __name__ == "__main__":
    PROBLEM_ID = int(sys.argv[1])
    name, G = load_dataset()
    print(f"generated {name} with nodes:{len(G.nodes)} edges:{len(G.edges)}")
    nx.write_gml(G, f"./result/{PROBLEM_ID}/{name}.gml")
