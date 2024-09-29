from uuid import UUID

import chromadb
import numpy as np
from django.conf import settings

_chromadb_client = None

_face_collection = 'face_embeddings'


def get_chroma_client():
    global _chromadb_client
    if _chromadb_client is None:
        _chromadb_client = chromadb.PersistentClient(path=str(settings.CHROMA_DB))
    return _chromadb_client


def delete_face(face_uuid: UUID):
    chroma_client = get_chroma_client()
    collection = chroma_client.get_collection(_face_collection)
    collection.delete([str(face_uuid)])


def get_face(face_uuid: UUID):
    chroma_client = get_chroma_client()
    collection = chroma_client.get_collection(_face_collection)
    return collection.get(str(face_uuid))


def save_face(face_uuid: UUID, embedding: list[float]):
    chroma_client = get_chroma_client()
    collection = chroma_client.get_collection(_face_collection)
    collection.add(str(face_uuid), embedding)


def search_face(embedding: list[float], threshold: float):
    chroma_client = get_chroma_client()
    collection = chroma_client.get_collection(_face_collection)
    results = collection.query(
        query_embeddings=[embedding],
        n_results=10,
    )

    distances = results['distances'][0]
    ids = results['ids'][0]

    if not ids or not distances:
        return None

    best_match_index = np.argmin(distances)
    best_match_distance = distances[best_match_index]
    best_match_id = ids[best_match_index]

    confidence = max(0.0, 1 - best_match_distance / 2)

    if confidence > threshold:
        return best_match_id
    else:
        return None
