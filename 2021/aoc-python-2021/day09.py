from __future__ import annotations

import functools
import random
from typing import Any, Dict, List


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


with open("data-day09.txt") as f:
    heightmap = [split_row(r) for r in f.readlines()]

min_values = []
min_coords = []

for i, x in enumerate(heightmap):
    for j, y in enumerate(x):
        neighbouring_points = neighbourhood(i, j, len(heightmap)-1, len(x)-1)

        # print(f"Point: ({i},{j}), {y}")
        # print("Neighbouring Points: ", neighbouring_points)

        local_min = all(y < heightmap[p[0]][p[1]] for p in neighbouring_points)

        if local_min:
            min_values.append(y)
            min_coords.append((i,j))

risks = [x+1 for x in min_values]

print("Sum of Local Minima: ", sum(min_values))
print("Sum of Risks: ", sum(risks))

basins = []

for basin_centre in min_coords:
    basin = []
    points_to_check = [basin_centre]

    while points_to_check:
        point = points_to_check.pop(0)

        if heightmap[point[0]][point[1]] == 9 : continue
        if point in basin: continue

        neighbouring_points = neighbourhood(point[0], point[1], len(heightmap)-1, len(x)-1)
        points_to_check.extend(p for p in neighbouring_points if p not in points_to_check)

        basin.append(point)

    basins.append(basin)

print("Product of size of largest three basins: ",
    functools.reduce(
        lambda x,y: x*y,
        sorted((len(b) for b in basins), reverse=True)[:3],
        1
    )
)


print("Graph Approach")
print("==============")

# can formulate the heightmap as a graph consisting of disconnected subgraphs
# take edges to be both a -> b and b -> a (this makes building the graph easier)

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

edges = {}

for i, x in enumerate(heightmap):
    for j, y in enumerate(x):
        if heightmap[i][j] < 9:
            neighbouring_points = neighbourhood(i, j, len(heightmap)-1, len(x)-1)
            edges[(i, j)] = [p for p in neighbouring_points if heightmap[p[0]][p[1]] < 9]

graph = Graph(edges)
sub_graphs = graph.disconnected_subgraphs()

# can now get the value for all points in each subgraph and take the min
min_values = [min((heightmap[p[0]][p[1]]) for p in sg) for sg in sub_graphs]
risks = [x+1 for x in min_values]

print("Sum of Local Minima: ", sum(min_values))
print("Sum of Risks: ", sum(risks))

print("Product of size of largest three basins: ",
    functools.reduce(
        lambda x,y: x*y,
        sorted((len(sg) for sg in sub_graphs), reverse=True)[:3],
        1
    )
)
