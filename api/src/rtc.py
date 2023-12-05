from aiortc import MediaStreamTrack
from aiortc.contrib.media import MediaRelay, MediaBlackhole
from av import VideoFrame

from api.src.cv.contours import find_molecules


class VideoStream(MediaStreamTrack):
    kind = "video"

    def __init__(self, track, cv):
        super().__init__()
        self.track = track
        self.cv = cv

    async def recv(self):
        frame = await self.track.recv()

        if self.cv:
            pts = frame.pts
            time_base = frame.time_base
            img = frame.to_ndarray(format="bgr24")
            find_molecules(img)
            frame = VideoFrame.from_ndarray(img, format="bgr24")
            frame.time_base = time_base
            frame.pts = pts
        return frame


relay = MediaRelay()
recorder = MediaBlackhole()
pcs = set()
