from threading import Thread
import logging, random, time

import settings
from settings import resource_lock, shared_resource, max_resource_size

class Producer(Thread):

    def __init__(self):
        logging.info("producer thread starting")
        Thread.__init__(self)
        self.name = "Producer"
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
                if len(shared_resource) < max_resource_size:
                    shared_resource.append("some junk message " + str(random.randrange(10)))
                    logging.info("producing some random junk....")
                else: 
                    logging.info("resource is full. need to wait")
                resource_lock.release()
                logging.info("producer sleeping...")
                time.sleep(3 + random.random()*3)
        except Exception as e:
            logging.info("producer caught exception: " + str(e))
        finally: 
            self.cleanup()
