import sys
import os
import json
import socket
import ctypes
from pathlib import Path
from settings import settings

MS_REC = 16384
MS_PRIVATE = 262144
libc = ctypes.CDLL("libc.so.6", use_errno=True)

def init_cgroup():
    l = os.listdir(settings.cgroup_dir)
    if not settings.container_hostname in l:
        os.mkdir(settings.process_cgroup_dir)

    # writing each value from the config into its cgroup file
    limits = json.loads(Path(settings.cgroup_config).read_text())
    for file, value in limits.items():
        Path(f"{settings.process_cgroup_dir}/{file}").write_text(str(value))

def run():
    os.unshare(os.CLONE_NEWUTS | os.CLONE_NEWPID | os.CLONE_NEWNS)
    pid = os.fork()
    if pid == 0:
        libc.mount(None, b"/", None, MS_REC | MS_PRIVATE, None) 
        socket.sethostname(settings.container_hostname)
        os.chroot(settings.fs_root)
        os.chdir(settings.fs_dir)
        res = libc.mount(b"proc", b"/proc", b"proc", 0, None)
        if res == -1:
            print("Error mounting proc:", os.strerror(ctypes.get_errno()))
            exit(1)
        os.execv("/bin/bash", ["/bin/bash"])
    else:
        Path(f"{settings.process_cgroup_dir}/cgroup.procs").write_text(str(pid))
        (pid, status) = os.waitpid(pid, 0)
        sys.exit(os.waitstatus_to_exitcode(status))





if __name__ == "__main__":
    init_cgroup()
    run()