import cv2
import torch

from api.src.cv.params import get_center, get_arc_lenght, eq_dia, get_radius, get_area
from api.src.models.predict_model import get_octane_number_from_model
from api.src.models.segmentation_model import SegmentationModel
from api.src.models.classification_model import OctaneClassifier
from api.src.utils.paths import PATH_TO_SEGMENTATION_MODEL, PATH_TO_CLASSIFICATION_MODEL

device = "cuda:0" if torch.cuda.is_available() else "cpu"

segmentation_model = SegmentationModel(model_path=PATH_TO_SEGMENTATION_MODEL)
classification_model = OctaneClassifier().load_from_checkpoint(
    checkpoint_path=PATH_TO_CLASSIFICATION_MODEL, map_location=device
)


def _highlight_contours(img, contours):
    for contour in contours:
        if len(contour):
            cv2.drawContours(img, [contour], -1, (0, 255, 0), 2)


def find_molecules(img):
    contours = segmentation_model.predict(img)
    octane_number = get_octane_number_from_model(
        model=classification_model, device=device, image=img
    )
    for contour in contours:
        if len(contour):
            cx, cy = get_center(contour)
            if cx is not None and cy is not None:
                cv2.circle(img, (cx, cy), 4, (0, 255, 255), -1)
            arc_lenght = get_arc_lenght(contour)
            diam = eq_dia(contour)
            rad = get_radius(contour)
            area = get_area(contour)
            text = (
                f"Octane number:\n{octane_number}\nArea: "
                f"{int(area)}\nArc lenght: "
                f"{int(arc_lenght)}\nDiameter: "
                f"{int(diam)}\nRadius: {int(rad)}"
            )
            for i, txt in enumerate(text.split("\n")):
                dy = 15 * i
                if i in [0, 1]:
                    cv2.putText(
                        img,
                        txt,
                        (int(cx - rad), int(cy - diam + dy)),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.5,
                        (51, 115, 184),
                        2,
                    )
                else:
                    cv2.putText(
                        img,
                        txt,
                        (int(cx - rad), int(cy - diam + dy)),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.5,
                        (0, 255, 255),
                        2,
                    )

                cv2.rectangle(
                    img,
                    (cx - int(rad) - 5, cy - int(diam) - 15),
                    (cx - int(rad) - 5 + 150, cy - int(diam) - 15 + 95),
                    (0, 255, 255),
                    1,
                )
                cv2.line(
                    img,
                    (cx, cy),
                    (cx - int(rad) - 5 + 150, cy - int(diam) - 15 + 95),
                    (0, 255, 255),
                    1,
                )
    _highlight_contours(img, contours)
