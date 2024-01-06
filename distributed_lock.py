#distributed_lock.py
import time
import uuid
from multiprocessing import Process
import redis

redis_client = redis.Redis(host='127.0.0.1', port=6379)


# 加锁的过程
def acquire_lock(lock_name, args, acquite_timeout=30, time_out=120):
    identifier = str(uuid.uuid4())
    # 客户端获取锁的结束时间
    end = time.time() + acquite_timeout
    lock_names = "lock_name:" + lock_name
    print(f"进程 {str(args)} end_time:{end}")
    while time.time() < end:
        # setnx(key,value) 只有key不存在情况下，将key的值设置为value 返回True,若key存在则不做任何动作,返回False
        if redis_client.setnx(lock_names, identifier):
            # 设置键的过期时间，过期自动剔除，释放锁
            print('获得锁:进程' + str(args))
            # print(f'分布式锁value:{identifier}')
            redis_client.expire(lock_name, time_out)
            return identifier
        # 当锁未被设置过期时间时，重新设置其过期时间
        elif redis_client.ttl(lock_name) == -1:
            redis_client.expire(lock_name, time_out)
        time.sleep(0.001)
    return False

# 锁的释放
def release_lock(lock_name, identifire):
    lock_names = "lock_name:" + lock_name
    pipe = redis_client.pipeline(True)
    while True:
        try:
            # 通过watch命令监视某个键，当该键未被其他客户端修改值时，事务成功执行。当事务运行过程中，发现该值被其他客户端更新了值，任务失败
            pipe.watch(lock_names)
            if pipe.get(lock_names).decode() == identifire:  # 检查客户端是否仍然持有该锁
                # multi命令用于开启一个事务，它总是返回ok
                # multi执行之后， 客户端可以继续向服务器发送任意多条命令， 这些命令不会立即被执行， 而是被放到一个队列中， 当 EXEC 命令被调用时， 所有队列中的命令才会被执行
                pipe.multi()
                # 删除键，释放锁
                pipe.delete(lock_names)
                # execute命令负责触发并执行事务中的所有命令
                pipe.execute()
                return True
            pipe.unwatch()
            break
        except redis.exceptions.WatchError:
            # # 释放锁期间，有其他客户端改变了键值对，锁释放失败，进行循环
            pass
    return False




