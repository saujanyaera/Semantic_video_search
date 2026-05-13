from app.services.video_text_embedding_service_ import get_frame_embedding, get_video_clip_embeddings, get_text_embedding
from app.services.video_text_processor import clean_text, extract_frames, save_frames
from app.services.faiss_search import search_faiss
from app.services.video_vector_store import index, metadata_store, add_all_vectors
import numpy as np


text="birds"
videopath="app/services/animalvideo.mp4"

# text
def final_query_embedding(text):
    cleaned_text=clean_text(text)
    query_embedding=get_text_embedding(cleaned_text)

    query_embedding = query_embedding / np.linalg.norm(query_embedding)
    return query_embedding 


# video

def final_video_processed(text, video_path):
  index.reset()
  metadata_store.clear()
  query_embedding=final_query_embedding(text)
  frames, timestamps, fps, duration = extract_frames(video_path, every_n_seconds=2)
  save_frames(frames, timestamps, "output_frames")

# frame_embedding=get_frame_embedding(frames)
  clip_embeddings=get_video_clip_embeddings(frames, timestamps)

  add_all_vectors(clip_embeddings)

  result=search_faiss(query_embedding, index, metadata_store, k=5)
  return result  

# results=final_video_processed(text, videopath)
# print(results)


