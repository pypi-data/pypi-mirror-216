from concurrent.futures import ThreadPoolExecutor


class Singleton(type):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]

class ThreadPool(ThreadPoolExecutor,metaclass=Singleton):
    '''单例'''
    def __init__(self,max_workers = 8) -> None:
        super().__init__(max_workers=max_workers)
        
    def set_max_workers(self, max_workers):
        self._max_workers = max_workers
        self._adjust_thread_count()

class ThreadPools(ThreadPoolExecutor):
    '''多例'''
    def __init__(self,max_workers = 8) -> None:
        super().__init__(max_workers=max_workers)