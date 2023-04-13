import os, json


#comments_dir = "data/YouTube/comments/"
comments_dir = "./"

count = 0
for fname in os.listdir(comments_dir):
    if ".json" not in fname:
        continue
    try:
        with open(comments_dir+fname, "r") as f:
            data = json.load(f)
    except:
        continue
    #print(data["like_count"], data["duration"], data["comment_count"])
    #print(data["duration"])
    if data["uploader_id"]=="@5AABTODAYCHANNEL":
        continue
    if "like_count" not in data: # or data["duration"]>60:
        continue
    print(data["like_count"], data["duration"], data["comment_count"])
    if data["like_count"] > 10 or data["comment_count"]>2:
        print(data["id"])
        """
        print(data["title"])
        print(data["description"])
        print(data["webpage_url"])
        print(data["comments"])
        """
        count += 1
print(count)
