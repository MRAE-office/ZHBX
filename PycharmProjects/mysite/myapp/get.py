import requests
import random
import json
def get(n):
    url = "http://cn.bing.com/HPImageArchive.aspx?format=js&idx=%s&n=1&mkt=zh-CN" % n
    print(url)
    site = requests.get(url)
    json_of_site = json.loads(site.text)
    print(json_of_site)
    url_of_background = json_of_site["images"][0]["url"]
    print(url_of_background)
    background = "http://cn.bing.com/" + url_of_background
    print(background)
    return background

