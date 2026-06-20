import os
import shutil
import subprocess
import sys


def main():
    builtins = {"echo", "exit", "type", "pwd", "cd"}

    while True:
        sys.stdout.write("$ ")
        sys.stdout.flush()

        command = input()

        parts = command.split()
        if not parts:
            continue

        cmd = parts[0]

        if cmd == "exit":
            sys.exit(0)

        if cmd == "echo":
            print(command[5:])
            continue

        if cmd == "pwd":
            print(os.getcwd())
            continue

        if cmd == "cd":
            if len(parts) < 2:
                path = os.environ.get("HOME")
            else:
                path = parts[1]
                if path == "~":
                    path = os.environ.get("HOME")
            try:
                os.chdir(path)
            except FileNotFoundError:
                print(f"cd: {parts[1]}: No such file or directory")
            continue

        if cmd == "type":
            if len(parts) > 1:
                target = parts[1]
                if target in builtins:
                    print(f"{target} is a shell builtin")
                else:
                    path = shutil.which(target)
                    if path:
                        print(f"{target} is {path}")
                    else:
                        print(f"{target}: not found")
            continue

        # Check if the command is an external program executable in PATH
        path = shutil.which(cmd)
        if path:
            subprocess.run(parts, executable=path)
            continue

        print(f"{cmd}: not found")


if __name__ == "__main__":
    main()
