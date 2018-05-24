from hashlib import sha1

def xxx(str):
    sh=sha1()
    sh.update(str.encode('utf-8'))
    return sh.hexdigest()
if __name__=="__main__":
    pwd=xxx(str(12345))
   
    print(pwd)