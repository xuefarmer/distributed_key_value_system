#middle.py
import grpc
import storage_pb2
import storage_pb2_grpc
import threading
import random
from distributed_lock import *
from functools import lru_cache
count = 0  # 添加全局变量 count


class Cache:
    def __init__(self):
        self.cache = {}
        self.cache_status = {}
        self.lock = threading.Lock()

    @lru_cache(maxsize=500)
    def get(self, key):
        with self.lock:
            if key in self.cache_status and self.cache_status[key] == "valid":
                # 如果缓存状态为有效，直接返回缓存值
                print(f"Cache - Get: {self.cache[key]} (from cache)")
                return self.cache[key]
            else:
                # 缓存状态为无效或缓存中不存在，返回None
                return None

    def put(self, key, value):
        with self.lock:
            # 在缓存中更新键值对
            self.cache[key] = value
            # 更新缓存状态
            self.cache_status[key] = "valid"

    def delete(self, key):
        with self.lock:
            # 删除缓存中的键值对
            if key in self.cache:
                del self.cache[key]
            # 更新缓存状态为无效
            self.cache_status[key] = "invalid"

def perform_operation(nodes, key, value, operation_type,cache):
    global count
    identifire = acquire_lock('test', count)
    count += 1

    if identifire:
        # 随机选择一个节点
        stub = random.choice(nodes)
        response = None
        try:
            if operation_type == "Put":
                response = stub.Put(storage_pb2.Request(key=key, value=value, source_node="Client"))
                cache.put(key, value)
                print(f"Response - {operation_type}: {response.value}")
            elif operation_type == "Get":
                cached_value = cache.get(key)
                if cached_value is not None:
                    print(f"Response - {operation_type}: {cached_value} (from cache)")

                # 从节点获取值
                else:
                    response = stub.Get(storage_pb2.Request(key=key))
                    cache.put(key,response.value)
                    print(f"Response - {operation_type}: {response.value}")

            elif operation_type == "Delete":
                response = stub.Delete(storage_pb2.Request(key=key))
                cache.delete(key)
                print(f"Response - {operation_type}: {response.value}")
            # 添加其他操作类型的判断


        except grpc.RpcError as e:
            # 如果节点不可用，选择另一个节点
            print(f"Error executing {operation_type}: {e}")
            nodes.remove(stub)
            if not nodes:
                print("All nodes are unavailable.")
                return
            else:
                print("Choosing another node...")
                stub = random.choice(nodes)
                print(f"Selected node: {stub}")

                # 重新执行操作
                if operation_type == "Put":
                    response = stub.Put(storage_pb2.Request(key=key, value=value, source_node="Client"))
                    cache.put(key, value)
                    print(f"Response - {operation_type}: {response.value}")
                elif operation_type == "Get":
                    cached_value = cache.get(key)
                    if cached_value is not None:
                        print(f"Response - {operation_type}: {cached_value} (from cache)")

                    # 从节点获取值
                    else:
                        response = stub.Get(storage_pb2.Request(key=key))
                        cache.put(key, response.value)
                        print(f"Response - {operation_type}: {response.value}")

                elif operation_type == "Delete":
                    response = stub.Delete(storage_pb2.Request(key=key))
                    cache.delete(key)
                    print(f"Response - {operation_type}: {response.value}")
                # 添加其他操作类型的判断



        res = release_lock('test', identifire)
        print(f'Release status: {res}')
    else:
        print('Failed to acquire Redis distributed lock, another process is using it')



channel1 = grpc.insecure_channel("localhost:50051")
stub1 = storage_pb2_grpc.KeyValueStoreStub(channel1)
channel2 = grpc.insecure_channel("localhost:50052")
stub2 = storage_pb2_grpc.KeyValueStoreStub(channel2)
channel3 = grpc.insecure_channel("localhost:50053")
stub3 = storage_pb2_grpc.KeyValueStoreStub(channel3)
nodes = [stub1, stub2,stub3]