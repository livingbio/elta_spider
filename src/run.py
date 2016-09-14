#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright © 2016 lizongzhe 
#
# Distributed under terms of the MIT license.
import os
import cv2
import numpy as np
import json
from multiprocessing import Pool
curr_dir = os.path.dirname(os.path.abspath(__file__))

pool = Pool(2)

def feature(img):
    feat = []
    img = cv2.imread(os.path.join(curr_dir, img))
    feat.append(img.mean(axis=(0, 1)))
    for i in np.hsplit(img, 3):
        for j in np.vsplit(i, 3):
            feat.append(j.mean(axis=(0, 1)))
    return np.array(feat).flatten()

def parse_index(data):
    st, ed = data
    img_template = "{:0>8}.jpg"
    result = []  
    old = None
    for i in xrange(st, ed + 1):
        curr = feature(img_template.format(i))
        if old != None:
            d = np.linalg.norm(curr - old)
            if d > 50:
                result.append((i, d))

        old = curr
    return result


def split_worker(st, ed, size=100):
    assert ed > st, 'range error'

    ins = range(st, ed+1, size)
    if ins[-1] != ed:
        ins.append(ed)
    return [(ins[i], ins[i+1]) for i in range(len(ins) -1)]


def get_works(st_second, ed_second, size=100):
    st = 30 * int(st_second) - 30
    ed = 30 * int(ed_second)
    return split_worker(st, ed, size)


if __name__ == '__main__':
    from multiprocessing import Pool
    from datetime import datetime
    import sys
    print curr_dir
    try:
        _, st, ed = sys.argv
    except:
        total = os.popen('ls {}|grep jpg|wc -l'.format(curr_dir)).read()
        ed = int(total)
        st = 1
    st = int(st)
    ed = int(ed)
    pool = Pool(48)


    begin = datetime.now()
    inputs = split_worker(st, ed, 1000)
    tmp = pool.map(parse_index, inputs)
    result = []
    for r in tmp:
        result+=r
    with open(os.path.join(curr_dir, 'index'), 'w+') as f:
        f.write(json.dumps(result))
    end = datetime.now()
    print end - begin
