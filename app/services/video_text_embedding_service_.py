import torch
import clip
import cv2
import numpy as np
from PIL import Image
import logging

device = "cuda" if torch.cuda.is_available() else "cpu"

model, preprocess = clip.load("ViT-B/32", device=device)

def get_frame_embedding(frame):
    """
    Convert single OpenCV frame → CLIP embedding
    """

    # BGR → RGB
    image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    image = Image.fromarray(image)

    # preprocess
    image_input = preprocess(image).unsqueeze(0).to(device)

    with torch.no_grad():
        embedding = model.encode_image(image_input)

    # normalize (VERY IMPORTANT for similarity search)
    embedding = embedding / embedding.norm(dim=-1, keepdim=True)

    return embedding.cpu().numpy()[0]


def get_video_clip_embeddings(frames, timestamps):
    """
    Convert multiple frames into embeddings + metadata
    """

    clip_data = []

    for i in range(len(frames)):

        emb = get_frame_embedding(frames[i])

        clip_data.append({
            "clip_id": i,
            "timestamp": timestamps[i],
            "embedding": emb
        })

    return clip_data


# from video_processor import extract_frames, save_frames

# video_path = "video.mp4"

# frames, timestamps, fps, duration = extract_frames(video_path, every_n_seconds=2)

# print("FPS:", fps)
# print("Duration:", duration)
# print("Frames extracted:", len(frames))
# print("First timestamps:", timestamps[:5])

# # optional save
# save_frames(frames, timestamps, "output_frames")

# clip_data=get_video_clip_embeddings(frames, timestamps)
# print("\nSample output:\n")

# print("Clip count:", len(clip_data))

# print("First clip:")
# print("Timestamp:", clip_data[0]["timestamp"])
# print("Embedding shape:", clip_data[0]["embedding"].shape)


# text embedding

import torch
import clip
# from text_processor import clean_text

model, _=clip.load("ViT-B/32",)

def get_text_embedding(text):

  try:
    """
      convert text-clip embedding
    """
    text_tokens=clip.tokenize([text])

    with torch.no_grad():
        embedding=model.encode_text(text_tokens)

        # normalize(very important)

        embedding=embedding/embedding.norm(dim=-1, keepdim=True)

        return embedding.numpy()[0]
  except Exception as e:
     logging.error(f"clean_text_not executed {e}")
     
  finally:
     print("function executed")
    
# text=clean_text("what@!!!! is my @!!!!!! name")

# result=get_text_embedding(text)
# print(result)