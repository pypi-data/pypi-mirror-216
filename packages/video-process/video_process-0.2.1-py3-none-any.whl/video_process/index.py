# -*- coding: utf-8 -*-
import os
import logging
import sys
from video_process.utils import process_data, check_dir, get_video_min
from video_process.graph_builder import GraphBuilder
from video_process.lib import upload_file, get_cos_url
from video_process.subtitle import set_script_info

logging.basicConfig(level=logging.INFO, stream=sys.stdout)
logger = logging.getLogger()
logger.setLevel(level=logging.INFO)


def video_process(body):
    print("Loading function")

    base_dir = "/tmp"
    check_dir(base_dir)
    process_data(body, base_dir)
    gb = GraphBuilder(body["video_path"])
    x, y = gb.scale_overlay(body["xpos"], body["ypos"], float(body["scale"]))

    if body.get("enable_bg"):
        gb.add_bg(body["bg"], x, y)

    if body.get("enable_layers"):
        layers = body["layers"]
        for layer in layers:
            gb.add_overlay(layer)

    if body.get("enable_bgm"):
        gb.add_bg_music(body["bgm"])

    if body.get("enable_subtitle"):
        print("enable_subtitle")
        set_script_info(body["subtitle"]["subtitle_path"], gb.width, gb.height)
        gb.add_subtitle(body["subtitle"]["subtitle_path"])
    output_path = os.path.join(base_dir, "output.mp4")
    gb.drop_first_frame()
    command = gb.build(output_path)
    gb.run(command)

    upload_file(body["key"], output_path)
    result = {}
    result["media_url"] = get_cos_url(body["key"])
    result["duration"] = get_video_min(output_path)
    return result
