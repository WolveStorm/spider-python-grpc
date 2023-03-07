import json

from model.redis_m import r
from model.mongo import collection
from const.const import kv_game_list,kv_game_detail
from const.const import logger
from proto import game_pb2, game_pb2_grpc

seven_day_time = 60*60*24*7

def exist_key(key):
    try:
        exist = r.exists(key)
        logger.debug(exist)
        return exist
    except Exception as e:
        logger.error(e)
        return 0
def hexist_key(key,field):
    try:
        exist = r.hexists(key,field)
        logger.error(exist)
        return exist
    except Exception as e:
        logger.error(e)
        return 0

def game_list_to_redis():
    try:
        results = collection.find()
        game_list = []
        for result in results:
            del result["_id"]
            game_list.append(result)
        json_str = json.dumps(game_list)
        r.setex(kv_game_list,seven_day_time,json_str)
    except Exception as e:
        logger.error(e)

def find_game_list_redis(page, page_size, keyword):
    try:
        json_str = r.get(kv_game_list)
        l = json.loads(json_str)
        filter_list = []
        d = {}
        for info in l:
            if keyword in info['name']:
                filter_list.append(info)
        d['total'] = len(filter_list)
        game_list = []
        for result in filter_list:
            resp = dict_to_resp(result)
            game_list.append(resp)
        offset = (page - 1) * page_size
        d['list'] = game_list[offset:offset+page_size]
        logger.debug(d)
        return d
    except Exception as e:
        logger.error(e)

# 业务处理
def find_game_detail_redis(game_name):
    try:
        json_str = r.get(kv_game_detail+game_name)
        l = json.loads(json_str)
        rsp = dict_to_resp(l)
        return rsp
    except Exception as e:
        logger.error(e)

def game_detail_to_redis(game_name):
    try:
        result = collection.find_one({'name': game_name})
        del result["_id"]
        json_str = json.dumps(result)
        r.setex(kv_game_detail+game_name,seven_day_time,json_str)
    except Exception as e:
        logger.error(e)



def dict_to_resp(result):
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