import logging
from typing import List
from concurrent import futures
import argparse
import datetime
import gc
import os
import time

import grpc

from utils import env_var
from models import EASE
from recommendations import RecommendationService
from proto.recommend_service_pb2_grpc import add_RecommendationServiceServicer_to_server

logging.basicConfig(level=logging.DEBUG, format="[%(asctime)s] %(levelname)s - %(module)s@%(funcName)s: %(message)s")

HOST = env_var("MAKI_ModelHost", "[::]:50051")
NUM_WORKERS = int(env_var("MAKI_ModelWorkers", 10))
PERSIST_PATH = env_var("MAKI_PersistentPath", "data/")
RETRAIN_DELAY = int(env_var("MAKI_RetrainEverySeconds", 7 * 24 * 3600))

anime_model = EASE()

##################################################################################
# startup setup

parser = argparse.ArgumentParser()
parser.add_argument('-t', '--trainer', default="false")

args = parser.parse_args()
is_trainer = bool(args.trainer)

is_trainer |= env_var("MAKI_IsRetrainer", "") != ""

print("┌───────────────────────────────────────────────────┐")
print(f"|{'Maki v2.0.0'.center(51)}|")
print(f"|{'(c) 2023 rickycorte'.center(51)}|")
print(f"|{('Trainer Mode: '+ str(is_trainer)).center(51)}|")
print("└───────────────────────────────────────────────────┘")

if is_trainer: 
    try:
        anime_model.load(PERSIST_PATH)
    except Exception as e:
        logging.error("No model could be loaded!")


    # create services
    recommemnd_service = RecommendationService(anime_model)


    logging.info("Starting grpc server...")
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=NUM_WORKERS))

    #add services to the server
    add_RecommendationServiceServicer_to_server(recommemnd_service, server)

    server.add_insecure_port('[::]:50051')
    server.start()
    logging.info("gRPC server running at: %s", HOST)

    # watch for parameter changes
    model_path = os.path.join(PERSIST_PATH, "ease_b.npz")
    file_stamp = os.stat(model_path).st_mtime
    logging.info("Watching for paramters changes...")
    while True:
        stamp = os.stat(model_path).st_mtime
        if stamp != file_stamp:
            file_stamp = stamp
            logging.info("Detected model change")
            temp = EASE()
            temp.load(PERSIST_PATH)
            # swap model, assignment should be atomic in python 
            recommemnd_service._anime_model = temp

        time.sleep(5)
    
    #server.wait_for_termination()
else:
    import trainer

    trainer.set_db_url(env_var("MAKI_PostgresUrl"))

    while True:
        try:
            nxt = datetime.datetime.utcnow()
            nxt += datetime.timedelta(seconds=RETRAIN_DELAY)
            logging.info(f"Next scheduled retrain: {nxt.strftime('%d/%m/%Y %H:%M:%S')}")

            time.sleep(RETRAIN_DELAY)

            trainer.retrain_anime_model(anime_model)

            anime_model.save(PERSIST_PATH)
            
            # cleanup
            anime_model = EASE()
            gc.collect()
        
        except Exception as e:
            logging.error(f"Model retrain failer: {e}", stack_info=True)
    