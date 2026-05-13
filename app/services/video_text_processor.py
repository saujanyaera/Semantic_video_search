import cv2
import os

def load_video(video_path):
    """
    Load video using OpenCV
    """

    cap = cv2.VideoCapture(video_path)

    if not cap.isOpened():
        raise ValueError(f"Cannot open video: {video_path}")

    fps = cap.get(cv2.CAP_PROP_FPS)
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    duration = total_frames / fps if fps else 0

    return cap, fps, total_frames, duration

def extract_frames(video_path, every_n_seconds=1):
    """
    Extract frames every N seconds
    """

    cap, fps, total_frames, duration = load_video(video_path)

    frames = []
    timestamps = []

    step = int(fps * every_n_seconds)

    frame_id = 0

    while True:
        ret, frame = cap.read()

        if not ret:
            break

        if frame_id % step == 0:
            timestamp = frame_id / fps

            frames.append(frame)
            timestamps.append(timestamp)

        frame_id += 1

    cap.release()

    return frames, timestamps, fps, duration


def save_frames(frames, timestamps, output_folder="frames"):
    """
    Save extracted frames as images
    """

    os.makedirs(output_folder, exist_ok=True)

    saved_files = []

    for i, (frame, t) in enumerate(zip(frames, timestamps)):
        filename = f"{output_folder}/frame_{i}_t{int(t)}.jpg"

        cv2.imwrite(filename, frame)
        saved_files.append(filename)

    return saved_files


# video_path = "video.mp4"

# frames, timestamps, fps, duration = extract_frames(video_path, every_n_seconds=2)

# print("FPS:", fps)
# print("Duration:", duration)
# print("Frames extracted:", len(frames))
# print("First timestamps:", timestamps[:5])

# # optional save
# save_frames(frames, timestamps, "output_frames")


# text processor

import re
import logging

def clean_text(text):
 
  try:
     text=text.lower()
# special character removal
     text = re.sub(r"[^a-zA-Z0-9\s]", "", text)
# spaces removal
     text = re.sub(r"\s+", " ", text).strip()

     return text
  except Exception as e:
     logging.error(f"clean_text failed:{e}")
     return ""
  finally:
      logging.info("clean text executed")
  

# result=clean_text("what is my name")
# print(result)