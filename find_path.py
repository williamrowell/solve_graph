import json
import sys
import networkx as nx
import matplotlib.pyplot as plt

ENDS = {"LEFT": True, "RIGHT": False}

# create graph
G = nx.DiGraph()

# Nodes data
with open(sys.argv[1]) as f:
    nodes_data = json.load(f)


def complementary_node_id(node_id):
    return node_id if node_id.endswith("'") else f"{node_id}'"


def minus_strand_node(node):
    return {
        "node_id": complementary_node_id(node["node_id"]),
        "first": node["last"],
        "last": node["first"],
    }


# add nodes
for node in nodes_data + [minus_strand_node(_) for _ in nodes_data]:
    node_id = node["node_id"]
    G.add_node(node_id, first=node["first"], last=node["last"])

# Explicit edges data
with open(sys.argv[2]) as f:
    explicit_edges_data = json.load(f)

implicit_edges_data = [
    {
        "node_id1": first["node_id"],
        "node_id2": second["node_id"],
        "node1_exit": "RIGHT",
        "node2_enter": "LEFT",
        "explicit": False,
        "read_support": 5,
    }
    for first, second in zip(nodes_data, nodes_data[1:])
]

# add edges
for edge in implicit_edges_data + explicit_edges_data:
    # we're going to add the edge twice, once for each direction
    # since it's still just a single edge, we'll assign a unique id
    # use the unique_id later to require that an explicit edge is only traversed once
    unique_edge_id = f"{edge['node_id1']}_{edge['node_id2']}"
    G.add_edge(
        edge["node_id1"],
        edge["node_id2"],
        node1_exit=ENDS[edge["node1_exit"]],
        node2_enter=ENDS[edge["node2_enter"]],
        explicit=edge["explicit"],
        read_support=edge["read_support"],
        unique_id=unique_edge_id,
    )
    G.add_edge(
        complementary_node_id(edge["node_id2"]),
        complementary_node_id(edge["node_id1"]),
        node1_exit=ENDS[edge["node1_exit"]],
        node2_enter=ENDS[edge["node2_enter"]],
        explicit=edge["explicit"],
        read_support=edge["read_support"],
        unique_id=unique_edge_id,
    )

# print(G.nodes(data=True))
# print(G.edges(data=True))

first_node = nodes_data[0]["node_id"]
last_node = nodes_data[-1]["node_id"]

# def sort_neighbors(G, current_node):
#   neighbors = G.neighbors(current_node)
#   return sorted(neighbors, key=lambda neighbor: G[current_node][neighbor]['explicit'])

# def follow_path(G, first_node, last_node, path, visited_edges=set()):
#   current_node = first_node
#   for neighbor in sort_neighbors(G, current_node):
#     if G[current_node][neighbor]['explicit'] and G[current_node][neighbor]['unique_id'] in visited_edges:
#       continue
#     if neighbor != last_node:
#       if G[first_node][neighbor]['explicit']:
#         visited_edges.add(G[first_node][neighbor]['unique_id'])
#       follow_path(G, neighbor, last_node, path + str(neighbor), visited_edges=visited_edges)
#     else:
#       print (path + str(neighbor))

# follow_path(G, first_node, last_node, first_node)


def plot_graph(G):
    nx.draw_networkx(
        G,
        pos=nx.planar_layout(G),
        with_labels=True,
    )
    plt.show()


# plot_graph(G)

print("All simple paths:")
for path in sorted(
    nx.all_simple_paths(G, first_node, last_node), key=lambda path: len(path)
):
    print(" -> ".join(path))

print("All shortest paths:")
for path in sorted(
    nx.all_shortest_paths(G, first_node, last_node), key=lambda path: len(path)
):
    print(" -> ".join(path))

print("Cycles:")
for cycle in nx.simple_cycles(G):
    print(" -> ".join(cycle))
