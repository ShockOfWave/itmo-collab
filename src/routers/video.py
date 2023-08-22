import os
from tempfile import NamedTemporaryFile

from fastapi import APIRouter, UploadFile

from ..cv import create_handled_video


router = APIRouter(prefix='/video')


@router.post('/molecules')
def upload_video(
    file: UploadFile
):
    print('Здесь')
    temp = NamedTemporaryFile(delete=False)
    try:
        try:
            contents = file.file.read()
            print('Здесь 2')
            with temp as f:
                f.write(contents)
            print('Дошло')
        except Exception as e:
            raise e
            return {"message": "There was an error uploading the file"}
        finally:
            file.file.close()
        print('Дошло 2')
        link = create_handled_video(temp.name)  # Pass temp.name to VideoCapture()
    except Exception as e:
        raise e
        # return {"message": "There was an error processing the file"}
    finally:
        # temp.close()  # the `with` statement above takes care of closing the file
        os.remove(temp.name)

    return {'uri': link}

