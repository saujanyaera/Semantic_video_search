import faiss
import numpy as np

dimension = 512

# Better for CLIP embeddings
index = faiss.IndexFlatIP(dimension)

print("Faiss index created")

metadata_store = []


def add_all_vectors(clip_data):

    global index, metadata_store

    vectors = []

    for clip in clip_data:

        # embedding
        emb = np.array(clip["embedding"], dtype="float32")

        # normalize
        emb = emb / np.linalg.norm(emb)

        # IMPORTANT: INSIDE LOOP
        vectors.append(emb)

        # IMPORTANT: INSIDE LOOP
        metadata_store.append({
            "clip_id": clip["clip_id"],
            "start_time": clip["timestamp"] - 2,
            "end_time": clip["timestamp"] + 2
        })

    # convert to shape (N, 512)
    vectors = np.vstack(vectors).astype("float32")

    print("Shape going into FAISS:", vectors.shape)

    # add all vectors
    index.add(vectors)