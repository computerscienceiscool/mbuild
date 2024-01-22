import networkx as nx
#   taken from a good answer by Gambit1614 on StackOverflow https://stackoverflow.com/questions/57095809/networkx-connecting-nodes-using-ports

class GroupGraph(nx.Graph):
    """A graph with ports as parts of nodes that can be connected to other ports."""
    def __init__(self, node_types=None):
        super(GroupGraph, self).__init__()
        self.node_types = node_types

    def add_node(self, nodeID, node_type):
        super(GroupGraph, self).add_node(nodeID)
        self.nodes[nodeID]['type'] = node_type
        self.nodes[nodeID]['ports'] = self.node_types[self.nodes[nodeID]['type']]
    
    def add_bond(self, node1, port1, node2, port2):

        edge_ports = []

        for n, p in [(node1, port1), (node2, port2)]:
            # Sanity check to see if the nodes and ports are present in Graph
            if n not in self.nodes:
                raise Exception(f"Node: {p} is not present in Graph")
            if p not in self.nodes(data=True)[n]['ports']:
                raise Exception(f"Port: {p} is incorrect for Node: {n}!")

            edge_ports.append(n + '.' + p)

        # Add the anchor points as edge attributes
        if self.has_edge(node1, node2):
            self.edges[node1, node2]['anchors'].append(edge_ports)
        else:
            super(GroupGraph, self).add_edge(node1, node2, anchors=[edge_ports])

    def make_undirected(self):
        for edge in self.edges:
            node_port = tuple(self.edges[edge]['anchors'].split('.'))
            node_s, node_t = edge
            port_s, port_t = edge['anchors'][0], edge['anchors'][1]
            self.add_bond(node_t, port_t, node_s, port_s)
            self.edges[edge]['anchors'].append(f'{node_port[1]}.{node_port[0]}')
        
    def n_free_ports(self, node):
        # num ports - num edges - num edges with node as target
        n_edges_with_node_target = 0
        for e in self.edges():
            for port_edge in self.edges[e]['anchors']:
                if port_edge[-1].split('.')[0] == node:
                    n_edges_with_node_target += 1
        return len(self.nodes[node]['ports']) - len(list(list(self.edges(data=True))[0][-1].values())[0]) - n_edges_with_node_target

    def __str__(self):
        return f"Nodes (type, ports): {self.nodes.data('type')}, {self.nodes.data('ports')}\nEdges (ports): {self.edges.data('anchors')}"

if __name__ == '__main__':
    pG = GroupGraph(node_types={
        'C4':['s1', 's2', 's3', 's4'], 
        'H1':['s1'], 
        'N3':['s1', 's2', 's3'],
    })
    
    pG.add_node('a', node_type='C4')
    pG.add_node('b', node_type='H1')
    pG.add_node('c', node_type='N3')
    pG.add_bond('a', 's1', 'c', 's1')
    print(pG.n_free_ports('a'))
    pG.add_bond('a', 's2', 'c', 's2')
    print(pG.n_free_ports('a'))
    pG.add_bond('b', 's1', 'a', 's3')
    # pG.make_undirected()
    print(pG.n_free_ports('a'))
    print(pG)