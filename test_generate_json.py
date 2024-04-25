from unittest import TestCase

from generate_json import ObjectDetectionImageClassifier, ImageAnalyzer, FileSystem


class Test(TestCase):
    def test_process_images(self):
        classifier = ObjectDetectionImageClassifier(FakeFileSystem(), FakeImageAnalyzer())
        generator = classifier.process_images('sourcedir', 'destinationdir', 'annotation.json')
        self.assertEqual('destinationdir/annotation.json', classifier.annotations_file)


class FakeImageAnalyzer(ImageAnalyzer):
    def display_image_tool(self, dir_file, toggle_selector):
        return

class FakeFileSystem(FileSystem):
    def list_files_in(self, path):
        return ['puppy_1.jpg', 'puppy_2.jpg', 'wolf_3.jpg']

    def write_file(self, filename, content):
        pass