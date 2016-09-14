#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright © 2016 lizongzhe 
#
# Distributed under terms of the MIT license.

import os

videos = os.listdir(u'2014')

for video in videos:
    video_path =  u"2014/{}".format(video)
    img_path = video.replace('.mp4', '')
    os.mkdir("image/"+video.replace('.mp4', ''))
    #print(u'ffmpeg -i {} -vf fps=5 image/{}/%8d.jpg'.format(video_path, img_path))

