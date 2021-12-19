import pickle
import os


class Pickle_Handler():

    def __init__(self):
        self.file_path = f'{os.path.dirname(__file__)}/data/data.pickle'

    def save_to_file(self, data):
        with open(f'{self.file_path}', 'bw') as pkl:
            pickle.dump(data, pkl)

    def load_from_file(self):
        with open(f'{self.file_path}', 'br') as pkl:
            return pickle.load(pkl)

    def append_to_file(self, img_name, img_score):

        pkl_data = self.load_from_file()
        pkl_data[img_name] = img_score

        with open(f'{self.file_path}', 'bw') as pkl:
            pickle.dump(pkl_data, pkl)
