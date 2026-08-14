"""
Model Manager - Singleton pattern for shared AI models across cameras
This ensures only one copy of each model is loaded in memory and shared across all cameras.
"""
import threading
from typing import Optional
import torch
import pickle
from pathlib import Path
from ultralytics import YOLO

from src.ai_models.detector import PersonDetector
from src.ai_models.tracker import RestaurantTracker
from src.core.classifiers import PoseLSTM


class ModelManager:
    """
    Singleton manager for AI models.
    Loads models once and shares them across all camera processes.
    Thread-safe for concurrent access.
    """
    _instance = None
    _lock = threading.Lock()
    
    def __new__(cls):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
                    cls._instance._initialized = False
        return cls._instance
    
    def __init__(self):
        if self._initialized:
            return
            
        self._lock = threading.Lock()
        self._detector: Optional[PersonDetector] = None
        self._tracker: Optional[RestaurantTracker] = None
        self._action_model: Optional[PoseLSTM] = None
        self._label_encoder = None
        self._project_dir = Path.cwd()
        
        self._initialized = True
    
    def load_detector(
        self,
        model_name: str,
        conf_threshold: float,
        imgsz: int,
        min_box_width: int,
        min_box_height: int,
        device: str
    ) -> PersonDetector:
        """Load or get cached YOLO detector (thread-safe)."""
        with self._lock:
            if self._detector is None:
                print(f"[ModelManager] Loading YOLO detector: {model_name}")
                self._detector = PersonDetector(
                    model_name=model_name,
                    conf_threshold=conf_threshold,
                    imgsz=imgsz,
                    min_box_width=min_box_width,
                    min_box_height=min_box_height,
                    device=device
                )
                print(f"[ModelManager] YOLO detector loaded successfully")
            return self._detector
    
    def load_tracker(
        self,
        max_age: int,
        n_init: int,
        nms_max_overlap: float
    ) -> RestaurantTracker:
        """Load or get cached tracker (thread-safe)."""
        with self._lock:
            if self._tracker is None:
                print(f"[ModelManager] Loading DeepSORT tracker")
                self._tracker = RestaurantTracker(
                    max_age=max_age,
                    n_init=n_init,
                    nms_max_overlap=nms_max_overlap
                )
                print(f"[ModelManager] DeepSORT tracker loaded successfully")
            return self._tracker
    
    def load_action_model(
        self,
        model_path: str,
        le_path: str,
        device: str
    ) -> tuple[PoseLSTM, object]:
        """Load or get cached PoseLSTM model and label encoder (thread-safe)."""
        with self._lock:
            if self._action_model is None:
                print(f"[ModelManager] Loading PoseLSTM action model: {model_path}")
                self._action_model = PoseLSTM()
                state_dict = torch.load(model_path, map_location=device)
                self._action_model.load_state_dict(state_dict)
                self._action_model.eval()
                
                if device == "cuda":
                    self._action_model = self._action_model.cuda()
                
                with open(le_path, "rb") as f:
                    self._label_encoder = pickle.load(f)
                
                print(f"[ModelManager] PoseLSTM model loaded successfully")
            return self._action_model, self._label_encoder
    
    def get_detector(self) -> Optional[PersonDetector]:
        """Get the cached detector."""
        return self._detector
    
    def get_tracker(self) -> Optional[RestaurantTracker]:
        """Get the cached tracker."""
        return self._tracker
    
    def get_action_model(self) -> Optional[tuple[PoseLSTM, object]]:
        """Get the cached action model and label encoder."""
        if self._action_model is not None:
            return self._action_model, self._label_encoder
        return None
    
    def is_loaded(self) -> bool:
        """Check if all models are loaded."""
        return all([
            self._detector is not None,
            self._tracker is not None,
            self._action_model is not None
        ])


# Global singleton instance
_model_manager = ModelManager()


def get_model_manager() -> ModelManager:
    """Get the global ModelManager singleton instance."""
    return _model_manager