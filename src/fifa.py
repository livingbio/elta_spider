#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright © 2016 lizongzhe
#
# Distributed under terms of the MIT license.

from bs4 import BeautifulSoup
import requests
import json


def parse(url):

    sourse_code_request = requests.get(url)
    sourse_code = sourse_code_request.text
    soup = BeautifulSoup(sourse_code, "html.parser")

    event_list = soup.select(".event-wrap")
    event_dict_list = []
    for event in event_list:
        event_info = {}
        event_info['time'] = event.select(".event-minute")[0].getText()
        event_info['event'] = event.select(".event")[0]["class"][1]
        event_info['message'] = event.select(".event-text")[0].getText()
        
        if '+' in event_info['time']:
            continue
        
        if event_info['event'] in ('second-start'):
            event_info['time'] = "45'"

        if event_info['event'] in ('third-start'):
            event_info['time'] = "90'"

        event_dict_list.append(event_info)

    return event_dict_list


def main():
    import sys
    if len(sys.argv) != 3:
        print 'python fifa {{fifa url}} {{output path}}'
    f, u, o = sys.argv
    event_list = parse(u)
    with open(o, 'w') as ouput_file:
        json.dump(event_list, ouput_file)

if __name__ == "__main__":
    main()
