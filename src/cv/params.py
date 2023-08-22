import cv2
import numpy as np


def get_area(cnt):
    area = cv2.contourArea(cnt)
    return area

def get_radius(cnt):
    return np.sqrt(get_area(cnt)/np.pi)

def eq_dia(cnt):
   equi_diameter = np.sqrt(4*get_area(cnt)/np.pi)
   return equi_diameter

def get_arc_lenght(cnt):
    return cv2.arcLength(cnt, True)

def get_center(contour):
    M = cv2.moments(contour)
    cx, cy = None, None
    if M['m00'] != 0:
        cx = int(M['m10']/M['m00'])
        cy = int(M['m01']/M['m00'])
    return cx, cy