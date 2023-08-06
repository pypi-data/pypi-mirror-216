import ctypes
import threading

from loguru import logger


class TerminableThread(threading.Thread):
    """a thread that can be stopped by forcing an exception in the execution context"""

    def terminate(self, exception_cls, repeat_sec=2.0):
        if self.is_alive() is False:
            return True
        killer = ThreadKiller(self, exception_cls, repeat_sec=repeat_sec)
        killer.start()


class ThreadKiller(threading.Thread):
    """separate thread to kill TerminableThread"""

    def __init__(self, target_thread, exception_cls, repeat_sec=2.0):
        threading.Thread.__init__(self)
        self.target_thread = target_thread
        self.exception_cls = exception_cls
        self.repeat_sec = repeat_sec
        self.daemon = True

    def run(self):
        """loop raising exception incase it's caught hopefully this breaks us far out"""
        while self.target_thread.is_alive():
            ctypes.pythonapi.PyThreadState_SetAsyncExc(ctypes.c_long(self.target_thread.ident),
                                                       ctypes.py_object(self.exception_cls))
            self.target_thread.join(self.repeat_sec)


class StopRunningCommand(Exception):
    pass


class JobManager:

    def __init__(self, semaphore=2):
        """
        :param semaphore: 并行度
        """
        self.job_store = {}
        self.job_lock = threading.RLock()
        self.semaphore = threading.Semaphore(semaphore)

    def add_job(self, job_id, target, *args, **kwargs):

        def inner_job(*args, **kwargs):
            try:
                self.semaphore.acquire()
                ret = target(*args, **kwargs)
                print(f"{job_id} is finished.")
                return ret
            except StopRunningCommand as e:
                print(f"{job_id} has been stopped.")
            except Exception as e:
                print(f"{job_id} is finished.")
                raise e
            finally:
                if job_id in self.job_store:
                    self.job_store.pop(job_id)
                self.semaphore.release()

        with self.job_lock:
            t = TerminableThread(target=inner_job, *args, **kwargs)
            t.daemon = True
            # if job_id in self.job:
            #     self.job[job_id].terminate(StopRunningCommand)
            self.job_store[job_id] = t
        return self.job_store[job_id]

    def remove_job(self, job_id):
        with self.job_lock:
            if job_id in self.job_store:
                self.job_store[job_id].terminate(StopRunningCommand)

    def start_job(self):
        with self.job_lock:
            for j, t in self.job_store.items():
                if t.is_alive() is False:
                    t.start()

    def print_current_job(self):
        info = {jid: t.is_alive() for jid, t in self.job_store.items()}
        logger.info(info)
