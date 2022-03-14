import logging, time, atexit, signal, os
from threading import Thread

import settings
from Worker import Worker
from Producer import Producer

def run():
    # starting multiple workers/threads
    workers = []
    for i in range(settings.number_of_workers):
        t = Worker()  
        t.start()
        workers.append(t)

    producers = []
    for i in range(settings.number_of_producers):
        t = Producer()  
        t.start()
        producers.append(t)

    # cleanup handler on program exit
    def cleanup():
        for w in workers:
            w.cleanup()
        for w in producers:
            w.cleanup()

    # signal handler
    def signal_handler(signum, frame):
        logging.info("caught signal " + str(signum))
        cleanup()
        os._exit(0)
    atexit.register(cleanup)
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)

    # monitoring all workers, restart them if a worker is not alive
    while True:
        logging.info("main thread monitoring...")
        # monitoring workers. Restart a dead worker if needed
        for i, t in enumerate(workers):
            if not t.isAlive():
                t.cleanup()
                t.join()
                t = Worker()
                t.start()
                workers[i] = t
        # monitoring producers. Restart a dead producer if needed
        for i, t in enumerate(producers):
            if not t.isAlive():
                t.cleanup()
                t.join()
                t = Producer()
                t.start()
                producers[i] = t

        time.sleep(5)

if __name__ == "__main__":
   print("here are are at main")
   logging.info("from main")
   run()
