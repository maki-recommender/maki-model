import os
import logging
from typing import List
import time

import numpy as np
import scipy.sparse as sps

from . import Model

class EASE(Model):
    """
    EASE implementation with parameter threshold to reduce used space at cost of a bit of performance
    
    User ids and item ids are assumed to be compact and without any missing values between them
    """

    def __init__(self) -> None:
        self.b = None
        self.num_items = 0

    def fit(self, urm: sps.coo_matrix, alpha: float = 100, threshold: float = 0.01):
        """Fit the model to the given implicit urm"""
        
        try:
            urm = urm.tocsr()

            logging.info("Started training on urm  with shape: %s", urm.shape)

            # implemented with closed form solution like in the original paper

            G = urm.T * urm 
            diag = np.diag_indices(G.shape[0])
            G[diag] += alpha

            logging.debug("G shape: %s", G.shape)

            P = np.linalg.inv(G.todense())
            B = P / -np.diag(P)
            B[diag] = 0

            # compress data as much as possible for performance and memory usage
            B = sps.coo_matrix(B)

            under = np.logical_or(B.data <= -threshold, B.data >= threshold)
            B.data = np.multiply(B.data, under)

            B.eliminate_zeros()

            self.b = B.tocsr()

            # keep number of known items saved
            self.num_items = urm.shape[1]

            logging.info("Training complete")
            logging.debug("B: Expected memory size %sMB", B.shape[0] * B.shape[1] * 4 /1e6)
            logging.debug("URM: Expected memory size %sMB",(urm.shape[0] + urm.shape[1] + urm.nnz) * 4 /1e6)

        except Exception as e:
            logging.exception(e, stack_info=True)
        
    def recommend(self, seen_items: List[int], at: int = -1):
        """Get recommender items for the user ad a list of ids and an array of scores
        """
        start_t = time.perf_counter()
        # if list is empty use a random anime as a starting point
        if seen_items is None:
            seen_items = [1]
        
        # keep valid ids and convert to onehot
        seen_items = np.asarray(seen_items)
        seen_items = seen_items[seen_items < self.num_items]
        seen_items = self.as_item_array(seen_items)

        scores = np.squeeze(seen_items * self.b)
            
        scores[seen_items != 0] = -np.inf

        if at == -1 or at == 0:
            at = len(scores) - len(seen_items)
        else:
            at = min(at, len(scores)- len(seen_items)) # crop at valid items


        top_items = np.flip(np.argsort(scores)[-at:])
        top_scores = np.nan_to_num(np.array(scores[top_items]))
        top_scores = np.clip(top_scores, -1e3 , 1e3)

        delta = time.perf_counter() - start_t
        logging.info("Generated %d recommendations in %fms", len(scores), round(delta * 1000, 2))

        return top_items.tolist(), (top_scores / (np.max(top_scores)+1e-6)).tolist()


    def save(self, folder_path: str):
        """Save current model to disk"""
        os.makedirs(folder_path, exist_ok=True)
        # save to a temporaty file, in case of failure either this new file or the
        # older ones are briked
        temp_fpath = os.path.join(folder_path, "ease_b_temp.npz")
        fpath = os.path.join(folder_path, "ease_b.npz")
        sps.save_npz(temp_fpath, self.b)
        os.renames(temp_fpath, fpath)
        logging.info("Model saved to disk")



    def load(self, folder_path: str):
        """Load model from disk"""
        self.b = sps.load_npz(os.path.join(folder_path, "ease_b.npz"))
        self.num_items = self.b.shape[0]
        logging.info("Model loaded from disk")
    

    def item_count(self):
        """Return number of items kwno by the system"""
        return self.num_items

    @staticmethod
    def make_coo(user_col, item_col, score_col, shape=None):
        """Make a coo matrix from passed data"""
        coo = sps.coo_matrix(
                (
                    score_col,
                    (user_col, item_col)
                ),
                shape=shape
            )
        return coo
    
    def train_implicit(self, user_ids, anime_ids):
        scores = [1] * len(user_ids)
        urm = EASE.make_coo(user_ids, anime_ids, scores)
        self.fit(urm)