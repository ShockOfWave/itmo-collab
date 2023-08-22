import cv2

from src.cv.params import *


def _get_inv_threshold(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (15, 15), 0)
    threshold = cv2.adaptiveThreshold(blurred, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY_INV, 181, 17)
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
    for contour in contours:
        cv2.drawContours(img, contour, -1, (0, 255, 0), 2)


def find_molecules(img):
    threshold = _get_inv_threshold(img)
    contours = _filter_contours(*_get_external_contours_by_threshold(threshold))
    for contour in contours:
        cx, cy = get_center(contour)
        if cx is not None and cy is not None:
            cv2.circle(img, (cx, cy), 4, (0, 255, 255), -1)
        area = get_area(contour)
        arc_lenght = get_arc_lenght(contour)
        diam = eq_dia(contour)
        rad = get_radius(contour)
        text =  f"Area: {int(area)}\nArc lenght: {int(arc_lenght)}\nDiameter: {int(diam)}\nRadius: {int(rad)}"
        for i, txt in enumerate(text.split('\n')):
            dy = 15*i
            cv2.putText(img, txt, (int(cx-rad), int(cy-diam+dy)), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,255,255), 2)
        cv2.rectangle(img, (cx-int(rad)-5, cy-int(diam)-15), (cx-int(rad)-5+150, cy-int(diam)-15+65), (0, 255, 255), 1)
        cv2.line(img, (cx, cy), (cx-int(rad)-5+150, cy-int(diam)-15+65), (0,255,255), 1)
    _highlight_contours(img, contours)




if __name__ == '__main__':
    while True:
        success, img = cap.read()
        find_molecules(img)
        cv2.imshow('img image', img)
        cv2.waitKey(150)
