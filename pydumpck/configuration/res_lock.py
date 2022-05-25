import threading
import os
global_lock = threading.Lock()


def check_directory(src_path: str):
    if not os.path.exists(src_path):
        global_lock.acquire(True)  # TODO optimize concurrent safty
        if not os.path.exists(src_path):
            os.makedirs(src_path)
        global_lock.release()
