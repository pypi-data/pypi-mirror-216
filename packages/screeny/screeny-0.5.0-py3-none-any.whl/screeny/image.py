from screeny import *
from typing import Union

import copy
import numpy as np, cv2, pytesseract


class Image:

    data: np.ndarray = np.array([])
    color_code: str = ""
    orb_detector: cv2.ORB = None
    keypoints: tuple = ()
    descriptors: np.ndarray = np.array([])

    def __init__(self, image: Union[str, np.ndarray, "Image"]):
        self.orb_detector = cv2.ORB_create()

        if type(image) is str:
            self.data = cv2.imread(image)
            self.color_code = "BGR"
        elif type(image) is np.ndarray:
            self.data = image
            self.color_code = "BGR"
        elif type(image) is Image:
            self.data = image.get_data()
            self.color_code = image.color_code
            self.keypoints = image.keypoints
            self.descriptors = image.descriptors
        else:
            raise Exception("Unknown image-type!")

    def get_data(self):
        return self.data

    def binarize(self, method: str = "otsus_thresholding", threshold: int = 127) -> "Image":
        if self.color_code != "GRAY":
            raise Exception("Colorcode should be 'GRAY' for binarizing image!")


        if method == "simple_thresholding":
            ret, self.data = cv2.threshold(self.data, threshold, 255, cv2.THRESH_BINARY_INV) # Todo: Check, why the binarization is done inverted here??
        elif method == "adaptive_thresholding":
            self.data = cv2.adaptiveThreshold(self.data, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 11, 2) # Todo: Check, why the binarization is done inverted here??
        elif method == "otsus_thresholding":
            # The threshold-value will be automatically detected
            ret, self.data = cv2.threshold(self.data, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU) # Todo: Check, why the binarization is done inverted here??
        else:
            raise Exception(f"Binarization-metho '{method}' is unknown!")

        return self

    def compute_descriptors(self) -> "Image":
        """
        Computes the descriptors of the image.

        :return: Image
        """
        # compute the descriptors with ORB
        self.keypoints, self.descriptors = self.orb_detector.compute(self.data, self.keypoints)
        return self

    def denoise(self) -> "Image":
        self.data = cv2.fastNlMeansDenoising(self.data, None, 10, 21, 7)
        return self

    def detect_features(self) -> "Image":
        """
        Finds feature in the image.

        :return: Image
        """
        self.keypoints, self.descriptors = self.orb_detector.detectAndCompute(self.data, None)
        return self

    def detect_keypoints(self) -> "Image":
        """
        Finds the keypoints of the image.

        :return: Image
        """
        # find the keypoints with ORB
        self.keypoints = self.orb_detector.detect(self.data, None)
        return self

    def invert(self) -> "Image":
        self.data = cv2.bitwise_not(self.data)
        return self

    def locate_image(self, image_to_find: Union[str, np.ndarray, "Image"], confidence: float = 0.8) -> Point | bool:
        template = Image(image_to_find).to_grayscale()
        image = copy.copy(self)
        image.to_grayscale()

        heat_map = cv2.matchTemplate(image.get_data(), template.get_data(), cv2.TM_CCOEFF_NORMED)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(heat_map)
        if max_val >= confidence:
            w, h = template.get_data().shape
            return Point(max_loc[0] + (w / 2), max_loc[1] + (h / 2))
        else:
            return False

    def match_features(self, image_to_find: Union[str, np.ndarray, "Image"], cross_check = True) -> list:
        """
        Matches the features of the image with another image.

        :param cross_check: bool
        :param image_to_find: str | np.ndarray | Image
        :return: list
        """
        template = Image(image_to_find)  #.to_grayscale()

        if len(template.descriptors) <= 0:
            template.detect_features()

        if len(self.descriptors) <= 0:
            self.detect_features()

        bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=cross_check)
        matches = bf.match(self.descriptors, template.descriptors)  # Match descriptors.
        matches = sorted(matches, key=lambda x: x.distance)  # Sort them in the order of their distance.
        return matches

    def read_text(
            self, resize_factor: int = None,
            whitelist: str = "._0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"
    ):
        image = copy.copy(self)
        image.to_grayscale()

        if resize_factor:
            image.resize(resize_factor)

        image.binarize("otsus_thresholding")
        image.denoise()

        # psm:
        # 3     - Fully automatic page segmentation, but no OSD. (Default)
        # 13    - (Raw line. Treat the image as a single text line, bypassing hacks that are Tesseract-specific.)
        text = pytesseract.image_to_string(
            image.get_data(),
            config="-c tessedit_char_whitelist=" + whitelist + " --psm 3 load_system_dawg=0 load_freq_dawg=0"
        ).strip("\n\r")
        return text

    def resize(self, factor: int) -> "Image":
        self.data = cv2.resize(self.data, None, fx=factor, fy=factor, interpolation=cv2.INTER_CUBIC)
        return self

    def save(self, title: str, path: str = "") -> bool:
        """
        Saves the image on the disk in a given path with a given title.
        If no path is specified, the file will be saved in the current active directory.

        :param title: str
        :param path: str
        :return: bool
        """
        return cv2.imwrite(path + title, self.get_data())

    def show(self, title: str = "", with_keypoints: bool = False):
        if with_keypoints:
            img2 = cv2.drawKeypoints(self.data, self.keypoints, None, color=(0, 255, 0), flags=0)
            cv2.imshow(title, img2)
            cv2.waitKey(0)

            """plt.imshow(img2)
            plt.show()"""
        else:
            cv2.imshow(title, self.data)
            cv2.waitKey(0)

    def show_matches(self, image_to_find: Union[str, np.ndarray, "Image"], matches: list) -> None:
        """
        Show the two images with matches as lines connect points.

        :param image_to_find: str | np.ndarray | Image
        :param matches: list
        :return:
        """
        template = Image(image_to_find)

        Image(cv2.drawMatches(
            self.data, self.keypoints, template.get_data(),
            template.keypoints, matches, None, flags=cv2.DrawMatchesFlags_NOT_DRAW_SINGLE_POINTS
        )).show("Matched images")

    def to_grayscale(self) -> 'Image':
        if self.color_code == "RGB":
            self.data = cv2.cvtColor(self.data, cv2.COLOR_RGB2GRAY)
        elif self.color_code == "BGR":
            self.data = cv2.cvtColor(self.data, cv2.COLOR_BGR2GRAY)
        elif self.color_code == "HSV":
            self.data = cv2.cvtColor(self.data, cv2.COLOR_HSV2GRAY)
        elif self.color_code == "GRAY":
            pass
        else:
            raise Exception(f"Colorcode {self.color_code} is unknown!")

        self.color_code = "GRAY"
        return self

    def to_hsv(self) -> "Image":
        if self.color_code == "RGB":
            self.data = cv2.cvtColor(self.data, cv2.COLOR_RGB2HSV)
        elif self.color_code == "BGR":
            self.data = cv2.cvtColor(self.data, cv2.COLOR_BGR2HSV)
        elif self.color_code == "HSV":
            pass
        elif self.color_code == "GRAY":
            self.data = cv2.cvtColor(self.data, cv2.COLOR_GRAY2HSV)
        else:
            raise Exception(f"Colorcode {self.color_code} is unknown!")

        self.color_code = "HSV"
        return self
