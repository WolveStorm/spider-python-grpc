from proto import game_pb2, game_pb2_grpc
from srv.game import GameServicer

from concurrent import futures
import grpc

# 启动
def start():
    # 1.实例化server
    Thread = futures.ThreadPoolExecutor(max_workers=2)  ## 设置线程池，并发大小
    server = grpc.server(Thread)
    # 2.注册逻辑到server中
    game_pb2_grpc.add_GameServicer_to_server(GameServicer(), server)
    # 3.启动server
    server.add_insecure_port("127.0.0.1:6781")
    server.start()
    server.wait_for_termination()
if __name__ == '__main__':
    start()