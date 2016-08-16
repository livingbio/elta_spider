#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright © 2016 lizongzhe
#
# Distributed under terms of the MIT license.

from bs4 import BeautifulSoup
import requests
import json


def parse(video, url):

    sourse_code_request = requests.get(url)
    sourse_code = sourse_code_request.text
    soup = BeautifulSoup(sourse_code, "html.parser")

    event_list = soup.select(".event-wrap")
    event_dict_list = []
    for event in event_list:
        event_dict_list.append(
            {"video": video,
             "time": event.select(".event-minute")[0].getText(),
             "event": event.select(".event")[0]["class"][1],
             "message": event.select(".event-text")[0].getText()}
        )
    return event_dict_list


def main():
    import sys
    f, v, u, o = sys.argv
    event_list = parse(v, u)
    with open(o, 'w') as ouput_file:
        json.dump(event_list, ouput_file)

if __name__ == "__main__":
    main()