#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright © 2016 lizongzhe 
#
# Distributed under terms of the MIT license.
import sys
import fifa
import os
import json

def parse(video, fifa_url, first_offset, second_offset, overtime_offset=0, output_path='result'):
    first_offset = int(first_offset)
    second_offset = int(second_offset)
    overtime_offset = int(overtime_offset)

    fifa_indexs = fifa.parse(fifa_url)
    real_indexs = []
    for index in fifa_indexs:
        real_index = {}
        real_index['event'] = index['event']
        real_index['message'] = index['message']

        time = index['time'].replace("'", '')

        real_index['fifa_time'] = time
        if "+" in time:
            continue

        else:
            try:
                time = int(time) * 60
            except:
                continue

        if time >= 90 * 60:
            real_time = time + overtime_offset - 90*60
            real_index['st'] = real_time - 60
            real_index['ed'] = real_time + 60
        elif time >= 45 * 60:
            real_time = time + second_offset - 45*60
            real_index['st'] = real_time - 60
            real_index['ed'] = real_time + 60
        else:
            real_time = time + first_offset
            real_index['st'] = real_time - 60
            real_index['ed'] = real_time + 60

        real_indexs.append(real_index)

    f_name = os.path.basename(video) + ".index"
    f_path = os.path.join('result', f_name)

    with open(f_path, 'w+') as f:
        for index in real_indexs:
            f.write(json.dumps(index))
            f.write('\n')

        

if __name__ == '__main__':
    if len(sys.argv) not in [5, 6]:
        print 'python index {{video}} {{fifa_url}} {{offset_上半場}} {{offset 下半場}} {{offset 延長賽}}'
    print sys.argv 
    parse(*sys.argv[1:])
