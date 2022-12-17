# notes, stopping conditions
# all valves are open, hit 30 minute mark...

import re
from typing import Union
from dataclasses import dataclass
from collections import defaultdict

INPUT_REGEX = r"Valve (\w+) has flow rate=(\d+); tunnels? leads? to valves? ([A-Z, ]+)"


def get_data(fname: str) -> dict[str, dict[str, Union[int, list[str]]]]:
    """
    example output: {'AA': {'flow': 0, 'neighbors': ['DD', 'II', 'BB']}, 'BB': {'flow': 13, 'neighbors': ['CC', 'AA']} }
    """
    output = {}
    with open(fname) as f:
        idx = 0
        for line in f.readlines():
            line = line.strip()
            g = re.match(INPUT_REGEX, line).groups()
            output[g[0]] = {"idx": idx, "flow": int(g[1]), "neighbors": g[2].split(", ")}
            idx += 1
    return output

@dataclass
class Node:
    """
    Node is a class that represents a node in the graph
    It stores information like the name of the node, the timetsamp at which it was visited
    the action that was taken and the state of the other nodes in the graph (open or closed)
    """

    flow: int
    name: str
    timestamp: int
    action_open_valve: bool
    state: tuple[bool, ...]
    # prior_steps: tuple[str]

    def get_state(self, graph: dict[str, dict[str, Union[int, list[str]]]], neighbor: str, open_valve: bool) -> tuple[bool, ...]:
        """
        Returns the state of the other nodes in the graph
        """
        new_state = list(self.state)
        new_state[graph[neighbor]["idx"]] = new_state[graph[neighbor]["idx"]] or open_valve
        return tuple(new_state)

    def get_neighbors(self, graph: dict[str, dict[str, Union[int, list[str]]]]) -> list["Node"]:
        """
        Returns a list of nodes that are neighbors of the current node
        """
        neighbors = []
        # can chose to move to a neighbor or
        for neighbor in graph[self.name]["neighbors"]:
            neighbors.append(
                Node(
                    graph[neighbor]["flow"],
                    neighbor,
                    self.timestamp + 1,
                    False,
                    self.get_state(graph, neighbor, False),
                    # tuple(list(self.prior_steps) +[self.name + " OPEN" if self.action_open_valve else self.name]),
                )
            )

        # if the valve is closed and the flow > 0 then you can choose to open it
        if not self.state[graph[self.name]["idx"]]:
            # if the valve is closed you can open it
            # print(self)
            neighbors.append(
                Node(
                    graph[self.name]["flow"],
                    self.name,
                    self.timestamp + 1,
                    True,
                    self.get_state(graph, self.name, True),
                    # tuple(list(self.prior_steps) +[self.name]),
                )
            )
        return neighbors

    # def __hash__(self):
    #     return hash(f"{self.name} {str(self.state)} {self.timestamp} {self.action_open_valve}")

    def future_total_reward(self, max_time_stamp=30):
        """
        Returns the future total reward of the current node
        """
        if self.action_open_valve:
            return self.flow * (max_time_stamp - self.timestamp)
        return 0

    def __hash__(self):
        "hash based on name and state"
        return hash((self.name, self.state))

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.name == other.name and self.state == other.state
        return NotImplemented



def djikstras_algorithm(graph):
    """
    Find the path with the highest reward
    """
    init_flow_state = [False] * len(graph)
    node_index = {node: i for i, node in enumerate(graph)}
    print(node_index)
    for node in graph:
        if graph[node]["flow"] == 0:
            init_flow_state[node_index[node]] = True

    start_node = Node(
        timestamp=0,
        name="AA",
        flow=graph["AA"]['flow'],
        action_open_valve=False,
        state=tuple(init_flow_state),
        # prior_steps=("start",),
    )
    max_flow = sum([graph[node]["flow"]*30 for node in graph])
    print(max_flow)
    total_reward = defaultdict(lambda: max_flow)
    total_reward[start_node] = max_flow
    visited = set()
    queue: set[Node] = {start_node}

    max_reward = max_flow
    max_reward_node = None
    i = 0
    while queue and i < 10000000:
        # print(total_reward)
        node = min(queue, key=lambda x: total_reward[x])
        cumm_reward = total_reward[node]

        if i % 1000 == 0:
            print('queue-len', len(queue), len(set(queue)), len(visited))
            print(node, cumm_reward)

        if node.timestamp == 30 or all(node.state):
            # print("winner", node, cumm_reward)
            if cumm_reward < max_reward:
                max_reward = cumm_reward
                max_reward_node = node
        else:
            for neighbor in node.get_neighbors(graph):
                if neighbor not in visited:
                    # print(node.name, neighbor.name, cumm_reward, neighbor.future_total_reward(), total_reward[neighbor.name])
                    new_cumm_reward = cumm_reward - neighbor.future_total_reward()
                    if new_cumm_reward < total_reward[neighbor]:
                        total_reward[neighbor] = new_cumm_reward
                    queue.add(neighbor)
        visited.add(node)
        queue.remove(node)
        i += 1
        # queue = sorted(queue, reverse=True, key=lambda x: x[0])

    # for k,v in sorted(total_reward.items(), key=lambda x : x[1]):
    #     # if k.timestamp == 24:
    #         print(v, k)
    return max_reward, max_reward_node


def bfs(graph):
    """
    Find the path with the highest reward
    """
    init_flow_state = [False] * len(graph)
    node_index = {node: i for i, node in enumerate(graph)}
    print(node_index)
    for node in graph:
        if graph[node]["flow"] == 0:
            init_flow_state[node_index[node]] = True

    start_node = Node(
        timestamp=0,
        name="AA",
        flow=graph["AA"]['flow'],
        action_open_valve=False,
        state=tuple(init_flow_state),
    )
    visited = set()
    queue: set[tuple[int,Node]] = {(0, start_node)}

    max_reward = 0
    max_reward_node = None
    i = 0
    while queue and i < 10000000:
        cumm_reward, node = queue.pop()
        if i % 10000 == 0:
            print(i, 'queue-len', len(queue), len(set(queue)), len(visited))

        if node.timestamp == 30 or all(node.state):
            # print("winner", node, cumm_reward)
            if cumm_reward > max_reward:
                max_reward = cumm_reward
                max_reward_node = node
        else:
            for neighbor in node.get_neighbors(graph):
                new_cumm_reward = cumm_reward + neighbor.future_total_reward()
                if (new_cumm_reward, neighbor) not in visited:
                    queue.add((new_cumm_reward, neighbor))
        visited.add((cumm_reward, node))
        i += 1
    return max_reward, max_reward_node

# def generate_neighbors(node: str, time_stamp: int, )

def solution1(graph):
    # takes about 10 seconds
    max_reward, node = bfs(graph=graph)
    return max_reward

if __name__ == "__main__":


    node = Node(flow=1, name="A", timestamp=2,  action_open_valve=True, state=(True, False))
    node2 = Node(flow=2, name="A", timestamp=6, action_open_valve=True, state=(True, False))
    node3 = Node(flow=2, name="A", timestamp=6, action_open_valve=True, state=(False, False))

    s = set()
    s.add(node)
    s.add(node2)
    s.add(node3)
    assert len(s) == 2
    print(s)

    # example
    graph = get_data("inputs/day-16-sample.txt")
    assert solution1(graph=graph) == 1651


    graph = get_data("inputs/day-16-input.txt")
    # not optimal solution is to do something with topological sorting and then
    # max length....but this works as well

    # print(djikstras_algorithm(graph=graph))
    assert solution1(graph=graph) == 1915

