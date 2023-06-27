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
        print(f"Killed {killed_processes} instances of process '{process_name}'.")
        return True
    print(f"No instances of process '{process_name}' found.")
    return False

def list_processes():
    for i, proc in enumerate(psutil.process_iter(['pid', 'name'])):
        print(f"\033[0m{i}\t{proc.info['name']}\033[0m")

def main(argv):
    process_name = None
    try:
        opts, args = getopt.getopt(argv, "n:l", ["name=", "list"])
    except getopt.GetoptError:
        print("kill_process.py -n <process_name>")
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
        print("kill_process.py -n <process_name> or -l")
        sys.exit(2)

if __name__ == '__main__':
    main(sys.argv[1:])
