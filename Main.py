from ftplib import FTP
import ftplib
import json
# import re


class Connection:

    def __init__(self, host, user, password):
        self.host = host
        self.user = user
        self.password = password

    bool_connected_with_ftp = False

    def connect_with_ftp(self):
        try:
            global ftp
            print('Connecting with {0} ..'.format(self.host), end='')
            ftp = FTP(self.host, timeout=10)
            print('.Logging in..', end='')
            ftp.login(user=self.user, passwd=self.password)
            Connection.bool_connected_with_ftp = True
            print('.Connected.')
        except ftplib.all_errors as e:
            print(str(e))

    def disconnect_with_ftp(self):
        print('\nClosing connection with {0}..'.format(self.host), end='')
        try:
            ftp.voidcmd('NOOP')
        except Exception as e:
            print('.Error, not connected! \n\tError: {0}'.format(e))
            Connection.bool_connected_with_ftp = False
        else:
            ftp.close()
            print('.Connection closed.')
            Connection.bool_connected_with_ftp = False

    def send_ftpcommand(self, command='NOOP'):
        # Commands Home.pl:
        # ABOR    ACCT*   ADAT*   ALLO    APPE    AUTH    CCC *   CDUP
        # CONF*   CWD     DELE    ENC *   EPRT    EPSV    FEAT    HELP
        # LIST    MDTM    MFF     MFMT    MIC *   MKD     MLSD    MLST
        # MODE    NLST    NOOP    OPTS    PASS    PASV    PBSZ    PORT
        # PROT    PWD     QUIT    REIN*   REST    RETR    RMD     RNFR
        # RNTO    SITE    SIZE    SMNT*   STAT*   STOR    STOU*   STRU
        # SYST    TYPE    USER    XCUP    XCWD    XMKD    XPWD    XRMD
        # ftp.retrlines('LIST')!!!!
        self.cmnd = command.upper()
        try:
            print('Sending {}'.format(self.cmnd))
            print(ftp.retrlines(self.cmnd))
        except Exception as e:
            print('Error when sending {0}\n\t{1}'
                  .format(str(self.cmnd).upper(), e))

    def list_files():
        files = ftp.nlst()
        return files
        # ftp.retrlines('LIST')

    def change_att(filename, att='666'):

        try:
            print('Changing {} to {}'.format(filename, att))
            msg = ftp.voidcmd('SITE chmod {} {}'.format(att, filename))
            # print(msg)
            print('oh fuck')
        except ftplib.error_reply as e:
            print('Error: "{3}"\n\twhen changing {0} to {1}'
                  .format(str(att), str(filename, e)))
        except Exception as e:
            print('Error: "{3}"\n\twhen changing {0} to {1}'
                  .format(str(att), str(filename, e)))

# All Connection Data should be pass protected eg.(AES)


with open('../Cred/NeltonFTP.json', 'r') as f:
    data = json.load(f)

NeltonHostName = data['NeltonHostName']
NeltonUserName = data['NeltonUserName']
NeltonPassword = data['NeltonPassword']

# To be changed
MWCatiaHostName = data['NeltonHostName']
MWCatiaUserName = data['NeltonHostName']
MWCatiaPassword = data['NeltonHostName']

try:
    ConNelton = Connection(host=NeltonHostName,
                           user=NeltonUserName, password=NeltonPassword)

    ConNelton.connect_with_ftp()

    newList = Connection.list_files()

    Connection.change_att('LFUDS.rar')

    if '0710_SYNCHRO' in newList:
        print('0710_SYNCHRO exist!')

except Exception as e:
    print('Error: "{}"\n'.format(e))
    pass

finally:
    ConNelton.disconnect_with_ftp()
