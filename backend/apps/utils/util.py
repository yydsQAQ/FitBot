# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：     util
   Description :
   Author :       guxu
   date：          6/22/24
-------------------------------------------------
   Change Activity:
                   6/22/24:
-------------------------------------------------
"""
import cv2
import os
import time
import random
import string
from PIL import Image
import base64
def video_to_images(video_path, output_folder, frame_interval=15):
    """
    Convert a video to a sequence of images and save them to the output folder.

    Parameters:
    video_path (str): The path to the video file.
    output_folder (str): The path to the folder to save the images to.
    frame_interval (int): Number of frames to skip between each image extraction.
    """
    if not os.path.exists(output_folder):
        os.mkdir(output_folder)

    cap = cv2.VideoCapture(video_path)
    frame_count = 0
    saved_frame_count = 0

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        if frame_count % frame_interval == 0:
            frame_filename = os.path.join(output_folder, f"frame{saved_frame_count:04d}.png")
            cv2.imwrite(frame_filename, frame)
            saved_frame_count += 1
        frame_count += 1

    cap.release()

def video_to_gif(video_path, output_gif_path, frame_interval=15, max_size=5 * 1024 * 1024):
    """
    Convert a video to a GIF and save it to the output path.

    Parameters:
    video_path (str): The path to the video file.
    output_gif_path (str): The path to save the GIF file.
    frame_interval (int): Number of frames to skip between each image extraction.
    max_size (int): Maximum size of the output GIF in bytes.
    """
    # Extract frames from video
    cap = cv2.VideoCapture(video_path)
    frames = []
    frame_count = 0

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        if frame_count % frame_interval == 0:
            frames.append(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
        frame_count += 1

    cap.release()

    # Create GIF from frames
    frame_images = [Image.fromarray(frame) for frame in frames]
    frame_images[0].save(output_gif_path, save_all=True, append_images=frame_images[1:], loop=0, duration=100)

    # Check GIF size and resize if necessary
    while os.path.getsize(output_gif_path) > max_size:
        new_size = (frame_images[0].width // 2, frame_images[0].height // 2)
        frame_images = [img.resize(new_size, Image.Resampling.LANCZOS) for img in frame_images]
        frame_images[0].save(output_gif_path, save_all=True, append_images=frame_images[1:], loop=0, duration=100)
        if new_size[0] < 10 or new_size[1] < 10:  # Prevent infinite loop on very small images
            break

    print(f"GIF saved to {output_gif_path}")

def gen_random_string(length=50):
    timestamp = str(int(time.time()))
    return ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(length)) + timestamp

def image_to_base64(image_path):
    if not os.path.exists(image_path):
        raise FileNotFoundError(f"No such file: '{image_path}'")
    with open(image_path, "rb") as image_file:
        image_data = base64.b64encode(image_file.read()).decode("utf-8")
    return image_data

def make_gif_path(video_path):
    paths = video_path.split(".")
    return ".".join(paths[:-1]) + ".gif"

if __name__ == '__main__':
    video_path = "06t5J1719099014IMG_3723.MOV"
    output_gif_path = "output.gif"
    print(make_gif_path(video_path))
    # video_to_gif(video_path, output_gif_path)
    # print(image_to_base64(output_gif_path))