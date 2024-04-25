from unittest import TestCase

from generate_json import ObjectDetectionImageClassifier, ImageAnalyzer, FileSystem, \
    ObjectDetectionImageClassifierEvents


class Test(TestCase):
    def test_process_images(self):
        classifier = ObjectDetectionImageClassifier(FakeFileSystem(['puppy_1.jpg']), FakeImageAnalyzer())
        generator = classifier.process_images('sourcedir', 'destinationdir', 'annotation.json')
        self.assertEqual('destinationdir/annotation.json', classifier.annotations_file)

    def test_analyzes_each_image_in_file_system(self):
        self.classificationEvents = ClassificationEventsSpy()
        classifier = ObjectDetectionImageClassifier(FakeFileSystem(['puppy_1.jpg', 'puppy_2.jpg', 'wolf_3.jpg']), FakeImageAnalyzer(), self.classificationEvents)
        classifier.process_images('sourcedir',
                                  'destinationdir',
                                  'annotation.json')
        self.assertEqual(3, len(self.classificationEvents.processing_started_events))
        self.assertTrue(self.classificationEvents.image_processed('puppy_1.jpg'))
        self.assertTrue(self.classificationEvents.image_processed('puppy_2.jpg'))
        self.assertTrue(self.classificationEvents.image_processed('wolf_3.jpg'))

    def test_only_processes_images(self):
        self.classificationEvents = ClassificationEventsSpy()
        self.fs = FakeFileSystem('notanimage_1.json')
        classifier = ObjectDetectionImageClassifier(self.fs, FakeImageAnalyzer(), self.classificationEvents)
        classifier.process_images('sourcedir',
                                  'destinationdir',
                                  'annotation.json')
        self.assertFalse(self.classificationEvents.image_processed('not_an_image.json'))


class FakeImageAnalyzer(ImageAnalyzer):
    def display_image_tool(self, dir_file, toggle_selector):
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
        self.processing_started_events = []

    def image_processed(self, image):
        return image in self.processing_started_events

    def image_processing_started_for(self, file):
        self.processing_started_events.append(file)
