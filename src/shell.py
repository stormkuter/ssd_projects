import subprocess


class Shell:

    def __init__(self):
        pass

    def write(self, lba, val):
        # system call wrtie
        ssd_sp = subprocess.run(f"ssd_cmd w {lba} {val}")

        ssd_sp.returncode
        # error 처리

    def read(self, lba, val):
        pass

    def help(self, lba, val):
        pass


    def full_write(self, val):
        pass


    def full_read(self):
        pass

    def run(self):
        print('================= SSD Shell Started! =================')
        while True:
            user_input = input(">> ").strip()
            args = user_input.split()

            if args[0] == 'write':
                self.write(args[1], args[2])
            elif args[0] == 'read':
                self.read(args[1], args[2])
            elif args[0] == 'exit':
                break
            elif args[0] == 'help':
                self.help()
            elif args[0] == 'fullwrite':
                self.full_write(args[1])
            elif args[0] == 'fullread':
                self.full_read()
            else:
                print("INVALID COMMAND")


if __name__ == "__main__":
    shell = Shell()

    shell.run()
