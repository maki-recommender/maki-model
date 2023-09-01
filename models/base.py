import numpy as np
from numpy.typing import NDArray
from typing import List

class Model:

    def recommend(self, seen_items: List[int], at: int = 10):
        """Get recommender items for the user ad a list of ids and an array of scores
        """
        raise NotImplementedError


    def as_item_array(self, items: List[int],) -> NDArray:
        """
        Return a numpy array of len: item_count() containing 1's at the index corresponding of 
        the items ids found in items array
        """
        size = self.item_count()

        result = np.zeros(shape=(size, ))

        if len(items) > 0:
            item_ids = np.array(items)
            result[item_ids[item_ids < size]] = 1
            
        return result
    
    def item_count(self) -> int:
        """Return number of items kwno by the system"""
        raise NotImplementedError
    

    def load(self, folder_path: str):
        """Load model from disk"""
        raise NotImplementedError
    
    def train_implicit(self, user_ids, anime_ids):
        """Train model using inplicit recommendations with 1 as score"""
        raise NotImplementedError