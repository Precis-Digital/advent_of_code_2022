# partially compelted

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


def simple_bfs(graph, start, end):

    queue = [(0, start)]
    visited = set()

    while queue:
        path_len, n = queue.pop(0)
        if n == end:
            return path_len

        for neighbor in graph[n]['neighbors']:
            if neighbor not in visited:
                queue.append((path_len + 1, neighbor))
        visited.add(n)

def compute_pairwise_distance(graph) -> dict[str, dict[str, int]]:
    output = {}
    for i in graph:
        for j in graph:
            if i != j:
                # from_node = min(i, j)
                # to_node = max(i, j)
                dist: int = simple_bfs(graph=graph, start= i, end=j)
                inner_dict: dict = output.get(i, {})
                inner_dict[j] = dist
                output[i] = inner_dict
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
    prior_steps: tuple[str] = None

    def set_state(self, state: tuple[bool, ...]):
        self.state = state

    def get_state(self, graph: dict[str, dict[str, Union[int, list[str]]]], neighbor: str, open_valve: bool) -> tuple[bool, ...]:
        """
        Returns the state of the other nodes in the graph
        """
        new_state = list(self.state)
        new_state[graph[neighbor]["idx"]] = new_state[graph[neighbor]["idx"]] or open_valve
        return tuple(new_state)


    def get_neighbors_with_pairwise_distance(self, graph: dict[str, dict[str, Union[int, list[str]]]], pairwise_distance: dict[str, dict[str, int]], max_time_stamp: int = 30) -> list["Node"]:
        """
        using the pairwise distance to get the neighbors, simulate the time it takes to get to the neighbor
        and turn on the value if it is not already on
        :param graph:
        :param pairwise_distance:
        :return:
        """

        neighbors = []
        for to_node, distance in pairwise_distance[self.name].items():
            new_timestamp = self.timestamp + distance + 1
            if new_timestamp > max_time_stamp:
                continue
            if not self.state[graph[to_node]["idx"]]:
                neighbors.append(
                    Node(
                        graph[to_node]["flow"],
                        to_node,
                        new_timestamp,
                        True,
                        self.get_state(graph, to_node, True),
                    )
                )
        return neighbors

    def future_total_reward(self, max_time_stamp=30):
        """
        Returns the future total reward of the current node
        """
        if self.action_open_valve:
            return self.flow * (max_time_stamp - self.timestamp)
        return 0

    def __hash__(self):
        "hash based on name and state"
        return hash((self.name, self.state, self.action_open_valve))

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.name == other.name \
                and self.state == other.state \
                and self.action_open_valve == other.action_open_valve
        return NotImplemented

def get_init_flow(graph):
    init_flow_state = [False] * len(graph)
    node_index = {node: i for i, node in enumerate(graph)}
    for node in graph:
        if graph[node]["flow"] == 0:
            init_flow_state[node_index[node]] = True
    return tuple(init_flow_state)


