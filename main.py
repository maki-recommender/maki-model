import logging
from typing import List
from concurrent import futures

import grpc

from utils import env_var
from models import EASE
from recommendations import RecommendationService
from proto.recommend_service_pb2_grpc import add_RecommendationServiceServicer_to_server

logging.basicConfig(level=logging.DEBUG, format="[%(asctime)s] %(levelname)s - %(module)s@%(funcName)s: %(message)s")

HOST = env_var("MAKI_ModelHost", "[::]:50051")
NUM_WORKERS = int(env_var("MAKI_ModelWorkers", 10))
PERSIST_PATH = env_var("MAKI_PersistentPath", "data/")

anime_model = EASE()

# TODO: lock-free periodic model reload from disk


##################################################################################
# startup setup
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
server.wait_for_termination()