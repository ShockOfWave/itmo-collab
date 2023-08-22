from .contours import find_molecules

import cv2
import uuid

def create_handled_video(video_name):
    vcap = cv2.VideoCapture(video_name)

    width = int(vcap.get(3))
    height = int(vcap.get(4))
    fps = int(vcap.get(cv2.CAP_PROP_FPS))

    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    new_video_name = f'video_{uuid.uuid4()}.mp4'
    writer = cv2.VideoWriter(f'/home/antonio/PycharmProjects/itmo_collab/src/upload/{new_video_name}', fourcc, fps,
                          (width, height))

    while vcap.isOpened():
        ret, frame = vcap.read()
        if ret:
            find_molecules(frame)
            writer.write(frame)
        else:
            print('беды с видосом')
            break

    print('Дошло 3')
    vcap.release()
    writer.release()
    print(f'/home/antonio/PycharmProjects/itmo_collab/src/upload/{new_video_name}')
    return f'/home/antonio/PycharmProjects/itmo_collab/src/upload/{new_video_name}'