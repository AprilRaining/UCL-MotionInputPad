import json
import os
import win32api
import win32con
from AppOperations.MailOperations import MailOperation


with open(os.path.join(os.path.dirname(__file__), 'configs', 'config_exe.json')) as path_file:
    path_exe = json.load(path_file)
    print(path_exe)


if __name__ == '__main__':
    # mail_handle = win32api.MessageBox(0, "test_message", "hello_test", win32con.MB_OK | win32con.MB_ICONWARNING)
    # mail_handle = win32api.ShellExecute(0, 'open', 'steam.exe', '', os.path.join('E:', 'steam'), 0)
    # print(mail_handle)
    # for i, j in os.environ.items():
    #     print(i + ':' + j)
    # os.startfile('cmd')
    s = MailOperation()
    pass