def bfs(graph, pairwise_distance=None):
    """
    Find the path with the highest reward
    """
    init_flow_state = get_init_flow(graph)

    start_node = Node(
        timestamp=0,
        name="AA",
        flow=graph["AA"]['flow'],
        action_open_valve=False,
        state=init_flow_state,
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
            for neighbor in node.get_neighbors_with_pairwise_distance(graph, pairwise_distance=pairwise_distance):
                new_cumm_reward = cumm_reward + neighbor.future_total_reward()
                if (new_cumm_reward, neighbor) not in visited:
                    queue.add((new_cumm_reward, neighbor))
        visited.add((cumm_reward, node))
        i += 1
    return max_reward, max_reward_node


def djikstras_algorithm_for_max_value_path(graph, pairwise_distance):
    """
    take as input the graph and compute a variant of djikstra's algorithm to calculate
    the highest value path
    :param graph:
    :return:
    """

    init_flow_state = get_init_flow(graph)
    max_timestamp = 30
    distances = defaultdict(lambda : float("-inf"))

    start_node = Node(
        timestamp=0,
        name="AA",
        flow=graph["AA"]['flow'],
        action_open_valve=True,
        state=init_flow_state,
        prior_steps=("start",)
    )
    visited: set[Node] = set()
    queue: set[Node] = {start_node}
    distances[start_node] = 0

    max_reward = 0
    max_reward_node = None
    i = 0
    while queue and i < 10000000:
        T = max(queue, key=lambda x: distances[x])
        queue.remove(T)
        node = T
        cumm_reward = distances[node]
        # print(node, cumm_reward)
        if i % 10000 == 0:
            print(i, 'queue-len', len(queue), len(set(queue)), len(visited), max_reward)


        # udpate final reward
        final_reward = cumm_reward + node.timestamp
        if final_reward > max_reward:
            max_reward = final_reward
            max_reward_node = node

        # for neighbor in node.get_neighbors(graph):
        for neighbor in node.get_neighbors_with_pairwise_distance(graph, pairwise_distance=pairwise_distance):
            new_cumm_reward = cumm_reward + neighbor.future_total_reward() - (neighbor.timestamp - node.timestamp)
            # print(">>>", neighbor, new_cumm_reward)
            if new_cumm_reward > distances[neighbor]:
                distances[neighbor] = new_cumm_reward
                queue.add(neighbor)
        visited.add(node)
        i += 1
    print('num nodes checked', len(visited), 'iter', i)
    max_reward = max_reward
    return max_reward, max_reward_node



def djikstras_with_2_players(graph, pairwise_distance):
    """
    version of bfs but inseted 2 agents are traversing the graphs simultaneously
    :param graph:
    :return:
    """
    max_time_stamp = 26
    init_flow: tuple[bool, ...] = get_init_flow(graph=graph)

    start_node1 = Node(
        timestamp=0,
        name="AA",
        flow=graph["AA"]['flow'],
        action_open_valve=True,
        state=init_flow,
    )
    start_node2 = Node(
        timestamp=0,
        name="AA",
        flow=graph["AA"]['flow'],
        action_open_valve=True,
        state=init_flow,
    )

    visited = set()
    start = (start_node1, start_node2)
    queue: set[tuple[Node, Node]] = {start}
    distances = defaultdict(lambda : float("-inf"))
    distances[start] = 0

    max_reward = 0
    max_reward_node = None
    i = 0
    while queue and i < 10000000:
        T = max(queue, key=lambda x: distances[x])
        queue.remove(T)
        node = T
        cumm_reward = distances[node]
        # print(i, (node[0].name, node[0].timestamp), (node[1].name, node[1].timestamp), cumm_reward)
        if i % 10000 == 0:
            print(i, 'queue-len', len(queue), len(set(queue)), len(visited), max_reward)

        # udpate final reward
        final_reward = cumm_reward + node[0].timestamp + node[1].timestamp
        if final_reward > max_reward:
            print(max_reward, max_reward_node)
            max_reward = final_reward
            max_reward_node = node

        # for neighbor in node.get_neighbors(graph):
        agent1, agent2 = node

        for n1 in agent1.get_neighbors_with_pairwise_distance(graph, pairwise_distance=pairwise_distance, max_time_stamp=max_time_stamp):
            for n2 in agent2.get_neighbors_with_pairwise_distance(graph, pairwise_distance=pairwise_distance, max_time_stamp=max_time_stamp):
                if n1 != n2:

                    new_state = tuple(a or b for a, b in zip(n1.state, n2.state))
                    # new_timestamp = max(n1.timestamp, n2.timestamp)
                    n1_prime = Node(
                        timestamp=n1.timestamp,
                        name=n1.name,
                        flow=graph[n1.name]['flow'],
                        action_open_valve=True,
                        state=new_state
                    )
                    n2_prime = Node(
                        timestamp=n2.timestamp,
                        name=n2.name,
                        flow=graph[n2.name]['flow'],
                        action_open_valve=True,
                        state=new_state
                    )

                    new_node = (n1_prime, n2_prime)
                    # if new_node in queue:
                    #     print(new_node)

                    new_cumm_reward = cumm_reward \
                                      + n1_prime.future_total_reward(max_time_stamp=max_time_stamp) - (n1_prime.timestamp - agent1.timestamp) \
                                      + n2_prime.future_total_reward(max_time_stamp=max_time_stamp) - (n2_prime.timestamp - agent2.timestamp)
                    # print(">>>", neighbor, new_cumm_reward)
                    if new_cumm_reward > distances[new_node]:
                        distances[new_node] = new_cumm_reward
                        queue.add(new_node)
        visited.add(node)
        i += 1
    print('num nodes checked', len(visited), 'iter', i)
    max_reward = max_reward
    return max_reward, max_reward_node


def solution1(graph):
    # takes about 10 seconds
    pairwise_distance = compute_pairwise_distance(graph=graph)
    max_reward, node = djikstras_algorithm_for_max_value_path(graph=graph, pairwise_distance=pairwise_distance)
    return max_reward

def solution2(graph):
    pw_dist = compute_pairwise_distance(graph=graph)
    value, node = djikstras_with_2_players(graph=graph, pairwise_distance=pw_dist)
    return value
if __name__ == "__main__":


    graph = get_data("inputs/day-16-sample.txt")

    pw_dist = compute_pairwise_distance(graph=graph)
    value = solution1(graph=graph)
    # value, node = djikstras_algorithm_for_max_value_path(graph=graph, pairwise_distance=pw_dist)
    # print(node, value)
    assert value == 1651

    value = solution2(graph=graph)
    assert value == 1707

    graph = get_data("inputs/day-16-input.txt")
    value = solution1(graph=graph)
    assert value == 1915

    # this takes a long time laughing emoji :))), about 10 minutes
    value = solution2(graph=graph)
    assert value == 2772
