import cv2


def _get_inv_threshold(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (15, 15), 0)
    threshold = cv2.adaptiveThreshold(blurred, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY_INV, 181, 15)
    return threshold


def _get_external_contours_by_threshold(threshold):
    contours, h = cv2.findContours(threshold, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    return contours, h


def _filter_contours(contours, h):
    is_not_small = lambda contour: contour.size > 200
    is_opened = lambda h, i: h[0][i][2] < 0 and h[0][i][3] < 0
    filtered_contours = tuple(contour for i, contour in enumerate(contours)
                              if is_not_small(contour) and is_opened(h, i))
    return filtered_contours


def _highlight_contours(img, contours):
    cv2.drawContours(img, contours, -1, (0, 255, 0), 2)


def find_molecules(img):
    threshold = _get_inv_threshold(img)
    contours = _filter_contours(*_get_external_contours_by_threshold(threshold))
    _highlight_contours(img, contours)


cap = cv2.VideoCapture('2.avi')

while True:
    success, img = cap.read()
    find_molecules(img)
    cv2.imshow('img image', img)
    cv2.waitKey(150)





