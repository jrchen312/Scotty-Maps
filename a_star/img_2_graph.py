



# 
from PIL import Image, ImageDraw
import json

image_path = 'hallofarts1.png'  # Replace with your image file path


def img_2_graph(image_path):
    img = Image.open(image_path)

    # dimensions
    width, height = img.size

    # to rows and cols
    rows, cols = height, width

    # create graph
    graph = [[1 for _ in range(cols)] for _ in range(width)]



    # rows
    rows = [(227, 311, 227, 781), (1088, 311, 1088, 781)]
    for row in rows:
        for dr in range(row[3]-row[1]):
            graph[row[0]][row[1]+dr] = 0

    # cols
    cols = [(227, 311, 1088, 311), (227, 781, 1088, 781)]
    for col in cols:
        for dc in range(col[2]-col[0]):
            graph[col[0]+dc][col[1]] = 0

    # save the graph
    with open("graph.json", "w") as file:
        json.dump(graph, file) 

    # visualize the graph to make sure it's correct. 
    image = Image.new('RGB', (width, height), color='white')
    draw = ImageDraw.Draw(image)

    for y in range(len(graph)):
        for x in range(len(graph[y])):
            color = "green" if graph[y][x] == 0 else "white" 
            draw.rectangle([x, y, x + 1, y + 1], fill=color)

    image.save("graph.png")


if __name__ == "__main__":
    img_2_graph(image_path)
