import os
import logging

import time


class Logger():
    ##########################################################
    ## Logging Initialization
    ##########################################################
    timestamp = time.strftime("%m%d%Y")
    logdir = '/tmp/indeedSearch/'
    logfile = logdir + "indeed_job_search_" + timestamp + ".log"
    dict_of_jobs_by_state = dict()

    # debug = False
    # debug = True

    if not os.path.exists(logdir):
        os.makedirs(logdir)

    log = logging.getLogger('indeed_anaysis')
    log.setLevel(logging.DEBUG)
    fileHandle = logging.FileHandler(logfile)
    fileHandle.setLevel(logging.DEBUG)
    fileHandle.setFormatter(
        logging.Formatter('%(asctime)s - %(name)s - (%(threadName)-10s) - %(levelname)s - %(message)s'))
    # fileHandle.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
    log.addHandler(fileHandle)

    def __init__(self):
        pass

    @staticmethod
    def debug(self, msg):
        self.log.debug(msg)

    def consoleTrace(self, msg):
        print msg
