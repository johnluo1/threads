import logging
import threading

# worker/producer configuration
number_of_workers     = 5
number_of_producers   = 3
sleep_time            = 10

# resource
resource_lock         = threading.Lock()
shared_resource       = []
max_resource_size      = 10

# logging
logging.basicConfig(level=logging.DEBUG, 
        filename='output.log',
        format='%(asctime)s - %(name)s - %(levelname)s - %(threadName)s - %(thread)s:  %(message)s')

