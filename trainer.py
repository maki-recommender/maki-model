from typing import List
import psycopg2
from models import Model
import time
import logging

db_url = ""

def set_db_url(url: str):
    global db_url
    db_url = url


def fetch_anime_entries(): 
    start_tm = time.perf_counter()

    conn = psycopg2.connect(db_url)
    cur = conn.cursor()
    cur.execute("SELECT user_id, anime_id FROM anime_list_entries")
    records = cur.fetchall()

    user_ids = []
    anime_ids = []

    for r in records:
        user_ids.append(r[0])
        anime_ids.append(r[1])

    enlapsed = time.perf_counter() - start_tm
    logging.info(f"[{round(enlapsed * 1000 ,2)}ms] Fetched {len(records)} anime list entires for the database")

    cur.close()
    conn.close()

    return user_ids, anime_ids



def retrain_anime_model(model: Model):
    """Retrain the required model with anime list entries stored in the database"""
    user_ids, anime_ids = fetch_anime_entries()

    start_tm = time.perf_counter()
    model.train_implicit(user_ids, anime_ids)

    enlapsed = time.perf_counter() - start_tm
    logging.info(f"[{round(enlapsed * 1000 ,2)}ms] Retrained model")