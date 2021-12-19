import numpy as np
import cv2
from hashlib import md5
import uuid
import base64
from PIL import Image as pill_img
import io


class Image:

    def __init__(self, url: str, origin: str):

        self.__difference_score = None
        self.__hash = None
        self.url = url
        self.origin = origin

    def save_to_file(self, folder_path):
        img = self.read_image(self.url, self.origin)
        img_name = f'{uuid.uuid1()}.jpg'
        cv2.imwrite(f'./{folder_path}/{img_name}', img)
        return img_name

    def __generate_difference_score(self, url, origin):
        img = self.read_image(url, origin)
        img_gray = self.__gray_img(img)
        row_res, col_res = self.__resize(img_gray)
        return self.__intensify_diff(row_res, col_res)

    def __generate_hash(self):
        return self.file_hash(self.__difference_score)

    def read_image(self, url: str, origin: str):

        if origin == 'base64':
            return self.__convert_base64_to_img(url)
        
        if origin == 'local_file':
            return cv2.imread(url)

    def __gray_img(self, img):
        return cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    def __resize(self, img, height=40, width=40):
        row_res = cv2.resize(img, (height, width), interpolation=cv2.INTER_AREA).flatten()
        col_res = cv2.resize(img, (height, width), interpolation=cv2.INTER_AREA).flatten('F')
        return row_res, col_res

    def __intensify_diff(self, row_res, col_res):

        difference_row = np.diff(row_res)
        difference_col = np.diff(col_res)

        # difference_row = difference_row > 0
        # difference_col = difference_col > 0

        return np.vstack((difference_row, difference_col)).flatten()

    def file_hash(self, array: list):
        return md5(array).hexdigest()

    def get_hash(self):
        return self.__hash

    def get_difference_score(self):

        if self.__difference_score is None:
            self.__difference_score = self.__generate_difference_score(self.url, self.origin)

        if self.__hash is None:
            self.__hash = self.__generate_hash()

        return self.__difference_score

    def __convert_base64_to_img(self, base64_str):
        base64_str = str(base64_str)
        image_data = base64.b64decode(base64_str[base64_str.find(','):len(base64_str)])
        image = pill_img.open(io.BytesIO(image_data))
        return cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
