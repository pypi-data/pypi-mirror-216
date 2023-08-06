import subprocess
import os

# CAVASS build path, default in installation is ~/cavass-build
if os.path.exists(os.path.expanduser('~/cavass-build')):
    CAVASS_PROFILE_PATH = os.path.expanduser('~/cavass-build')
else:
    CAVASS_PROFILE_PATH = None


def env():
    if CAVASS_PROFILE_PATH is not None:
        PATH = f'{os.environ["PATH"]}:{os.path.expanduser(CAVASS_PROFILE_PATH)}'
        VIEWNIX_ENV = os.path.expanduser(CAVASS_PROFILE_PATH)
        return {'PATH': PATH, 'VIEWNIX_ENV': VIEWNIX_ENV}
    return None


def execute_cmd(cavass_cmd):
    p = subprocess.Popen(cavass_cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, env=env())
    r, e = p.communicate()
    try:
        r = r.decode()
    except UnicodeDecodeError:
        r = r.decode('gbk')
    e = e.decode().strip()
    if e:
        print(e)
    r = r.strip()
    return r
