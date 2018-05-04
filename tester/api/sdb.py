import subprocess
import time
import signal

class TimeoutException(Exception):
    '''
    Custom exception in case of timeout.
    '''
    pass

def timeout_alarm_handler(signum, frame):
    '''
    Throw exception when alarm happens.
    '''
    raise TimeoutException


class SDB(object):
    '''
    The serial communication wrapper.
    '''
    def __init__(self, config):
        self.config = config
        
        subprocess.call('sdb root on', shell=True)

        self.dlog_shell = self.open_shell()
        self.exec_shell_cmd(self.dlog_shell, 'dlogutil -c')
        self.exec_shell_cmd(self.dlog_shell, 'dlogutil IOTJS')

    def open_shell(self):
        '''
        Open the sdb shell.
        '''
        shell = subprocess.Popen(['sdb', 'shell'], stdin=subprocess.PIPE,
                                    stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

        return shell

    def close(self):
        '''
        Close the sdb shell.
        '''
        self.dlog_shell.terminate()

    def push_file(self, src, des, quite=True):
        stdout = None
        if quite:
            stdout = subprocess.PIPE
        subprocess.call('sdb push ' + src + ' ' + des, shell=True, stdout=stdout)

    def exec_cmd(self, cmd, quite=True) :
        time.sleep(0.25)
        stdout = None
        if quite:
            stdout = subprocess.PIPE
        subprocess.call ('sdb shell ' + cmd, shell=True, stdout=stdout)

    def exec_shell_cmd(self, shell, cmd):
        '''
        Read line from the sdb shell.
        '''
        time.sleep(0.25)
        shell.stdin.write(cmd + '\n')
        self.read_shell_line(shell)

    def read_shell_line(self, shell):
        '''
        Read line from the sdb shell.
        '''
        return shell.stdout.readline()

    def read_dlog_until(self, *args):
        '''
        Read data until it contains terminator.
        '''
        line = bytearray()
        while True:
            c = self.dlog_shell.stdout.read(1)
            if c:
                line += c
                for stdout in args:
                    if line[-len(stdout):] == stdout:
                        return stdout, bytes(line)
            else:
                raise TimeoutException

        return False, False
