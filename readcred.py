import json


class ReadCredentials:

    FTP_CRED = False

    def read_credencials(self):

        try:
            with open('Cred/NeltonFTP.json', 'r') as f:
                try:
                    data = json.load(f)
                    print("Rading Credentials")
                    self.FTP_CRED = True
                    return(data)
                except Exception as e:
                    print("Error: {}".format(e))
        except EnvironmentError as e:
            print("Error: {}\n\tFile with Credentials not Found".format(e))

