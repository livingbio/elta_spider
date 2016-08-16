#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright © 2016 lizongzhe
#
# Distributed under terms of the MIT license.
import json
import os.path
import fifa


def test():
    path = os.path.dirname(os.path.abspath(__file__))

    def test_schema(result):
        schema_correct = True
        if isinstance(result, list):
            for event in result:
                if not isinstance(event, dict) or not len(event) == 4:
                    schema_correct = False
                    break
        else:
            schema_correct = False

        if schema_correct is True:
            return True
        else:
            return False

    def test_content(filepath_result, filepath_target):
        with open(filepath_result) as f1, open(filepath_target) as f2:
            content_correct = True
            for line1, line2 in zip(f1, f2):
                if line1 != line2:
                    content_correct = False
                    break
            if content_correct is True:
                print ("Parse Video Succeed!")
            else:
                print ("Parse Video Fail...")

    folder = u"2014世界盃"
    video = "128848_3500K_384K_1920x1080_00-00-01_14511_SH14052001-068.mp4"
    fifa_url = "http://www.fifa.com/worldcup/matches/" + \
               "round=255959/match=300186501/live-blog.html"
    result = fifa.parse(folder + "/" + video, fifa_url)

    if test_schema(result) is True:
        # Convert to file
        filepath_result = path + '/result/result_1'
        targetfile = open(filepath_result, 'a')
        for event in result:
            output = json.dumps(event)
            output += "\n"
            targetfile.write(output)
        targetfile.close()

        # Test result content
        print ("Testing result content.")
        filepath_target = path + '/target/target_1'
        test_content(filepath_result, filepath_target)
    else:
        print ("The schema of the result is not correct.")


test()
