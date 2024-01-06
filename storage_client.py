#client.py
from storage_middle import *
import time
cache = Cache()
def test1():
    perform_operation(nodes, "name", "John", "Put",cache)
    perform_operation(nodes, "city", "Shanghai", "Put",cache)
    perform_operation(nodes, "name", "", "Get",cache)

def test2():
    perform_operation(nodes, "name", "xue", "Put",cache)
    perform_operation(nodes, "city", "Beijing", "Put",cache)
    perform_operation(nodes, "city", "", "Get",cache)


if __name__ == "__main__":
    thread = threading.Thread(target=test1)
    thread.start()
    test2()
