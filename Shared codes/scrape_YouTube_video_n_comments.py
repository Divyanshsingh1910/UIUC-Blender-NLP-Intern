from __future__ import unicode_literals
import scrapetube
import youtube_dl
import yt_dlp
from yt_dlp import YoutubeDL
import json
import os
from pathlib import Path
import shutil

#ydl_opts_comments = {'write-comments':True, 'outtmpl': 'data/YouTube/comments/%(title)s-%(id)s.%(ext)s'}
#url = "https://www.youtube.com/watch?v=kOHXmlRaTqU"
#with YoutubeDL(ydl_opts_comments) as ydl:
#    ydl.download([url])
#quit()
# Write Function to scrape urls based on YouTube links
def scrape_YouTube_urls():
    output_fname = "data/YouTube/urls_scraped.json"
    url_tracker = []
    if os.path.exists(output_fname):
        with open(output_fname, "r") as f:
            url_tracker = json.load(f)
    channels_of_interest = ["UCqYTGjucWaKMdBqI6kgDrUg","UCeUGVe4-DQi1BEqdCGMJPnQ",\
            "UCFjNsaumCCbhfRSdlyQzrwQ","UCcqaFbjXPj8f7uoiIYs-C_A","UCMXPffV2NeApY7BstSWvOUg",\
            "UCuaG0PtD47mjGm2MG5OJMcw","UCJ67AiozLEYc0xrpD6c5Y1w","UC6VuuCC8AEzrsnyTb4TiZ9A",\
            "UCta4WFyUEE2t-ovy887Cwhg","UCMDPNmfnDpOSa9adbQj97lQ"]
    scraped_channels = list(set([x[0] for x in url_tracker]))
    for channelID in channels_of_interest:
        if channelID in scraped_channels:
            continue
        try:
            videos = scrapetube.get_channel(channelID)
            for video in videos:
                url_tracker.append((channelID, video['videoId'], video))
        except:
            pass
        try:
            videos = scrapetube.get_channel(channelID, content_type="shorts") 
            for video in videos:
                print(video)
                url_tracker.append((channelID, video['videoId'], video))
        except:
            pass
        with open(output_fname, "w") as f:
            json.dump(url_tracker, f)

# Write Function download videos from each url
def scrape_YouTube_videos():
    with open("data/YouTube/urls_scraped.json", "r") as f:
        url_tracker = json.load(f)
    for video_data in url_tracker:
        url = video_data[1]
        ydl_opts = {'outtmpl': 'data/YouTube/videos/%(title)s-%(id)s.%(ext)s'}
        ydl_opts_comments = {'write-comments':True, 'skip_downloads':True, 'outtmpl': 'data/YouTube/comments/%(title)s-%(id)s.%(ext)s'}
        try:
            if "lengthText" in video_data[2]:
                time_len = video_data[2]["lengthText"]['simpleText']
                num_m = int(time_len.split(":")[-2])
                if num_m<=1 and time_len.count(":")<=1:
                    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                        ydl.download([url])
                    #os.system("yt_dlp --write-comments --skip-download "+url)
                    #with YoutubeDL(ydl_opts_comments) as ydl:
                    #    info = ydl.extract_info(url, write_comments=True, download=False)
                    #    print(json.dumps(ydl.sanitize_info(info)))
                    pass    #ydl.download([url])
            if "lengthText" not in video_data[2]:
                with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                    ydl.download([url])
            os.system("yt-dlp --write-comments --skip-download "+url)
        except:
            pass
    src_path = '.'
    trg_path = 'data/YouTube/comments'
    for src_file in Path(src_path).glob('*.info.json'):
        shutil.copy(src_file, trg_path)
        os.system("rm "+str(src_file))
        
# Write Function to download comments from YT url
def scrape_YouTube_comments():
    with open("data/YouTube/urls_scraped.json", "r") as f:
        url_tracker = json.load(f)
    count = 0
    for video_data in url_tracker:
        if "lengthText" in video_data[2]:
            time_len = video_data[2]["lengthText"]['simpleText']
            num_m = int(time_len.split(":")[-2])
            if num_m<=1 and time_len.count(":")<=1:
                print(video_data[0], video_data[1])
                video_title = video_data[2]["title"]["runs"][0]["text"].lower()
                if "putin" in video_title or "trump" in video_title or "biden" in video_title \
                    or "nato" in video_title or "jinping" in video_title or "modi" in video_title:
                    count += 1
                    print(video_data[2]["title"]["accessibility"]['accessibilityData']["label"])
        else:
            video_title = video_data[2]["headline"]['simpleText'].lower()
            if "putin" in video_title or "trump" in video_title or "biden" in video_title \
                    or "nato" in video_title or "jinping" in video_title or "modi" in video_title:
                count += 1
                print(video_data[2]["headline"]['simpleText'])
    print(count, len(set([x[0] for x in url_tracker])))
    #print(len(url_tracker))

# Driver: keep track of source, url, saved video_fname,

#scrape_YouTube_urls()
scrape_YouTube_videos()
#scrape_YouTube_comments()

