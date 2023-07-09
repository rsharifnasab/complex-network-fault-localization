#!/usr/bin/env python3

import json
import sys
from os import system as shell

import networkx as nx

from commongraphgen import l_no, base_graph

from conf import EXTENSION


PROBLEM_ID = 1111
DG_PATH = "/home/roozbeh/Desktop/test-debug/project/DG/"


def compile(question_path):
    """
    clang -g -O0 sample.c -emit-llvm -S -o foo.ll
    """
    retcode = shell(f"""
            cd result/{question_path} && \
            clang++ \
                -O0 -g \
                -emit-llvm -S \
                sol{EXTENSION} \
                -o ir.ll && \
            cd ../..
             """)
    assert retcode == 0, "compile error"


def CDA(question_path):
    """
    /home/roozbeh/Desktop/test-debug/project/DG/dg/build/tools/llvm-cda-dump  ../cov/foo.ll --c-lines
    """
    retcode = shell(f"""
        {DG_PATH}/dg/build/tools/llvm-cda-dump \
                ./result/{question_path}/ir.ll \
                --c-lines \
                > ./result/{question_path}/cdg.txt
        """)
    assert retcode == 0, "error in llvm cda dump"


def load_dataset():

    src = open(f"result/{PROBLEM_ID}/sol.cpp", "r", encoding="UTF-8").read()
    src_lines = len(src.splitlines())

    _, G = base_graph(PROBLEM_ID)
    compile(PROBLEM_ID)
    CDA(PROBLEM_ID)
    with open(f"./result/{PROBLEM_ID}/cdg.txt", "r", encoding="UTf-8") as f:
        for line in f:
            if "no dbg" in line:
                continue
            from_, to = line.strip().split(" -> ")
            from_line = int(from_.split(":")[0]) + 1
            to_line = int(to.split(":")[0]) + 1
            from_node = l_no(from_line)
            to_node = l_no(to_line)
            # assert from_line <= src_lines+2
            # assert to_line <= src_lines+2

            # assert from_node in G.nodes, f"unknown node {from_node} in {G.nodes} ({line})"
            # assert to_node in G.nodes, f"unknown node {from_node} in {G.nodes} ({line})"
            if from_node in G.nodes and to_node in G.nodes:
                G.add_edge(from_node, to_node)

    return f"type-2-{PROBLEM_ID}", G


if __name__ == "__main__":
    PROBLEM_ID = int(sys.argv[1])
    name, G = load_dataset()
    print(f"generated {name} with nodes:{len(G.nodes)} edges:{len(G.edges)}")
    nx.write_gml(G, f"./result/{PROBLEM_ID}/{name}.gml")
