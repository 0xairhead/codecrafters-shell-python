import os
import shlex
import shutil
import subprocess
import sys


def main():
    builtins = {"echo", "exit", "type", "pwd", "cd"}

    while True:
        sys.stdout.write("$ ")
        sys.stdout.flush()

        command = input()

        try:
            parts = shlex.split(command)
        except ValueError:
            continue

        if not parts:
            continue

        cmd = parts[0]

        if cmd == "exit":
            sys.exit(0)

        if cmd == "echo":
            print(*parts[1:])
            continue

        if cmd == "pwd":
            print(os.getcwd())
            continue

        if cmd == "cd":
            if len(parts) > 1:
                target = parts[1]
            else:
                target = "~"

            if target == "~":
                path = os.environ.get("HOME")
            else:
                path = target

            try:
                os.chdir(path)
            except FileNotFoundError:
                print(f"cd: {target}: No such file or directory")
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
