import json
import os
import argparse

import cv2
import matplotlib.pyplot as plt
from matplotlib.widgets import RectangleSelector

SUPPORTED_IMAGE_SUGGESTIONS = ['.jpg']


def line_select_callback(clk, rls):
    global tl_list
    global br_list
    tl_list.append((int(clk.xdata), (int(clk.ydata))))
    br_list.append((int(rls.xdata), (int(rls.ydata))))


def toggle_selector(event):
    toggle_selector.RS.set_active(True)


def onkeypress(event):
    global tl_list
    global br_list
    if event.key == 'q':
        generate_json(tl_list, br_list)
        tl_list = []
        br_list = []


def generate_json(tl_list, br_list):
    image_dict = {"image": file_name, "annotations": []}
    if len(tl_list) != 0:
        label_dict = {"label": '', "coordinates": {}}
        coord_dict = {"x": int, "y": int, "width": int, "height": int}

        center_x = int(abs((tl_list[0][0] - br_list[0][0]) / 2)) + int(tl_list[0][0])
        center_y = int(abs((tl_list[0][1] - br_list[0][1]) / 2)) + int(tl_list[0][1])

        width = int(abs(tl_list[0][0] - br_list[0][0]))
        height = int(abs(tl_list[0][1] - br_list[0][1]))

        coord_dict['x'] = center_x
        coord_dict['y'] = center_y
        coord_dict['width'] = width
        coord_dict['height'] = height

        label_dict['label'] = name_class
        label_dict['coordinates'] = coord_dict

        image_dict['annotations'].append(label_dict)

    annotations.append(image_dict)


def process_images(source, destination, result):
    global file_name, name_class, annotations, tl_list, br_list, toggle_selector
    annotations_file = destination + '/' + result

    annotations = []
    tl_list = []
    br_list = []
    file_names = os.listdir(source)
    for file_name in file_names:
        if is_image(file_name):
            print(f'Processing {file_name}...')
            process_image(file_name, source, toggle_selector)
    print('Number of Processed Images:', len(annotations))
    json_file = json.dumps(annotations)
    with open(annotations_file, 'w') as f:
        f.write(json_file)


def process_image(file_name, source, toggle_selector):
    global name_class
    name_class, sep, tail = file_name.partition('_')
    dir_file = source + '/' + file_name
    fig, ax = plt.subplots(1)
    image = cv2.imread(dir_file)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    ax.imshow(image)
    toggle_selector.RS = RectangleSelector(
        ax, line_select_callback,
        useblit=True,
        button=[1], minspanx=5, minspany=5,
        spancoords='pixels', interactive=True
    )
    bbox = plt.connect('key_press_event', toggle_selector)
    key = plt.connect('key_press_event', onkeypress)
    plt.show()


def is_image(file_name):
    _, extension = os.path.splitext(file_name)
    return extension in SUPPORTED_IMAGE_SUGGESTIONS


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--source', help='Directory containing files to analyze', required=True)
    parser.add_argument('--destination', help='Directory where to drop the annotations file', required=True)
    parser.add_argument('--result', help='Filename of the resulting JSON file containing the annotations',
                        default='annotations.json')
    args = parser.parse_args()

    process_images(args.source, args.destination, args.result)
