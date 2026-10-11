import sys
import os
import json
import socket
import ctypes
from pathlib import Path

MS_REC = 16384
MS_PRIVATE = 262144
FS_ROOT = "fs"
FS_DIR = "/"
CONTAINER_HOSTNAME = "py-container"
CGROUP_DIR = "/sys/fs/cgroup"
CGROUP_CONFIG = "cgroup.json"
PROCESS_CGROUP_DIR = f"{CGROUP_DIR}/{CONTAINER_HOSTNAME}"
libc = ctypes.CDLL("libc.so.6", use_errno=True)

def init_cgroup():
    l = os.listdir(CGROUP_DIR)
    if not CONTAINER_HOSTNAME in l:
        os.mkdir(PROCESS_CGROUP_DIR)

    # writing each value from the config into its cgroup file
    limits = json.loads(Path(CGROUP_CONFIG).read_text())
    for file, value in limits.items():
        Path(f"{PROCESS_CGROUP_DIR}/{file}").write_text(str(value))

def run():
    os.unshare(os.CLONE_NEWUTS | os.CLONE_NEWPID | os.CLONE_NEWNS)
    pid = os.fork()
    if pid == 0:
        libc.mount(None, b"/", None, MS_REC | MS_PRIVATE, None) 
        socket.sethostname(CONTAINER_HOSTNAME)
        os.chroot(FS_ROOT)
        os.chdir(FS_DIR)
        res = libc.mount(b"proc", b"/proc", b"proc", 0, None)
        if res == -1:
            print("Error mounting proc:", os.strerror(ctypes.get_errno()))
            exit(1)
        os.execv("/bin/bash", ["/bin/bash"])
    else:
        Path(f"{PROCESS_CGROUP_DIR}/cgroup.procs").write_text(str(pid))
        (pid, status) = os.waitpid(pid, 0)
        sys.exit(os.waitstatus_to_exitcode(status))





if __name__ == "__main__":
    init_cgroup()
    run()