# node1.py
import grpc
import storage_pb2
import storage_pb2_grpc
from concurrent import futures
import threading

class KeyValueStoreServicer(storage_pb2_grpc.KeyValueStoreServicer):
    def __init__(self):
        self.data = {}
        self.stub_node2 = None
        self.stub_node3 = None
        self.locks = {}  # 用于存储键值对的锁

    def Put(self, request, context):
        with self.get_lock(request.key):
            self.data[request.key] = request.value
        self.sync_data()
        return storage_pb2.Response(value=f"Key {request.key} set Value {request.value} successfully in Node 1")

    def Get(self, request, context):
        value = self.data.get(request.key, "")
        return storage_pb2.Response(value=value)

    def Delete(self, request, context):
        with self.get_lock(request.key):
            if request.key in self.data:
                del self.data[request.key]
                self.sync_data()
                return storage_pb2.Response(value=f"Key {request.key} deleted successfully in Node 1")
            else:
                return storage_pb2.Response(value=f"Key {request.key} not found in Node 1")

    def Set(self, request, context):
        with self.get_lock(request.key):
            self.data = {request.key: request.value}
            self.sync_data()
        return storage_pb2.Response(value=f"Data set successfully in Node 1")

    def SyncData(self, request, context):
        with self.get_lock(request.source_node):
            self.data.update(request.data)
        return storage_pb2.SyncResponse(message="Data synchronized successfully in Node 1")

    def sync_data(self):
        if self.stub_node2:
            sync_request = storage_pb2.SyncRequest(data=self.data, source_node="Node1")
            response = self.stub_node2.SyncData(sync_request)
            print(response.message)
        if self.stub_node3:
            sync_request = storage_pb2.SyncRequest(data=self.data, source_node="Node1")
            response = self.stub_node3.SyncData(sync_request)
            print(response.message)

    def get_lock(self, key):
        if key not in self.locks:
            self.locks[key] = threading.Lock()
        return self.locks[key]

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    kv_servicer = KeyValueStoreServicer()
    storage_pb2_grpc.add_KeyValueStoreServicer_to_server(kv_servicer, server)
    server.add_insecure_port("[::]:50051")
    server.start()

    # Connect to Node 2
    with grpc.insecure_channel("localhost:50052") as channel2,grpc.insecure_channel("localhost:50053") as channel3:
        kv_servicer.stub_node2 = storage_pb2_grpc.KeyValueStoreStub(channel2)
        kv_servicer.stub_node3 = storage_pb2_grpc.KeyValueStoreStub(channel3)
        try:
            server.wait_for_termination()
        except KeyboardInterrupt:
            pass

if __name__ == "__main__":
    serve()
