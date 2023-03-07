import grpc
import re
from proto import game_pb2, game_pb2_grpc
from model.mongo import collection
from cache.game import exist_key,find_game_list_redis,game_list_to_redis,game_detail_to_redis,find_game_detail_redis,hexist_key
from const.const import kv_game_list,kv_game_detail
from const.const import logger



class GameServicer(game_pb2_grpc.GameServicer):
    def dict_to_resp(self, result):
        resp = game_pb2.GameDetailInfoResp()
        if result['name'] != "" :
            resp.name = result['name']
        if result['avatar'] != "" :
            resp.avatarUrl = result['avatar']
        if result['company'] != "" :
            resp.company = result['company']
        if result['score'] != "" :
            resp.score = result['score']
        if result['download_times'] != "" :
            resp.downloadTimes = result['download_times']
        if result['apk_url'] != "":
            resp.apkUrl = result['apk_url']
        if result['description'] != "":
            resp.desc = result['description']
        return resp

    def GameList(self, request, context):
        try:
            if request.page == 0:
                request.page = 1
            if request.pageSize == 0:
                request.pageSize = 10
            if exist_key(kv_game_list) == 1:
                logger.debug("search in redis")
                result = find_game_list_redis(request.page, request.pageSize, request.keyword)
                if result is not None:
                    return game_pb2.GameListResponse(total=result["total"], list=result["list"])
            else:
                logger.debug("search nothing in redis")
                game_list_to_redis()
            offset = (request.page - 1) * request.pageSize
            results = collection.find()
            if request.keyword != "":
                pattern = f'.*{request.keyword}.*'
                results = collection.find({'name': {'$regex': pattern}})
            game_list = []
            for result in results:
                resp = self.dict_to_resp(result)
                game_list.append(resp)
            total = len(game_list)
            game_list = game_list[offset:request.pageSize]
            rsp = game_pb2.GameListResponse(total=total, list=game_list)
            return rsp
        except Exception as e:
            logger.error(e)
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(e)

    def GameDetail(self, request: game_pb2.GameDetailRequest, context):
        try:
            if exist_key(kv_game_detail + request.gameName):
                logger.debug("search in redis")
                result = find_game_detail_redis(request.gameName)
                if result is not None:
                    return result
            else:
                game_detail_to_redis(request.gameName)
            result = collection.find_one({'name': request.gameName})
            if result is None:
                context.set_code(grpc.StatusCode.INTERNAL)
                context.set_details("search found nothing")
                return
            resp = self.dict_to_resp(result)
            return resp
        except Exception as e:
            logger.error(e)
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(e)
