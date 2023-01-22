import os
import subprocess
import sys
import tempfile
import shutil
import ctypes


def main():
    command = sys.argv[3]
    args = sys.argv[4:]

    with tempfile.TemporaryDirectory() as tmp_dir:
        shutil.copy(command, os.path.join(tmp_dir, command[command.rfind("/") + 1:]))

        command = command[command.rfind("/"):]

        unshare = 272
        clone_new_pid = 0x20000000
        libc = ctypes.CDLL(None)
        libc.syscall(unshare, clone_new_pid)

        os.chroot(tmp_dir)

        completed_process = subprocess.run([command, *args], capture_output=True)

        sys.stdout.buffer.write(completed_process.stdout)
        sys.stderr.buffer.write(completed_process.stderr)

        sys.exit(completed_process.returncode)


if __name__ == "__main__":
    main()
