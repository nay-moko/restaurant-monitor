"""
reid_gallery.py
---------------
Person Re-ID gallery using OSNet-x0.25 for embedding extraction
and faiss for fast CPU similarity search.

Workflow
--------
1. Worker crop arrives from live_pipeline
2. extract_embedding(crop) → 512-dim vector
3. match(embedding) → global_id if similarity > threshold, else None
4. register(embedding) → new global_id stored in gallery
"""

from __future__ import annotations

import uuid
from pathlib import Path

import cv2
import numpy as np
import faiss
import torch
import torchreid


# ---------------------------------------------------------------------------
# Gallery
# ---------------------------------------------------------------------------

class ReIDGallery:
    """
    Stateful gallery of known worker embeddings.

    Parameters
    ----------
    model_name      : OSNet variant — 'osnet_x0_25' is smallest/fastest
    threshold       : cosine similarity threshold to consider a match (0–1)
    device          : 'cpu' always for MX350-constrained inference
    weights_dir     : where to cache downloaded model weights
    """

    EMBEDDING_DIM = 512

    def __init__(
        self,
        model_name : str   = "osnet_x0_25",
        threshold  : float = 0.65,
        device     : str   = "cpu",
        weights_dir: str   = "models/reid",
    ):
        self.threshold   = threshold
        self.device      = device
        self.weights_dir = Path(weights_dir)
        self.weights_dir.mkdir(parents=True, exist_ok=True)

        # -- Load OSNet feature extractor ------------------------------------
        self.extractor = torchreid.utils.FeatureExtractor(
            model_name=model_name,
            model_path=str(self.weights_dir / f"{model_name}.pth"),
            device=device,
        )

        # -- Faiss flat index (cosine via L2 on normalized vectors) ----------
        self.index = faiss.IndexFlatIP(self.EMBEDDING_DIM)  # inner product = cosine when normalized

        # global_id list parallel to faiss index rows
        self._ids: list[str] = []

    # -- Public API ----------------------------------------------------------

    def process(self, track_id: int, crop: np.ndarray) -> str:
        """
        Main entry point called by live_pipeline for every worker crop.
        Returns the global_id (existing match or newly registered).
        """
        embedding = self._extract(crop)
        global_id = self._match(embedding)

        if global_id is None:
            global_id = self._register(embedding)

        return global_id

    # -- Internal ------------------------------------------------------------

    def _extract(self, crop: np.ndarray) -> np.ndarray:
        """Extract L2-normalized 512-dim embedding from a BGR crop."""
        # torchreid expects RGB, resize to 256x128 (standard Re-ID input)
        rgb = cv2.cvtColor(crop, cv2.COLOR_BGR2RGB)
        resized = cv2.resize(rgb, (128, 256))

        embedding = self.extractor([resized])           # returns (1, 512) tensor
        vec = embedding.cpu().numpy().astype(np.float32)
        faiss.normalize_L2(vec)                         # in-place L2 norm → cosine via IP
        return vec                                      # shape (1, 512)

    def _match(self, embedding: np.ndarray) -> str | None:
        """Return global_id of closest gallery entry if above threshold, else None."""
        if self.index.ntotal == 0:
            return None

        similarities, indices = self.index.search(embedding, k=1)
        sim   = float(similarities[0][0])
        idx   = int(indices[0][0])

        if sim >= self.threshold:
            return self._ids[idx]
        return None

    def _register(self, embedding: np.ndarray) -> str:
        """Add new embedding to gallery, return assigned global_id."""
        global_id = f"worker_{uuid.uuid4().hex[:8]}"
        self.index.add(embedding)
        self._ids.append(global_id)
        return global_id

    # -- Persistence ---------------------------------------------------------

    def save(self, path: str = "models/reid/gallery.index") -> None:
        """Persist faiss index + id list to disk."""
        p = Path(path)
        p.parent.mkdir(parents=True, exist_ok=True)
        faiss.write_index(self.index, str(p))
        np.save(str(p.with_suffix(".ids.npy")), np.array(self._ids))

    def load(self, path: str = "models/reid/gallery.index") -> None:
        """Load persisted gallery from disk."""
        p = Path(path)
        if not p.exists():
            return
        self.index = faiss.read_index(str(p))
        self._ids  = np.load(str(p.with_suffix(".ids.npy")), allow_pickle=True).tolist()