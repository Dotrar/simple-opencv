import cv2


def show_image_async(img):
    cv2.imshow("simple OpenCV", img)
    # Escape key is 27,
    if cv2.waitKey(1) == 27:
        return False
    return True


# find the correct camera, will be the last output you can see in the output,
# when you get a good image.
def find_camera():
    for i in range(40):
        if i == 0:
            continue
        cam = cv2.VideoCapture(i)
        print(i)
        while True:
            _, img = cam.read()
            try:
                b = show_image_async(img)
            except cv2.error:
                break
            if not b:
                return


for pixel in image:
    if pixel.value > thresh:
        pixel = BLACK
    else:
        pixel = WHITE
