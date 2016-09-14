#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright © 2016 lizongzhe 
#
# Distributed under terms of the MIT license.
import sys
import json
import os
import hashlib
base_url = 'gs://gliacloud-elta/2014世界盃/{}'

def parse_time(total_sec):
    s = total_sec % 60
    m = (total_sec / 60) % 60
    h = total_sec / 3600

    data = "{:0>2}:{:0>2}:{:0>2}".format(h, m, s)
    return data

def download_file(file_name, output_path):
    f_url = base_url.format(file_name)
    tmp_name = "{}/{}".format(output_path, file_name)
    if os.path.exists(tmp_name):
        return tmp_name
    cmd = 'gsutil cp {} {}'.format(f_url, tmp_name)
    result = os.system(cmd)
    return tmp_name


def process(index_file, output_path='el'):
    video_file_name = os.path.basename(index_file).replace(".index", '')
    video_file = download_file(video_file_name, 'tmp')
    
    event_index = "{}/{}.index".format(output_path, video_file_name)
    with open(event_index, 'a+') as e_i:
        with open(index_file) as f:
            for line in f.readlines():
                try:
                    event_info = json.loads(line)

                    duration = event_info['ed'] - event_info['st']
                    st = parse_time(event_info['st'])
                    duration = parse_time(duration)
                    event = event_info['event']
                    fifa_time = event_info['fifa_time']
                    message = event_info['message']

                    event_md5 = hashlib.md5()
                    event_md5.update(video_file)
                    event_md5.update(line)
                    event_key = event_md5.hexdigest()

                    event_video = "{}.mp4".format(event_key)
                    event_video_path = "{}/{}".format(output_path, event_video)
                    
                    #cmd = "ffmpeg -y -i {} -ss {} -t {} -acodec copy -vcodec copy {}".format(video_file, st, duration, event_video_path)
                    os.system(cmd)

                    new_info = {}
                    new_info['message'] = message
                    new_info['event'] = event
                    new_info['video_path'] = event_video
                    new_info['fifa_time']  = fifa_time
                    e_i.write(json.dumps(new_info))
                    e_i.write('\n')
                    
                except Exception as e:
                    import pdb;pdb.set_trace()
                
    os.remove(video_file)


if __name__ == '__main__':
    _, i, o = sys.argv

    process(i, o)
