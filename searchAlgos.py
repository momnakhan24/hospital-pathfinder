import heapq
import math

# 1. Hospital coordinates
locations = {
    "Pharmacy": (0, 0),
    "Main_Corridor": (2, 1),
    "Patient_Wing": (1, 4),
    "Nursing_Station": (4, 2),
    "Laboratory": (5, 5),
    "Emergency_Ward": (8, 6)
}

# 2. Hospital weighted graph
hospital_graph = {
    "Pharmacy": {
        "Main_Corridor": 2.2,
        "Patient_Wing": 4.1
    },
    "Main_Corridor": {
        "Nursing_Station": 2.2
    },
    "Patient_Wing": {
        "Laboratory": 5.0
    },
    "Nursing_Station": {
        "Laboratory": 3.2,
        "Emergency_Ward": 6.0
    },
    "Laboratory": {
        "Emergency_Ward": 3.2
    },
    "Emergency_Ward": {}
}


# 3. Euclidean heuristic
def heuristic(current, goal):
    x1, y1 = locations[current]
    x2, y2 = locations[goal]
    return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)


# 4. Path reconstruction
def reconstruct_path(came_from, current):
    path = []
    while current is not None:
        path.append(current)
        current = came_from[current]
    path.reverse()
    return path


# 5. GBFS
def gbfs(start, goal):
    frontier = [(heuristic(start, goal), start)]
    came_from = {start: None}
    visited = set()
    expansion_order = []

    while frontier:
        _, current = heapq.heappop(frontier)

        if current in visited:
            continue

        visited.add(current)
        expansion_order.append(current)

        if current == goal:
            break

        for neighbor in hospital_graph.get(current, {}):
            if neighbor not in visited:
                came_from.setdefault(neighbor, current)
                heapq.heappush(frontier, (heuristic(neighbor, goal), neighbor))

    if goal not in visited:
        return None, None, expansion_order

    path = reconstruct_path(came_from, goal)
    total_cost = sum(
        hospital_graph[path[i]][path[i + 1]] for i in range(len(path) - 1)
    )

    return path, total_cost, expansion_order


# 6. A*
def a_star(start, goal):
    g_cost = {start: 0}
    came_from = {start: None}
    expansion_order = []
    visited = set()

    frontier = [(heuristic(start, goal), start)]

    while frontier:
        _, current = heapq.heappop(frontier)

        if current in visited:
            continue

        visited.add(current)
        expansion_order.append(current)

        if current == goal:
            path = reconstruct_path(came_from, current)
            return path, g_cost[goal], expansion_order

        for neighbor, cost in hospital_graph.get(current, {}).items():
            tentative_g = g_cost[current] + cost

            if neighbor not in g_cost or tentative_g < g_cost[neighbor]:
                g_cost[neighbor] = tentative_g
                came_from[neighbor] = current
                f = tentative_g + heuristic(neighbor, goal)
                heapq.heappush(frontier, (f, neighbor))

    return None, None, expansion_order