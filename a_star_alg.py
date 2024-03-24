import heapq
import time

a_star_dirs = [(0, 1), (0, -1) , (1, 0), (-1, 0), (1, 1), (1, -1), (-1, 1), (-1, -1)]

class Node():
    def __init__(self, parent=None, position=None):
        self.parent = parent
        self.position = position
        self.g = 0
        self.h = 0
        self.f = 0
    
    def __eq__(self, other):
        return (self.position == other.position)

    def __lt__(self, other):
        return (self.f < other.f)

    def __gt__(self, other):
        return (self.f > other.f)
    
def return_path(node):
    path = list()
    c = node
    while (c is not None):
        path.append(c.position)
        c = c.parent
    return path[::-1]

def a_star_heuristic(end, node):
    h = (end.position[0] - node.position[0]) ** 2 + (end.position[1] - node.position[1]) ** 2
    return (h)

def a_star(graph, start, end):
    rows = len(graph)
    cols = len(graph[0])

    start_node = Node(position=start)
    end_node = Node(position=end)

    open_heap = list()
    closed_set = set()

    # convert to min heap and place element onto the heap. 
    heapq.heapify(open_heap)
    heapq.heappush(open_heap, start_node)

    # loop through elements in the open_heap
    while (len(open_heap) > 0):

        node = heapq.heappop(open_heap)
        closed_set.add(node.position)

        # done
        if (node == end_node):
            return return_path(node)
    
        # generate children for the node
        child_nodes = list()
        for (dr, dc) in a_star_dirs:
            # new row, new col
            nr = dr + node.position[0]
            nc = dc + node.position[1]

            # workable if in bounds, etc.
            if (0 <= nr < rows) and (0 <= nc < cols) and (graph[nr][nc] == 0):
                child_nodes.append(Node(parent=node, position=(nr, nc)))
        
        # work through child nodes
        for child in child_nodes:
            if (child.position in closed_set):
                continue

            child.g = node.g + 1
            child.h = a_star_heuristic(end_node, child)
            child.f = child.g + child.h

            # only add to open_heap if it will be better. 
            if len([open_node for open_node in open_heap if child == open_node and child > open_node]) == 0:
                heapq.heappush(open_heap, child)
            
    return None

