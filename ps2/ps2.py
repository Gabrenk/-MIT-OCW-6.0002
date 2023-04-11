# 6.0002 Problem Set 5
# Graph optimization
# Name: Breno
# Collaborators: --
# Time: 2days

#
# Finding shortest paths through MIT buildings
#
import unittest
from copy import deepcopy
from graph import Digraph, Node, WeightedEdge


# Problem 2b: Implementing load_map
def load_map(map_filename):
    """
    Parses the map file and constructs a directed graph

    Parameters:
        map_filename : name of the map file

    Assumes:
        Each entry in the map file consists of the following four positive
        integers, separated by a blank space:
            From To TotalDistance DistanceOutdoors
        e.g.
            32 76 54 23
        This entry would become an edge from 32 to 76.

    Returns:
        a Digraph representing the map
    """
    file = open(map_filename, "r")
    map_graph = Digraph()
    #each line has 4 entries 
    #first 2 are t location of the buildings
    #3rd is the total distance and 4th is the outside distance
    for line in file:
        Node_list = []
        line =  line.strip('\n').split(' ')        
        for i in range(0, 2):
            actual_node = Node(line[i])
            Node_list.append(actual_node)
            if not map_graph.has_node(actual_node):
                map_graph.add_node(actual_node)
                
        edge = WeightedEdge(Node_list[0], Node_list[1], int(line[2]), int(line[3]))
        map_graph.add_edge(edge)
    
    file.close()
    print("Loading map from file...")
    return map_graph

# Problem 2c: Testing load_map
# Include the lines used to test load_map below, but comment them out
#if __name__ == "__main__":
#     load_map("mit_map.txt")

# Problem 3b: Implement get_best_path
def get_best_path(digraph, start, end, path, max_dist_outdoors, best_dist,
                  best_path):
    """
    Finds the shortest path between buildings subject to constraints.

    Parameters:
        digraph: Digraph instance
            The graph on which to carry out the search
        start: string
            Building number at which to start
        end: string
            Building number at which to end
        path: list composed of [[list of strings], int, int]
            Represents the current path of nodes being traversed. Contains
            a list of node names, total distance traveled, and total
            distance outdoors.
        max_dist_outdoors: int
            Maximum distance spent outdoors on a path
        best_dist: int
            The smallest distance between the original start and end node
            for the initial problem that you are trying to solve
        best_path: list of strings
            The shortest path found so far between the original start
            and end node.

    Returns:
        A tuple with the shortest-path from start to end, represented by
        a list of building numbers (in strings), [n_1, n_2, ..., n_k],
        where there exists an edge from n_i to n_(i+1) in digraph,
        for all 1 <= i < k and the distance of that path.

        If there exists no path that satisfies max_total_dist and
        max_dist_outdoors constraints, then return None.
    """
    
    #change from the base case, allowing path to store more than just the path
    #but also the distances
    #path[0] = actual path, [1] = current distance, [2] = current outdoor
    
    #Check if node existis
    if not (digraph.has_node(Node(item)) for item in (start, end)):
        raise ValueError("Node not in digraph")
    
    #update actual path
    current_path, current_total_distance, current_outdoor = path
    current_path = current_path + [start]
    
    #check if we've arrived at the end, base case
    if start == end:
        if current_total_distance <= best_dist:
            best_dist = current_total_distance
            best_path = current_path
            return (best_path, best_dist)
        return None
    
    # If we haven't, start recursive part
    else:
        #get all children
        for edge in digraph.get_edges_for_node(Node(start)):
            #then check if alredy in path, avoiding cycles
            if str(edge.get_destination()) not in current_path:
                new_total_distance = current_total_distance + edge.get_total_distance()
                new_outdoor_distance = current_outdoor + edge.get_outdoor_distance()
                #check if max dist outdoors was exceeded
                #and if actual pathis longer than shortest path found
                if (max_dist_outdoors >= new_outdoor_distance 
                    and new_total_distance <= best_dist):
                    #storing in next_path, just to make it more readable
                    next_path = [current_path, new_total_distance, new_outdoor_distance]
                    new_path = get_best_path(digraph, str(edge.get_destination()), end, next_path,
                                             max_dist_outdoors, best_dist, best_path)
                    # new_path must be valid, check for none
                    if new_path != None:
                        best_path, best_dist = new_path
    return (best_path, best_dist)

                
            
            
    
    


