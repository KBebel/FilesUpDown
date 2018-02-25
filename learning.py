import datetime
import time
import threading
import logging
import os
import sys


print('.' * 70 + '\n')
start = datetime.datetime.now()
logg = logging.getLogger(__name__)
logg_full = logging.getLogger(__name__)
if not os.path.isdir('Log'):
    os.makedirs('Log')
log_filename = 'Log/download_.log'
log_full_filename = 'Log/download_full.log'
logging.basicConfig(filename = log_filename, level = logging.INFO)
logging.basicConfig(filename = log_full_filename, level = logging.DEBUG)
# ch = logging.StreamHandler(sys.stdout)
# ch.setLevel(logging.INFO)
# logg.addHandler(ch)

loggin.basicConfig()

class logger():
    def debug(self, logdata):
        logg_full.debug(logdata)

    def info(self, logdata):
        logg.info(logdata)
        logg_full.info(logdata)


logger = logger()

logger.info('This message should go to the log file')

print(logger.debug("Going to do some stuf"))
logger.info('Watch out!')


print(start.strftime("%Y-%m-%d %H:%M:%S (KW%W)"))
logger.info('printed ' + start.strftime("%Y-%m-%d %H:%M:%S (KW%W)"))

t = threading.Thread(target = lambda: time.sleep(5))
# t.setDaemon(True)
t.start()
while t.is_alive():
    t.join(1)
    print('dupa')

end = datetime.datetime.now()
elapsed = end-start
print(end.strftime("%Y-%m-%d %H:%M:%S (KW%W)"))

print('\n{}'.format(elapsed))
