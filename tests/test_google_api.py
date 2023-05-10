import unittest
import sys
import requests
import bs4

sys.path.append('..')
import google_api

class Test_google_api(unittest.TestCase):

    def test_channel_id(self):
        channel_id, yt_handle = google_api.get_channel_id("https://youtube.com/@ThePrimeagen")
        print((channel_id, yt_handle))
        self.assertNotEqual(type(channel_id), bool, "Channel_id is bool!")
        self.assertNotEqual(type(yt_handle), bool, "Channel_id is bool!")

        channel_id, yt_handle = google_api.get_channel_id("https://youtube.com/@margulan__seissembai")
        print((channel_id, yt_handle))
        self.assertNotEqual(type(channel_id), bool, "Channel_id is bool!")
        self.assertNotEqual(type(yt_handle), bool, "Channel_id is bool!")

        channel_id, yt_handle = google_api.get_channel_id("https://youtube.com/@ThePrimeagen")
        print((channel_id, yt_handle))


def get_channel_id(url: str) -> tuple:
    "Parses the link and gets the channelId meta information"
    response = requests.get(url)
    soup = bs4.BeautifulSoup(response.text, "lxml")
    meta = soup.find_all("meta")
    print(meta)

    channel_id = "Unknown"

    yt_handle = False
    channel_id = False
    for m in meta:
        if yt_handle and channel_id:
            break
        try:
            if m.attrs["itemprop"] == "channelId" or m.attrs["itemprop"] == "identifier":
                channel_id = m.attrs["content"]
        except:
            pass
        try:
            if m.attrs["itemprop"] == "name":
                yt_handle = m.attrs["content"]
        except:
            continue
    return channel_id, yt_handle

print(get_channel_id("https://youtube.com/@theprimetimeagen"))