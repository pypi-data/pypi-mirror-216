import os
import subprocess
import ffmpeg
import math
import requests
from video_process.subtitle import change_style


def download_file(url, path):
    response = requests.get(url)
    if response.status_code == 200:
        with open(path, "wb") as file:
            file.write(response.content)


def process_data(data, base_dir):
    """
    替换url为本地文件
    """
    video_url = data["video_url"]
    video_path = os.path.join(base_dir, "video.webm")
    download_file(video_url, video_path)
    data["video_path"] = video_path

    if data.get("enable_bg"):
        bg = data["bg"]
        if bg["bg_type"] == "video" and bg.get("bg_video_url"):
            video_url = bg["bg_video_url"]
            video_path = os.path.join(base_dir, "bg_video.mp4")
            download_file(video_url, video_path)
            bg["bg_video_path"] = video_path
        elif bg["bg_type"] == "image" and bg.get("bg_image_url"):
            image_url = bg["bg_image_url"]
            image_path = os.path.join(base_dir, "bg_image.jpg")
            download_file(image_url, image_path)
            bg["bg_image_path"] = image_path

    # 处理背景音乐字段
    if data.get("enable_bgm"):
        bg_music = data["bgm"]
        if bg_music.get("bgm_url"):
            music_url = bg_music["bgm_url"]
            music_path = os.path.join(base_dir, "bg_music.mp3")
            download_file(music_url, music_path)
            bg_music["path"] = music_path

    # 处理字幕字段
    if data.get("enable_subtitle"):
        subtitle = data["subtitle"]
        if subtitle.get("url"):
            subtitle_url = subtitle["url"]
            subtitle_path = os.path.join(base_dir, "subtitle.srt")
            download_file(subtitle_url, subtitle_path)
            subtitle["subtitle_path"] = subtitle_path

            # 转换SRT字幕为ASS字幕
            style = subtitle["subtitle_style"]
            output_ass_path = os.path.join(base_dir, "subtitle.ass")
            change_style(subtitle_path, output_ass_path, style)
            subtitle["subtitle_path"] = output_ass_path

    # 处理图层字段
    if data.get("enable_layers"):
        layers = data["layers"]
        for layer in layers:
            if layer.get("url"):
                layer_url = layer["url"]
                layer_path = os.path.join(base_dir, f"layer_{layer['index']}.png")
                download_file(layer_url, layer_path)
                layer["layer_path"] = layer_path

        sorted_layers = sorted(layers, key=lambda x: x["index"])
        data["layers"] = sorted_layers


def get_video_min(input_file):
    video_info = ffmpeg.probe(input_file)
    duration = float(video_info["format"]["duration"])
    video_length = math.ceil(duration / 60)  # 将秒数转换为分钟，不满一分钟按一分钟算
    return video_length


def check_dir(tar_dir):
    if not os.path.exists(tar_dir):
        os.makedirs(tar_dir)


def get_video_duration(filename):
    result = subprocess.run(
        [
            "ffprobe",
            "-v",
            "error",
            "-select_streams",
            "v:0",
            "-show_entries",
            "format=duration",
            "-of",
            "csv=p=0",
            filename,
        ],
        capture_output=True,
        text=True,
    )
    output = result.stdout.strip()
    duration = float(output)
    return duration
