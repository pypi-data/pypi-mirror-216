import sys
import tempfile
import subprocess

#mayFreeze为false时，解压缩，为True时压缩
def run_shell(command, mayFreeze=False):
    def check_retcode(retcode, cmd):
        if 0 != retcode:
            print >> sys.stderr, 'err executing ' + cmd + ':', retcode
            sys.exit(retcode)
    def read_close(f):
        f.seek(0)
        d = f.read()
        f.close()
        return d
    #print >> sys.stderr, '-- Executing', command
    if mayFreeze:
        tempout, temperr = tempfile.TemporaryFile(), tempfile.TemporaryFile()#open(os.devnull, 'w')
        p = subprocess.Popen(command, stdout=tempout, stderr=temperr)
        p.wait()
        output, errout = read_close(tempout), read_close(temperr)
    else:
        p = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        output = p.stdout.read()
        p.wait()
        errout = p.stderr.read()
        p.stdout.close()
        p.stderr.close()
    #check_retcode(p.returncode, command)
    return (output.strip(), errout.strip())