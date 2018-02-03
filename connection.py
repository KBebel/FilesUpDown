import ftplib
import inspect


class Connection:
    """connectig functions"""

    bool_connected_with_ftp = False
    FTP = None

    def __init__(self, host, user, password):
        self.host = host
        self.user = user
        self.password = password

    def connect_with_ftp(self):
        if not self.bool_connected_with_ftp:
            try:
                global FTP
                print('Connecting with {0} ..'.format(self.host), end='')
                FTP = ftplib.FTP_TLS(self.host, timeout=10)
                print('.Logging in..', end='')
                FTP.login(user=self.user, passwd=self.password)
                self.bool_connected_with_ftp = True
                print('.Connected.')
            except ftplib.all_errors as e:
                print(str(e))

    def disconnect_with_ftp(self):
        if self.is_connected(inspect.stack()[0][3]):
            print('\nClosing connection with {0}..'.format(self.host), end='')
            FTP.close()
            print('.Connection closed.')
            self.bool_connected_with_ftp = False

    def is_connected(self, name='no name'):
        if self.bool_connected_with_ftp:
            try:
                FTP.voidcmd('NOOP')
                return True
            except Exception as e:
                print("function: \"{0}\" can\'t run: \n\tnot connected with {1}".format(
                    name, str(self.host)))
                self.bool_connected_with_ftp = False
        else:
            print("function: \"{0}\" can\'t run: \n\tnot connected with {1}"
                  .format(name, str(self.host)))

    def list_files(self, list):
        if self.is_connected(inspect.stack()[0][3]):
            # files = FTP.nlst()
            files = FTP.retrlines('LIST', list.append)
            return files

    def send_command(self, command='NOOP', type = 'None'):
        # Commands Home.pl:
        # ABOR    ACCT*   ADAT*   ALLO    APPE    AUTH    CCC *   CDUP
        # CONF*   CWD     DELE    ENC *   EPRT    EPSV    FEAT    HELP
        # LIST    MDTM    MFF     MFMT    MIC *   MKD     MLSD    MLST
        # MODE    NLST    NOOP    OPTS    PASS    PASV    PBSZ    PORT
        # PROT    PWD     QUIT    REIN*   REST    RETR    RMD     RNFR
        # RNTO    SITE    SIZE    SMNT*   STAT*   STOR    STOU*   STRU
        # SYST    TYPE    USER    XCUP    XCWD    XMKD    XPWD    XRMD
        # ftp.retrlines('LIST')!!!!
        self.cmnd = command
        self.type = type
        if self.is_connected(inspect.stack()[0][3]):
            try:
                print('Sending {}'.format(self.cmnd))
                if self.type.upper() == 'ASCI':
                    FTP.retrlines(self.cmnd)
                else:
                    return FTP.sendcmd(self.cmnd)
            except Exception as e:
                print('Error when sending {0}\n\t{1}'
                  .format(str(self.cmnd).upper(), e))

    def change_att(self, filename, att='666'):
        if self.is_connected(inspect.stack()[0][3]):
            try:
                print('Changing {} to {}'.format(filename, att))
                FTP.voidcmd('SITE chmod {} {}'.format(att, filename))
            except ftplib.error_reply as e:
                print('Error: "{3}"\n\twhen changing {0} to {1}'
                      .format(str(att), str(filename, e)))
            except Exception as e:
                print('Error: "{3}"\n\twhen changing {0} to {1}'
                      .format(str(att), str(filename, e)))
