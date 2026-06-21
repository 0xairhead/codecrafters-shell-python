import os
import readline
import shlex
import shutil
import subprocess
import sys


def completer(text, state):
    matches = []
    for cmd in ["echo", "exit"]:
        if cmd.startswith(text):
            matches.append(cmd + " ")

    if state < len(matches):
        return matches[state]
    return None


def main():
    readline.set_completer(completer)
    readline.parse_and_bind("tab: complete")

    builtins = {"echo", "exit", "type", "pwd", "cd"}

    while True:
        sys.stdout.write("$ ")
        sys.stdout.flush()

        command = input()

        print(f"[DEBUG] Raw command input: {repr(command)}")
        try:
            parts = shlex.split(command)
            print(f"[DEBUG] shlex.split output: {parts}")
        except ValueError as e:
            print(f"[DEBUG] shlex.split failed with ValueError: {e}")
            continue

        if not parts:
            continue

        # Parse standard output and standard error redirection
        redirect_file = None
        redirect_stderr_file = None
        append_mode = False
        append_stderr_mode = False

        if ">" in parts:
            idx = parts.index(">")
            print(f"[DEBUG] Redirection '>' found at index {idx}")
            redirect_file = parts[idx + 1]
            parts = parts[:idx]
        elif "1>" in parts:
            idx = parts.index("1>")
            print(f"[DEBUG] Redirection '1>' found at index {idx}")
            redirect_file = parts[idx + 1]
            parts = parts[:idx]
        elif ">>" in parts:
            idx = parts.index(">>")
            print(f"[DEBUG] Redirection '>>' found at index {idx}")
            redirect_file = parts[idx + 1]
            append_mode = True
            parts = parts[:idx]
        elif "1>>" in parts:
            idx = parts.index("1>>")
            print(f"[DEBUG] Redirection '1>>' found at index {idx}")
            redirect_file = parts[idx + 1]
            append_mode = True
            parts = parts[:idx]
        elif "2>" in parts:
            idx = parts.index("2>")
            print(f"[DEBUG] Redirection '2>' found at index {idx}")
            redirect_stderr_file = parts[idx + 1]
            parts = parts[:idx]
        elif "2>>" in parts:
            idx = parts.index("2>>")
            print(f"[DEBUG] Redirection '2>>' found at index {idx}")
            redirect_stderr_file = parts[idx + 1]
            append_stderr_mode = True
            parts = parts[:idx]

        if not parts:
            continue

        cmd = parts[0]

        # Open redirection streams if specified
        out_stream = sys.stdout
        if redirect_file:
            dir_name = os.path.dirname(redirect_file)
            if dir_name:
                os.makedirs(dir_name, exist_ok=True)
            if append_mode:
                out_stream = open(redirect_file, "a")
            else:
                out_stream = open(redirect_file, "w")

        err_stream = sys.stderr
        if redirect_stderr_file:
            dir_name = os.path.dirname(redirect_stderr_file)
            if dir_name:
                os.makedirs(dir_name, exist_ok=True)
            if append_stderr_mode:
                err_stream = open(redirect_stderr_file, "a")
            else:
                err_stream = open(redirect_stderr_file, "w")

        if cmd == "exit":
            if redirect_file:
                out_stream.close()
            if redirect_stderr_file:
                err_stream.close()
            sys.exit(0)

        elif cmd == "echo":
            print(*parts[1:], file=out_stream)

        elif cmd == "pwd":
            print(os.getcwd(), file=out_stream)

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
                print(f"cd: {target}: No such file or directory", file=err_stream)

        elif cmd == "type":
            if len(parts) > 1:
                target = parts[1]
                if target in builtins:
                    print(f"{target} is a shell builtin", file=out_stream)
                else:
                    path = shutil.which(target)
                    if path:
                        print(f"{target} is {path}", file=out_stream)
                    else:
                        print(f"{target}: not found", file=err_stream)

        else:
            # Check if the command is an external program executable in PATH
            path = shutil.which(cmd)
            if path:
                subprocess.run(
                    parts, executable=path, stdout=out_stream, stderr=err_stream
                )
            else:
                print(f"{cmd}: not found", file=err_stream)

        # Close redirection files if opened
        if redirect_file:
            out_stream.close()
        if redirect_stderr_file:
            err_stream.close()


if __name__ == "__main__":
    main()
