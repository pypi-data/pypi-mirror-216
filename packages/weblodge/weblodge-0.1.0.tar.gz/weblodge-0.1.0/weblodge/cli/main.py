from weblodge.config import Config
from weblodge.web_app import WebApp


def main():
    c = Config()
    w = WebApp(c)

    if c.action == 'build':
        print('build')
        c.load(w.config()['build'])
        w.build()
    elif c.action == 'deploy':
        print('deploy')
        c.load(w.config()['deploy'])
        print(w.deploy())
