"""Compressor body"""

from os import system

from .exceptions import NonZeroExitCodeReturned
from .const import (COMPRESS_VIDEO_FPS, COMPRESS_VIDEO_BITRATE, COMPRESS_AUDIO_BITRATE,
                    COMPRESS_VIDEO_SIZE, COMPRESS_VOLUME_BOOST)


def compress_video(file) -> str:
    """Compress video func"""
    command = ("ffmpeg -y"
               f" -i {file}"
               f" -fpsmax {COMPRESS_VIDEO_FPS}"
               f" -s {COMPRESS_VIDEO_SIZE}"
               f" -b:v {COMPRESS_VIDEO_BITRATE}"
               f" -b:a {COMPRESS_AUDIO_BITRATE}"
               f" -filter:a 'volume={COMPRESS_VOLUME_BOOST}'"
               f" {file}_compressed.mp4")
    exit_code = system(command)
    if not exit_code:
        return file + "_compressed.mp4"
    raise NonZeroExitCodeReturned(exit_code)


def compress_audio(file) -> str:
    """Compress audio func"""
    command = ("ffmpeg -y"
               f" -i {file}"
               f" -b:a {COMPRESS_AUDIO_BITRATE}"
               f" -filter:a 'volume={COMPRESS_VOLUME_BOOST}'"
               f" {file}_compressed.mp3")
    exit_code = system(command)
    if not exit_code:
        return file + "_compressed.mp3"
    raise NonZeroExitCodeReturned(exit_code)
