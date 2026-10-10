import sys
import os
import socket
import ctypes

MS_REC = 16384
MS_PRIVATE = 262144
FS_ROOT = "fs"
FS_DIR = "/"
CONTAINER_HOSTNAME = "py-container"
libc = ctypes.CDLL("libc.so.6", use_errno=True)


def run():
    os.unshare(os.CLONE_NEWUTS | os.CLONE_NEWPID | os.CLONE_NEWNS)
    pid = os.fork()
    if pid == 0:
        socket.sethostname(CONTAINER_HOSTNAME)
        os.chroot(FS_ROOT)
        os.chdir(FS_DIR)
        res = libc.mount(b"proc", b"/proc", b"proc", MS_REC | MS_PRIVATE, None)
        if res == -1:
            print("Error mounting proc")
            exit(1)
        os.execv("/bin/bash", ["/bin/bash"])
    else:
        (pid, status) = os.waitpid(pid, 0)
        sys.exit(os.waitstatus_to_exitcode(status))





if __name__ == "__main__":
    run()