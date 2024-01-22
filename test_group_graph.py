
from mbuild.tests.base_test import BaseTest
from group_graph import GroupGraph

class TestGroupGraph(BaseTest):
    def __init__(self):
        # Define node types with ports
        node_types = {
            'type1': ['port1', 'port2'],
            'type2': ['port3', 'port4'],
        }

        # Create an instance of GroupGraph for testing
        self.graph = GroupGraph(node_types)

    def test_add_node(self):
        self.graph.add_node('node1', 'type1')
        assert 'node1' in self.graph.nodes
        assert self.graph.nodes['node1']['type'] == 'type1'
        assert self.graph.nodes['node1']['ports'] == ['port1', 'port2']

    def test_add_bond(self):
        self.graph.add_node('node1', 'type1')
        self.graph.add_node('node2', 'type2')
        self.graph.add_bond('node1', 'port1', 'node2', 'port3')

        assert ('node1', 'node2') in self.graph.edges
        assert self.graph.edges['node1', 'node2']['anchors'][0] == ['node1.port1', 'node2.port3']

    def test_make_undirected(self):
        self.graph.add_node('node1', 'type1')
        self.graph.add_node('node2', 'type2')
        self.graph.add_bond('node1', 'port1', 'node2', 'port3')
        self.graph.make_undirected()

        # Check if the graph is undirected
        assert ('node1', 'node2') in self.graph.edges
        assert ('node2', 'node1') in self.graph.edges
        assert self.graph.edges['node1', 'node2']['anchors'][1] == ['node2.port3', 'node1.port1']

    def test_n_free_ports(self):
        self.graph.add_node('node1', 'type1')
        self.graph.add_node('node2', 'type2')
        assert self.graph.n_free_ports('node1') ==  2

        # Connect a bond and recheck
        self.graph.add_bond('node1', 'port1', 'node2', 'port3')
        assert self.graph.n_free_ports('node1') == 1

    def test_str_representation(self):
        self.graph.add_node('node1', 'type1')
        self.graph.add_node('node2', 'type2')
        self.graph.add_bond('node1', 'port1', 'node2', 'port3')

        expected_str = "Nodes (type, ports): [('node1', 'type1'), ('node2', 'type2')], [['port1', 'port2'], ['port3', 'port4']]\nEdges (ports): [[['node1.port1', 'node2.port3']]]"
        assert str(self.graph) == expected_str

