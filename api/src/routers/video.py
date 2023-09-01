import os
from tempfile import NamedTemporaryFile

from fastapi import APIRouter, UploadFile

from api.src.cv import create_and_upload_handled_video


router = APIRouter(prefix='/video')


@router.post('/molecules')
def upload_video(
    file: UploadFile
):
    temp = NamedTemporaryFile(delete=False)
    try:
        try:
            contents = file.file.read()
            with temp as f:
                f.write(contents)
        except Exception as e:
            raise e
            return {"message": "There was an error uploading the file"}
        finally:
            file.file.close()
        download_url, stream_url = create_and_upload_handled_video(temp.name)
    except Exception as e:
        raise e
    finally:
        temp.close()  # the `with` statement above takes care of closing the file
        os.remove(temp.name)
    return {'download_url': download_url, 'stream_url': stream_url}

