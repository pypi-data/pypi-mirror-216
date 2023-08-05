import platform
import shlex
import subprocess

# -----------------------------------------------------------------------------
# Get OS
# -----------------------------------------------------------------------------


def get_os():
    """Returns the current OS name (OSX, Fedora, CentOS, Debian or Ubuntu)."""
    uname = platform.system()
    if uname == "Darwin":
        return "OSX"

    if uname == "Linux":
        find = ["Fedora", "CentOS", "Debian", "Ubuntu"]
        # If lsb_release then test that output
        status = exec_cmd("hash lsb_release &> /dev/null")
        for search in find:
            if status:
                status = exec_cmd(f"lsb_release -i | grep {search} > /dev/null 2>&1")
            else:
                status = exec_cmd(f"cat /etc/*release | grep {search} > /dev/null 2>&1")
            if status:
                return search

    return "Windows" if uname in ["Windows", "Win32", "Win64"] else "Unknown"


# -----------------------------------------------------------------------------
# Execute Command
# -----------------------------------------------------------------------------


def exec_cmd(cmd):
    """Executes a command and returns the status, stdout and stderror."""
    # call command
    proc = subprocess.Popen(
        shlex.split(cmd), stdout=subprocess.PIPE, stderr=subprocess.PIPE
    )

    # talk with command i.e. read data from stdout and stderr. Store this info in tuple
    stdout, stderr = proc.communicate()

    # wait for terminate. Get return returncode
    ret_code = proc.wait()
    status = ret_code == 0

    stdout = stdout.decode("utf-8").strip()
    stderr = stderr.decode("utf-8").strip()

    return (status, stdout, stderr)


def cmd_exists(program):
    """Returns True if a command exists."""
    cmd = "where" if get_os() == "Windows" else "which"
    (status, stdout, stderr) = exec_cmd("{0} {1}".format(cmd, program))
    return status


# -----------------------------------------------------------------------------

if __name__ == "__main__":
    print(get_os())
    print(cmd_exists("git"))

    # status, stdout, stderr = exec_cmd("git --help")
    # print(status, stdout, stderr)
