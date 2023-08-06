from subprocess import run
from typing import Optional

import magic
from django.core.files.uploadedfile import (
    InMemoryUploadedFile,
    TemporaryUploadedFile,
    UploadedFile,
)

from wideo.exceptions import UnsupportedUploadedFileType


def compute_division(division: str) -> Optional[float]:
    if division == "N/A":
        return None

    a, b = division.split("/")
    return float(a) / float(b)


def try_round(n: Optional[float]) -> Optional[float]:
    return round(n, 2) if n is not None else n


def get_video_info(file: UploadedFile) -> dict:
    if isinstance(file, InMemoryUploadedFile):
        filename = "-"
        file.seek(0)
        data = file.read()
        file.seek(0)
        mime = magic.from_buffer(data, mime=True)
    elif isinstance(file, TemporaryUploadedFile):
        filename = file.temporary_file_path()
        data = None
        mime = magic.from_file(filename, mime=True)
    else:
        raise UnsupportedUploadedFileType

    ffprobe = run(
        [
            "ffprobe",
            "-select_streams",
            "v:0",
            "-show_entries",
            "stream=width,height,nb_frames,avg_frame_rate:format=duration",
            "-of",
            "default=noprint_wrappers=1",
            filename,
        ],
        input=data,
        capture_output=True,
    )

    info = {
        key: try_round(compute_division(value) if "/" in value else float(value))
        for key, value in (line.split("=") for line in ffprobe.stdout.decode().split())
    }

    if not info["nb_frames"]:
        info["nb_frames"] = round(info["avg_frame_rate"] * info["duration"])

    info["mime"] = mime
    return info
