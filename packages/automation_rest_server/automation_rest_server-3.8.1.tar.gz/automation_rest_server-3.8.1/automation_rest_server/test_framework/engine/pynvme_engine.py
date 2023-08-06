import os
import yaml
import subprocess
from utils import log
from utils.system import get_ip_address
from test_framework.state import State
from utils.firmware_path import FirmwareBinPath


class PynvmeEngine(object):

    def __init__(self):
        self.local_ip = get_ip_address()
        self.working_path = os.environ["working_path"]
        self.prun_port = os.environ["prun_port"]
        self.log_path = self.get_log_path()
        self.orig_log_folders = ""
        self.fw_path_manage = FirmwareBinPath()

    def get_log_path(self):
        log_path = os.path.join(self.working_path, "logs")
        if os.path.exists(log_path) is False:
            os.mkdir(log_path)
        if self.local_ip is not None:
            log_path = os.path.join(log_path, self.local_ip)
        if os.path.exists(log_path) is False:
            os.mkdir(log_path)
        return log_path

    def get_new_log(self, test_case):
        test_name = test_case.split('.')[-1]
        latest_log_folders = os.listdir(self.log_path)
        orig_log_folders = self.read_orig_logs()
        new_logs = list()
        for item in latest_log_folders:
            if item not in orig_log_folders:
                if os.path.isfile(os.path.join(self.log_path, item)):
                    if test_name in item:
                        new_logs.append(os.path.join(self.log_path, item))
        return new_logs

    def get_orig_logs(self):
        self.orig_log_folders = os.path.join(self.log_path, "org_logs_{}.yaml".format(self.prun_port))
        orig_log_folders = os.listdir(self.log_path)
        orig_log_folders = [item for item in orig_log_folders if "test_" in item]
        with open(self.orig_log_folders, 'w') as f:
            yaml.dump(orig_log_folders, f)

    def read_orig_logs(self):
        with open(self.orig_log_folders) as f:
            log_folders = yaml.load(f.read(), Loader=yaml.SafeLoader)
        return log_folders

    @staticmethod
    def convert_para_2_string(parameters):
        para_list = [f"--{key} {value}" for key, value in parameters.items()]
        para_str = ' '.join(para_list)
        return para_str

    def run_test(self, test_case, parameters):
        log.INFO("pynvme run_test")
        para_str = self.convert_para_2_string(parameters)
        command_line = "python run.py testcase -n {} {}".format(test_case, para_str)
        log.INFO("pynvme run command: {}".format(command_line))
        child1 = subprocess.Popen(command_line, shell=True)
        return_code = child1.wait()
        return return_code

    def run(self, test_case, test_path, parameters, queue):
        log.INFO("pynvme run")
        self.get_orig_logs()
        ret_code = self.run_test(test_case, parameters)
        logs = self.get_new_log(test_case)
        result = {"name": test_case, "result": ret_code, "log": logs}
        print(f"testcase: {test_case} result {result}")
        queue.put(result)
        return ret_code
