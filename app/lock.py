
import fcntl
import time


# http://blog.vmfarms.com/2011/03/cross-process-locking-and.html
class Lock:

    def __init__(self, filename):
        self.filename = filename
        # This will create it if it does not exist already
        self.handle = open(filename, 'w')

    # Bitwise OR fcntl.LOCK_NB if you need a non-blocking lock
    def acquire(self):
        fcntl.flock(self.handle, fcntl.LOCK_EX)

    def release(self):
        fcntl.flock(self.handle, fcntl.LOCK_UN)

    def __del__(self):
        self.handle.close()


def locked_run(callback, lock_file_name):
    done = False
    while not done:
        try:
            lock = Lock(lock_file_name)
            lock.acquire()
            callback()
            done = True
        except:
            time.sleep(10)
        finally:
            lock.release()
