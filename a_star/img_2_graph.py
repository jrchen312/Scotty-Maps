



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
image_path = "wiegandv1.png"
name = "wiegandv1"
row_lines = [
    (225, 398, 225, 1420), # top horizontal
    (873, 398, 873, 859), # bottom horizontal one
    (757, 859, 757, 1420), # bottom horizontal two
    (577, 276, 577, 398), # left emergency exit
]
col_lines = [
    (225, 398, 873, 398), # left vertical
    (108, 870, 225, 870), # top vertical 1
    (225, 904, 421, 904), # top vertical 2
    (757, 859, 1057, 859), #bot vertical 1
    (225, 1420, 757, 1420), #right vertical 
]

# Weigand Gym smaller map around the center
image_path = "wiegandv1.png"
name ='wiegand_small_v1'
row_lines = [
    (326, 490, 326, 1390), #top row
    (390, 877, 390, 1000), #top-mid 1
    (390, 1130, 390, 1235), #top-mid 2
    (625, 872, 625, 1140), #bot-mid
    (690, 490, 690, 873), #bot left
    (662, 872, 662, 1390), #bot right
]
col_lines = [
    (326, 490, 690, 490), #leftmost
    (326, 877, 390, 877), #col 1
    (326, 1000, 390, 1000), #col 2
    (326, 1130, 390, 1130), #col 3
    (326, 1235, 390, 1235), #col 4
    (625, 872, 690, 872),   # col5
    (625, 1140, 662, 1140), #col6
    (326, 1390, 662, 1390), #rightmost
]


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
    # image = Image.new('RGB', (width, height), color='white')
    # image = Image.open(image_path)
    draw = ImageDraw.Draw(img)

    for y in range(len(graph)):
        for x in range(len(graph[y])):
            if graph[y][x] == 0:
                draw.rectangle([x, y, x + 1, y + 1], fill="green")
            # color = "green" if graph[y][x] == 0 else "white" 
            

    img.save(f"{name}_eg.png")


if __name__ == "__main__":

    img_2_graph(image_path, name)
