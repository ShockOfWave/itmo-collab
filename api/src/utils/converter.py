import asyncio

import ffmpeg_streaming
from ffmpeg_streaming import Formats


def mp4_to_hls(file_path):
    video = ffmpeg_streaming.input(file_path)
    hls = video.hls(Formats.h264())

    hls.auto_generate_representations()
    hls.output()

