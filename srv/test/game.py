import grpc
from proto import game_pb2, game_pb2_grpc
from model.mongo import collection

class TestGameServicer:
    def __init__(self, channel):
        self.channel = channel
    def test_game_list(self):
        stub = game_pb2_grpc.GameStub(self.channel)
        # 调用定义的SayHello方法
        rep = stub.GameList(
            game_pb2.GameListFilterRequest(keyword="a")
        )
        return rep
    def test_game_detail(self):
        stub = game_pb2_grpc.GameStub(self.channel)
        # 调用定义的SayHello方法
        rep = stub.GameDetail(
            game_pb2.GameDetailRequest(gameName="a")
        )
        return rep
if __name__ == '__main__':
        channel = grpc.insecure_channel("0.0.0.0:6781")
        test = TestGameServicer(channel=channel)
        # print(test.test_game_list())
        print(test.test_game_detail())
        channel.close()
        # result = collection.find_one({'name': "a"})
        # print(result)