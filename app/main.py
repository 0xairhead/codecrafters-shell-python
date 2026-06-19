import sys


def main():
    builtins = {"echo", "exit", "type"}

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

        if cmd == "type":
            target = parts[1]
            if target in builtins:
                print(f"{target} is a shell builtin")
            else:
                print(f"{target}: not found")
            continue

        print(f"{cmd}: not found")


if __name__ == "__main__":
    main()
