import cv2
import time
import threading
import pytesseract
import os
from plate_detection import PlateDetector
from utils.average_plate import *
from utils.find_best_quality_images import get_best_images
from concat import concat

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

cap = cv2.VideoCapture('video/test.MOV')  # video path

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
###########################


def recognized_plate(list_char_on_plate, filename=''):
    """
    input is a list that contains a images of the same plate
    get the best images in the list calculates the average plate
    """
    global recog_plate

    time_start = time.time()

    list_char_on_plate = get_best_images(
        list_char_on_plate, num_img_return=1)  # get the best images

    for segmented_characters in list_char_on_plate:
        chars = segmented_characters[1]
        final = concat(chars[0], filename)
        final_plate = ocr(final)
        # ......

    time_end = time.time()
    print("Recognized plate: " + final_plate)
    print("Threading time: " + str(time_end - time_start))


def ocr(image):
    predicted_result = pytesseract.image_to_string(image, lang='eng',
                                                   config='--oem 3 --psm 6 -c tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789')

    filter_predicted_result = "".join(
        predicted_result.split()).replace(":", "").replace("-", "")
    return filter_predicted_result


if __name__ == "__main__":
    while(cap.isOpened()):
        ret, frame = cap.read()
        if (frame is None):
            print("[INFO] End of Video")
            break

        # resize the frame to fit the screen
        _frame = cv2.resize(frame, (960, 540))
        frame_height, frame_width = frame.shape[:2]
        _frame_height, _frame_width = _frame.shape[:2]
        cropped_frame = frame[int(
            frame_height*0.3):frame_height, 0:int(frame_width*0.8)]  # crop the ROI
        cv2.rectangle(_frame, (0, int(_frame_height*0.3)), (int(_frame_width*0.8),
                      _frame_height), (255, 0, 0), 2)  # draw a rectangle to locate the ROI

        # print the result
        cv2.rectangle(_frame, (0, 0), (190, 40), (0, 0, 0), -1)
        cv2.putText(_frame, recog_plate, (20, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)
        cv2.imshow('video', _frame)

        possible_plates = plateDetector.find_possible_plates(cropped_frame)
        if possible_plates is not None:
            num_frame_without_plates = 0
            # calculates the distance between two plates
            distance = tracking(
                coordinates, plateDetector.corresponding_area[0])
            # get the coordinate of the detected plate
            coordinates = plateDetector.corresponding_area[0]
            if (distance < 100):
                if(countPlates < countPlates_threshold):
                    cv2.imshow('Plate', possible_plates[0])
                    temp = []
                    temp.append(possible_plates[0])
                    temp.append(plateDetector.char_on_plate[0])
                    # temp = [image of plate, segmented characters on plate]

                    list_char_on_plate.append(temp)
                    countPlates += 1
                elif(countPlates == countPlates_threshold):
                    # create a new thread for image recognition
                    threading.Thread(target=recognized_plate, args=(
                        list_char_on_plate, 128)).start()
                    countPlates += 1
            else:
                countPlates = 0
                list_char_on_plate = []

        # the program will try to catch 11 images of the same plate and then pick the top 7 best
        # quality images out of 11. However, if the program cannot catch enough images, after
        # num_frame_without_plates frames without plates, it will process the and calculate the
        # final plate
        if (possible_plates == None):
            num_frame_without_plates += 1
            if (countPlates <= countPlates_threshold and countPlates > 0 and num_frame_without_plates > 5):
                threading.Thread(target=recognized_plate, args=(
                    list_char_on_plate, 128)).start()
                countPlates = 0

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
