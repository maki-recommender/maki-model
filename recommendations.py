import grpc
from proto.recommend_service_pb2_grpc import RecommendationServiceServicer
import proto.recommend_service_pb2 as prs
from models import Model

class RecommendationService(RecommendationServiceServicer):

    def __init__(self, anime_model: Model) -> None:
        super().__init__()
        self._anime_model = anime_model

    def GetAnimeRecommendations(self, req: prs.WatchedAnime, ctx: grpc.ServicerContext):
        k = -1
        if req.HasField("k"):
            k = req.k
        
        ids = [i.id for i in req.items]

        recs, scores = self._anime_model.recommend(ids, k)

        res = prs.RecommendedAnime()
        for id, score in zip(recs, scores):
            res.items.append(prs.RecommendedItem(id=id, score=score))

        return res
