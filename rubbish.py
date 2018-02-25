class jakas():
    def __init__(self):
        self.FTP_CRED = False

    def zmien(self):
        self.FTP_CRED = True


j = jakas()
print(j.FTP_CRED)
j.zmien()
print(j.FTP_CRED)
