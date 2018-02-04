import connection
import readcred

Cred = readcred.ReadCredentials()
CredentialsDic = Cred.read_credencials()

if Cred.FTP_CRED:
    NeltonFTP = connection.Connection(host=CredentialsDic['NeltonHostName'],
                                      user=CredentialsDic['NeltonUserName'],
                                      passwd=CredentialsDic['NeltonPassword'])

    NeltonFTP.connect_with_ftp()
    print(NeltonFTP.list_files())
    NeltonFTP.cwd('_Jan')
    print(NeltonFTP.list_files())
    NeltonFTP.disconnect_with_ftp()
