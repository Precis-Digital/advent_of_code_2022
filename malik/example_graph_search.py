
# q: what is the capital of france?
# a: paris

# q: what is the capital of sweden?
# a: stockholm

# Q: what is the capital of cambodia?
# A: phnom penh

# q: what is the command for undoing a commit?
# a: git reset --soft HEAD~1
# q: what is the command for undoing a commit and keeping the files?
# a: git reset --mixed HEAD~1

# Q: what is the command for stashing changes?
# A: git stash

# q: do you like python?
# a: yes

# q: do you like javascript?




acyclic_graph = {
    "A": ["B", "C"],
    "B": ["D", "E"],
    "C": ["F", "G"],
    "D": ["H", "I"],
    "E": ["J", "K"],
    "F": ["L", "M"],
    "G": ["N", "O"],
    "O": ["P"],
    "P": ["Q"],
    "Q": ["R"],
    "R": ["S"],
    "S": ["T"],
}


def graph_search(graph, pop_index=0):
    """graph search"""
    visited = []
    arr = [("A",)]
    while arr:
        path = arr.pop(pop_index)
        print(" > ".join(path))
        node = path[-1]

        if node not in visited:
            visited.append(node)
            children = graph.get(node, [])
            for child in children:
                arr.append(tuple(list(path) + [child]))
    return visited

def breadth_first_search(graph):
    return graph_search(graph, pop_index=0)

def depth_first_search(graph):
    return graph_search(graph, pop_index=-1)

if __name__ == '__main__':
    print("Breadth first search:")
    print("#" * 20)
    breadth_first_search(acyclic_graph)

    print("Depth first search:")
    print("#" * 20)
    depth_first_search(acyclic_graph)
