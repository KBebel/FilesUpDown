import connection
import readcred
import rarfile
import os
import sys
import io
import re
import platform
import shutil
import threading
import datetime
import logging
import argparse
unrarpath = os.getcwd() + '\\unrar.exe'
rarfile.UNRAR_TOOL = unrarpath

start = datetime.datetime.now()

logger = logging.getLogger(__name__)
prt = logging.StreamHandler(sys.stdout)
prt.setLevel(logging.INFO)
logger.addHandler(prt)

if not os.path.isdir('Log'):
    os.makedirs('Log')
logfilename = 'Log/FileUpDown{}.log'.format(start.strftime("_KW%W"))
logging.basicConfig(filename=logfilename, level=logging.DEBUG)

parser = argparse.ArgumentParser()
parser.add_argument('-nowait', action='store_true',
    help='program will NOT WAIT at the end until key is pressed')
args = parser.parse_args()

starttime = start.strftime("%Y-%m-%d %H:%M:%S (KW%W)")
logger.info(starttime)
logger.debug(sys.stdin.encoding)

testing_patform = 'AntaresDesktop'

if platform.node() == testing_patform:
    logger.info('\t\tTesting mode on {}. Dummy folders active'
                .format(platform.node()))
    folder_remote_download = '/MWM_VPN/test/Aktualizacje/'
    folder_local_temp = 'c:/DATATRANSFER/temp/'
    folder_thrash = 'c:/DATATRANSFER/$Bin/'
    folder_remote_upload_mod = '/MWM_VPN/test/mod/'
    folder_remote_upload_ses = '/MWM_VPN/test/ses/'
    folder_remote_upload_she = '/MWM_VPN/test/she/'
    folder_remote_upload_def = '/MWM_VPN/test/0000/def/'
else:
    folder_remote_download = '/Aktualizacje/'
    folder_local_temp = 'd:/DATATRANSFER/temp/'
    folder_thrash = 'd:/DATATRANSFER/$Bin/'
    folder_remote_upload_mod = '/cdmw/mod/'
    folder_remote_upload_ses = '/cdmw/ses/'
    folder_remote_upload_she = '/cdmw/she/'
    folder_remote_upload_def = '/cdmw/adm/0000/data/MWA/SHD/define/'

Cred = readcred.ReadCredentials()
CredentialsDic = Cred.read_credencials()
if not CredentialsDic:
    logger.error('Application stopped')
    end = datetime.datetime.now()
    elapsed = end - start
    endtime = end.strftime("%Y-%m-%d %H:%M:%S")
    logger.info(endtime)
    logger.info('Elapsed %s', elapsed)
    logger.info('.' * 72 + '\n')
    sys.exit()

for path in folder_local_temp, folder_thrash:
    if not os.path.isdir(path):
        os.makedirs(path)

os.chdir(folder_local_temp)

if Cred.FTP_CRED:
    NeltonFTP = connection.Connection(
        host=CredentialsDic['NeltonHostName'],
        user=CredentialsDic['NeltonUserName'],
        passwd=CredentialsDic['NeltonPassword'],
        encoding='utf-8')
    if platform.node() == testing_patform:
        CatiaFTP = connection.Connection(
            host=CredentialsDic['NeltonHostName'],
            user=CredentialsDic['NeltonUserName'],
            passwd=CredentialsDic['NeltonPassword'],
            encoding='utf-8')
    else:
        CatiaFTP = connection.Connection(
            host=CredentialsDic['CatiaHostName'],
            user=CredentialsDic['CatiaUserName'],
            passwd=CredentialsDic['CatiaPassword'])

    NeltonFTP.connect_with_ftp()

    # I can't find a way to check error from 'cwd' directly,
    # so I'm checking print out for error instead
    stdout_ = sys.stdout
    sys.stdout = stream = io.StringIO()
    NeltonFTP.cwd(folder_remote_download)
    sys.stdout = stdout_

    if '550' not in stream.getvalue():
        folder_dir = NeltonFTP.list_files()
        rarlist = []

        for file in folder_dir:
            if re.search('\.rar|\.RAR', file):
                rarlist.append(file)

        if len(rarlist) > 0:
            logger.info('\nDownloading from {0} to {1}:'
                        .format(folder_remote_download, folder_local_temp))
            for rar in rarlist:
                logger.info('\n' + rar)
                t = threading.Thread(target=NeltonFTP.get(rar, delete='yes'))
                t.start()
                while t.is_alive():
                    t.join(60)
                    NeltonFTP.voidcmd('NOOP')
    NeltonFTP.disconnect_with_ftp()

rarlist = []
templist = os.listdir()
for file in templist:
    if re.search('\.rar|\.RAR', file):
        rarlist.append(file)

