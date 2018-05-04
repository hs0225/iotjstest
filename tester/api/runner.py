import re
import os
import signal
import util
import path
from sdb import SDB

CVIOLET = '\33[35m'
CEND      = '\33[0m'
CBOLD     = '\33[1m'
CYELLOW = '\33[33m'
CGREEN  = '\33[32m'
CRED    = '\33[31m'
CBLUEBG   = '\33[44m'

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

class Runner(object):
    '''
    The serial communication wrapper.
    '''
    def __init__(self, config):
        self.config = config
        self.connection =  SDB(config)
        self.testfile = 'tmp/testfile'
        self.target_res_path = '/opt/usr/globalapps/' + self.config['appid'] + '/res/'

        if self.config['flash']['test'] == 'yes':
            self._copy_test_files()

        # Push index.js file
        index_file = os.path.join(os.getcwd(), 'index.js')
        self.connection.push_file(index_file, self.target_res_path)

        signal.signal(signal.SIGALRM, timeout_alarm_handler)

    def _pre_test(self):
        # Set copy library file for test_module_dynamicload.js
        try:
            dynamicmodule_path = os.path.join(path.GBS_IOTJS_BUILD_PATH,
                'release/test/dynamicmodule/')
            if not os.path.exists(dynamicmodule_path):
                dynamicmodule_path = os.path.join(path.GBS_IOTJS_BUILD_PATH,
                    'debug/test/dynamicmodule/')
            self.connection.push_file(dynamicmodule_path, self.target_res_path)
        except:
            print(CRED + 'Fail to copy dynamicmodule.iotjs file.' + CEND)

    def _copy_test_files(self):
        testfiles_path = os.path.join(self.config['iotjs_path'], 'test')
        self.connection.push_file(testfiles_path, self.target_res_path, quite=False)

    def write_test_file_name(self, file):
        with open("tmp/testfile", "w") as f:
            f.write(file)

    def terminate_test(self):
        self.connection.exec_cmd('app_launcher -t ' + self.config['appid'])
        self.connection.read_dlog_until('loop_method_fini_cb')

    def exec_test(self, file):
        signal.alarm(self.config['timeout'])

        self.write_test_file_name(file)
        self.connection.push_file(self.testfile, self.target_res_path)

        self.connection.exec_cmd('app_launcher -s ' + self.config['appid'])
        terminate, output = self.connection.read_dlog_until('loop_method_fini_cb')

        result = re.search(r'IoT\.js test result: (\d+)', output)
        if not result:
            result = re.search(r'Exit IoT\.js\((\d+)\)', output)

        signal.alarm(0)

        if result:
            result = int(result.group(1))
        else:
            result = 1
        return result, output

    def run(self):
        self._pre_test()

        success = fail = timeout = skip = 0

        testset_path = os.path.join(self.config['iotjs_path'], 'test/testsets.json')
        testset_json = util.read_json_file(testset_path)
        
        print('')
        print(CVIOLET + CBOLD + 'IoT.js Test'+ CEND)

        for test_group in testset_json:
            print('')
            print(CVIOLET + CBOLD + '  ' + test_group + CEND)
            for testset in testset_json[test_group]:
                # 1. Skip test file
                if 'skip' in testset and  set(testset['skip']) & set(['all', 'tizen', 'stable']):
                    print(CYELLOW + '   SKIP: ' + testset['name'] + CEND + ': ' + testset['reason'])
                    skip = skip + 1
                    continue

                # 2. Execute test
                try:
                    result, output = self.exec_test(test_group + '/' + testset['name'])
                except TimeoutException:
                    self.terminate_test()
                    print(CRED + '   TIMEOUT: ' + testset['name'] + CEND)
                    timeout = timeout + 1
                    continue

                if ('expected-failure' in testset and result != 0) or result == 0:
                    print(CGREEN + '   PASS: ' + testset['name'] + CEND)
                    success = success + 1
                else:
                    print(output)
                    print(CRED + '   FAIL: ' + testset['name'] + CEND)
                    fail = fail + 1

        # Print result
        print('')
        print(CBLUEBG + '<<Test Result>>' + CEND)
        print(CGREEN + ' PASS: %d' % success+ CEND)
        print(CRED + ' FAIL: %d' % fail + CEND)
        print(CRED + ' TIMEOUT: %d' % timeout + CEND)
        print(CYELLOW + ' SKIP: %d' % skip + CEND)

        self.connection.close()
