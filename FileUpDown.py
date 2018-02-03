import connection
import readcred

Cred = readcred.ReadCredentials()
CredentialsDic = Cred.read_credencials()

if Cred.FTP_CRED:
    NeltonFTP = connection.Connection(CredentialsDic['NeltonHostName'],
                                      CredentialsDic['NeltonUserName'],
                                      CredentialsDic['NeltonPassword'])

    NeltonFTP.disconnect_with_ftp()

    NeltonFTP.connect_with_ftp()

    # ls = []
    # NeltonFTP.list_files(ls)
    # print(ls)

    print(NeltonFTP.send_command('HELP'))


    NeltonFTP.disconnect_with_ftp()
