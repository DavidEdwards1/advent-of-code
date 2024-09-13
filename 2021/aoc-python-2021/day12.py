from __future__ import annotations

import random

from collections import Counter
from typing import Any, List, Dict


class Graph:
    def __init__(self, edges: Dict[Any, List[Any]]) -> None:
        self.edges = edges

    def disconnected_subgraphs(self) -> List[Graph]:
        # perform flood fill Graph -> List[Graph]
        unlabelled_graph = self.edges.copy()
        sub_graphs = []

        while unlabelled_graph:
            starting_point = random.sample(list(unlabelled_graph), 1)[0]

            # perform BFS to find connected points
            visited_points = []
            points_to_process = [starting_point]

            while points_to_process:
                point = points_to_process.pop(0)
                if point not in visited_points:
                    visited_points.append(point)
                    points_to_process.extend(p for p in self.edges[point])

            sub_graphs.append(visited_points)

            for p in visited_points:
                unlabelled_graph.pop(p)

        return sub_graphs

    def paths_between(self, start, end, can_revisit) -> List[Dict[Any, Any]]:
        paths = [[start, p] for p in self.edges[start]]
        completed_paths = []

        while paths:
            new_paths = []
            for p in paths:
                for new_p in self.edges[p[-1]]:
                    if new_p == end:
                        completed_paths.append(p+[new_p])
                    elif can_revisit(new_p, p):
                        new_paths.append(p+[new_p])

            paths = new_paths

        return completed_paths


def process_input_line(line):
    return line.strip().split("-")


with open("data-day12.txt") as f:
    connections = [process_input_line(l) for l in f.readlines()]

edges = {}

for c in connections:
    start, end = c

    # mirror the connections
    if start in edges:
        edges[start].append(end)
    else:
        edges[start] = [end]
    if end in edges:
        edges[end].append(start)
    else:
        edges[end] = [start]

graph = Graph(edges)

def challenge_one_can_revisit(p, current_path):
    return not(p.islower() and p in current_path)

def challenge_two_can_revisit(new_point: str, current_path):
    if new_point in ("start", "end"):
        ans = False
    elif new_point.isupper():
        ans = True
    elif new_point not in current_path:
        ans = True
    else:
        # now we know that new_point is small, and has been visited before
        small_point_visits = Counter(p for p in current_path if p.islower())
        if any(v > 1 for v in small_point_visits.values()):
            ans = False # already revisited a point
        else:
            ans = True

    return ans

paths = graph.paths_between("start", "end", challenge_one_can_revisit)
print("Number of paths from `start` to `end`: ", len(paths))

paths = graph.paths_between("start", "end", challenge_two_can_revisit)
print("Number of paths from `start` to `end` (expanded rules): ", len(paths))
