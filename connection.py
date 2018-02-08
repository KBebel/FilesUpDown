import ftplib
import inspect
import progressbar
import encodings

class Connection(ftplib.FTP):
    """connectig functions
    I've tried to inherit from FTP and adding/modifing my own functions
    but no success. Got 2 separate connections. So I've added/overwritten
    useful for me functions
    - in init without self.host, user, passwd but with super ERROR:
        AttributeError: 'Connection' object has no attribute 'user'"""

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
                EFTP = ftplib.FTP_TLS(self.host, timeout=10)
                print('.Logging in..', end='')
                EFTP.login(self.user, self.passwd)
                self.bool_connected_with_ftp = True
                print('.Connected.')
                EFTP.encoding='utf-8'
                EFTP.sendcmd('OPTS UTF8 ON')

            except ftplib.all_errors as e:
                print(str(e))

    def disconnect_with_ftp(self):
        if self.is_connected(inspect.stack()[0][3]):
            print('\nClosing connection with {0}..'.format(self.host), end='')
            EFTP.close()
            print('.Connection closed.')
            self.bool_connected_with_ftp = False

    def is_connected(self, name=''):
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

    def list_files(self, withatt="withoutatt", callback='None'):
        if self.is_connected(inspect.stack()[0][3]):
            if withatt.lower() == 'withatt':
                return EFTP.retrlines('LIST', callback)
            else:
                return EFTP.nlst()

    def allowed_commands():
        # return tuple of allowed commands
        pass

    def sendcmd(self, cmd='NOOP', type='None'):
        # Commands Home.pl:
        # ABOR    ACCT*   ADAT*   ALLO    APPE    AUTH    CCC *   CDUP
        # CONF*   CWD     DELE    ENC *   EPRT    EPSV    FEAT    HELP
        # LIST    MDTM    MFF     MFMT    MIC *   MKD     MLSD    MLST
        # MODE    NLST    NOOP    OPTS    PASS    PASV    PBSZ    PORT
        # PROT    PWD     QUIT    REIN*   REST    RETR    RMD     RNFR
        # RNTO    SITE    SIZE    SMNT*   STAT*   STOR    STOU*   STRU
        # SYST    TYPE    USER    XCUP    XCWD    XMKD    XPWD    XRMD
        # ftp.retrlines('LIST')!!!!
        self.cmnd = cmd
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

    def check_att(self, filename):
        pass

    def cwd(self, directory):
        # EFTP.voidcmd('CWD ' + directory)
        EFTP.cwd(directory)

    def mlsd(self, path="", facts=[]):
        EFTP.mlsd(path="", facts=[])

    def retrlines(self, cmd, callback = None):
        EFTP.retrlines(cmd, callback = None)

    def get(self, filename, delete='no'):

        # gfile = open(filename, "wb")
        filesize = self.size(filename)
        progress = progressbar.AnimatedProgressBar(end=filesize, width=50)
        with open(filename, 'wb') as f:
            def callback(chunk):
                f.write(chunk)
                progress + len(chunk)
                progress.show_progress()

            EFTP.retrbinary('RETR ' + filename, callback, 1024)
        # gfile.close()



        if delete.lower() == 'delete':
            EFTP.delete(filename)

    def size(self, filename):
        return EFTP.size(filename)




