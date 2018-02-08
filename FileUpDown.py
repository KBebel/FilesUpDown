import connection
import readcred
import patoolib
import os
import encodings
import sys
import codecs

print(sys.stdin.encoding)


Cred = readcred.ReadCredentials()
CredentialsDic = Cred.read_credencials()

if Cred.FTP_CRED:
    NeltonFTP = connection.Connection(host=CredentialsDic['NeltonHostName'],
                                      user=CredentialsDic['NeltonUserName'],
                                      passwd=CredentialsDic['NeltonPassword'])

    NeltonFTP.connect_with_ftp()

    NeltonFTP.cwd('MWM_VPN/test/')

    folder_dir = []
    files_list_dict = []
    NeltonFTP.list_files('withatt', folder_dir.append)

    if len(folder_dir) > 1:
        del folder_dir[0]
        for line in folder_dir:
            temp = line.split()
            if temp[1] == '1':
                files_list_dict.append({'Att': temp[0],
                                        'Owner': temp[2],
                                        'Group': temp[3],
                                        'Size': temp[4],
                                        'Date': temp[5:8],
                                        'Name': temp[8]})


    print(files_list_dict[0]['Name'])
    print(NeltonFTP.size(files_list_dict[1]['Name']))
    NeltonFTP.get(files_list_dict[1]['Name'])


    # for entry in files_list_dict:
    #     print('{0}\t{1}'.format(entry['Name'], entry['Att']))
    #     if entry['Att'] == '-rw-r-----':
    #         NeltonFTP.change_att(entry['Name'], '664')



    NeltonFTP.disconnect_with_ftp()
