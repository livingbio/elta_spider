#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright © 2016 lizongzhe 
#
# Distributed under terms of the MIT license.

import numpy as np
import json
from multiprocessing import Pool
import cv2
import numpy as np
import os
import math

curr_dir = os.path.dirname(os.path.abspath(__file__))

def get_hash(img):
    new_img = cv2.resize(img, (32, 32))
    mask1 = red_mask(new_img)
    mask2 = default_mask(new_img)
    return (mask1, mask2)


def red_mask(img):
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    l_r = np.array([-10, 50, 50])
    h_r = np.array([10, 255, 255])
    return cv2.inRange(hsv, l_r, h_r) > 200

def default_mask(img):
    l_default = np.array([0, 150, 180])
    h_default = np.array([80, 255, 255])
    return cv2.inRange(img, l_default, h_default) > 200


def training():
    imgs = ["target/" + path for path in os.listdir('target') if ".jpg" in path]
    target_hashs = []
    for img in imgs:
        img_obj = cv2.imread(img)
        img_hash = get_hash(img_obj)
        target_hashs.append(img_hash)
    np.save('target.data', target_hashs)

def is_target(img_obj):
    if isinstance(img_obj, basestring):
        img_obj = cv2.imread(img_obj)

    x1, y1 = get_hash(img_obj)
    data = np.load('target.data.npy')
    tx = np.sum(x1) +1
    ty = np.sum(y1) +1

    result = []
    for x, y in data:
        tdx = np.sum(x ^ x1)
        idx = np.sum((x | x1) ^ x1)
        odx = tdx - idx 

        delta_x = math.sqrt(idx ** 2 + odx ** 2 + tdx ** 2) * 1.0 / tx
        delta_ix = idx * 1.0 / tx

        tdy = np.sum(y ^ y1)
        idy = np.sum((y | y1) ^ y1)
        ody = tdy - idy

        delta_y = math.sqrt(idy **2 + ody **2 + tdy **2) * 1.0 / ty
        delta_iy = idy * 1.0 / ty
        result.append( (math.sqrt(delta_x **2 + delta_y **2), math.sqrt(delta_ix**2 + delta_iy**2)))
    data = sorted(result, key=lambda x: x[0])
    return data[0]

        

def test():
    imgs = ["video/" + path for path in os.listdir('video') if ".jpg" in path]
    for img in imgs:
        img_obj = cv2.imread(img)
        data = is_target(img_obj)
        if data:
            print img, data

def video_split(video_path):
    "ffmpeg -i video_path -vf fps=5 tmp_%05d.jpg"

def video_cut(video_path):
    video = cv2.VideoCapture(video_path)       
    video.set(cv2.cv.CV_CAP_PROP_FPS, 10)
    fps = video.get(cv2.cv.CV_CAP_PROP_FPS)
    fps = 30
    out = cv2.VideoWriter('output.avi',cv2.cv.CV_FOURCC(*'X264'), 20.0, (1080, 720))
    out = cv2.VideoWriter('output.avi', -1, 20.0, (1080, 720))
    count = 0
    flat, img = video.read()
    result = []
    
    du = []
    while True:
        count+=1
        flat, frame = video.read()
        if not flat:
            break
        if count % 6:
            continue
        if is_target(frame):
            print count, du
            if not du:
                du.append(count)
            else:
                if (count - du[0]) > 10:
                    du.append(count)
                    break
    print du[0]/30.0, du[1]/30.0
    return result


def split_worker(st, ed, size=100):
    assert ed > st, 'range error'

    ins = range(st, ed+1, size)
    if ins[-1] != ed:
        ins.append(ed)
    return [(ins[i], ins[i+1]) for i in range(len(ins) -1)]


def parse_index(data):
    st, ed = data
    img_template = "{:0>8}.jpg"
    result = []  
    old = None
    for i in xrange(st, ed):
        curr = is_target(img_template.format(i))
        result.append((i, curr))
    return result

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
        f.write(json.dumps(result, indent=4))
    end = datetime.now()
    print end - begin
