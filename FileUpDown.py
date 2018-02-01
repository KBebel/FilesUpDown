import ftplib
import json

FTP_CRED = False


class Connection:
    """connectig functions"""

    bool_connected_with_ftp = False
    FTP = None

    def __init__(self, host, user, password):
        self.host = host
        self.user = user
        self.password = password

    def connect_with_ftp(self):
        try:
            global FTP
            print('Connecting with {0} ..'.format(self.host), end='')
            FTP = ftplib.FTP(self.host, timeout=10)
            print('.Logging in..', end='')
            FTP.login(user=self.user, passwd=self.password)
            self.bool_connected_with_ftp = True
            print('.Connected.')
        except ftplib.all_errors as e:
            print(str(e))

    def disconnect_with_ftp(self):
        self.check_if_connected()
        if self.bool_connected_with_ftp:
            print('\nClosing connection with {0}..'.format(self.host), end='')
            FTP.close()
            print('.Connection closed.')
            self.bool_connected_with_ftp = False

    def check_if_connected(self):
        if self.bool_connected_with_ftp:
            try:
                FTP.voidcmd('NOOP')
            except Exception as e:
                print("not connected with {}".format(str(self.host)))
                self.bool_connected_with_ftp = False
        else:
            print("not connected with {}".format(str(self.host)))


def read_credencials():
    global FTP_CRED
    FTP_CRED = False
    try:
        with open('Cred/NeltonFTP.json', 'r') as f:
            try:
                data = json.load(f)
                FTP_CRED = True
                print("Rading Credentials")
                return(data)
            except Exception as e:
                print("Error: {}".format(e))

            # NeltonHostName = data['NeltonHostName']
            # NeltonUserName = data['NeltonUserName']
            # NeltonPassword = data['NeltonPassword']
            # # To be changed
            # MWCatiaHostName = data['NeltonHostName']
            # MWCatiaUserName = data['NeltonHostName']
            # MWCatiaPassword = data['NeltonHostName']

    except EnvironmentError as e:
        print("Error: {}\n\tFile with Credentials not Found".format(e))


CredentialsDic = read_credencials()

if FTP_CRED:
    NeltonFTP = Connection(CredentialsDic['NeltonHostName'],
                           CredentialsDic['NeltonUserName'],
                           CredentialsDic['NeltonPassword'])

    NeltonFTP.connect_with_ftp()

    NeltonFTP.disconnect_with_ftp()

