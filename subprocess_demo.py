

import os
import subprocess
import shlex

def system(command, env=None, raise_on_error=False, timeout=None, **kwargs):
    env = {} if env is None else env
    env.update(os.environ)

    ret = subprocess.run(shlex.split(command), env=env, check=raise_on_error, timeout=timeout, **kwargs)
    return ret.returncode


def comm():
    try:
        command = 'kubectl get namespace'
        env={}
        ret = system(command, env=env, timeout=60)
        if ret != 0:
            return False, "Command exited with non-zero: %s" % ret
        print(111,ret)
    except subprocess.TimeoutExpired:
        return False, "Command didn't complete within 60s."
    return True,"ok"







if __name__ == '__main__':
   print(comm())