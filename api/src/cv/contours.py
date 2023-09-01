import cv2

from api.src.cv.params import get_center, get_arc_lenght, eq_dia, get_radius
from api.src.models.segmentation_model import SegmentationModel

model = SegmentationModel(model_path='api/src/models/weigths')


def _highlight_contours(img, contours):
    for contour in contours:
        cv2.drawContours(img, contour, -1, (0, 255, 0), 2)


def find_molecules(img):
    contours = model.predict(img)
    if len(contours[0][0]) is not None:
        for contour, area in contours:
            cx, cy = get_center(contour)
            if cx is not None and cy is not None:
                cv2.circle(img, (cx, cy), 4, (0, 255, 255), -1)
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
