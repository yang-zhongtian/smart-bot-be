import builtins
from contextlib import contextmanager

import cv2
import insightface
import numpy as np
from django.conf import settings
from insightface.app.common import Face


@contextmanager
def suppress_print():
    original_print = builtins.print
    builtins.print = lambda *args, **kwargs: None
    try:
        yield
    finally:
        builtins.print = original_print


class FaceLib:
    def __init__(self):
        with suppress_print():
            self.model = insightface.app.FaceAnalysis(root=str(settings.INSIGHTFACE_MODEL))
            self.model.prepare(ctx_id=-1)

    @staticmethod
    def load_from_file(face_image):
        if not face_image:
            return None
        raw = np.frombuffer(face_image, dtype=np.uint8)
        img = cv2.imdecode(raw, cv2.IMREAD_COLOR)
        return img

    def detect(self, image: np.ndarray) -> list[Face]:
        faces = self.model.get(image)
        return faces

    @staticmethod
    def normalize(embedding: np.array) -> np.array:
        norm = np.linalg.norm(embedding)
        return embedding / norm if norm != 0 else embedding
