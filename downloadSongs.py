from pathlib import Path
import yt_dlp
import os
import re
import requests

def DownloadFromTitles(songs):

    ids = []
    for index ,item in enumerate(songs):
        vid_id = ScrapeVidId(item)
        ids += [vid_id]
    print(ids)
    print("Downloading Songs")
    DownloadSongsfromId(ids)

def DownloadSongsfromId(ids):
    SAVE_PATH = str(os.path.join(Path.home(),'Documents/Songs'))
    try:
        os.mkdir(SAVE_PATH)
    except:
        print('Download folder exists')

    ydl_opts = {

        'ffmpeg_location': r"D:\ffmpeg-7.1-essentials_build\bin\ffmpeg.exe",
        'format':'bestaudio/best',
        'postProcessors':[{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'prefferedquality':'192'
        }],
        'outtmpl' : SAVE_PATH + '/%(title)s.%(ext)s',
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        try:
            ydl.download(ids)
        except:
            pass
def ScrapeVidId(query):

    url = f"https://www.youtube.com/results?search_query={query}"
    query = url.replace(" ","+")
    response = requests.get(url)
    vid_ids = re.findall(r"watch\?v=(\S{11})",response.text)
    return vid_ids[0]