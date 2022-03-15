from threading import Thread
import logging

import time, random
import settings
from settings import resource_lock, shared_resource, max_resource_size


class Worker(Thread):
    def __init__(self):
        logging.info("worker thread starting")
        Thread.__init__(self)

    def cleanup(self):
        try: 
            if resource_lock.locked():
                resource_lock.release()   # just in case 
        finally:
            pass
    def run(self):
        logging.info("running producer thread...")
        try:
            while True:
                resource_lock.acquire()
                if len(shared_resource) > 0:
                    msg = shared_resource.pop(0)
                    logging.info("consuming message: " + msg)
                    resource_lock.release()
                else:
                    resource_lock.release()
                    logging.info("resource is empty. will sleep and wait")
                    logging.info("worker sleeping...")
                    time.sleep(10 + random.random()*3)
        except Exception as e:
            logging.info("worker caught exception: " + str(e))
        finally: 
            self.cleanup()

