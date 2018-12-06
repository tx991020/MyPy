command = 'python -u %s/generalMaker.py %s %s' % (module_dir, ' '.join(sys.argv[1:]), flagsToAppend)
args = shlex.split(command)
generalMaker = Popen(args)
generalMaker.wait()


#使用管道连接标准流文件

import subprocess
child1 = subprocess.Popen(['ls', '-l'], stdout=subprocess.PIPE)
child2 = subprocess.Popen(['wc', '-l'], stdin=child1.stdout, stdout=subprocess.PIPE)
out = child2.communicate()
child1.wait()
child2.wait()
print(out)