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

        # Parse standard output redirection
        redirect_file = None
        if ">" in parts:
            idx = parts.index(">")
            redirect_file = parts[idx + 1]
            parts = parts[:idx]
        elif "1>" in parts:
            idx = parts.index("1>")
            redirect_file = parts[idx + 1]
            parts = parts[:idx]

        if not parts:
            continue

        cmd = parts[0]

        # Open redirection file if specified
        if redirect_file:
            os.makedirs(os.path.dirname(redirect_file), exist_ok=True)
            sys.stdout = open(redirect_file, "w")

        if cmd == "exit":
            sys.exit(0)

        elif cmd == "echo":
            print(*parts[1:])

        elif cmd == "pwd":
            print(os.getcwd())

        elif cmd == "cd":
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
                print(f"cd: {target}: No such file or directory", file=sys.stderr)

        elif cmd == "type":
            if len(parts) > 1:
                target = parts[1]
                if target in builtins:
                    print(f"{target} is a shell builtin")
                else:
                    path = shutil.which(target)
                    if path:
                        print(f"{target} is {path}")
                    else:
                        print(f"{target}: not found", file=sys.stderr)

        else:
            # Check if the command is an external program executable in PATH
            path = shutil.which(cmd)
            if path:
                subprocess.run(parts, executable=path, stdout=sys.stdout)
            else:
                print(f"{cmd}: not found", file=sys.stderr)


if __name__ == "__main__":
    main()
