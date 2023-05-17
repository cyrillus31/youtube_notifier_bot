import pytube
import os


def download_audio(url):
    try:
        if not os.path.exists("downloads"):
            os.mkdir("downloads")
        yt = pytube.YouTube(url)
        stream = yt.streams.filter(only_audio=True, file_extension="mp4")[0]
        stream.download(output_path="downloads")
        return 1
    except Exception as e:
        return 0

# url = "https://www.youtube.com/watch?v=djzXzAQShgQ"
# download_audio(url)
