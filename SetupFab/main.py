# general imports
import sys

# subcommands
from src.apps.setup.main import command_interpreter as setup_command_interpreter
from src.apps.test.main import command_interpreter as test_command_interpreter
from src.apps.download.main import command_interpreter as download_command_interpreter


# CLI --help & invalid command message
def help_command():
    print(
        '''\033[34mavailable sub commands are:\033[0m
        \033[34m*\033[0m setup
        \033[34m*\033[0m test
        \033[34m*\033[0m download'''
    )


# default execution sequence
def run():
    # removing module name from argv
    args = sys.argv[1:]

    # checking for invalid input & help request
    if len(args) < 1 or '--help' == sys.argv[0]:
        help_command()
    else:
        # removing subcommand name from args and calling command interpreter
        if args[0] == 'setup':
            setup_command_interpreter(args[1:])

        elif args[0] == 'test':
            test_command_interpreter(args[1:])

        elif args[0] == 'download':
            download_command_interpreter(args[1:])

        else:
            help_command()

    exit(0)


# executing run method
run()
