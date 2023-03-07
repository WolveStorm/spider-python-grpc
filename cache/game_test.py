from model.redis_m import r
from const.const import kv_game_list,kv_game_detail
seven_day_time = 60*60*24*7
from cache.game import exist_key,find_game_list_redis,game_list_to_redis,game_detail_to_redis,find_game_detail_redis,hexist_key

if __name__ == '__main__':
    if exist_key(kv_game_list) == 1:
        result = find_game_list_redis(1, 5, "")
        if result is not None:
            print(result)
    else:
        game_list_to_redis()
