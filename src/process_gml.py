#!/usr/bin/env python3

import json
import sys
from pathlib import Path

from stats import GraphStats
import networkx as nx


def process_gml_by_path(path):
    name = Path(path).stem
    G = nx.read_gml(path)
    stats = GraphStats(name, G, slow=False)
    stats.print_summary()


if __name__ == "__main__":
    gml_path = sys.argv[1]
    process_gml_by_path(gml_path)
