import ftplib
import inspect


class Connection(ftplib.FTP):
    """connectig functions
    I've tried to inherit from FTP and adding/modifing my own functions
    but no success. Got 2 separate connections. So I've added/overwritten
    useful for me functions"""

    bool_connected_with_ftp = False
    EFTP = None

    def __init__(self, host='', user='', passwd='', acct=''):
        self.ftp = ftplib.FTP(host='', user='', passwd='', acct='')
        self.host = host
        self.user = user
        self.passwd = passwd
        # super().__init__(host='', user='', passwd='', acct='')

    def connect_with_ftp(self):
        if not self.bool_connected_with_ftp:
            try:
                global EFTP
                print('Connecting with {0} ..'.format(self.host), end='')
                EFTP = ftplib.FTP(self.host, timeout=10)
                print('.Logging in..', end='')
                EFTP.login(self.user, self.passwd)
                self.bool_connected_with_ftp = True
                print('.Connected.')
            except ftplib.all_errors as e:
                print(str(e))

    def disconnect_with_ftp(self):
        if self.is_connected(inspect.stack()[0][3]):
            print('\nClosing connection with {0}..'.format(self.host), end='')
            EFTP.close()
            print('.Connection closed.')
            self.bool_connected_with_ftp = False

    def is_connected(self, name='no name'):
        if self.bool_connected_with_ftp:
            try:
                EFTP.voidcmd('NOOP')
                return True
            except Exception as e:
                print("function: \"{0}\" can\'t run: \n\tnot connected with {1}".format(
                    name, str(self.host)))
                self.bool_connected_with_ftp = False
        else:
            print("function: \"{0}\" can\'t run: \n\tnot connected with {1}"
                  .format(name, str(self.host)))

    def list_files(self, withatt="NO"):
        if self.is_connected(inspect.stack()[0][3]):
            if withatt.upper() == 'YES':
                return EFTP.retrlines('LIST')
            else:
                return EFTP.nlst()

    def allowed_commands():
        # return tuple of allowed commands
        pass

    def send_command(self, command='NOOP', type='None'):
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
                    EFTP.retrlines(self.cmnd)
                else:
                    return EFTP.sendcmd(self.cmnd)
            except Exception as e:
                print('Error when sending {0}\n\t{1}'
                      .format(str(self.cmnd).upper(), e))

    def change_att(self, filename, att='666'):
        if self.is_connected(inspect.stack()[0][3]):
            try:
                print('Changing {} to {}'.format(filename, att))
                EFTP.voidcmd('SITE chmod {} {}'.format(att, filename))
            except ftplib.error_reply as e:
                print('Error: "{3}"\n\twhen changing {0} to {1}'
                      .format(str(att), str(filename, e)))
            except Exception as e:
                print('Error: "{3}"\n\twhen changing {0} to {1}'
                      .format(str(att), str(filename, e)))

    def cwd(self, directory):
        EFTP.voidcmd('CWD ' + directory)
