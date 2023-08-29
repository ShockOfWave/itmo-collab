import os
import uuid
import shutil

import cv2

from ..utils.converter import mp4_to_hls
from .contours import find_molecules
from ..config import settings
from ..utils.s3 import create_s3_folder, upload_file_to_s3, create_presigned_s3_url

def create_and_upload_handled_video(video_name):
    vcap = cv2.VideoCapture(video_name)

    width = int(vcap.get(3))
    height = int(vcap.get(4))
    fps = int(vcap.get(cv2.CAP_PROP_FPS))

    fourcc = cv2.VideoWriter_fourcc(*'mp4v')

    new_video_name = f'video_{uuid.uuid4()}'
    new_video_name_mp4 = new_video_name+'.mp4'
    new_video_name_m3u8 = new_video_name + '.m3u8'

    if os.path.exists(f'{settings.PROJECT_DIR_PATH}/api/src/upload'):
        shutil.rmtree(f'{settings.PROJECT_DIR_PATH}/api/src/upload')

    os.mkdir(f'{settings.PROJECT_DIR_PATH}/api/src/upload')

    writer = cv2.VideoWriter(f'{settings.PROJECT_DIR_PATH}/api/src/upload/{new_video_name_mp4}', fourcc, fps,
                          (width, height))

    while vcap.isOpened():
        ret, frame = vcap.read()
        if ret:
            find_molecules(frame)
            writer.write(frame)
        else:
            break

    vcap.release()
    writer.release()

    folder = create_s3_folder(new_video_name) # will return with /
    upload_file_to_s3(f'{settings.PROJECT_DIR_PATH}/api/src/upload/{new_video_name_mp4}',
                      folder+new_video_name_mp4)
    mp4_to_hls(f'{settings.PROJECT_DIR_PATH}/api/src/upload/{new_video_name_mp4}')

    for _, _, files in os.walk(f'{settings.PROJECT_DIR_PATH}/api/src/upload'):
        for file in files:
            upload_file_to_s3(f'{settings.PROJECT_DIR_PATH}/api/src/upload/{file}',
                              folder+file)
    download_url = create_presigned_s3_url(folder+new_video_name_mp4)
    stream_url = '/'.join([settings.S3_URL, settings.S3_BUCKET, new_video_name, new_video_name_m3u8])

    shutil.rmtree(f'{settings.PROJECT_DIR_PATH}/api/src/upload')

    return download_url, stream_url