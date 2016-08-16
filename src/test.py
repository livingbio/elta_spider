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

    def test_schema(event_dict_list):
        event_list = ["goal", "goal-own", "yellow-card", "red-card", "yellow-card-second",
                      "substitution-in-out", "substitution-out", "substitution-in",
                      "first-start", "first-end", "second-start", "second-end",
                      "third-start", "third-end", "penalty", "penalty-wrong",
                      "match-report", "hidden"]
        schema_correct = True
        if isinstance(event_dict_list, list):
            for event_dict in event_dict_list:
                if isinstance(event_dict, dict):
                    video = event_dict["video"]
                    if isinstance(video, str):
                        if not video.endswith(".mp4"):
                            print ("Video name is not correct")
                            schema_correct = False
                            break
                    else:
                        print ("The type of video is wrong")
                        schema_correct = False
                        break

                    event = event_dict["event"]
                    if isinstance(event, str):
                        if not event in event_list:
                            print ("Unknown event")
                            schema_correct = False
                            break
                    else:
                        print ("The type of event is wrong")
                        schema_correct = False
                        break

                    message = event_dict["message"]
                    if not isinstance(message, str):
                        schema_correct = False
                        break

                    time = event_dict["time"]
                    if not isinstance(time, str):
                        schema_correct = False
                        break

                else:
                    print ("An element in the parser result should be a dict")
                    schema_correct = False
                    break
        else:
            print ("Parser result is not a list.")
            schema_correct = False

        return schema_correct


    def test_content(filepath_result, filepath_target):
        with open(filepath_result) as f1, open(filepath_target) as f2:
            content_correct = True
            for line1, line2 in zip(f1, f2):
                if line1 != line2:
                    content_correct = False
                    break
            if content_correct is True:
                print ("Parsing match Succeeds!")
            else:
                print ("Parsing match Fails.")


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
        filepath_target = path + '/target/target_1'
        test_content(filepath_result, filepath_target)
    else:
        print ("The schema of the result is not correct.")


test()