cwd = os.getcwd()
if len(rarlist) > 0:
    logger.info('Extracting files:')
    for rar in rarlist:
        rar = cwd + '\\' + rar
        opened_rar = rarfile.RarFile(rar)
        for f in opened_rar.infolist():
            if f.file_size > 0:
                logger.info(str(f.filename) + '\t' + str(f.file_size))
                opened_rar.extract(f)

for file in rarlist:
    shutil.move(os.path.join(cwd, file), os.path.join(folder_thrash, file))

dirlist = []
templist = os.listdir()
for file in templist:
    if os.path.isdir(file):
        dirlist.append(file)


CatiaFTP.connect_with_ftp()


def uploadfolder(ftp, localpath, remotepath, folder, endtype='\.model',
                 att='664'):
    os.chdir(localpath)
    logger.debug(folder)
    stdout_ = sys.stdout
    sys.stdout = stream = io.StringIO()
    ftp.cwd(remotepath)
    sys.stdout = stdout_

    if '550' not in stream.getvalue():
        logger.info(
            '\n...Uploading files from {0} to {1}'.format(
                os.getcwd(), remotepath))
        remote_folder_dir = []
        files_dict_att = {}
        CatiaFTP.list_files('withatt', remote_folder_dir.append)
        if len(remote_folder_dir) > 0:
            del remote_folder_dir[0]
            for line in remote_folder_dir:
                temp = line.split()
                if temp[1] == '1':
                    files_dict_att[temp[8]] = {'Size': temp[4],
                                               'Date': temp[5:8],
                                               'Att': temp[0],
                                               'Owner': temp[2],
                                               'Group': temp[3]}
        for file in os.listdir():
            if re.search(endtype, file):
                if file in files_dict_att:
                    logger.info(file)
                    try:
                        t = threading.Thread(target=ftp.put(file))
                        t.start()
                        while t.is_alive():
                            t.join(60)
                            ftp.voidcmd('NOOP')
                        logger.info(
                            '\tfile overwritten. Owner:{0}. Att:{1}'
                            .format(files_dict_att[file]['Owner'],
                                    files_dict_att[file]['Att'],))
                    except Exception as e:
                        logger.error('Error: ' + str(e) + '\n')
                else:
                    logger.info(file)
                    try:
                        t = threading.Thread(target=ftp.put(file))
                        t.start()
                        while t.is_alive():
                            t.join(60)
                            ftp.voidcmd('NOOP')
                        ftp.change_att(file, att)
                        logger.info('\tsaved as new. Owner:{0}. Att:{1}'
                                    .format(ftp.user, att))
                    except Exception as e:
                        logger.error('Error: ' + str(e) + '\n')

    elif '550' in stream.getvalue():
        logger.error('\n{}'.format(stream.getvalue()))


cwd = os.getcwd()
logger.info('Folders to be uploaded: \n{}'.format(dirlist))

for folder in dirlist:
    if re.search('M$', folder):
        remotepath = folder_remote_upload_mod + folder
        localpath = os.path.join(cwd, folder)
        uploadfolder(CatiaFTP, localpath, remotepath, folder)

    if re.search('SE$', folder):
        remotepath = folder_remote_upload_ses + folder
        localpath = os.path.join(cwd, folder)
        uploadfolder(CatiaFTP, localpath, remotepath, folder,
                     endtype='\.session')

    if re.search('S$', folder):
        remotepath = folder_remote_upload_she + folder
        localpath = os.path.join(cwd, folder)
        uploadfolder(CatiaFTP, localpath, remotepath, folder,
                     endtype='\.sheet')

    if re.search('_define$', folder):
        ship = re.search('^0...', folder)
        if ship:
            remotepath = folder_remote_upload_def.replace('0000',
                                                          ship.group(0))
            localpath = os.path.join(cwd, folder)
            uploadfolder(CatiaFTP, localpath, remotepath, folder,
                         endtype='\.def', att='666')
        else:
            logger.info('Wrong def folder name:{}'.format(folder))

CatiaFTP.disconnect_with_ftp()

os.chdir(cwd)
for folder in dirlist:
    shutil.rmtree(folder)

end = datetime.datetime.now()
elapsed = end - start
endtime = end.strftime("%Y-%m-%d %H:%M:%S")
logger.info(endtime)
logger.info('Elapsed %s', elapsed)
logger.info('.' * 72 + '\n')

if args.nowait == False:
    input('press Any key...')


# for name in files_dict_att.keys():
#     print(name + ' ' + files_dict_att[name]['Size'] +
#           files_dict_att[name]['Att'])

# print(files_list_dict[0]['Name'])
# print(NeltonFTP.size(files_list_dict[1]['Name']))
# NeltonFTP.get(files_dict_att[1]['Name'], delete='yes')

# for entry in files_list_dict:
#     print('{0}\t{1}'.format(entry['Name'], entry['Att']))
#     if entry['Att'] == '-rw-r-----':
#         NeltonFTP.change_att(entry['Name'], '664')
