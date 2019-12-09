from configparser import ConfigParser


def initconfig(confilename):
    cfg = ConfigParser()
    cfg.read(confilename)
    configs = {
        'url': {
            'base': cfg.get('url', 'base'),
            'login': cfg.get('url', 'login'),
            'mutualurl': cfg.get('url', 'mutualpref') + cfg.get('url', 'mutualid')
        },
        'username': cfg.get('user', 'username'),
        'password': cfg.get('user', 'password')
    }

if __name__ == '__main__':
    initconfig('my.ini')