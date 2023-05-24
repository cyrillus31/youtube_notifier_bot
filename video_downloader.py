import pytube
import os

import logging

logger = logging.getLogger(__name__)

file_handler = logging.FileHandler("logs/pytube.log")

formatter = logging.Formatter(fmt="%(asctime)s %(levelname)s %(message)s",
                              datefmt="%Y-%m-%d %H:%M:%S")

file_handler.setFormatter(formatter)

logger.addHandler(file_handler)
logger.setLevel(logging.DEBUG)


def download_audio(url):
    try:
        if not os.path.exists("downloads"):
            os.mkdir("downloads")
        yt = pytube.YouTube(url)
        stream = yt.streams.filter(only_audio=True, file_extension="mp4")[0]
        stream.download(output_path="downloads")
        return 1
    except Exception as e:
        logger.exception(f"The following error happend while trying to download the audio:\n {e}")
        return 0

