from __future__ import annotations

import heapq
import random

from collections import Counter, defaultdict
from typing import Any, List, Dict



def split_row(row):
    return [int(x) for x in row.strip()]

def neighbourhood(x_coord, y_coord, max_x, max_y):
    if (x_coord == 0):
        vertical_neighbours = [(x_coord+1, y_coord)]
    elif (x_coord == max_x):
        vertical_neighbours = [(x_coord-1, y_coord)]
    else:
        vertical_neighbours = [(x_coord-1, y_coord), (x_coord+1, y_coord)]

    if (y_coord == 0):
        horiztonal_neighbours = [(x_coord, y_coord+1)]
    elif (y_coord == max_y):
        horiztonal_neighbours = [(x_coord, y_coord-1)]
    else:
        horiztonal_neighbours = [(x_coord, y_coord-1), (x_coord, y_coord+1)]

    return vertical_neighbours + horiztonal_neighbours

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

    def shortest_distance_between(self, start, finish):
        # dijkstras algorithm
        # heap queue implementation
        # each element in the queue is a tuple (distance, node)

        visited_nodes = {}
        tentative_distances = defaultdict(lambda: float('inf'))

        current_node = start
        tentative_distances[start] = 0

        while finish not in visited_nodes:
            current_distance = tentative_distances[current_node]
            neighbours = self.edges[current_node]

            new_tentative_distances = {n: current_distance+n[-1] for n in neighbours if n not in visited_nodes}

            for node, td in new_tentative_distances.items():
                tentative_distances[node] = min(td, tentative_distances[node])

            tentative_distances.pop(current_node) # once visited not coming back, so get rid of it, helps sorting in next step
            visited_nodes[current_node] = current_distance

            unvisited_nodes = sorted(
                ((node, td) for node,td in tentative_distances.items() if node not in visited_nodes),
                key=lambda x: x[-1]
            )

            if unvisited_nodes:
                current_node = unvisited_nodes[0][0]
            else: break

        return visited_nodes[finish]

with open("data-day15.txt") as f:
    risk_map = [split_row(l) for l in  f.readlines()]

max_x = len(risk_map[0]) - 1
max_y = len(risk_map) - 1

for i, row in enumerate(risk_map):
    risk_map[i] = row * 5

new_risk_map = []

for j in range(5):
    for row in risk_map:
        new_risk_map.append([x for x in row])

risk_map = new_risk_map

for j, row in enumerate(risk_map):
    for i, el in enumerate(row):
        new_risk = el + (i // (max_x+1)) + (j // (max_y+1))
        risk_map[j][i] = new_risk if new_risk < 10 else new_risk % 9

max_x = len(risk_map[0]) - 1
max_y = len(risk_map) - 1

edges = {}

for i, x in enumerate(risk_map):
    for j, y in enumerate(x):
        neighbouring_points = neighbourhood(i, j, len(risk_map)-1, len(x)-1)
        edges[((i, j), risk_map[i][j])] = [(p, risk_map[p[0]][p[1]]) for p in neighbouring_points]

start_point = ((0, 0), risk_map[0][0])
end_point = ((max_x, max_y), risk_map[-1][-1])

graph = Graph(edges)
print("Shortest distance: ", graph.shortest_distance_between(start_point, end_point))
