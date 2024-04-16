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


# convert the path into line segments for the front end to display. 
def convert_path_to_line_segments(path):
    vertices = [path[0]]
    curr_dir = (path[1][0] - path[0][0], path[1][1] - path[0][1])

    for i in range(2, len(path)):
        dir = (path[i][0] - path[i-1][0], path[i][1] - path[i-1][1])
        if (dir != curr_dir):
            curr_dir = dir
            vertices.append(path[i-1]) #ummmm
    vertices.append(path[-1])

    # now need to convert the vertices into line segments
    segments = []
    for i in range(1, len(vertices)):
        segments.append(
            (vertices[i-1][1], vertices[i-1][0], vertices[i][1], vertices[i][0])
        )

    return segments


# possibly provide the icon as well as the direction
ARRIVED_ICON = '<i class="bi bi-pin-map-fill"></i>'
ARRIVED_TEXT = "Arrive"
TURN_LEFT_ICON = '<i class="bi bi-sign-turn-left"></i>'
TURN_LEFT_TEXT = "Turn Left"
TURN_RIGHT_ICON = '<i class="bi bi-sign-turn-right"></i>'
TURN_RIGHT_TEXT = "Turn Right"

def direction_of_turn(segments):
    if (len(segments) <= 1):
        return ARRIVED_TEXT, ARRIVED_ICON

    v0 = (segments[0][2]-segments[0][0], segments[0][1]-segments[0][3])
    v1 = (segments[1][2]-segments[1][0], segments[1][1]-segments[1][3])

    print(v0, v1)
    # vertical direction
    if (v0[0] == 0):
        if (v0[1] * v1[0] < 0):
            return TURN_LEFT_TEXT, TURN_LEFT_ICON
        else:
            return TURN_RIGHT_TEXT, TURN_RIGHT_ICON
    else:
        if (v0[0] * v1[1] < 0):
            return TURN_RIGHT_TEXT, TURN_RIGHT_ICON
        else:
            return TURN_LEFT_TEXT, TURN_LEFT_ICON


# TESTBECH :3
# def hh_A_example():
#     graph = load_graph_from_json("hha_graph.json")
#     print(find_nearest_graph_location(graph, 933, 312))


# provide the navigation path and directions
# TODO: finish implementing directions. 
def navigation_directions(graph_path, user_row, user_col, dest_row, dest_col):
    a = time.time()
    graph = load_graph_from_json(graph_path)

    start = find_nearest_graph_location(graph, user_row, user_col)
    end = find_nearest_graph_location(graph, dest_row, dest_col)

    path = a_star(graph, start, end)

    result = convert_path_to_line_segments(path)

    icon, txt = direction_of_turn(result)

    b = time.time()
    print(f"time_elapsed({b-a})")

    return result, txt, icon
    # save_path_as_image(graph, path)


# runs pretty fast, <0.04 seconds
# def hoa_example():
#     graph = load_graph_from_json("graph.json")

#     start = (1088, 313)
#     end = (250, 781)

#     a = time.time()
#     path = a_star(graph, start, end)
#     b = time.time()
#     print(b-a)

#     print(f"len({len(path)})")
#     save_path_as_image(graph, path)
    
# hoa_example()
# hh_A_example()
    
if __name__ == "__main__":
    # navigation_directions("hha_graph.json", 933, 312, 177, 173)
    vectors = [
        #going up
        [(330, 901, 330, 432), (330, 432, 295, 432)], # left
        [(330, 901, 330, 432), (330, 432, 500, 432)], # right

        #going left
        [(330, 432, 295, 432), (295, 432, 295, 500)], # left
        [(330, 432, 295, 432), (295, 432, 295, 396)], # right

        #going down
        [(330, 432, 330, 901), (330, 901, 500, 901)], # left
        [(330, 432, 330, 901), (330, 901, 200, 901)], # right

        # going right
        [(330, 432, 440, 432), (440, 432, 440, 100)], # left
        [(330, 432, 440, 432), (440, 432, 440, 896)], # right
    ]

    for s in vectors:
        direction_of_turn(s)