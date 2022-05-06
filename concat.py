import cv2

def concat(images, filename=''):
    max_height = 0
    max_width = 0
    new_images = []
    for image in images:
        if image.shape[0] > max_height:
            max_height = image.shape[0]
        if image.shape[1] > max_width:
            max_width = image.shape[1]
    for image in images:
        new_images.append(cv2.resize(image, (max_width, max_height),
                                  interpolation=cv2.INTER_AREA))
    final = cv2.hconcat(new_images)
    cv2.imwrite(filename, final)
