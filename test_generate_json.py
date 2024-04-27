from unittest import TestCase

from generate_json import ObjectDetectionImageClassifier, ImageAnalyzer, FileSystem, \
    ObjectDetectionImageClassifierEvents


class Test(TestCase):
    def setUp(self):
        self.event_handler = ClassificationEventsSpy()
        self.classifier = ObjectDetectionImageClassifier(FakeFileSystem(['puppy_1.jpg', 'puppy_2.jpg', 'wolf_3.jpg']), FakeImageAnalyzer(), self.event_handler)

    def test_process_images(self):
        self.classifier.process_images('sourcedir', 'destinationdir', 'annotation.json')
        self.assertEqual('destinationdir/annotation.json', self.classifier.annotations_file)

    def test_analyzes_each_image_in_file_system(self):
        self.classifier.process_images('sourcedir',
                                  'destinationdir',
                                  'annotation.json')

        self.assertEqual(3, self.event_handler.total_files_processed)
        self.assertTrue(self.event_handler.image_processed('puppy_1.jpg'))
        self.assertTrue(self.event_handler.image_processed('puppy_2.jpg'))
        self.assertTrue(self.event_handler.image_processed('wolf_3.jpg'))

    def test_only_processes_images(self):
        self.event_handler = ClassificationEventsSpy()
        self.fs = FakeFileSystem('notanimage_1.json')
        classifier = ObjectDetectionImageClassifier(self.fs, FakeImageAnalyzer(), self.event_handler)
        classifier.process_images('sourcedir',
                                  'destinationdir',
                                  'annotation.json')
        self.assertFalse(self.event_handler.image_processed('not_an_image.json'))


class FakeImageAnalyzer(ImageAnalyzer):
    def display_image_tool(self, dir_file):
        return


class FakeFileSystem(FileSystem):
    def __init__(self, files):
        self.files = files

    def list_files_in(self, path):
        return self.files

    def write_file(self, filename, content):
        pass


class ClassificationEventsSpy(ObjectDetectionImageClassifierEvents):
    def __init__(self):
        self.total_files_processed = None
        self.processing_started_events = []

    def image_processed(self, image):
        return image in self.processing_started_events

    def image_processing_started_for(self, file):
        self.processing_started_events.append(file)

    def processing_complete(self, total_processed):
        self.total_files_processed = total_processed
