#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright © 2016 lizongzhe 
#
# Distributed under terms of the MIT license.

import re
import sys

_, source_file = sys.argv

def get_seconds(time_str):
    time_str = time_str.split(':', 1)[1]
    times = time_str.split(':')
    times.reverse()
    times = times + ['0', '0']
    total_sec = sum([int(times[i])*60**i for i in range(3) ])
    return total_sec

    

with open(source_file) as f: 
    for line in f.readlines():
        name, video, fifa_url, time = line.split('|')
        time = re.sub('[\w:]*_end[\w:]*', '', time).strip()
        times = re.split("\s+", time)
        times = [get_seconds(time) for time in times]
        print "python index.py", video, fifa_url, " ".join([str(t) for t in times])

