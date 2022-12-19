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

    def get_neighbors(self, graph: dict[str, dict[str, Union[int, list[str]]]]) -> list["Node"]:
        """
        Returns a list of nodes that are neighbors of the current node
        """
        neighbors = []
        # can choose to move to a neighbor or
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
            return self.name == other.name and self.state == other.state and self.action_open_valve == other.action_open_valve
        return NotImplemented

def get_init_flow(graph):
    init_flow_state = [False] * len(graph)
    node_index = {node: i for i, node in enumerate(graph)}
    for node in graph:
        if graph[node]["flow"] == 0:
            init_flow_state[node_index[node]] = True
    return tuple(init_flow_state)


def bfs(graph):
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
            for neighbor in node.get_neighbors(graph):
                new_cumm_reward = cumm_reward + neighbor.future_total_reward()
                if (new_cumm_reward, neighbor) not in visited:
                    queue.add((new_cumm_reward, neighbor))
        visited.add((cumm_reward, node))
        i += 1
    return max_reward, max_reward_node


def djikstras_algorithm_for_max_value_path(graph):
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
        action_open_valve=False,
        state=init_flow_state,
        prior_steps=("start",)
    )
    visited: set[Node] = set()
    # queue: set[tuple[int,Node]] = {(0, start_node)}
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
            print(i, 'queue-len', len(queue), len(set(queue)), len(visited))

        visited.add(node)
        if node.timestamp == 30 or all(node.state):
            # print("winner", node, cumm_reward)
            if cumm_reward > max_reward:
                max_reward = cumm_reward
                max_reward_node = node
        else:
            for neighbor in node.get_neighbors(graph):
                # figuring out the movement cost of -1 took me 2.5 days "haha"!!
                new_cumm_reward = cumm_reward + neighbor.future_total_reward() - 1
                if new_cumm_reward > distances[neighbor]:
                    distances[neighbor] = new_cumm_reward
                    queue.add(neighbor)

                # if node.name == "BB" and node.timestamp == 5 and node.action_open_valve:
                #     print(">>>>", neighbor, neighbor in visited, new_cumm_reward, distances[neighbor])
                # if neighbor not in visited:
                #     queue.add(neighbor)


        i += 1
    max_reward = max_reward + max_reward_node.timestamp
    return max_reward, max_reward_node



def bfs_with_2_players(graph):
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
        action_open_valve=False,
        state=init_flow,
    )
    start_node2 = Node(
        timestamp=0,
        name="AA",
        flow=graph["AA"]['flow'],
        action_open_valve=False,
        state=init_flow,
    )

    visited = set()
    queue: set[tuple[int,Node, Node]] = {(0, start_node1, start_node2)}

    max_reward = 0
    max_reward_node = None
    i = 0
    while queue and i < 10000000:
        cumm_reward, node1, node2 = queue.pop()
        if i % 10000 == 0:
            print(i, 'queue-len', len(queue), len(set(queue)), len(visited))

        if node1.timestamp == max_time_stamp \
                or node2.timestamp == max_time_stamp \
                or all(node1.state) \
                or all(node2.state):
            # print("winner", node, cumm_reward)
            if cumm_reward > max_reward:
                max_reward = cumm_reward
                max_reward_node = (node1, node2)

        # TODO: dont let the neighbors compete with each other,
        for neighbor1 in node1.get_neighbors(graph):
            for neighbor2 in node2.get_neighbors(graph):

                n1_state = neighbor1.state
                n2_state = neighbor2.state
                if n1_state != n2_state:
                    # merge states
                    # this line is slow!!!!
                    new_state = tuple(n1 or n2 for n1, n2 in zip(n1_state, n2_state))
                    neighbor1.set_state(new_state)
                    neighbor2.set_state(new_state)

                new_cumm_reward = cumm_reward \
                                  + neighbor1.future_total_reward(max_time_stamp=max_time_stamp) \
                                  + neighbor2.future_total_reward(max_time_stamp=max_time_stamp)

                new_node = (new_cumm_reward, neighbor1, neighbor2)

                if new_node not in visited:
                    queue.add(new_node)

        visited.add((cumm_reward, node1, node2))
        i += 1
    return max_reward, max_reward_node





def solution1(graph):
    # takes about 10 seconds
    max_reward, node = bfs(graph=graph)
    return max_reward

def solution2(graph):
    return bfs_with_2_players(graph=graph)

if __name__ == "__main__":


    # node = Node(flow=1, name="A", timestamp=2,  action_open_valve=True, state=(True, False))
    # node2 = Node(flow=2, name="A", timestamp=6, action_open_valve=True, state=(True, False))
    # node3 = Node(flow=2, name="A", timestamp=6, action_open_valve=True, state=(False, False))
    #
    # s = set()
    # s.add(node)
    # s.add(node2)
    # s.add(node3)
    # assert len(s) == 2
    # print(s)
    #
    # example
    graph = get_data("inputs/day-16-sample.txt")
    # assert solution1(graph=graph) == 1651
    print("starting djikstra's ")
    value, node = djikstras_algorithm_for_max_value_path(graph=graph)
    print(node, value)
    assert value == 1651
    # print(solution2(graph=graph))


    graph = get_data("inputs/day-16-input.txt")
    # not optimal solution is to do something with topological sorting and then
    # max length....but this works as well

    value, node = djikstras_algorithm_for_max_value_path(graph=graph) #== 1915
    assert value == 1915
    # assert solution1(graph=graph) == 1915
    # value, node = djikstras_algorithm_for_max_value_path(graph=graph)
    # print(value, node)

