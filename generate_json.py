import json
import os
import argparse

import cv2
import matplotlib.pyplot as plt
from matplotlib.widgets import RectangleSelector

SUPPORTED_IMAGE_TYPES = ['.jpg']


class ObjectDetectionImageClassifierEvents:
    def image_processing_started_for(self, file_name):
        print(f'Processing {file_name}...')

    def processing_complete(self, total_processed):
        print('Number of Processed Images:', total_processed)


class FileSystem:

    def list_files_in(self, source):
        return os.listdir(source)

    def write_file(self, filename, content):
        with open(filename, 'w') as f:
            f.write(content)

    def join(self, path, *paths):
        return os.path.join(path, *paths)





class ImageAnalyzer:
    instance = None

    @staticmethod
    def get_instance():
        if ImageAnalyzer.instance is None:
            ImageAnalyzer.instance = ImageAnalyzer()
        return ImageAnalyzer.instance

    def __init__(self):
        self.top_left_coords = []
        self.top_right_coords = []

    def display_image_tool(self, dir_file):
        image = cv2.imread(dir_file)
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

        _, ax = plt.subplots(1, figsize=(10, 10))
        ax.imshow(image)

        self.selector = RectangleSelector(
            ax, self.line_select_callback,
            useblit=True,
            button=[1], minspanx=5, minspany=5,
            spancoords='pixels', interactive=True
        )

        plt.connect('key_press_event', self.onkeypress)
        plt.show()

    def line_select_callback(self, clk, rls):
        self.top_left_coords.append((int(clk.xdata), (int(clk.ydata))))
        self.top_right_coords.append((int(rls.xdata), (int(rls.ydata))))

    def analyze_complete(self):
        self.generate_json(self.top_left_coords, self.top_right_coords)
        self.top_left_coords.clear()
        self.top_right_coords.clear()

    def generate_json(top_left_coords, bottom_right_coords):
        image_dict = {"image": file_name, "annotations": []}
        if len(top_left_coords) != 0:
            label_dict = {"label": '', "coordinates": {}}
            coord_dict = {"x": int, "y": int, "width": int, "height": int}

            center_x = int(abs((top_left_coords[0][0] - bottom_right_coords[0][0]) / 2)) + int(top_left_coords[0][0])
            center_y = int(abs((top_left_coords[0][1] - bottom_right_coords[0][1]) / 2)) + int(top_left_coords[0][1])

            width = int(abs(top_left_coords[0][0] - bottom_right_coords[0][0]))
            height = int(abs(top_left_coords[0][1] - bottom_right_coords[0][1]))

            coord_dict['x'] = center_x
            coord_dict['y'] = center_y
            coord_dict['width'] = width
            coord_dict['height'] = height

            label_dict['label'] = name_class
            label_dict['coordinates'] = coord_dict

            image_dict['annotations'].append(label_dict)

        annotations.append(image_dict)
    @staticmethod
    def onkeypress(event):
        if event.key == 'q':
            ImageAnalyzer.get_instance().analyze_complete()


class ObjectDetectionImageClassifier:
    def __init__(self, file_system=FileSystem(), image_analyzer=ImageAnalyzer().get_instance(),
                 events=ObjectDetectionImageClassifierEvents()):
        self.fs = file_system
        self.image_analyzer = image_analyzer
        self.events = events

    def process_images(self, source, destination, result):
        global file_name, name_class, annotations, tl_list, br_list, toggle_selector
        self.annotations_file = self.fs.join(destination, result)

        annotations = []
        for file_name in self.fs.list_files_in(source):
            if self.is_image(file_name):
                self.events.image_processing_started_for(file_name)
                self.process_image(file_name, source)
        total_processed = len(annotations)
        self.events.processing_complete(total_processed)
        self.fs.write_file(self.annotations_file, json.dumps(annotations))

    def process_image(self, file_name, source):
        global name_class
        name_class, sep, tail = file_name.partition('_')
        dir_file = self.fs.join(source, file_name)
        self.image_analyzer.display_image_tool(dir_file)

    def is_image(self, file_name):
        _, extension = os.path.splitext(file_name)
        return extension in SUPPORTED_IMAGE_TYPES


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--source', help='Directory containing files to analyze', required=True)
    parser.add_argument('--destination', help='Directory where to drop the annotations file', required=True)
    parser.add_argument('--result', help='Filename of the resulting JSON file containing the annotations',
                        default='annotations.json')
    args = parser.parse_args()

    ObjectDetectionImageClassifier().process_images(args.source, args.destination, args.result)
