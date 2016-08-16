#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright © 2016 lizongzhe
#
# Distributed under terms of the MIT license.

from bs4 import BeautifulSoup
import requests


def parse(video, url):

    sourse_code_request = requests.get(url)
    sourse_code = sourse_code_request.text
    soup = BeautifulSoup(sourse_code, "html.parser")

    event_list = soup.select(".event-wrap")
    print(len(event_list))
    event_dict_list = []
    for event in event_list:
        event_dict_list.append(
            {"video": video,
             "time": event.select(".event-minute")[0].getText(),
             "event": event.select(".event")[0]["class"][1],
             "message": event.select(".event-text")[0].getText()}
        )
    return event_dict_list

folder = "2014世界盃"
video_name = "128848_3500K_384K_1920x1080_00-00-01_14511_SH14052001-068.mp4"
fifa_url = "http://www.fifa.com/worldcup/matches/ \
            round=255959/match=300186501/live-blog.html"
print(parse(folder + "/" + video_name, fifa_url))
