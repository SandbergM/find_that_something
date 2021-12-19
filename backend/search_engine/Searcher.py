
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
        img = Image(img_path, 'base64')
        img_score = img.get_difference_score()
        img_name = img.save_to_file(self.__images_folder)
        self.__pickle_handler.append_to_file(img_name, img_score)

    def search(self, img_path):
        query_score = Image(img_path, 'base64').get_difference_score()
        result = []
        images = self.__pickle_handler.load_from_file()
        print("dwadwadwa : ", len(images))
        for key, val in images.items():

            def hamming_distance(img_a, img_b):
                score = hamming(img_a, img_b) * len(img_a)
                return score

            distance = hamming_distance(query_score, val)
            result.append((f'{key}', distance))

            if key == '2bfdf870-79b7-4f1b-8a1b-ba48b1633087.jpg':
                print(distance)


        result = sorted(result, key=lambda tup: tup[1])
        return result[:self.max_results]

    def send_image(self, img_id):

        path = f'/search_engine/images/{img_id}'

        if os.path.exists('./' + path):
            return 200, path
        else:
            return 404, f'/search_engine/404.jpg'

    def reset_dataset(self):
        ds = {}
        for img_name in os.listdir('./search_engine/images'):
            img = Image(f'./search_engine/images/{img_name}', 'local_file')
            score = img.get_difference_score()
            ds[img_name] = score
        self.__pickle_handler.save_to_file(ds)