from .base import Model
from typing import List
import logging

import numpy as np
from numpy.typing import NDArray


class DummyModel(Model):


    def recommend(self, seen_items: List[int], at: int = 10):
        """Get recommender items for the user ad a list of ids and an array of scores
        """
        logging.warning("Generated no recommendations with dummy model!")
        return [], []

    
    def item_count(self) -> int:
        """Return number of items kwno by the system"""
        return 0
    

    def load(self, folder_path: str):
        """Load model from disk"""
        pass
    
    def train_implicit(self, user_ids, anime_ids):
        """Train model using implicit recommendations with 1 as score"""
        pass