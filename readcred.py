import json
import logging
import sys

logger = logging.getLogger(__name__)
prt = logging.StreamHandler(sys.stdout)
prt.setLevel(logging.INFO)
logger.addHandler(prt)


class ReadCredentials:

    def __init__(self):
        self.FTP_CRED = False

    def read_credencials(self):

        try:
            with open('Cred/NeltonFTP.json', 'r') as f:
                try:
                    data = json.load(f)
                    logger.info("Rading Credentials")
                    self.FTP_CRED = True
                    return(data)
                except Exception as e:
                    logger.error("Error: {}".format(e))
        except EnvironmentError as e:
            logger.error(
                "Error: {}\n\tFile with Credentials not Found".format(e))
