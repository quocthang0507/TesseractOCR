import pytesseract
import cv2
import glob
import os

# specify path to the license plate images folder as shown below
path_for_license_plates = os.getcwd() + "/license-plates/**/*.jpg"
list_license_plates = []
predicted_license_plates = []

for path_to_license_plate in glob.glob(path_for_license_plates, recursive=True):
    license_plate_file = path_to_license_plate.split("\\")[-1]
    license_plate, _ = os.path.splitext(license_plate_file)
    '''
	Here we append the actual license plate to a list
	'''
    list_license_plates.append(license_plate)

    '''
	Read each license plate image file using openCV
	'''
    img = cv2.imread(path_to_license_plate)

    '''
	We then pass each license plate image file
	to the Tesseract OCR engine using the Python library
	wrapper for it. We get back predicted_result for
	license plate. We append the predicted_result in a
	list and compare it with the original the license plate
	'''
    pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
    predicted_result = pytesseract.image_to_string(img, lang='eng',
                                                   config='--oem 3 --psm 6 -c tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789')

    filter_predicted_result = "".join(
        predicted_result.split()).replace(":", "").replace("-", "")
    predicted_license_plates.append(filter_predicted_result)

print("Actual License Plate", "\t", "Predicted License Plate", "\t", "Accuracy")
print("--------------------", "\t", "-----------------------", "\t", "--------")


def calculate_predicted_accuracy(actual_list, predicted_list):
    for actual_plate, predict_plate in zip(actual_list, predicted_list):
        accuracy = "0 %"
        num_matches = 0
        if actual_plate == predict_plate:
            accuracy = "100 %"
        else:
            if len(actual_plate) == len(predict_plate):
                for a, p in zip(actual_plate, predict_plate):
                    if a == p:
                        num_matches += 1
                accuracy = str(
                    round((num_matches / len(actual_plate)), 2) * 100)
                accuracy += "%"
        print("	 ", actual_plate, "\t\t\t", predict_plate, "\t\t ", accuracy)


calculate_predicted_accuracy(list_license_plates, predicted_license_plates)
