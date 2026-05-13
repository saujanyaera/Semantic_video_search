import numpy as np

def search_faiss(query_embedding, index, metadata_store, k=5):
 
    query_vector = np.array(query_embedding, dtype="float32")
    query_vector = np.expand_dims(query_vector, axis=0)

    distances, indices = index.search(query_vector, k)

    results = []

    for i in range(len(indices[0])):

        idx = int(indices[0][i])

        if idx < 0:
            continue

        meta = metadata_store[idx]

        results.append({
            "clip_id": meta["clip_id"],
            "start_time": meta["start_time"],
            "end_time": meta["end_time"],
            "score": float(distances[0][i])
        })

    # AFTER loop finishes
    # best_result = max(results, key=lambda x: x["score"])

    return results