import sys
import getopt
import psutil

def kill_process_by_name(process_name):
    killed_processes = 0
    for proc in psutil.process_iter(['pid', 'name']):
        if proc.info['name'] == process_name:
            proc.kill()
            killed_processes += 1
    if killed_processes > 0:
        print(f"Killed \033[33m{killed_processes}\033[0m instances of process \033[32m'{process_name}'\033[0m.")
        return True
    print(f"No instances of process '{process_name}' found.")
    return False

def list_processes():
    for i, proc in enumerate(psutil.process_iter(['pid', 'name'])):
        print(f"\033[0m{i}\t\033[32m{proc.info['pid']}\t{proc.info['name']}\033[0m")

banner = """\033[31m
 _______             _       _________ _        _        _______  _______ 
(  ____ )|\     /|  | \    /\\\__   __/( \      ( \      (  ____ \(  ____ )
| (    )|( \   / )  |  \  / /   ) (   | (      | (      | (    \/| (    )|
| (____)| \ (_) /   |  (_/ /    | |   | |      | |      | (__    | (____)|
|  _____)  \   /    |   _ (     | |   | |      | |      |  __)   |     __)
| (         ) (     |  ( \ \    | |   | |      | |      | (      | (\ (   
| )         | |     |  /  \ \___) (___| (____/\| (____/\| (____/\| ) \ \__
|/          \_/     |_/    \/\_______/(_______/(_______/(_______/|/   \__/
\033[0m"""

usage = """                                                                        
USAGE:

Get the list of running processes:
    
    python main.py -l

Kill a process:
    python main.py -n <process_name>
"""

def py_killer(argv):
    print(banner)
    process_name = None
    list = None
    try:
        opts, _ = getopt.getopt(argv, "n:l", ["name=", "list"])
    except getopt.GetoptError:
        print(usage)
        sys.exit(2)
    for opt, arg in opts:
        if opt in ("-n", "--name"):
            process_name = arg
        if opt in ("-l", "--list"):
            list = True
    if process_name:
        if not kill_process_by_name(process_name):
            sys.exit(1)
    elif list:
        list_processes()
    else:
        print(usage)
        sys.exit(2)


if __name__ == '__main__':
    py_killer(sys.argv[1:]) # pragma: no cover