def directed_dfs(digraph, start, end, max_total_dist, max_dist_outdoors):
    """
    Finds the shortest path from start to end using a directed depth-first
    search. The total distance traveled on the path must not
    exceed max_total_dist, and the distance spent outdoors on this path must
    not exceed max_dist_outdoors.
    Parameters:
        digraph: Digraph instance
            The graph on which to carry out the search
        start: string
            Building number at which to start
        end: string
            Building number at which to end
        max_total_dist: int
            Maximum total distance on a path
        max_dist_outdoors: int
            Maximum distance spent outdoors on a path
    Returns:
        The shortest-path from start to end, represented by
        a list of building numbers (in strings), [n_1, n_2, ..., n_k],
        where there exists an edge from n_i to n_(i+1) in digraph,
        for all 1 <= i < k
        If there exists no path that satisfies max_total_dist and
        max_dist_outdoors constraints, then raises a ValueError.
    """
    
    #call get_best_path function with an empty path
    best_path = get_best_path(digraph, start, end, [[],0,0],
                              max_dist_outdoors, max_total_dist, None)
    #using max_total_dist as best_dist will check it. Giving an travaled path
    #different than None if it's possible
    if best_path[0] != None:
        return best_path[0]
    else:
        raise ValueError("Unable to find a path")
    

    

# ================================================================
# Begin tests -- you do not need to modify anything below this line
# ================================================================

class Ps2Test(unittest.TestCase):
    LARGE_DIST = 99999

    def setUp(self):
        self.graph = load_map("mit_map.txt")

    def test_load_map_basic(self):
        self.assertTrue(isinstance(self.graph, Digraph))
        self.assertEqual(len(self.graph.nodes), 37)
        all_edges = []
        for _, edges in self.graph.edges.items():
            all_edges += edges  # edges must be dict of node -> list of edges
        all_edges = set(all_edges)
        self.assertEqual(len(all_edges), 129)

    def _print_path_description(self, start, end, total_dist, outdoor_dist):
        constraint = ""
        if outdoor_dist != Ps2Test.LARGE_DIST:
            constraint = "without walking more than {}m outdoors".format(
                outdoor_dist)
        if total_dist != Ps2Test.LARGE_DIST:
            if constraint:
                constraint += ' or {}m total'.format(total_dist)
            else:
                constraint = "without walking more than {}m total".format(
                    total_dist)

        print("------------------------")
        print("Shortest path from Building {} to {} {}".format(
            start, end, constraint))

    def _test_path(self,
                   expectedPath,
                   total_dist=LARGE_DIST,
                   outdoor_dist=LARGE_DIST):
        start, end = expectedPath[0], expectedPath[-1]
        self._print_path_description(start, end, total_dist, outdoor_dist)
        dfsPath = directed_dfs(self.graph, start, end, total_dist, outdoor_dist)
        print("Expected: ", expectedPath)
        print("DFS: ", dfsPath)
        self.assertEqual(expectedPath, dfsPath)

    def _test_impossible_path(self,
                              start,
                              end,
                              total_dist=LARGE_DIST,
                              outdoor_dist=LARGE_DIST):
        self._print_path_description(start, end, total_dist, outdoor_dist)
        with self.assertRaises(ValueError):
            directed_dfs(self.graph, start, end, total_dist, outdoor_dist)

    def test_path_one_step(self):
        self._test_path(expectedPath=['32', '56'])

    def test_path_no_outdoors(self):
        self._test_path(
            expectedPath=['32', '36', '26', '16', '56'], outdoor_dist=0)

    def test_path_multi_step(self):
        self._test_path(expectedPath=['2', '3', '7', '9'])

    def test_path_multi_step_no_outdoors(self):
        self._test_path(
            expectedPath=['2', '4', '10', '13', '9'], outdoor_dist=0)

    def test_path_multi_step2(self):
        self._test_path(expectedPath=['1', '4', '12', '32'])

    def test_path_multi_step_no_outdoors2(self):
        self._test_path(
            expectedPath=['1', '3', '10', '4', '12', '24', '34', '36', '32'],
            outdoor_dist=0)

    def test_impossible_path1(self):
        self._test_impossible_path('8', '50', outdoor_dist=0)

    def test_impossible_path2(self):
        self._test_impossible_path('10', '32', total_dist=100)


if __name__ == "__main__":
    unittest.main()
