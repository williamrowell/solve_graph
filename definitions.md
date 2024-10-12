# Definitions



## node

Nodes represent 1-indexed segments of sequence.  Nodes have an id, a first position, and a last position used BED-style coordinates.  The first or last positions may be specified as `*` to denote that they are the first or last node in the path. Nodes are always represented as top strand reference orientation.  node_id are assigned as consecutive letters in top strand reference order.

```
N node_id first last
```

## edge

Edges are connections between nodes.

```
E node_id1 node_id2 node_id1_end node_id2_end orientation explicit read_support
```

- node ends are defined as true (5', left) or false (3', right), wrt the reference orientation of the node and always represent the first or last position of the node
- orientation is defined as true (same) or false (opposite) with respect to the relative orientations, i.e., an edge that exits node2 on the right and enters node1 from the right as an opposite orientation
- explicit/implicit (bool) is a flag that indicates whether the edge is explicit (true) or implicit (false)
  - explicit edges pass from node to node with a discontinuity in position, i.e., the right end of node_id1 is not the same as the left end of node_id2
  - implicit edges pass from node to node without a discontinuity in position; i.e. the right end of node_id1 is directly connected to the left end of node_id2 in the same orientation
  - edges representing deletions or insertions always connect opposite ends in the same orientation
  - edges representing inversions always connect ends in opposite orientations
- read_support is the number (int) of reads supporting the edge
  - for implicit edges, read_support is the read depth at the position of the edge
  - for explicit edges, read_support is the number of reads that span the edge
- edges are bidirectional, i.e., an edge exiting node1 on the right and entering node2 on the left in the same orientation is equivalent to an edge exiting node2 on the right and entering node1 on the left in the same orientation
- paths travel from left to right, unless the edge specifies opposite orientation, in which case the path switches direction

## directions

Using python3 and the networkx library:
- create nodes for all segments between breakpoints
- create explicit edges (in both directions) for all breakpoints represented in the BAM file
- create implicit edges for all adjacent segments in the BAM file
- find all parsimonious paths that:
  - enter from the "first" node and exits from the "last" node in the left-to-right-orientation
  - passes through all explicit edges at least once
- a parsimonious path is a path that includes no more cycles than necessary to pass through all explicit edges at least once
