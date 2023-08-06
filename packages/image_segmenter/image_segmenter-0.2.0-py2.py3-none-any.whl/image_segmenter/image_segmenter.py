"""
author: Rich Baird
email: rich.baird@utah.edu
homepage: rbaird.me
repository: https://github.com/richbai90/image_annotator
date: 2023-06-08
description: A class for annotating images with bounding boxes using various image processing techniques.
"""

import cv2
import numpy as np
import matplotlib.pyplot as plt
from os import path, listdir
from .voc_writer import VOCWriter

class ImageSegmenter:
    """
    A class for annotating images with bounding boxes using various image processing techniques.
    """

    def __init__(self):
        plt.rcParams['image.cmap'] = 'gray'

    def read_image(self, filename):
        """
        Read an image from a path. If the path is a directory, select a random image from the directory.

        Parameters:
            filename (str): The path to the image or directory.

        Returns:
            img (np.array): The image in BGR format.
        """
        # if the path does not include a file name, select a random image from the path
        if path.isdir(filename):
            filename = path.join(filename, np.random.choice([f for f in listdir(filename) if f.endswith('.jpg')]))
        img = cv2.imread(filename)
        return img

    def select_colorsp(self, img, colorsp='gray'):
        """
        Select a color space from an image.
        Given an image, split it into its channels and return the selected color space.

        Parameters:
            img (np.array): The image in BGR format.
            colorsp (str): The color space to return. Options are 'gray', 'red', 'green', 'blue', 'hue', 'sat', 'val'.

        Returns:
            channels[colorsp] (np.array): The selected color space.
        """
        # Convert to grayscale.
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        # Split BGR.
        red, green, blue = cv2.split(img)
        # Convert to HSV.
        im_hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        # Split HSV.
        hue, sat, val = cv2.split(im_hsv)
        # Store channels in a dict.
        channels = {'gray': gray, 'red': red, 'green': green, 'blue': blue, 'hue': hue, 'sat': sat, 'val': val}

        return channels[colorsp]

    def display(self, im_left, im_right, name_l='Left', name_r='Right', figsize=(10, 7)):
        """
        Display two images side by side.

        Display two images side by side with optional titles, and optional figure size.

        Parameters:
            im_left (np.array): The left image.
            im_right (np.array): The right image.
            name_l (str): The title for the left image, default is 'Left'.
            name_r (str): The title for the right image, default is 'Right'.
            figsize (tuple): The figure size, default is (10, 7).

        Returns:
            void
        """
        # Flip channels for display if RGB as matplotlib requires RGB.
        im_l_dis = im_left[..., ::-1] if len(im_left.shape) > 2 else im_left
        im_r_dis = im_right[..., ::-1] if len(im_right.shape) > 2 else im_right

        plt.figure(figsize=figsize)
        plt.subplot(121)
        plt.imshow(im_l_dis)
        plt.title(name_l)
        plt.axis(False)
        plt.subplot(122)
        plt.imshow(im_r_dis)
        plt.title(name_r)
        plt.axis(False)
        plt.show(block=True)

    def threshold(self, img, thresh=127, mode='inverse'):
        """
        Threshold an image.

        Threshold an image using a given threshold value and mode.

        Parameters:
            img (np.array): The image to threshold.
            thresh (int): The threshold value, default is 127.
            mode (str): The threshold mode, options are 'direct' and 'inverse', default is 'inverse'.

        Returns:
            The thresholded image.
        """
        im = img.copy()

        if mode == 'direct':
            thresh_mode = cv2.THRESH_BINARY
        else:
            thresh_mode = cv2.THRESH_BINARY_INV

        _, thresh = cv2.threshold(im, thresh, 150, thresh_mode)

        return thresh

    def get_bboxes(self, img):
        """
        Get the bounding boxes of objects in an image.

        Perform contour analysis on a binary image to extract the bounding boxes of objects.

        Parameters:
            img (np.array): The binary image.

        Returns:
            bboxes (list): The list of bounding boxes in the format (x_min, y_min, x_max, y_max).
        """
        contours, hierarchy = cv2.findContours(img, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
        # Sort according to the area of contours in descending order.
        sorted_cnt = sorted(contours, key=cv2.contourArea, reverse=True)
        # Remove max area, outermost contour.
        sorted_cnt.remove(sorted_cnt[0])
        bboxes = []
        for cnt in sorted_cnt:
            x, y, w, h = cv2.boundingRect(cnt)
            cnt_area = w * h
            bboxes.append((x, y, x + w, y + h))
        return bboxes

    def morph_op(self, img, mode='open', ksize=5, iterations=1):
        """
        Perform morphological operations on a binary image.

        Parameters:
            img (np.array): The binary image.
            mode (str): The morphological operation mode. Options are 'open', 'close', 'erode', 'dilate'.
            ksize (int): The size of the structuring element, default is 5.
            iterations (int): The number of times to apply the morphological operation, default is 1.

        Returns:
            morphed (np.array): The morphologically processed image.
        """
        im = img.copy()
        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (ksize, ksize))

        if mode == 'open':
            morphed = cv2.morphologyEx(im, cv2.MORPH_OPEN, kernel)
        elif mode == 'close':
            morphed = cv2.morphologyEx(im, cv2.MORPH_CLOSE, kernel)
        elif mode == 'erode':
            morphed = cv2.erode(im, kernel)
        else:
            morphed = cv2.dilate(im, kernel)

        return morphed

    def draw_annotations(self, img, bboxes, thickness=2, color=(0, 255, 0)):
        """
        Draw bounding box annotations on an image.
        
        Draw bounding box annotations on an image for display purposes. Not required for the pipeline.

        Parameters:
            img (np.array): The image to annotate.
            bboxes (list): The list of bounding boxes in the format (x_min, y_min, x_max, y_max).
            thickness (int): The thickness of the bounding box lines, default is 2.
            color (tuple): The color of the bounding box lines in BGR format, default is (0, 255, 0).

        Returns:
            annotations (np.array): The annotated image.
        """
        annotations = img.copy()
        for box in bboxes:
            tlc = (box[0], box[1])
            brc = (box[2], box[3])
            cv2.rectangle(annotations, tlc, brc, color, thickness, cv2.LINE_AA)

        return annotations

    def filter_bboxes_by_area(self, img, bboxes, min_area_ratio=0.001):
        """
        Filter bounding boxes by area.

        Remove bounding boxes that have an area smaller than a certain ratio of the image area.

        Parameters:
            img (np.array): The image.
            bboxes (list): The list of bounding boxes in the format (x_min, y_min, x_max, y_max).
            min_area_ratio (float): The minimum area ratio to filter the bounding boxes, default is 0.001.

        Returns:
            filtered (list): The filtered list of bounding boxes.
        """
        filtered = []
        # Image area.
        im_area = img.shape[0] * img.shape[1]
        for box in bboxes:
            x, y, w, h = box
            cnt_area = w * h
            # Remove very small detections.
            if cnt_area > min_area_ratio * im_area:
                filtered.append(box)
        return filtered

    def filter_bboxes_by_xy(self, bboxes, min_x=None, max_x=None, min_y=None, max_y=None):
        """
        Filter bounding boxes by their x and y coordinates.

        Remove bounding boxes that do not meet the specified x and y coordinate criteria.

        Parameters:
            bboxes (list): The list of bounding boxes in the format (x_min, y_min, x_max, y_max).
            min_x (int): The minimum x coordinate value, default is None.
            max_x (int): The maximum x coordinate value, default is None.
            min_y (int): The minimum y coordinate value, default is None.
            max_y (int): The maximum y coordinate value, default is None.

        Returns:
            filtered_bboxes (list): The filtered list of bounding boxes.
        """
        filtered_bboxes = []
        for box in bboxes:
            x, y, w, h = box
            x1, x2 = x, x + w
            y1, y2 = y, y + h
            if min_x is not None and x1 < min_x:
                continue
            if max_x is not None and x2 > max_x:
                continue
            if min_y is not None and y1 < min_y:
                continue
            if max_y is not None and y2 > max_y:
                continue
            filtered_bboxes.append(box)
        return filtered_bboxes

    def save_annotations(self, img: np.ndarray, filename: str, bboxes: tuple, class_name: str = '0'):
        """
        Save the annotations as a VOC XML file.

        Parameters:
            img (np.ndarray): The input image.
            filename (str): The path to save the annotations XML file.
            bboxes (tuple): The list of bounding boxes in the format (x_min, y_min, x_max, y_max).
            class_name (str): The class name for the annotations, default is '0'.

        Returns:
            None
        """
        writer = VOCWriter(filename, img, False)
        with writer as w:
            for box in bboxes:
                w.annotate(class_name, box)