



# 
from PIL import Image, ImageDraw
import json

# simple HOA graph
image_path = 'hallofarts1.png'  
# (flip the x-y coordinates to rows and cols)
row_lines = [(227, 311, 227, 781), (1088, 311, 1088, 781)]
col_lines = [(227, 311, 1088, 311), (227, 781, 1088, 781)]


# simple HHA level graph
image_path = "hha.png"
row_lines = [(153, 188, 153, 295), (432, 188, 432, 330)]
col_lines = [(153, 188, 432, 188), (153, 295, 432, 295), (432, 330, 949, 330)]

# simple ReH3 Right side graph
image_path = "roberts3.png"
name="roberts3"
row_lines = [(168, 781, 168, 1140), (307, 781, 307, 1140)]
col_lines = [(168, 781, 307, 781),  (168, 1140, 308, 1140)] # needed a +1 on one of the columns... why. 

# TODO: Wiegand gym graph

def img_2_graph(image_path, name):
    img = Image.open(image_path)

    # dimensions
    width, height = img.size

    # to rows and cols
    rows, cols = height, width

    # create graph
    graph = [[1 for _ in range(cols)] for _ in range(rows)]

    # rows
    for row in row_lines:
        for dr in range(row[3]-row[1]):
            graph[row[0]][row[1]+dr] = 0

    # cols
    for col in col_lines:
        print(col)
        for dc in range(col[2]-col[0]):
            graph[col[0]+dc][col[1]] = 0

    # save the graph
    with open(f"{name}.json", "w") as file:
        json.dump(graph, file) 

    # visualize the graph to make sure it's correct. 
    image = Image.new('RGB', (width, height), color='white')
    draw = ImageDraw.Draw(image)

    for y in range(len(graph)):
        for x in range(len(graph[y])):
            color = "green" if graph[y][x] == 0 else "white" 
            draw.rectangle([x, y, x + 1, y + 1], fill=color)

    image.save(f"{name}_eg.png")


if __name__ == "__main__":

    img_2_graph(image_path, name)
