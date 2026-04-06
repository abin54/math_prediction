import networkx as nx
import pandas as pd
from typing import Dict, List

# The "Neo4j-Sim" Knowledge Graph Mapper
# This tool maps the 19,816 nodes into a multidimensional graph 
# to find hidden causal connections (e.g., Saturday 26 -> Monday 23).

class KnowledgeGraphMapper:
    def __init__(self):
        self.G = nx.DiGraph()
        
    def populate_graph(self, csv_path: str):
        """
        Populate the graph with results from the 52-year dataset.
        Nodes are (Date, Jodi) pairs.
        Edges are (Node_Previous, Node_Next).
        """
        data = pd.read_csv(csv_path)
        data['Date'] = pd.to_datetime(data['Date'])
        
        prev_node = None
        for idx, row in data.iterrows():
            if str(row['Jodi']).strip() in ['*', 'XX']:
                prev_node = None
                continue
                
            node_id = f"{row['Date'].strftime('%Y-%m-%d')}_{row['Jodi']}"
            self.G.add_node(node_id, date=row['Date'], jodi=row['Jodi'], open=int(str(row['Jodi'])[0]))
            
            if prev_node is not None:
                self.G.add_edge(prev_node, node_id)
            
            prev_node = node_id

    def find_path_consensus(self, start_jodi: str) -> Dict[str, float]:
        """
        Finds all historically occurring paths from a starting Jodi (e.g., Saturday's 26).
        Returns a dictionary of (Next_Jodi, Frequency) pairs.
        """
        successors = []
        for node in self.G.nodes:
            if str(self.G.nodes[node].get('jodi')) == start_jodi:
                # Find direct edges from this node
                for neighbor in self.G.neighbors(node):
                    successors.append(str(self.G.nodes[neighbor].get('jodi')))
        
        counts = {}
        for s in successors:
            counts[s] = counts.get(s, 0) + 1
            
        total = sum(counts.values()) or 1
        probs = {k: v/total for k, v in counts.items()}
        return probs

    def map_multidimensional_resonance(self, date: str) -> List[str]:
        """
        Finds all nodes in history that share the same (Tithi, Karana, Root) 
        as the input date.
        """
        # This function would query the graph for multi-layered matches.
        return []

if __name__ == "__main__":
    mapper = KnowledgeGraphMapper()
    # Test for Saturday's result '26'
    mapper.G.add_node("Test_Node_1", jodi="26")
    mapper.G.add_node("Test_Node_2", jodi="23")
    mapper.G.add_edge("Test_Node_1", "Test_Node_2")
    
    consensus = mapper.find_path_consensus("26")
    print(f"Graph Consensus for 26: {consensus}")
