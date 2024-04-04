import heapq
import time
import json
from PIL import Image, ImageDraw

a_star_dirs = [(0, 1), (0, -1) , (1, 0), (-1, 0)] #, (1, 1), (1, -1), (-1, 1), (-1, -1)]

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
    return (h)**(0.5)

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
            if (0 <= nr < rows) and (0 <= nc < cols) and (graph[nr][nc] == 0) and ((nr, nc) not in closed_set):
                child_nodes.append(Node(parent=node, position=(nr, nc)))
        
        # work through child nodes
        for child in child_nodes:
            # compute f, g, h for the child node
            child.g = node.g + 1
            child.h = a_star_heuristic(end_node, child)
            child.f = child.g + child.h
            
            # if child already exists on the heap, merge nodes
            # idx = open_heap.index(child)
            if child in open_heap: 
                idx = open_heap.index(child) 
                
                if (child.g < open_heap[idx].g):
                   open_heap[idx] = child
            else:
                # Add the child to the open list
                heapq.heappush(open_heap, child)
    return None

def load_graph_from_json(filename="graph.json"):
    with open(filename, "r") as file:
        return json.load(file)


def save_path_as_image(graph, path):
    width = len(graph[0])
    height = len(graph)

    for p in path:
        graph[p[0]][p[1]] = 10

    # visualize the graph to make sure it's correct. 
    image = Image.new('RGB', (width, height), color='white')
    draw = ImageDraw.Draw(image)

    for y in range(len(graph)):
        for x in range(len(graph[y])):
            color = "green" if graph[y][x] == 10 else "white" 
            draw.rectangle([x, y, x + 1, y + 1], fill=color)

    image.save("graph.png")


# bfs search to find the nearest nearest graph point to the user point
bfs_directions = [(1, 0), (0, 1), (-1, 0), (0, -1)]
def find_nearest_graph_location(graph, init_row, init_col):
    rows = len(graph)
    cols = len(graph[0])

    seen = set() # seen objects
    search = list() # search list

    seen.add((init_row, init_col))
    search.append((init_row, init_col))

    while len(search) > 0:

        # for the elements in our current layer
        for _ in range(len(search)):
            parent_row, parent_col = search.pop(0)

            if (graph[parent_row][parent_col] == 0):
                return (parent_row, parent_col)

            for (dr, dc) in bfs_directions:
                nr, nc = parent_row + dr, parent_col + dc

                if (0 <= nr < rows) and (0 <= nc < cols) and ((nr, nc) not in seen):
                    seen.add((nr, nc))
                    search.append((nr, nc))

def hh_A_example():
    graph = load_graph_from_json("hha_graph.json")
    print(find_nearest_graph_location(graph, 933, 312))


def navigation_directions(graph_path, user_row, user_col, dest_row, dest_col):
    a = time.time()
    graph = load_graph_from_json(graph_path)

    start = find_nearest_graph_location(graph, user_row, user_col)
    end = find_nearest_graph_location(graph, dest_row, dest_col)

    path = a_star(graph, start, end)
    b = time.time()
    print(len(path), b-a)

    save_path_as_image(graph, path)


# runs pretty fast, <0.04 seconds
def hoa_example():
    graph = load_graph_from_json("graph.json")

    start = (1088, 313)
    end = (250, 781)

    a = time.time()
    path = a_star(graph, start, end)
    b = time.time()
    print(b-a)

    print(f"len({len(path)})")
    save_path_as_image(graph, path)
    
# hoa_example()
# hh_A_example()
    
navigation_directions("hha_graph.json", 933, 312, 177, 173)