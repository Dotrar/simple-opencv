#!/usr/bin/env python
import sys

import cv2

import helpers


def main(command):
    # on my PC, the camera is id=2. look at `find_camera` in helpers.py
    cam = cv2.VideoCapture(2)

    while True:
        _, img = cam.read()

        if command == 1:
            print("ok")

        if not helpers.show_image_async(img):
            break

    cv2.destroyAllWindows()


if __name__ == "__main__":
    segment = sys.argv[1]

    main(segment)
