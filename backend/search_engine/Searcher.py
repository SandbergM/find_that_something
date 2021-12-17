
# Custom
from .Pickle_Handler import Pickle_Handler
from .Image import Image

# General
from scipy.spatial.distance import hamming
import os


class Searcher:

    def __init__(self):

        self.__pickle_handler = Pickle_Handler()
        self.__images_folder = f'{os.path.dirname(__file__)}/images'
        self.max_results = 10

    def append_data(self, img_path):
        img = Image(img_path, True)
        img_score = img.get_difference_score()
        img.save_to_file(self.__images_folder)
        self.__pickle_handler.append_to_file({img_path: img_score})

    def search(self, img_path):
        query_score = Image(img_path, 'base64').get_difference_score()
        result = []
        images = self.__pickle_handler.load_from_file()

        for key, val in images.items():

            def hamming_distance(img_a, img_b):
                score = hamming(img_a, img_b)
                return score

            distance = hamming_distance(query_score, val)
            result.append((f'{img_path}', f'{self.__images_folder}/{key}', distance))

        return sorted(result, key=lambda tup: tup[2])[:self.max_results]
