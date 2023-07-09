#!/usr/bin/env python3

import signal
from typing import Dict
import sys
from os import system as shell

import networkx as nx
import angr
from angrutils import *
from matplotlib import pyplot as plt

from commongraphgen import l_no, base_graph
from conf import EXTENSION


PROBLEM_ID = 1111
DG_PATH = "/home/roozbeh/Desktop/test-debug/project/DG/"


class timeout:
    def __init__(self, seconds=1, error_message='Timeout'):
        self.seconds = seconds
        self.error_message = error_message

    def handle_timeout(self, signum, frame):
        raise TimeoutError(self.error_message)

    def __enter__(self):
        signal.signal(signal.SIGALRM, self.handle_timeout)
        signal.alarm(self.seconds)

    def __exit__(self, type, value, traceback):
        signal.alarm(0)


def compile_clang(question_path):
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


def DDA_llvm_dda(question_path):
    """
    /home/roozbeh/Desktop/test-debug/project/DG/dg/build/tools/llvm-cda-dump  ../cov/foo.ll --c-lines
    --dbg --dot --graph-only --pta=inv
    """
    retcode = shell(f"""
        {DG_PATH}/dg/build/tools/llvm-dda-dump \
                ./result/{question_path}/ir.ll \
                --c-lines \
                > ./result/{question_path}/ddg.txt
        """)
    assert retcode == 0, "error in llvm dda dump"


def compile_gcc(question_path):
    retcode = shell(f"""
            cd result/{question_path} && \
            g++ \
                -O0 -g \
                sol{EXTENSION} \
                -o angr_bin && \
            cd ../..
             """)
    assert retcode == 0, "compile error"


def addr2line(addr: str) -> int | None:
    question_path = PROBLEM_ID
    # print(f"converting address {addr}")
    shell(f"""
        echo "{addr}" | addr2line -e ./result/{question_path}/angr_bin -p -a > /tmp/line.txt
    """)
    line_no = open("/tmp/line.txt", "r", encoding="UTF-8").read().strip()
    # print(f"converted : {line_no}")
    if "??" in line_no:  # or "?" in line_no:
        return None

    try:
        return int(line_no.split(":")[-1].split(" ")[0])
    except:
        print(f"cannot parse {line_no}")
        assert False


addr_cache: Dict[str, int | None] = {}


def addr2line_cached(addr: str) -> int | None:
    if addr not in addr_cache.keys():
        addr_cache[addr] = addr2line(addr)
    return addr_cache.get(addr)


def calculate_ddg(b):
    cfg = b.analyses.CFGEmulated(
        keep_state=True,
        state_add_options=angr.options.refs,
        context_sensitivity_level=2,
    )
    plot_cfg(cfg, "ais3_cfg",
             asminst=True,
             remove_imports=True,
             remove_path_terminator=True)

    # cfg = b.analyses.CFGFast(
    #   keep_state=True,
    # )
    # print("------cfg complete----")
    # _ = b.analyses.CDG(cfg)
    # print("------cdg complete----")
    ddg = b.analyses.DDG(cfg)
    # print("------ddg complete----")
    return ddg


def DDA(question_path):
    res = []
    b = angr.Project(f"./result/{question_path}/angr_bin",
                     load_options={"auto_load_libs": False}, )

    try:
        with timeout(seconds=10):
            ddg = calculate_ddg(b)
    except TimeoutError:
        print(f"error in calculating ddg for {question_path}")
        return []
    for edge in ddg.graph.edges:
        from_str, to_str = edge
        from_str = str(from_str)
        to_str = str(to_str)

        from_addr = from_str[4:10].strip()
        to_addr = to_str[4:10].strip()

        from_line = addr2line_cached(from_addr)
        to_line = addr2line_cached(to_addr)
        if from_line is not None and to_line is not None:
            res.append((from_line, to_line))
    return res


def load_dataset():
    src = open(f"result/{PROBLEM_ID}/sol.cpp", "r", encoding="UTF-8").read()
    src_lines = len(src.splitlines())

    _, G = base_graph(PROBLEM_ID)
    compile_gcc(PROBLEM_ID)
    edges = DDA(PROBLEM_ID)
    for from_line, to_line in edges:

        assert from_line <= src_lines+1
        assert to_line <= src_lines+1

        G.add_edge(l_no(from_line), l_no(to_line))

    return f"type-3-{PROBLEM_ID}", G


if __name__ == "__main__":
    PROBLEM_ID = int(sys.argv[1])
    name, G = load_dataset()
    print(f"generated {name} with nodes:{len(G.nodes)} edges:{len(G.edges)}")

    nx.write_gml(G, f"./result/{PROBLEM_ID}/{name}.gml")
