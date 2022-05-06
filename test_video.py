import cv2
import time
import threading
from plate_detection import PlateDetector
from utils.average_plate import *
from utils.find_best_quality_images import get_best_images

########### INIT ###########
# Initialize the plate detector
plateDetector = PlateDetector(type_of_plate='RECT_PLATE',
                              minPlateArea=4100,
                              maxPlateArea=15000)
list_char_on_plate = []  # contains an array of the segmented characters in each frame
countPlates = 0  # count the number of same plates
recog_plate = ''
coordinates = (0, 0)
num_frame_without_plates = 0
countPlates_threshold = 11  # the maximum number of images of the same plate to get
###########################


def recognized_plate(list_char_on_plate, size):
    """
    input is a list that contains a images of the same plate
    get the best images in the list
    calculates the average plate
    """
    global recog_plate

    t0 = time.time()
    plates_value = []
    plates_length = []

    list_char_on_plate = get_best_images(
        list_char_on_plate, num_img_return=1)  # get the best images

    for segmented_characters in list_char_on_plate:
        chars = segmented_characters[1]
        # ...


cap = cv2.VideoCapture('video/test.MOV')  # video path

if __name__ == "__main__":
    while(cap.isOpened()):
        ret, frame = cap.read()
        if (frame is None):
            print("[INFO] End of Video")
            break
