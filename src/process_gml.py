#!/usr/bin/env python3

import sys
from pathlib import Path

from stats import GraphStats
import networkx as nx
from os import system as shell


def process_gml_by_path(path):
    name = Path(path).stem
    G = nx.read_gml(path)
    stats = GraphStats(name, G, slow=False)
    stats.print_summary()

    shell(f"cat ./result/{name.split('-')[2]}/sol_info.txt | grep 'fault'")
    print(f"failed tests: ", end="")
    print(" - ".join([line.strip()
          for line in open(f"./result/{name.split('-')[2]}/failed.txt")]))

    # shell(f"cat ./result/{name.split('-')[2]}/failed.txt")


if __name__ == "__main__":
    gml_path = sys.argv[1]
    process_gml_by_path(gml_path)
