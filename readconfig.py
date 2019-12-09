from configparser import ConfigParser

class Config(object):
    def __init__(self,confilename):
        cfg = ConfigParser()
        cfg.read(confilename, encoding='utf-8')
        self.baseurl = cfg.get('url', 'base')
        self.loginurl = cfg.get('url', 'login')
        self.mutualurl = cfg.get('url', 'mutualpref') + cfg.get('url', 'mutualid')  # 互填问卷的 自身问卷的ID号

        self.loginusername = cfg.get('user', 'username')
        self.loginpassoword = cfg.get('user', 'password')


if __name__ == '__main__':
    print(Config('my.ini').__dict__)